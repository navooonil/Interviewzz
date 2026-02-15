# Logic Flow & Setup Guide

## 1. 🛠️ One-Time Setup (Crucial!)

### A. Install FFmpeg (Required for Audio Processing)
Whisper relies on a tool called **FFmpeg** to handle audio files. You likely don't have this yet.

**Option 1: Using Winget (Easiest)**
Open a new terminal (PowerShell or Command Prompt) and run:
```powershell
winget install Gyan.FFmpeg
```
*Note: You may need to restart your terminal or computer after this for the command to be recognized.*

**Option 2: Manual Install**
1.  Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z).
2.  Extract the folder.
3.  Add the `bin` folder to your System PATH environment variable.

### B. Install Python Libraries
Navigate to your `backend` folder and run:
```bash
pip install -r requirements.txt
```
This installs FastAPI, Whisper, and other tools we added.

---

## 2. 🏃 How to Run the App

1.  Make sure you are in the `backend` folder.
2.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```
3.  You should see: `Uvicorn running on http://127.0.0.1:8000`

---

## 3. 🧪 How to Test (No Frontend Needed)

1.  Open your browser to: **`http://127.0.0.1:8000/docs`**
    *   This is the **Swagger UI** - a built-in testing tool for FastAPI.
2.  Scroll down to the **Transcription** section.
3.  Click on **`POST /api/v1/transcription/transcribe`**.
4.  Click **"Try it out"**.
5.  **Upload a file**: Choose a short `.mp3` or `.wav` file (start with a small one, < 1MB, as the model needs to load).
6.  Click **"Execute"**.

### What happens next?
*   The server receives the file.
*   It loads the AI model (this might take 10-20 seconds the first time).
*   It transcribes the audio.
*   You will see a JSON response with the text!

---

## 4. 🧩 Understanding the Logic Flow

1.  **Input**: User uploads `interview.mp3`.
2.  **API Layer (`api/transcription.py`)**:
    *   Receives the file.
    *   Checks if it is a valid audio file.
    *   Saves it to a temporary `uploads/` folder.
3.  **Service Layer (`services/transcription_service.py`)**:
    *   Loads the Whisper AI model.
    *   Processes the audio file.
    *   Extracts text and timestamps (start/end time for each word).
    *   Deletes the temporary file to save space.
4.  **Output**: Returns the JSON to the user.
