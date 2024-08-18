import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
import os
from config.constants import ENGLISH, GPT_MODEL, TEMP, ANSWER_TOKENS
from services.transcript_qa_service import TranscriptQAService

class TestTranscriptQAService(unittest.TestCase):

    """Tests the answer_question method by simulating a scenario where the transcript is provided,
    and the method generates an answer to a question using the OpenAI API.
    The test verifies the API call, the content written to the mock JSON file,
    and ensures the answer is correctly saved when the file does not already exist."""
    @patch('builtins.open', new_callable=mock_open, read_data="Sample transcript content")
    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_answer_question(self, mock_getsize, mock_exists, mock_open_file):
        mock_exists.return_value = False
        mock_getsize.return_value = 0

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Sample answer"))]
        mock_client.create.return_value = mock_response

        service = TranscriptQAService(client=mock_client)

        transcript = "Sample transcript content"
        question = "What was discussed?"
        language = ENGLISH

        answer = service.answer_question(transcript, question, language)

        self.assertEqual(answer, "Sample answer")
        mock_client.create.assert_called_once_with(
            model=GPT_MODEL,
            messages=[{"role": "user",
                       "content": f"Based on the following sales call transcript, answer the question:\n\nTranscript:\n{transcript}\n\nQuestion: {question}. The answer should be in the following language: {language} "}],
            max_tokens=ANSWER_TOKENS,
            temperature=TEMP
        )

        written_content = "".join([call.args[0] for call in mock_open_file().write.call_args_list])
        expected_content = json.dumps([{"question": question, "answer": "Sample answer"}], indent=4)
        self.assertEqual(written_content, expected_content)

    """Tests the save_to_db method by simulating a scenario where the JSON file already exists 
    and contains previous question-answer pairs. 
    The test verifies that the new question-answer pair is correctly appended to the existing data and saved back to the file."""
    @patch('builtins.open', new_callable=mock_open, read_data='[{"question": "Old question", "answer": "Old answer"}]')
    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_save_to_db_existing_file(self, mock_getsize, mock_exists, mock_open_file):
        mock_exists.return_value = True
        mock_getsize.return_value = 100  # Assume file has content

        service = TranscriptQAService(client=MagicMock())
        question = "What was discussed?"
        answer = "New answer"

        service.save_to_db(question, answer)

        mock_open_file.assert_called_with(service.db_file, "w")

        written_content = "".join([call.args[0] for call in mock_open_file().write.call_args_list])
        expected_content = json.dumps([
            {"question": "Old question", "answer": "Old answer"},
            {"question": question, "answer": answer}
        ], indent=4)
        self.assertEqual(written_content, expected_content)

    """Tests the qa_from_file method by simulating reading a transcript from a file, 
    generating an answer to a question using the OpenAI API, 
    and verifying the API call and the returned answer. 
    The test checks that the correct transcript is read from the file and the appropriate prompt is sent to the API for processing."""
    @patch('builtins.open', new_callable=mock_open)
    def test_qa_from_file(self, mock_open_file):
        mock_open_file.return_value.read.return_value = "Transcript from file"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Sample answer from file"))]
        mock_client.create.return_value = mock_response

        service = TranscriptQAService(client=mock_client)

        answer = service.qa_from_file(filename="dummy_transcript.txt", question="Who was the client?",
                                      language="French")

        mock_open_file.assert_any_call("dummy_transcript.txt", "r")
        self.assertEqual(answer, "Sample answer from file")
        mock_client.create.assert_called_once_with(
            model=GPT_MODEL,
            messages=[{"role": "user",
                       "content": "Based on the following sales call transcript, answer the question:\n\nTranscript:\nTranscript from file\n\nQuestion: Who was the client?. The answer should be in the following language: French "}],
            max_tokens=ANSWER_TOKENS,
            temperature=TEMP
        )

if __name__ == '__main__':
    unittest.main()
