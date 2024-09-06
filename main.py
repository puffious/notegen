import os
from gemini import Gemini
from fastapi import FastAPI
from pdfgen import create_pdf
from dotenv import load_dotenv
from captions import YoutubeCaption, AudioCaption
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

load_dotenv()
GEM_API = os.getenv("GEMINI_API_KEY")
DOWN_DIR = r"C:\\Users\\Administrator\\Desktop\\hackathon\\downloads"
jam = Gemini(GEM_API)
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

cap = YoutubeCaption()
aud = AudioCaption("cookies.txt")

@app.get("/yt")
async def captions(url, task="notes", language="english", prompt=f"output {task} of this in {language} language"):
    print(url)
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    
    captions = cap.get_subtitle(url)
    if captions: 
        caption = captions[0]
        output = jam.prompt(f"{prompt} of {caption}")
    else:
        if not os.path.exists(f"{hash}.m4a"):
            aud_name = aud.download_audio(url, filename=hash)
            audio_path = os.path.join(DOWN_DIR, aud_name)
            output = jam.audio_prompt(audio_path, prompt)
        else:
            audio_path = os.path.join(DOWN_DIR, f"{hash}.m4a")
            output = jam.audio_prompt(audio_path, prompt)
    pdf_path = os.path.join(DOWN_DIR, f"{hash}.pdf")
    create_pdf(output, pdf_path, language)
    return output

@app.get("/download_pdf")
async def downpdf(url):
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    file_path = os.path.join(DOWN_DIR, f"{hash}.pdf")
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="note.pdf", media_type="application/pdf")
