import whisper
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Load the Whisper model with CPU-only mode
model = whisper.load_model("base", device="cpu")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes the given audio file and returns the text in English.

    Args:
        file_path (str): Path to the audio file (.wav format)

    Returns:
        str: Transcribed text in English
    """
    try:
        print(f"Transcribing: {file_path}...")
        
        # Force Whisper to use English only for faster processing
        result = model.transcribe(file_path, language="en")
        
        print(result["text"])
        return result['text']
    except Exception as e:
        print(f"Error during transcription: {e}")
        return "Error"
