import os
from gemini import Gemini
from fastapi import FastAPI
from pdfgen import create_pdf
from dotenv import load_dotenv
from captions import YoutubeCaption, AudioCaption
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
GEM_API = os.getenv("GEMINI_API_KEY")
CUR_DIR = r"C:\\Users\\Administrator\\Desktop\\hackathon"
jam = Gemini(GEM_API)
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Adjust to specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

cap = YoutubeCaption()
aud = AudioCaption("cookies.txt")

@app.get("/yt")
async def captions(url, task="notes", language="english"):
    print(url)
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    prompt = f"output {task} of this in {language} language.\n"

    captions = cap.get_subtitle(url)
    if captions: 
        caption = captions[0]
        output = jam.prompt(f"{prompt} of {caption}")
    else:
        if not os.path.exists("downloads/{hash}.m4a"):
            aud_name = aud.download_audio(url, filename=hash)
            audio_path = os.path.join(CUR_DIR, aud_name)
            output = jam.audio_prompt(audio_path, prompt)
        else:
            audio_path = os.path.join(CUR_DIR, "downloads/{hash}.m4a")
            output = jam.audio_prompt(audio_path, prompt)
    create_pdf(output, f"downloads/{hash}.pdf", language)
    return output

@app.get("/download_pdf")
async def downpdf(url):
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    file_path = f"downloads/{hash}.pdf"
    if os.path.exists(file_path):
        return FileRespose(path=file_path, filename=note.pdf, media_type="application/pdf")
