from dotenv import load_dotenv
from gemini import Gemini
import os
from fastapi import FastAPI
from captions import YoutubeCaption
from pdfgen import create_pdf_from_string
from ytdl import AudioCaption
load_dotenv()
GEM_API = os.getenv("GEMINI_API_KEY")
CUR_DIR = r"C:\\Users\\Administrator\\Desktop\\hackathon\\downloads"
jam = Gemini(GEM_API)
app = FastAPI()
cap = YoutubeCaption()
aud = AudioCaption("cookies.txt")

@app.get("/yt")
async def captions(url, task="notes in detail", language="english"):
    print(url)
    prompt = f"output {task} of this in {language} language"
    captions = cap.get_subtitle(url)
    if captions: 
        caption = captions[0] # if lists is non-empty, gets english subtitle
        output = jam.prompt(f"{prompt} of {caption}")
    else: # downloads audio and transcribes
        aud_name = aud.download_audio(url)
        audio_path = os.path.join(CUR_DIR, aud_name)
        print(audio_path)  # Debugging: Print the audio path
        output = jam.audio_prompt(audio_path, prompt)
        # os.remove(aud_name)
    
    # try:
    create_pdf_from_string(output, "file.pdf")
    # except:
        # create_pdf_from_string(output.decode('utf-8'), "file.pdf")
    return output


