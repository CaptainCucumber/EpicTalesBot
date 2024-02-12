import logging
import traceback

import openai
import requests
from bs4 import BeautifulSoup
from cache import cache_disk
from config import Config
from localization import _
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

logger = logging.getLogger(__name__)


class ArticleGPT:

    def __init__(self, config: Config) -> None:
        openai.api_key = config.get_open_ai_key()
        self._prompt_content = _("ARTICLE_SUMMARY_PROMPT")

        playwright = sync_playwright().start()
        self._browser = playwright.chromium.launch(headless=True)
        self._context = self._browser.new_context()

    # Return None if an error occurred
    def _download_webpage(self, url: str) -> str:
        logger.info(f"Downloading article content: {url}")
        page = self._context.new_page()
        stealth_sync(page)

        try:
            page.goto(url, wait_until="load")
            html_content = page.content()
            return html_content

        except requests.RequestException as e:
            logger.error(f"Error in downloading webpage {url}: {e}")

        finally:
            page.close()

        return None

    def _extract_title_and_content(self, html: str) -> tuple[str, str]:
        soup = BeautifulSoup(html, "html.parser")
        text = " ".join([p.get_text() for p in soup.find_all("p")])
        title = soup.title.get_text()
        return title, text

    def _gpt_it(self, title: str, text: str) -> str:
        title_name = _("Title")
        text_name = _("Text")
        try:
            response = openai.chat.completions.create(
                messages=[
                    {"role": "user", "content": self._prompt_content},
                    {
                        "role": "system",
                        "content": f"{title_name}: {title}\n{text_name}: {text}",
                    },
                ],
                model="gpt-4-1106-preview",
                temperature=0.2,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.9,
            )

            first_choice = response.choices[0]
            message = first_choice.message

            return message.content
        except Exception as e:
            logger.error(f"Error in generating summary: {e}")
            return _("Sorry, I couldn't generate the article summary.")

    @cache_disk
    def summarize(self, url: str) -> str:
        try:
            html = self._download_webpage(url)
            if html:
                title, text = self._extract_title_and_content(html)
                summary = self._gpt_it(title, text)
                return summary
        except Exception as e:
            # Capture the entire stack trace and log it
            stack_trace = traceback.format_exc()
            logger.error(
                f"Exception occurred while processing URL {url}:\n{e}\n{stack_trace}"
            )

        return _("Sorry, I couldn't generate the article summary.")
