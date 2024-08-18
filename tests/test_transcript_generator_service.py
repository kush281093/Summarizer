import unittest
from unittest.mock import MagicMock, patch
from config.constants import ENGLISH, GPT_MODEL, TEMP, TRANSCRIPT_TOKENS
from services.transcript_generator_service import TranscriptService

class TestTranscriptService(unittest.TestCase):

    # AI-Generated Code
    """Tests the generate_transcript method of the TranscriptService with the default language.
    Verifies that the method correctly generates a transcript in English,
    calls the OpenAI API with the appropriate prompt, and saves the transcript to a file."""
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_generate_transcript_default_language(self, mock_open):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Sample transcript"))]
        mock_client.create.return_value = mock_response

        service = TranscriptService(client=mock_client)

        result = service.generate_transcript()

        self.assertEqual(result, "Sample transcript")
        mock_client.create.assert_called_once_with(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": f"""
                   Generate a detailed sales call transcript between a salesperson and a potential client.
                   The salesperson should introduce the product, address client concerns, and attempt to close the sale.
                   The transcript should be in the following language: {ENGLISH}.
               """},
            ],
            max_tokens=TRANSCRIPT_TOKENS,
            temperature=TEMP
        )
        mock_open.assert_called_once_with("transcript.txt", "w")
        mock_open().write.assert_called_once_with("Sample transcript")

    """Tests the generate_transcript method of the TranscriptService with a custom language ("Spanish"). 
    Verifies that the method generates a transcript in the specified language, 
    calls the OpenAI API with the correct prompt, and saves the transcript to a file."""
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_generate_transcript_custom_language(self, mock_open):
        custom_language = "Spanish"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Transcripción de muestra"))]
        mock_client.create.return_value = mock_response

        service = TranscriptService(client=mock_client)

        result = service.generate_transcript(language=custom_language)

        self.assertEqual(result, "Transcripción de muestra")
        mock_client.create.assert_called_once_with(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": f"""
                   Generate a detailed sales call transcript between a salesperson and a potential client.
                   The salesperson should introduce the product, address client concerns, and attempt to close the sale.
                   The transcript should be in the following language: {custom_language}.
               """},
            ],
            max_tokens=TRANSCRIPT_TOKENS,
            temperature=TEMP
        )
        mock_open.assert_called_once_with("transcript.txt", "w")
        mock_open().write.assert_called_once_with("Transcripción de muestra")

if __name__ == '__main__':
    unittest.main()
