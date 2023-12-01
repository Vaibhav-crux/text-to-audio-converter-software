import os
import eyed3

def extract_mp3_properties(file_path):
    audiofile = eyed3.load(file_path)

    if audiofile is not None:
        print("File Name:", os.path.basename(file_path))
        print("Directory Name:", os.path.basename(os.path.dirname(file_path)))
        total_time_seconds = int(audiofile.info.time_secs)
        print("Total Time (seconds):", total_time_seconds)
        print("-" * 40)  # Separator for better readability
    else:
        print("Error loading or missing metadata in the MP3 file.")

def scan_folder(folder_path):
    mp3_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".mp3")]

    for file in mp3_files:
        file_path = os.path.join(folder_path, file)
        extract_mp3_properties(file_path)

# Example usage
mp3_folder_path = "C:/Users/vaibh/Music/Skoob Audio/Color(new)"
scan_folder(mp3_folder_path)
