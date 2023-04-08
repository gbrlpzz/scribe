import sys
import os
from pydub import AudioSegment
import openai
from moviepy.editor import *

openai.api_key = "insert-your-api-key" #insert your api key here

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

def transcribe(saved_wav_file_path):
    file = open(saved_wav_file_path, "rb")
    transcription = openai.Audio.transcribe("whisper-1", file)
    
    text_output = transcription["text"]

    txt_file_path = os.path.splitext(saved_wav_file_path)[0] + ".txt"
    with open(txt_file_path, "w") as txt_file:
        txt_file.write(text_output)
    print(f"Transcription saved to: {txt_file_path}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audio_to_txt.py <input_file.mp3 or input_file.m4a or input_file.mp4>")
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
