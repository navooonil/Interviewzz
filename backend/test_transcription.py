import requests
import os

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1/transcription/transcribe"

def create_dummy_audio_file():
    """Creates a tiny valid WAV file for testing purposes."""
    # This is a minimal valid WAV header + 1 second of silence
    # We are doing this so we don't need to hunt for a file on your disk.
    header = b'\x52\x49\x46\x46\x24\x00\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61\x00\x00\x00\x00'
    filename = "test_audio.wav"
    with open(filename, "wb") as f:
        f.write(header)
    return filename

def test_transcription():
    print(f"Connecting to: {API_URL}")
    print("Generating dummy audio file...")
    filename = create_dummy_audio_file()
    
    try:
        print("Uploading file to server...")
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "audio/wav")}
            response = requests.post(API_URL, files=files)
            
        if response.status_code == 200:
            print("\n✅ SUCCESS! The server is working correctly.")
            print("Response from Whisper AI:")
            print(response.json())
        else:
            print(f"\n❌ FAILED. Status Code: {response.status_code}")
            print("Error details:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR: Could not connect to the server.")
        print("Make sure the black window is running properly!")
    except Exception as e:
        print(f"\n❌ AN ERROR OCCURRED: {e}")
    finally:
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    test_transcription()
