import yt_dlp
import random
import os, string
import hashlib


class AudioCaption:
    def __init__(self, cookie_file):
        self.cookie_file = cookie_file
    
    def generate_random_hash_name(self):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        hash_object = hashlib.md5(random_string.encode())
        return hash_object.hexdigest()
    
    def download_audio(self, url):
        random_hash_name = self.generate_random_hash_name()
        output_template = f'downloads/{random_hash_name}.%(ext)s'

        ydl_opts = {
            'format': 'm4a',
            'outtmpl': output_template,
            'cookiefile': self.cookie_file,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        
        # Get the file extension of the downloaded file
        downloaded_files = [file for file in os.listdir('downloads') if random_hash_name in file]
        if downloaded_files:
            downloaded_file_name = downloaded_files[0]
            print(f'Downloaded audio file: {downloaded_file_name}')
            return downloaded_file_name
        else:
            print('No file was downloaded.')
            return None