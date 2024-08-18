from config.constants import ENGLISH, GPT_MODEL, TEMP, ANSWER_TOKENS

class SummaryService:
    def __init__(self, client):
        self.client = client

    """Generates a summary of the provided sales call transcript in the specified language using the GPT model"""
    def generate_summary(self, transcript, language):
        prompt = f"Summarize the following sales call transcript:\n\n{transcript}.  The transcript should be in the following language: {language}."

        response = self.client.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=ANSWER_TOKENS,
            temperature=TEMP
        )

        summary = response.choices[0].message.content
        return summary

    """Reads a sales call transcript from a file and generates a summary in the specified language"""
    def summarize_from_file(self, filename="transcript.txt", language=ENGLISH):
        # Read the content of the transcript file
        with open(filename, "r") as file:
            transcript = file.read()

        # Generate and return the summary
        return self.generate_summary(transcript, language)
