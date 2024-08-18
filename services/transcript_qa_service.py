import os, json

from config.constants import ENGLISH

class TranscriptQAService:
    def __init__(self, client):
        self.client = client
        self.db_file = "db.json"

    def answer_question(self, transcript, question, language):
        prompt = f"Based on the following sales call transcript, answer the question:\n\nTranscript:\n{transcript}\n\nQuestion: {question}. The answer should be in the following language: {language} "

        response = self.client.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.5
        )

        answer = response.choices[0].message.content
        self.save_to_db(question=question, answer=answer)

        return answer

    def save_to_db(self, question, answer):
        # Load existing data if file exists
        if os.path.exists(self.db_file) and os.path.getsize(self.db_file) > 0:
            try:
                with open(self.db_file, "r") as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        # Append new entry
        data.append({
            "question": question,
            "answer": answer
        })

        # Save updated data back to file
        with open(self.db_file, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Question and answer saved to {self.db_file}")

    def qa_from_file(self, filename="transcript.txt", question="what persons are involved in this call ?", language=ENGLISH):
        # Read the content of the transcript file
        with open(filename, "r") as file:
            transcript = file.read()

        return self.answer_question(transcript, question, language)