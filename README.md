Description : 
1) This project gives user the ability to generate sales call transcript. 
     - each time transcript is generated, it will be saved to transcript.txt file and previous contents of file will be erased 
2) User can also generate summary for the transcript from step 1 and can see the output in console
3) User can also perform q&a on the transcript generated. Q&A record will be saved to a mock db. Q&A output will be visible in console

Setup:
1) install python 3.12.5 from https://www.python.org/downloads/
2) pip install openai
3) add your api key -> create a .env file and add ' OPEN_API_KEY = 'your api key' '
   alternatively adding api key to line 'self.api_key = your_api_key' in open_ai_client.py file should work too

How to run:
1) use command 'python main.py --generate' to generate transcript
2) use command 'python main.py --summarize' to summarize transcript
3) use command ' python main.py --query "question" ' to query the transcript
   note: With all the above commands you can also add ' --language "specified language" ' to specify the language. 
   The choices are English, Spanish and French. The default language is English  
4) run all unit tests in 'tests' directory using 'python -m unittest discover -s tests' or individually like 'python -m unittest tests.test_transcript_generator_service' 