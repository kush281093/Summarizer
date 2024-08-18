from config.constants import ENGLISH

class SummaryService:
    def __init__(self, client):
        self.client = client

    def generate_summary(self, transcript, language):
        prompt = f"Summarize the following sales call transcript:\n\n{transcript}.  The transcript should be in the following language: {language}."

        response = self.client.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.5
        )

        summary = response.choices[0].message.content
        return summary

    def summarize_from_file(self, filename="transcript.txt", language=ENGLISH):
        # Read the content of the transcript file
        with open(filename, "r") as file:
            transcript = file.read()

        # Generate and return the summary
        return self.generate_summary(transcript, language)
