import google.generativeai as genai

class Gemini():
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def prompt(self, text):
        response = self.model.generate_content(text)
        return response.text

    def audio_prompt(self, audio_path, prompt):
        audio = genai.upload_file(audio_path)
        response = self.model.generate_content([prompt, audio])
        return response.text