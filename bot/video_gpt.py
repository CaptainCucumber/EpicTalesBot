import json
import logging
import re
import xml.etree.ElementTree as ET

import openai
import requests
from cache import cache_disk
from config import Config
from localization import _
from metrics import track_function

logger = logging.getLogger(__name__)

class VideoGPT:
    SUPPORTED_SUBTITLE_LANGUAGES = ['en', 'es', 'fr', 'de', 'it', 'nl', 'pt', 'ru', 'zh', 'ja', 'ko', 'uk']

    def __init__(self, config: Config) -> None:
        openai.api_key = config.get_open_ai_key()
        self._prompt_content = _("VIDEO_SUMMARY_PROMPT")

    def _gpt_it(self, title: str, subtitles: str) -> str:
        title_name = _('Title')
        subtitles_name = _('Subtitles')
        try:
            response = openai.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self._prompt_content
                    },
                    {
                        "role": "system",
                        "content": f"{title_name}: {title}\n{subtitles_name}: {subtitles}"
                    }
                ],
                model="gpt-4-1106-preview",
                temperature=0.2,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.9
            )

            first_choice = response.choices[0]
            message = first_choice.message

            return message.content
        except Exception as e:
            logger.error(f"Error in generating summary: {e}")
            return _("Sorry, I couldn't generate the video summary.")

    def _get_video_info(self, video_url: str) -> dict:
        response = requests.get(video_url)
        html_content = response.text

        # Find the JSON data within the HTML
        json_pattern = r"ytInitialPlayerResponse\s*=\s*({.+?})\s*;"
        json_data = re.search(json_pattern, html_content)
        if not json_data:
            return None

        video_info = json.loads(json_data.group(1))
        return video_info

    def _extract_subtitles_url(self, video_info: dict, language_code='en') -> str:
        # Extract the caption tracks from the video info. Returns first found track and None if not found.
        def find_track(caption_tracks, condition):
            return next((track for track in caption_tracks if condition(track)), None)

        caption_tracks = video_info.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get('captionTracks')
        if not caption_tracks:
            logger.error('No caption tracks found.')
            return None

        # Search for the specified language code
        result = find_track(caption_tracks, lambda track: track['languageCode'] in self.SUPPORTED_SUBTITLE_LANGUAGES)
        if result:
            return result['baseUrl']

        logger.error('Cannot find any suitable subtitles.')
        return None

    def _download_subtitles(self, subtitles_url: str) -> str:
        response = requests.get(subtitles_url)
        return response.text
    
    def _convert_xml_to_text(self, xml_data):
        root = ET.fromstring(xml_data)
        
        # Convert to text format
        subtitles_text = ""
        for child in root:
            start_time = child.attrib.get('start')
            text = child.text.replace("\n", " ")  # Replace newline characters with spaces
            subtitles_text += f"{start_time}\n{text}\n\n"
        
        return subtitles_text.strip()

    @track_function
    @cache_disk
    def summarize(self, video_url: str) -> str:
        video_info = self._get_video_info(video_url)

        if not video_info:
            logger.error(f'Cannot process URL {video_url}, video info is empty')
            return _("The video is not available for reviewing")

        subtitles_url = self._extract_subtitles_url(video_info)
        if not subtitles_url:
            logger.error(f'Cannot process URL {video_url}, subtitles URL is empty')
            return _("The subtitles are not available.")

        xml_subtitles = self._download_subtitles(subtitles_url)
        text_subtitles = self._convert_xml_to_text(xml_subtitles)

        title = video_info['videoDetails']['title']
        return self._gpt_it(title, text_subtitles)
