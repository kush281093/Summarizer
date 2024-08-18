from config.constants import ENGLISH

class TranscriptService:
    def __init__(self, client):
        self.client = client

    def generate_transcript(self, language=ENGLISH):
        prompt = f"""
                   Generate a detailed sales call transcript between a salesperson and a potential client.
                   The salesperson should introduce the product, address client concerns, and attempt to close the sale.
                   The transcript should be in the following language: {language}.
               """

        response = self.client.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.5
        )

        transcript = response.choices[0].message.content
        self.save_transcript_to_file(transcript)

        return transcript

    def save_transcript_to_file(self, transcript, filename="transcript.txt"):
        # Open the file in write mode to clean its content
        with open(filename, "w") as file:
            # Write the transcript to the file
            file.write(transcript)

        print(f"Transcript saved to {filename}")
