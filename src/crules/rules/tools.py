import os

from openai import OpenAI
from termcolor import colored

# Constants
API_KEY = os.getenv("PERPLEXITY_API_KEY")
BASE_URL = "https://api.perplexity.ai"
MODEL = "llama-3_1-sonar-large-128k-online"

def web_search(query):
    """
    Perform a web search using the Perplexity AI API
    
    Args:
        query (str): The search query
    
    Returns:
        str: The response from the API
    """
    try:
        print(colored(f"Initiating search for: {query}", "cyan"))
        
        messages = [
            {"role": "system", "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
       },
    ]
	client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

	print(colored("Making API request...", "yellow"))

	response = client.chat_completions.create(
		model=MODEL,
		messages=messages,
	)

	result = response.choices[0].message.content

	print(colored("Search Results:", "green"))
	print(colored(result, "white"))

	return result

	except Exception as e:
		error_message = f"Error during web search: {e}"
		print(colored(error_message, "red"))
		return None
