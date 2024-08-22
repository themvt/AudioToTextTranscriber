import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

def transcribe_audio_files(file_paths, output_dir, log_callback):
    """
    Transcribes multiple audio files using OpenAI's Whisper API and saves the transcriptions as markdown and SRT files.
    """
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    for file_path in file_paths:
        log_callback(f"Starting processing of {file_path}...")
        
        with open(file_path, "rb") as audio_file:
            log_callback(f"Uploading {file_path} to API...")
            files = {"file": audio_file}
            data = {"model": "whisper-1", "response_format": "verbose_json"}
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()  # Raises an error for bad responses

            log_callback(f"Received response for {file_path}...")

            transcription_data = response.json()

            # Save transcription to markdown
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            md_output_path = os.path.join(output_dir, f"{base_name}.md")
            with open(md_output_path, "w") as md_file:
                log_callback(f"Saving transcription to {md_output_path}...")
                md_file.write(f"# Transcription for {base_name}\n\n")
                md_file.write(transcription_data['text'])

            # Save transcription to SRT
            srt_output_path = os.path.join(output_dir, f"{base_name}.srt")
            with open(srt_output_path, "w") as srt_file:
                log_callback(f"Saving SRT file to {srt_output_path}...")
                for i, segment in enumerate(transcription_data['segments']):
                    start_time = format_time(segment['start'])
                    end_time = format_time(segment['end'])
                    srt_file.write(f"{i+1}\n")
                    srt_file.write(f"{start_time} --> {end_time}\n")
                    srt_file.write(f"{segment['text'].strip()}\n\n")

            log_callback(f"Completed processing of {file_path}.")


def format_time(seconds):
    """
    Converts time in seconds to SRT timestamp format (hours, minutes, seconds, milliseconds).

    :param seconds: Time in seconds
    :return: Time in SRT format
    """
    milliseconds = int((seconds % 1) * 1000)
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
