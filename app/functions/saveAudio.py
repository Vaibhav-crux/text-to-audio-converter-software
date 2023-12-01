from elevenlabs import generate, VoiceSettings, Voice
import elevenlabs
import threading
from PyQt6.QtCore import Qt, QCoreApplication, QMetaObject, Q_ARG
import os, io
from pydub import AudioSegment



audio_thread = None

def saveAudio(textEdit, storytitle, fileName, storyComboBox, slider, boostSlider, bgMusicSlider, styleSlider, switchCheckBox, spinner_movie, spinner_label):
    spinner_movie.start()
    spinner_label.setVisible(True)
    QCoreApplication.processEvents()

    textEditValue = textEdit.toPlainText()
    storytitleValue = storytitle.toPlainText()
    fileNameValue = fileName.toPlainText()

    if not textEditValue.strip():
        spinner_movie.stop()
        spinner_label.setVisible(False)
        textEdit.setStyleSheet("border: 2px solid red;")
        return
    
    if not fileNameValue.strip():
        spinner_movie.stop()
        spinner_label.setVisible(False)
        fileName.setStyleSheet("border: 1px solid red;")
        return

    selected_voice = storyComboBox.currentData(Qt.ItemDataRole.UserRole)
    slider_value = slider.value()
    boost_value = boostSlider.value()
    style_value = styleSlider.value()
    switch_value = switchCheckBox.isChecked()
    print(textEditValue)

    def generate_and_save():
        voice = Voice(
            voice_id=selected_voice[0],
            settings=VoiceSettings(
                stability=slider_value / 100.0,
                similarity_boost=boost_value / 100.0,
                style=style_value / 100.0,
                use_speaker_boost=switch_value
            )
        )


        max_chunk_length = 5000
        completeStory =  storytitleValue+'<break time="1.75s" />'+textEditValue
        chunks = [completeStory[i:i + max_chunk_length] for i in range(0, len(completeStory), max_chunk_length)]

        concatenated_audio = b"" 

        for chunk in chunks:
            audio = generate(
                text=chunk,
                voice=voice
            )
            concatenated_audio += bytes(audio)

         # Load background music
        background_music_path = "" # "app/static/Background Music/bg4.mp3"
        bg_music_file_path = os.path.join("app/static/files", "Latest Background Music Used.txt")
        if os.path.exists(bg_music_file_path):
            with open(bg_music_file_path, "r") as f:
                background_music_path = f.readline()
        print(background_music_path)
        if os.path.isfile(background_music_path):
            background_music = AudioSegment.from_file(background_music_path, format="mp3")

            # Adjust the length of the background music to match the generated audio
            background_music = background_music[:len(concatenated_audio)]

            bg_music_value = bgMusicSlider.value()

            # Adjust background audio volume (adjust the value as needed)
            background_volume = bg_music_value / 100  # Adjust as needed, 1.0 means full volume
            background_music = background_music - (60 - (60 * background_volume))

            # Mix the generated audio with the background music
            mixed_audio = AudioSegment.from_file(io.BytesIO(concatenated_audio), format="mp3")
            mixed_audio = mixed_audio.overlay(background_music)
        else:
            # If background music file is not present, use the generated audio directly
            mixed_audio = AudioSegment.from_file(io.BytesIO(concatenated_audio), format="mp3")

        QMetaObject.invokeMethod(spinner_movie, "stop", Qt.QueuedConnection)
        QMetaObject.invokeMethod(spinner_label, "setVisible", Qt.QueuedConnection, Q_ARG(bool, False))

        file_path = os.path.join("app/static/files", "VoiceSaveLocation.txt")
        with open(file_path, 'r') as f:
            save_directory = f.readline()
        full_path = os.path.join(save_directory, fileNameValue + ".mp3")

        # Save the mixed or generated audio
        mixed_audio.export(full_path, format="mp3")

        fileName.setStyleSheet("")

    audio_thread = threading.Thread(target=generate_and_save)
    audio_thread.start()


























# audio_thread = None

# def saveAudio(textEdit, storytitle, fileName, storyComboBox, slider, boostSlider, styleSlider, switchCheckBox, spinner_movie, spinner_label):
#     spinner_movie.start()
#     spinner_label.setVisible(True)
#     QCoreApplication.processEvents()

#     textEditValue = textEdit.toPlainText()
#     storytitleValue = storytitle.toPlainText()
#     fileNameValue = fileName.toPlainText()

#     if not textEditValue.strip():
#         spinner_movie.stop()
#         spinner_label.setVisible(False)
#         textEdit.setStyleSheet("border: 2px solid red;")
#         return
    
#     if not fileNameValue.strip():
#         spinner_movie.stop()
#         spinner_label.setVisible(False)
#         fileName.setStyleSheet("border: 1px solid red;")
#         return

#     selected_voice = storyComboBox.currentData(Qt.ItemDataRole.UserRole)
#     slider_value = slider.value()
#     boost_value = boostSlider.value()
#     style_value = styleSlider.value()
#     switch_value = switchCheckBox.isChecked()
#     print(storytitleValue+"\n"+textEditValue)

#     def generate_and_save():
#         voice = Voice(
#             voice_id=selected_voice[0],
#             settings=VoiceSettings(
#                 stability=slider_value / 100.0,
#                 similarity_boost=boost_value / 100.0,
#                 style=style_value / 100.0,
#                 use_speaker_boost=switch_value
#             )
#         )

#         max_chunk_length = 5000
#         completeStory =  storytitleValue+'<break time="1.75s" />'+textEditValue
#         chunks = [completeStory[i:i + max_chunk_length] for i in range(0, len(completeStory), max_chunk_length)]

#         concatenated_audio = b"" 

#         for chunk in chunks:
#             audio = generate(
#                 text=chunk,
#                 voice=voice
#             )
#             concatenated_audio += bytes(audio)

#         QMetaObject.invokeMethod(spinner_movie, "stop", Qt.QueuedConnection)
#         QMetaObject.invokeMethod(spinner_label, "setVisible", Qt.QueuedConnection, Q_ARG(bool, False))

#         file_path = os.path.join("app/static/files","VoiceSaveLocation.txt")
#         with open(file_path,'r') as f:
#             save_directory = f.readline()
#         full_path = os.path.join(save_directory, fileNameValue + ".mp3")
#         elevenlabs.save(concatenated_audio, full_path)

#         fileName.setStyleSheet("")
        

#     audio_thread = threading.Thread(target=generate_and_save)
#     audio_thread.start()