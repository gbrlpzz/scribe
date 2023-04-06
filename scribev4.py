import sys
import os
from pydub import AudioSegment
import openai
import whisper
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY
from moviepy.editor import *

def convert_audio_to_wav(input_file):
    try:
        output_file = os.path.splitext(input_file)[0] + ".wav"
        file_extension = os.path.splitext(input_file)[1].lower()

        if file_extension == ".mp3":
            audio = AudioSegment.from_mp3(input_file)
        elif file_extension == ".m4a":
            audio = AudioSegment.from_file(input_file, "m4a")
        elif file_extension == ".mp4":
            video = VideoFileClip(input_file)
            video.audio.write_audiofile(output_file, codec="pcm_s16le", verbose=False)
            print(f"Conversion successful! WAV file saved as: {output_file}")
            return output_file
        else:
            raise ValueError("Unsupported audio format")

        audio.export(output_file, format="wav")
        print(f"Conversion successful! WAV file saved as: {output_file}")
        return output_file
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None
    
def generate_title(text):
    openai.api_key = "openai-api-key"  # Replace with your actual API key

    prompt = f"Based on the following transcription, generate a concise and relevant title that captures the essence of the content:\n\n{text}\n\nTitle:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant that generates a title for a transcription."}, {"role": "user", "content": prompt}],
        max_tokens=20,
        n=1,
        temperature=0.3,
    )

    title = response.choices[0]['message']['content'].strip()
    return title

def save_to_pdf(text, filename, title):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Add the title to the PDF
    style_title = ParagraphStyle("Title", parent=styles["Heading1"], alignment=TA_CENTER, fontSize=14, spaceAfter=12)
    paragraphs = [Paragraph(title, style_title)]

    # Add the transcription text to the PDF
    style_text = ParagraphStyle("Text", parent=styles["BodyText"], alignment=TA_JUSTIFY, fontSize=12, spaceAfter=6)
    paragraphs += [Paragraph(line.strip(), style_text) for line in text.splitlines() if line.strip()]

    doc.build(paragraphs)

def transcribe(saved_wav_file_path):
    model = whisper.load_model("small")
    result = model.transcribe(saved_wav_file_path)
    text_output = result["text"]

    # Generate title using GPT-3.5-turbo
    title = generate_title(text_output)
    print(f"Generated title: {title}")

    pdf_file_path = os.path.splitext(saved_wav_file_path)[0] + ".pdf"
    save_to_pdf(text_output, pdf_file_path, title)
    print(f"Transcription saved to: {pdf_file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audio_to_wav.py <input_file.mp3 or input_file.m4a or input_file.mp4>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' not found.")
        sys.exit(1)

    if not (input_file.lower().endswith(".mp3") or input_file.lower().endswith(".m4a") or input_file.lower().endswith(".mp4")):
        print("Input file must be an MP3, M4A, or MP4 file.")
        sys.exit(1)

    saved_wav_file_path = convert_audio_to_wav(input_file)
    if saved_wav_file_path is not None:
        transcribe(saved_wav_file_path)
    else:
        print("Conversion failed, no WAV file path available.")
