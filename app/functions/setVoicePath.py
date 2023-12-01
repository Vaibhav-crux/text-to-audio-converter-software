from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QStandardPaths
import os

def setVoicePath():
    options = QFileDialog.Option.ShowDirsOnly
    voicePath = ""

    folder_path = QFileDialog.getExistingDirectory(
        None,  # Passing None as the parent
        "Select Voice Path",
        voicePath,
        options=options
    )

    if folder_path:
        voicePath = folder_path
        save_location = os.path.join("app/static/files", "VoiceSaveLocation.txt")
        
        # Create the "Files" folder if it doesn't exist
        os.makedirs("Files", exist_ok=True)

        with open(save_location, "w") as file:
            file.write(voicePath)
            

def save_default_music_directory():
        default_music_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MusicLocation)

        skoob_audio_folder = os.path.join(default_music_directory, 'Skoob Audio')
        if not os.path.exists(skoob_audio_folder):
            os.makedirs(skoob_audio_folder)

        file_path = os.path.join("app/static/files","VoiceSaveLocation.txt")
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(skoob_audio_folder)

