from functions.audioIdName import voices_list
from PyQt6.QtCore import Qt


def apiVoiceList(storyComboBox):
    for voice_id, voice_name in voices_list:
        storyComboBox.addItem(voice_name, (voice_id, voice_name))
        storyComboBox.setEditable(True)
        storyComboBox.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
