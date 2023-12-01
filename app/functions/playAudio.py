from elevenlabs import generate, VoiceSettings, Voice
from PyQt6.QtCore import Qt
import pygame
import io, os, threading
from time import sleep
from pydub import AudioSegment


pygame.mixer.init()
audio_channel = None
audio_process = None
audio_thread = None
stop_audio_flag = threading.Event()
# background_music_path = "app/static/Background Music/bg.mp3"

def updateButtonText(button1, is_playing):
    if is_playing:
        button1.setText("🛑")
    else:
        button1.setText("▶️")

def playAudio(textEdit, storytitle, button1, storyComboBox, slider, boostSlider, bgMusicSlider, styleSlider, switchCheckBox):
    global stop_audio_flag

    selected_voice = storyComboBox.currentData(Qt.ItemDataRole.UserRole)
    textEditValue = textEdit.toPlainText()
    storytitleValue = storytitle.toPlainText()

    if not textEditValue.strip():
        textEdit.setStyleSheet("border: 2px solid red;")
        return

    max_chunk_length = 5000
    completeStory =  storytitleValue+'<break time="1.75s" />'+textEditValue
    chunks = [completeStory[i:i + max_chunk_length] for i in range(0, len(completeStory), max_chunk_length)]

    slider_value = slider.value()
    boost_value = boostSlider.value()
    style_value = styleSlider.value()
    switch_value = switchCheckBox.isChecked()
    print(completeStory, selected_voice, slider_value, boost_value, style_value, switch_value)

    voice = Voice(
        voice_id=selected_voice[0],
        settings=VoiceSettings(
            stability=slider_value / 100.0,
            similarity_boost=boost_value / 100.0,
            style=style_value / 100.0,
            use_speaker_boost=switch_value
        )
    )

    audio_chunks = []

    for chunk in chunks:
        audio = generate(
            text=chunk,
            voice=voice
        )

        generated_audio = AudioSegment.from_file(io.BytesIO(bytes(audio)))

        background_music_path = ""  # "app/static/Background Music/bg4.mp3"
        bg_music_file_path = os.path.join("app/static/files", "Latest Background Music Used.txt")
        if os.path.exists(bg_music_file_path):
            with open(bg_music_file_path, "r") as f:
                background_music_path = f.readline()

        print(background_music_path)

        if background_music_path:
            background_music = AudioSegment.from_file(background_music_path, format="mp3")

            bg_music_value = bgMusicSlider.value()
            background_volume = bg_music_value / 100
            background_music = background_music - (60 - (60 * background_volume))

            mixed_audio = generated_audio.overlay(background_music)
        else:
            mixed_audio = generated_audio

        audio_chunks.append(mixed_audio)

    updateButtonText(button1, True)

    if not stop_audio_flag.is_set():
        for audio_chunk in audio_chunks:
            mixed_audio_wav = io.BytesIO()
            audio_chunk.export(mixed_audio_wav, format="wav")

            mixed_audio_wav.seek(0)
            pygame.mixer.music.load(mixed_audio_wav)
            pygame.mixer.music.play()

            while not stop_audio_flag.is_set() and audio_thread.is_alive() and pygame.mixer.music.get_busy():
                sleep(0.1)

            if stop_audio_flag.is_set():
                stopPlayingAudio()

    updateButtonText(button1, False)

def buttonClicked(textEdit, storytitle, button1, storyComboBox, slider, boostSlider, bgMusicSlider, styleSlider, switchCheckBox):
    global audio_thread, stop_audio_flag

    stop_audio_flag.clear()

    if audio_thread and audio_thread.is_alive():
        stop_audio_flag.set()  
        audio_thread.join()  
    else:
        audio_thread = threading.Thread(target=playAudio, args=(textEdit, storytitle, button1, storyComboBox, slider, boostSlider, bgMusicSlider, styleSlider, switchCheckBox), daemon=True)
        audio_thread.start()

    
def stopPlayingAudio():
    global audio_channel
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        audio_channel = None
