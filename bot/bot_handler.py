import json
import logging
import re
import openai
import requests
from bs4 import BeautifulSoup
from config import Config


TELEGRAM_TOKEN = Config.get_telegram_token()
OPENAI_API_KEY = Config.get_open_api_key()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY


def fetch_webpage_content(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the main content of the webpage.
            text = ' '.join([p.get_text() for p in soup.find_all('p')])
            return text
        else:
            return None
    except Exception as e:
        logger.error(f"Error fetching webpage content: {e}")
        return None


def summarize(url):
    article = fetch_webpage_content(url)
    
    prompt = f"""
    Summarize the following article: 
    "{article}". 
    
    Give a short summary first in a few sentenses, then 3-5 bullet points highlights. Keep the language simple and straightforward. 
    Keep the format as a executive summary. For each point choose emoji.

    In case you can't summarize the article. Just say why and give an error.

    Give the answer in Russian.

    The output must be adapted to Telegram message
    """

    logger.warn(prompt)

    try:
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-4-1106-preview"    
        )
        # refactor the below line by checking the response.choices[0].message.content step by step, and handle the error.
        if not response.choices or len(response.choices) == 0:
            raise Exception(
                f"Failed to parse choices from openai.ChatCompletion response. The response: {response}"
            )
        first_choice = response.choices[0]
        if not first_choice.message:
            raise Exception(
                f"Failed to parse message from openai.ChatCompletion response. The choices block: {first_choice}"
            )
        message = first_choice.message
        if not message.content:
            raise Exception(
                f"Failed to parse content openai.ChatCompletion response. The message block: {message}"
            )
        result = message.content
        return result

    except Exception as e:
        logger.error(f"Error in generating summary: {e}")
        return "Sorry, I couldn't generate the summary."

def send_message(chat_id, text):
    # Sends a message back
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

def lambda_handler(event, context):
    if len(event['Records']) > 1:
        logger.error(f"Expected only one record but received {len(event['Records'])}")

    # Iterate over each message, although it must be only one.
    for record in event['Records']:
        message_body = json.loads(record['body'])
        
        # Extract chat_id and text from the message
        chat_id = message_body.get('message', {}).get('chat', {}).get('id', '')
        text = message_body.get('message', {}).get('text', '')

        # Look for a URL in the message
        url_pattern = r'https?://[^\s]+'
        url = re.findall(url_pattern, text)
        if url:
            # If a URL is found, summarize the article
            summary = summarize(url[0])
            send_message(chat_id, summary)
        else:
            send_message(chat_id, "Please send a valid URL.")

    return {'statusCode': 200}
