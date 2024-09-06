import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp
import random
import os, string
import hashlib

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

class AudioCaption:
    def __init__(self, cookie_file):
        self.cookie_file = cookie_file
    
    def generate_random_hash_name(self, text):
        # random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        hash_object = hashlib.md5(text.encode())
        return hash_object.hexdigest()
    
    def download_audio(self, url, filename):
        output_template = f'downloads/{filename}.%(ext)s'

        ydl_opts = {
            'format': 'm4a',
            'outtmpl': output_template,
            'cookiefile': self.cookie_file,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        
        # Get the file extension of the downloaded file
        downloaded_files = [file for file in os.listdir('downloads') if filename in file]
        if downloaded_files:
            downloaded_file_name = downloaded_files[0]
            print(f'Downloaded audio file: {downloaded_file_name}')
            return downloaded_file_name
        else:
            print('No file was downloaded.')
            return None