
import os
import requests
from config import Config
import openai
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class ArticleGPT:
    _ARTICLE_SUMMARY_PROMPT_FILE = "article_summary_prompt.txt"

    def __init__(self, config: Config) -> None:
        openai.api_key = config.get_open_ai_key()
        self._prompt_content = None

    def _gpt_prompt(self) -> str:
        if self._prompt_content is None:
            file_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(file_dir, self._ARTICLE_SUMMARY_PROMPT_FILE)
        
            with open(file_path, 'r', encoding='utf-8') as file:
                self._prompt_content = file.read()

        return self._prompt_content

    # Return None if an error occurred
    def _download_webpage(self, url: str) -> str:
        try:
            response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=30)
            if response.status_code == 200:
                return response.text
            
            logger.error(f"Error in downloading webpage {url}: status code {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error in downloading webpage {url}: {e}")
        
        return None
    
    def _extract_title_and_content(self, html: str) -> tuple[str, str]:
        soup = BeautifulSoup(html, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        title = soup.title.get_text()
        return title, text 

    def _gpt_it(self, title: str, text: str) -> str:
        try:
            response = openai.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self._gpt_prompt() + f"\nTitle: {title}\nText: {text}"
                    }
                ],
                model="gpt-4-1106-preview"    
            )

            first_choice = response.choices[0]
            message = first_choice.message

            return message.content
        except Exception as e:
            logger.error(f"Error in generating summary: {e}")
            return "Sorry, I couldn't generate the summary."

    def summarize(self, url: str) -> str:
        html = self._download_webpage(url)
        if html:
            title, text = self._extract_title_and_content(html)
            summary = self._gpt_it(title, text)
            return summary
        
        return "Sorry, I couldn't generate the summary."
        

