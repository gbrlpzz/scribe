# Scribe - Audio and Video Transcription and PDF Export

Scribe is a Python script that transcribes audio files using OpenAI Whisper and exports the transcriptions as PDF documents, enhanced by the gpt-3.5-turbo API. It supports MP3, M4A, and MP4 file formats as input and generates a PDF file with the transcription text formatted on an A4 size page. The script also utilizes OpenAI's GPT-3.5-turbo model to generate a title for the transcription.

## Local Version (scribe.py)

Features
Convert MP3, M4A, and MP4 files to WAV format for transcription
Transcribe audio files using the Whisper ASR model
Generate a title for the transcription using OpenAI's GPT-3.5-turbo model
Create a PDF file with the transcription text formatted on an A4 size page
Customize the style of the PDF output, including text alignment and font size

Usage: python scribev4.py <input_file>

Replace <input_file> with the path to your MP3, M4A, or MP4 file.

The script will transcribe the audio file, generate a title, and create a PDF file in the same directory as the input file with the same name but a .pdf extension.

Pre-requisites:

install whisper: pip install git+https://github.com/openai/whisper.git

Check out the different available pre-trained models and their performance on whisper's github: https://github.com/openai/whisper

Install  other dependencies:
pydub
openai
reportlab
moviepy

## API Version (diet-scribe.py)

1. Set your api key

2. Install all required dependencies: pydub, moviepy, openai

3. Run: python diet-scribe.py <input_file>

