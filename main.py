import os
from gemini import Gemini
from fastapi import FastAPI
from pdfgen import create_pdf
from dotenv import load_dotenv
from captions import YoutubeCaption, AudioCaption
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

load_dotenv()
GEM_API = os.getenv("GEMINI_API_KEY")
DOWN_DIR = os.path.join(os.getcwd(), "downloads")
# Create downloads directory if it doesn't exist
os.makedirs(DOWN_DIR, exist_ok=True)

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

# Mount the frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/index.html", "r") as f:
        return f.read()

cap = YoutubeCaption()
aud = AudioCaption("cookies.txt", downloads_dir=DOWN_DIR)

@app.get("/yt")
async def captions(url, prompt="", task="notes", language="english"):
    print(url)
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    audio_name = f"{hash}.m4a"
    audio_path = os.path.join(DOWN_DIR, audio_name)
    print(audio_path)
    if not prompt: prompt = f"output {task} of this in {language} language"

    captions = cap.get_subtitle(url) 
    if captions: 
        caption = captions[0]
        output = jam.prompt(f"{prompt} of {caption}")
    else:
        if not os.path.exists(audio_path): 
            aud.download_audio(url, filename=hash)
        output = jam.audio_prompt(audio_path, prompt)
    pdf_path = os.path.join(DOWN_DIR, f"{hash}.pdf")
    create_pdf(output, pdf_path, language)
    # remove audio file
    os.remove(audio_path)
    return output

@app.get("/download_pdf")
async def downpdf(url):
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    file_path = os.path.join(DOWN_DIR, f"{hash}.pdf")
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="note.pdf", media_type="application/pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
