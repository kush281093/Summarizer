from config.constants import ENGLISH, GPT_MODEL, TEMP, TRANSCRIPT_TOKENS

class TranscriptService:
    def __init__(self, client):
        self.client = client

    """ Generates a detailed sales call transcript between a salesperson and a potential client, 
    formatted in the specified language. Saves the transcript to a file if generated."""
    def generate_transcript(self, language=ENGLISH):
        prompt = f"""
                   Generate a detailed sales call transcript between a salesperson and a potential client.
                   The salesperson should introduce the product, address client concerns, and attempt to close the sale.
                   The transcript should be in the following language: {language}.
               """

        response = self.client.create(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=TRANSCRIPT_TOKENS,
            temperature=TEMP
        )

        # get response from open ai llm model
        transcript = response.choices[0].message.content
        self.save_transcript_to_file(transcript)

        return transcript

    """Saves the provided transcript to a specified file, overwriting the file's contents if it already exists"""
    def save_transcript_to_file(self, transcript, filename="transcript.txt"):
        # Open the file in write mode to clean its content
        with open(filename, "w") as file:
            # Write the transcript to the file
            file.write(transcript)

        print(f"Transcript saved to {filename}")