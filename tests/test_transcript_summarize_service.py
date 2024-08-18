import unittest
from unittest.mock import MagicMock, patch, mock_open
from config.constants import ENGLISH, GPT_MODEL, TEMP, ANSWER_TOKENS
from services.transcript_summarize_service import SummaryService

class TestSummaryService(unittest.TestCase):

    """Tests the summarize_from_file method by simulating reading a transcript from a file
    and generating a summary using the OpenAI API.
    The test verifies that the correct transcript is read from the file,
    the API is called with the appropriate prompt, and the generated summary is returned."""
    @patch('builtins.open', new_callable=mock_open, read_data="Sample transcript content")
    @patch('os.path.exists')
    def test_summarize_from_file(self, mock_exists, mock_open_file):
        mock_exists.return_value = True
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Sample summary from file"))]
        mock_client.create.return_value = mock_response

        service = SummaryService(client=mock_client)

        summary = service.summarize_from_file(filename="transcript.txt", language=ENGLISH)

        mock_open_file.assert_called_with("transcript.txt", "r")
        mock_client.create.assert_called_once_with(
            model=GPT_MODEL,
            messages=[{"role": "user",
                       "content": "Summarize the following sales call transcript:\n\nSample transcript content.  The transcript should be in the following language: English."}],
            max_tokens=ANSWER_TOKENS,
            temperature=TEMP
        )
        self.assertEqual(summary, "Sample summary from file")

    """Tests the generate_summary method by providing a sample transcript 
    and language to the method and verifying that the OpenAI API is called with the correct prompt. 
    The test ensures that the summary returned by the API matches the expected summary."""
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_summary(self, mock_open_file):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Sample summary"))]
        mock_client.create.return_value = mock_response

        service = SummaryService(client=mock_client)

        transcript = "This is a sample sales call transcript."
        language = ENGLISH

        summary = service.generate_summary(transcript, language)

        mock_client.create.assert_called_once_with(
            model=GPT_MODEL,
            messages=[{"role": "user",
                       "content": f"Summarize the following sales call transcript:\n\n{transcript}.  The transcript should be in the following language: {language}."}],
            max_tokens=ANSWER_TOKENS,
            temperature=TEMP
        )
        self.assertEqual(summary, "Sample summary")


if __name__ == '__main__':
    unittest.main()
