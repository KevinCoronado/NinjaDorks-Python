# NinjaDorks-Python

Google Dorks Generator and Searcher

## Steps

1. Create a virtual environment in Conda; it should look like in this image:  
   ![image](https://github.com/user-attachments/assets/69d7932a-6aea-40c8-b276-3e66e94d54b8)

2. Install the Requirements

3. Ensure you have your `.env` file with the following API keys:
   - GOOGLE
   - SEARCH ENGINE
   - OPENAI
   - DUCKDUCKGO (Not necessary, it was just a little experiment)

4. You can do automated searches using Google dorks, download the results, generate Google dorks using OpenAI or a local model (this last one will download the model to your machine).
5. Example: ```python ninjadorks.py -q 'filetype:pdf kittys' --pages 3 --download all```


