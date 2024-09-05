import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

class YoutubeCaption:
    def extract_video_id(self, url):
        regex = r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|.+\?v=|.+\/videos\/|.+\/)([a-zA-Z0-9_-]{11})|(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})'
        match = re.match(regex, url)
        if match: return match.group(1) or match.group(2)
        else: raise ValueError("Invalid YouTube URL")

    def get_subtitle(self, url):
        video_id = self.extract_video_id(url)
        captions = YouTubeTranscriptApi.list_transcripts(video_id)
        
        english_subtitles = []
        for caption in captions:
            if not caption.is_generated and caption.language_code in ['en', 'en-US']:
                subtitle = caption.fetch()
                formatter = TextFormatter()
                formatted_sub = formatter.format_transcript(subtitle)
                english_subtitles.append(formatted_sub)
        return english_subtitles