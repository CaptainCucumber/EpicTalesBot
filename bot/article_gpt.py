
import logging

import openai
import requests
from bs4 import BeautifulSoup
from config import Config
from localization import _
from cache import cache_disk

logger = logging.getLogger(__name__)

class ArticleGPT:

    def __init__(self, config: Config) -> None:
        openai.api_key = config.get_open_ai_key()
        self._prompt_content = _("ARTICLE_SUMMARY_PROMPT")

    # Return None if an error occurred
    def _download_webpage(self, url: str) -> str:
        logger.info(f"Downloading article content: {url}")
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
        title_name = _('Title')
        text_name = _('Text')
        try:
            response = openai.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self._prompt_content + f"\n{title_name}: {title}\n{text_name}: {text}"
                    }
                ],
                model="gpt-4-1106-preview"    
            )

            first_choice = response.choices[0]
            message = first_choice.message

            return message.content
        except Exception as e:
            logger.error(f"Error in generating summary: {e}")
            return _("Sorry, I couldn't generate the article summary.")

    @cache_disk
    def summarize(self, url: str) -> str:
        html = self._download_webpage(url)
        if html:
            title, text = self._extract_title_and_content(html)
            summary = self._gpt_it(title, text)
            return summary
        
        logger.error(f'Cannot process URL {url}, content is empty')
        return _("Sorry, I couldn't generate the article summary.")
        

