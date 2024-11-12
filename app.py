import os
import logging
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import openai
from pydub import AudioSegment
import tempfile
import pytube
import PyPDF2
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://teachingassistant-g5fba8fcdrc5a9b9.canadacentral-01.azurewebsites.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set.")
    raise Exception("OPENAI_API_KEY must be set as an environment variable.")

openai.api_key = OPENAI_API_KEY

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

def transcribe_audio(audio_file_path):
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="verbose_json")
            return transcript
    except Exception as e:
        logger.error(f"Error in transcribe_audio: {e}")
        raise HTTPException(status_code=500, detail="Error during audio transcription.")

def summarize_text(text):
    try:
        system_prompt = "You are an assistant that summarizes text in 1000 words."
        user_prompt = f"""
        Text to summarize:
        "{text}"
        Provide a concise summary of 1000 words with key takeaways.
        """

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.5,
        )

        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"Error in summarize_text: {e}")
        raise HTTPException(status_code=500, detail="Error during summarization.")

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
    <head>
        <title>Lecture Notes Generator</title>
    </head>
    <body>
        <h1>Lecture Notes Generator</h1>
        <p>This is the backend API for the Lecture Notes Generator. Please use the /process endpoint to submit data.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/process")
async def process_files(
    youtube_link: str = Form(None),
    pdf_file: UploadFile = File(None),
    audio_file: UploadFile = File(None)
):
    try:
        if not youtube_link and not pdf_file and not audio_file:
            raise HTTPException(status_code=400, detail="Please provide one input: YouTube link, PDF file, or audio file.")

        text_content = ""

        # Handle YouTube Link
        if youtube_link:
            video = pytube.YouTube(youtube_link)
            stream = video.streams.filter(only_audio=True).first()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                stream.download(filename=tmp_file.name)
                tmp_file_path = tmp_file.name
            transcript = transcribe_audio(tmp_file_path)
            text_content = " ".join([segment['text'] for segment in transcript.get('segments', [])])
            os.unlink(tmp_file_path)

        # Handle PDF File
        elif pdf_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(await pdf_file.read())
                tmp_file_path = tmp_file.name
            with open(tmp_file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text_content = " ".join([page.extract_text() for page in reader.pages])
            os.unlink(tmp_file_path)

        # Handle Audio File
        elif audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(await audio_file.read())
                tmp_file_path = tmp_file.name
            transcript = transcribe_audio(tmp_file_path)
            text_content = " ".join([segment['text'] for segment in transcript.get('segments', [])])
            os.unlink(tmp_file_path)

        # Summarize and generate notes
        summary = summarize_text(text_content)

        return JSONResponse(content={
            'transcription': text_content,
            'summary': summary
        })
    except HTTPException as e:
        logger.error(f"HTTPException in /process endpoint: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled exception in /process endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
