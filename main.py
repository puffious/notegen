from dotenv import load_dotenv
from gemini import Gemini
import os
from fastapi import FastAPI
from captions import YoutubeCaption

load_dotenv()
GEM_API = os.getenv("GEMINI_API_KEY")

jam = Gemini(GEM_API)
app = FastAPI()
cap = YoutubeCaption()

@app.get("/yt")
async def captions(url, task="summarize"):
    print(url)
    captions = cap.get_subtitle(url)
    if captions: caption = captions[0] # if lists is non-empty, gets english subtitle
    output = jam.prompt(f"can you {task} the following captions? {caption}")
    print(output)
    return output


