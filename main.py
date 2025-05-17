from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pydub import AudioSegment
from transcription import transcribe_audio  # Corrected the import

app = FastAPI()

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the file temporarily
    temp_path = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert to WAV format
    output_wav_path = f"{UPLOAD_FOLDER}/{file.filename.split('.')[0]}.wav"
    
    try:
        # Convert to WAV using pydub
        audio = AudioSegment.from_file(temp_path, format="webm")
        audio.export(output_wav_path, format="wav")
        
        # Transcribe the audio
        transcription = transcribe_audio(output_wav_path)
        
        # Remove the temporary webm file
        os.remove(temp_path)

        return {"message": "ok", "transcription": transcription}
    
    except Exception as e:
        return {"error": str(e)}
