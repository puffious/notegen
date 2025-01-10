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

def save_to_cache(content, cache_path):
    with open(cache_path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_from_cache(cache_path):
    with open(cache_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.get("/yt")
async def captions(url, prompt="", task="notes", language="english"):
    print(url)
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    cache_path = os.path.join(DOWN_DIR, f"{hash}.txt")
    
    # Check if cached result exists
    if os.path.exists(cache_path):
        output = read_from_cache(cache_path)
        return output

    # If not cached, generate new output
    audio_name = f"{hash}.m4a"
    audio_path = os.path.join(DOWN_DIR, audio_name)
    if not prompt: prompt = f"output {task} of this in {language} language"

    captions = cap.get_subtitle(url) 
    if captions: 
        caption = captions[0]
        output = jam.prompt(f"{prompt} of {caption}")
    else:
        if not os.path.exists(audio_path): 
            aud.download_audio(url, filename=hash)
        output = jam.audio_prompt(audio_path, prompt)
        # Clean up audio file after processing
        if os.path.exists(audio_path):
            os.remove(audio_path)
    
    # Cache the output
    save_to_cache(output, cache_path)
    
    # Generate PDF from the output
    pdf_path = os.path.join(DOWN_DIR, f"{hash}.pdf")
    create_pdf(output, pdf_path, language)
    
    return output

@app.get("/download_pdf")
async def downpdf(url):
    id = cap.extract_video_id(url)
    hash = aud.generate_random_hash_name(id)
    cache_path = os.path.join(DOWN_DIR, f"{hash}.txt")
    pdf_path = os.path.join(DOWN_DIR, f"{hash}.pdf")
    
    # If PDF doesn't exist but cache does, regenerate PDF from cache
    if not os.path.exists(pdf_path) and os.path.exists(cache_path):
        output = read_from_cache(cache_path)
        create_pdf(output, pdf_path, "english")  # Default to English if not specified
        
    if os.path.exists(pdf_path):
        return FileResponse(path=pdf_path, filename="note.pdf", media_type="application/pdf")
    else:
        return {"error": "PDF not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
