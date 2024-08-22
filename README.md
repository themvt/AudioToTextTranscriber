# Audio to Text Transcriber

**Author**: Marco V. Torresi  
**Version**: 20240822-1920

## **Overview**
Audio to Text Transcriber is a Python application that transcribes audio files into text using OpenAI's Whisper API. This tool supports batch processing of audio files, saving transcriptions in Markdown (`.md`) and SubRip Subtitle (`.srt`) formats. The application features a graphical user interface (GUI) with folder path caching, real-time debugging output, and an "Always on Top" option for ease of use.

## **Key Features**
- **Batch Processing**: Transcribe multiple audio files in one go by selecting entire folders.
- **Multiple Output Formats**: Save transcriptions as Markdown and SRT files.
- **Real-Time Debugging**: View detailed logs of the transcription process in the GUI.
- **Folder Path Caching**: Automatically remember the last used folders for input and output.
- **Always on Top**: Keep the application window on top of other windows for better accessibility.

## **Installation and Setup**

### **1. Clone the Repository**
First, clone the repository to your local machine:
```bash
git clone https://github.com/your-username/audio-to-text-transcriber.git
cd audio-to-text-transcriber
```

### **2. Install Dependencies**
Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### **3. Set Up API Keys**
You'll need an OpenAI API key to use Whisper for transcription. Create a `.env` file in the root directory of the project and add your API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## **Usage**

### **Running the Application**
To run the Audio to Text Transcriber, execute the following command from the root directory of the project:
```bash
python main.py
```

### **Using the GUI**
Once the application is running, you will be presented with a graphical interface.

1. **Target Folder**: Click "Browse Target" to select the folder containing your audio files.
2. **Output Folder**: Click "Browse Output" to select the folder where the transcriptions will be saved.
3. **RUN**: Click the "RUN" button to start the transcription process. Progress will be displayed in the debug area.
4. **CANCEL**: If a transcription process is running, you can click "CANCEL" to stop it.
5. **EXIT**: Close the application by clicking the "EXIT" button.
6. **Always on Top**: Enable the "Always on Top" checkbox to keep the window on top of other applications.

### **Supported Audio Formats**
The application supports the following audio formats:
- `.mp3`
- `.wav`
- `.flac`

### **Transcription Output**
- **Markdown (`.md`)**: Contains the plain text transcription of the audio.
- **SubRip Subtitle (`.srt`)**: Includes timestamps and segmenting for subtitle-style output.

## **File Map**

### **Key Files**
- **`main.py`**: Entry point for the application. Initializes the GUI and starts the Tkinter main loop.
- **`gui_app.py`**: Contains the main logic for the graphical user interface (GUI), handling user input, folder selection, and process control.
- **`transcription.py`**: Manages the interaction with the Whisper API for transcribing audio files. Handles the saving of transcription results in both Markdown and SRT formats.
- **`utils_file.py`**: Utility module for file handling, including retrieving lists of audio files from the selected directories.
- **`target_dir.txt` / `output_dir.txt`**: Cache files that store the last used directories for input and output folders. These files help the application remember previous folder selections.

## **Dependencies**
This project relies on the following dependencies:
- `requests`
- `python-dotenv`
- `tkinter`
- Other dependencies are listed in the `requirements.txt` file.

## **Future Improvements**
- **Multi-Language Support**: Add an option to specify the input language for more accurate transcriptions of non-English audio.
- **Batch Progress Indicators**: Display progress bars or other visual indicators to show the progress of batch transcription jobs.
- **Error Handling**: Improve error handling to manage network issues or unsupported file formats more gracefully.
- **Custom Output Formats**: Allow users to customize the transcription output formats (e.g., plain text, JSON, VTT).

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.