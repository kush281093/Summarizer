import argparse

from config.constants import ENGLISH
from services.transcript_generator_service import TranscriptService
from services.transcript_summarize_service import SummaryService
from services.transcript_qa_service import TranscriptQAService
from config.open_ai_client import OpenAIClient

def generate_sales_call_transcript(client, language=ENGLISH):
    transcript_service = TranscriptService(client=client)
    return transcript_service.generate_transcript(language=language)

def summarize_transcript(client, language=ENGLISH):
    summary_service = SummaryService(client=client)
    return summary_service.summarize_from_file(language=language)

def answer_query_about_transcript(client, query, language=ENGLISH):
    qa_service = TranscriptQAService(client=client)
    return qa_service.qa_from_file(question=query, language=language)

def main():
    parser = argparse.ArgumentParser(description="Sales Call Transcript Generator and Analyzer")
    parser.add_argument("--generate", action="store_true", help="Generate a sales call transcript")
    parser.add_argument("--summarize", action="store_true", help="Summarize the generated transcript")
    parser.add_argument("--query", type=str, help="Ask a query about the transcript")
    parser.add_argument("--language", type=str, default="English", choices=["English", "Spanish", "French"],
                        help="Specify the language for generating the transcript, summary, or answering the query")

    args = parser.parse_args()

    openai_client_instance = OpenAIClient()
    client = openai_client_instance.get_client()

    if args.generate:
        transcript = generate_sales_call_transcript(client, language=args.language)
        print("Generated Sales Call Transcript:")
        print(transcript)

    if args.summarize:
        summary = summarize_transcript(client, language=args.language)
        print("\nSummary of the Sales Call:")
        print(summary)

    if args.query:
        answer = answer_query_about_transcript(client, args.query, language=args.language)
        print("\nAnswer to Query:")
        print(f"Q: {args.query}\nA: {answer}")


if __name__ == "__main__":
    main()