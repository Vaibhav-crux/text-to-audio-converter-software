from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QSlider, QStatusBar, QComboBox, QCheckBox, QMenuBar, QMessageBox
from PyQt6.QtGui import QMovie, QAction, QCloseEvent
from PyQt6.QtCore import Qt, QSize
from functions.actions import  updateValueLabel, clearTextArea, updateBoostValueLabel, updatebgMusicValueLabel
from functions.playAudio import buttonClicked
from functions.saveAudio import saveAudio
from functions.countCharacter import updateCharacterCount
from functions.statusBar import cursorPositionChanged
from functions.setVoicePath import setVoicePath, save_default_music_directory
from functions.voiceList import apiVoiceList
from functions.bgAudio import bgMusic
from functions.audioIdName import voices_list
from functions.changeapidialog import ChangeApiDialog
from functions.saveBgMusicInExcel import bgGui
import sys, os

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Skoob (Speech to Audio)")
        self.setStyleSheet("QMainWindow::title {background-color: blue;}")

        menubar = QMenuBar(self)
        fileMenu = menubar.addMenu('⚙️ Config') 
        changeApi = QAction('🔑 Change API', self)
        chooseFileDir = QAction('💻 Set Voice Path', self)
        addBgMusicDir = QAction('➕ Save Background Audio', self)

        fileMenu.addAction(changeApi)
        fileMenu.addSeparator()
        fileMenu.addAction(chooseFileDir)
        fileMenu.addSeparator()
        fileMenu.addAction(addBgMusicDir)

        save_default_music_directory()

        chooseFileDir.triggered.connect(setVoicePath)
        changeApi.triggered.connect(self.showChangeApiDialog)
        addBgMusicDir.triggered.connect(bgGui)


        storyLabel = QLabel("Story")
        backgroundComboBox = QComboBox()
        bgMusic(backgroundComboBox)

        storyComboBox = QComboBox()
        apiVoiceList(storyComboBox)

        clearButton = QPushButton("↻")

        titleLabel = QLabel("Title")
        storytitle = QTextEdit("Title here")

        textEdit = QTextEdit("Hey, what a lovely day! I'm just writing this text as an example. You can pick a voice from " 
                             "the drop-down menu and listen to it. Don't forget to erase this message before you start your story.")
        button1 = QPushButton("▶️")
        fileName = QTextEdit()
        mp3Label = QLabel(".mp3")
        button_save = QPushButton("📥")

        stabilityLabel = QLabel("Voice Stability")        
        slider = QSlider(Qt.Orientation.Horizontal, self)
        slider.setRange(0, 100)
        sliderValueLabel = QLabel(str(slider.value()))

        similarityBoostLabel = QLabel("Voice Tone")
        boostSlider = QSlider(Qt.Orientation.Horizontal, self)
        boostSlider.setRange(0, 100)
        boostSliderValueLabel = QLabel(str(boostSlider.value()))

        styleLabel = QLabel("Speaking Style")
        styleSlider = QSlider(Qt.Orientation.Horizontal, self)
        styleSlider.setRange(0, 100)
        styleSliderValueLabel = QLabel(str(styleSlider.value()))

        bgMusicLabel = QLabel("Music Volume")
        bgMusicSlider = QSlider(Qt.Orientation.Horizontal, self)
        bgMusicSlider.setRange(0, 100)
        bgMusicSlider.setValue(50)
        bgMusicSliderrValueLabel = QLabel(str(bgMusicSlider.value()))

        switchCheckBox = QCheckBox("Boost")
        switchCheckBox.setChecked(True)  

        spinner_label = QLabel()
        spinner_movie = QMovie("app/static/image/ghjl.gif")  
        spinner_movie.setScaledSize(QSize(100, 110)) 
        spinner_label.setMovie(spinner_movie)
        
        titleLabel.setStyleSheet("font-weight: bold; font-size: 20px")
        storyLabel.setStyleSheet("font-weight: bold; font-size: 20px")
        clearButton.setStyleSheet("font-weight: bold; font-size: 18px; background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #FFA500, stop: 1 #36454f);")
        button1.setStyleSheet("font-size: 20px")
        button_save.setStyleSheet("font-size: 20px")
        stabilityLabel.setStyleSheet("font-weight: bold; font-size: 12px")
        similarityBoostLabel.setStyleSheet("font-weight: bold; font-size: 12px")
        styleLabel.setStyleSheet("font-weight: bold; font-size: 12px")
        bgMusicLabel.setStyleSheet("font-weight: bold; font-size: 12px")

        switchCheckBox.setStyleSheet("font-weight: bold; font-size: 15px")


        storyComboBox.setFixedWidth(180)
        backgroundComboBox.setFixedWidth(100)
        clearButton.setFixedSize(40,26)
        storytitle.setFixedHeight(30)
        button1.setFixedSize(30, 30)
        fileName.setFixedSize(150, 30)
        button_save.setFixedSize(60, 30)
        spinner_label.setFixedSize(60,30)
        characterCountLabel = QLabel("Characters: 0/25000")
        slider.setFixedSize(180, 20)
        boostSlider.setFixedSize(180, 20)
        styleSlider.setFixedSize(180, 20)
        bgMusicSlider.setFixedSize(180,20)
        switchCheckBox.setFixedSize(60,40)

        statusBar = QStatusBar()
        statusBar.showMessage("row: 0 | column: 0")

        button1.clicked.connect(lambda: buttonClicked(textEdit, storytitle, button1, storyComboBox, slider, boostSlider, bgMusicSlider, styleSlider, switchCheckBox))

        slider.valueChanged.connect(lambda value: updateValueLabel(sliderValueLabel, value))
        boostSlider.valueChanged.connect(lambda value: updateBoostValueLabel(boostSliderValueLabel, value))
        styleSlider.valueChanged.connect(lambda value: updateBoostValueLabel(styleSliderValueLabel, value))
        bgMusicSlider.valueChanged.connect(lambda value: updatebgMusicValueLabel(bgMusicSliderrValueLabel, value))

        button_save.clicked.connect(lambda: saveAudio(textEdit, storytitle, fileName, storyComboBox, slider, boostSlider, bgMusicSlider, styleSlider, switchCheckBox, spinner_movie, spinner_label))

        textEdit.textChanged.connect(lambda: updateCharacterCount(textEdit, characterCountLabel))
        textEdit.cursorPositionChanged.connect(lambda: cursorPositionChanged(textEdit, statusBar))

        clearButton.clicked.connect(lambda: clearTextArea(textEdit, storytitle))


        # getAudioDirectory(statusBar)

        

        align_button = QVBoxLayout()

        align_button.setMenuBar(menubar)

        # Create a QHBoxLayout for storyLabel and storyComboBox
        story_layout = QHBoxLayout()
        story_layout.addWidget(titleLabel)
        story_layout.addStretch()
        story_layout.addWidget(storyComboBox)
        story_layout.addWidget(backgroundComboBox)
        story_layout.addWidget(clearButton)
        align_button.addLayout(story_layout)
        
        align_button.addWidget(storytitle)

        align_button.addWidget(storyLabel)
        align_button.addWidget(textEdit)

        # Create a QHBoxLayout to arrange buttons horizontally
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addStretch() 
        button_layout.addWidget(spinner_label)
        button_layout.addWidget(fileName)
        button_layout.addWidget(mp3Label)
        align_button.addWidget(characterCountLabel)
        button_layout.addWidget(button_save)
        align_button.addLayout(button_layout)

        # Create a QHBoxLayout for Stability and Similarity Boost
        stability_layout = QHBoxLayout()
        stability_layout.addWidget(stabilityLabel)
        stability_layout.addWidget(similarityBoostLabel)
        stability_layout.addWidget(styleLabel)
        stability_layout.addWidget(bgMusicLabel)
        align_button.addLayout(stability_layout)

        # Create a QHBoxLayout for sliders
        sliders_layout = QHBoxLayout()
        sliders_layout.addWidget(slider)
        sliders_layout.addWidget(sliderValueLabel)
        sliders_layout.addWidget(boostSlider)
        sliders_layout.addWidget(boostSliderValueLabel)
        sliders_layout.addWidget(styleSlider)
        sliders_layout.addWidget(styleSliderValueLabel)
        sliders_layout.addWidget(bgMusicSlider)
        sliders_layout.addWidget(bgMusicSliderrValueLabel)
        sliders_layout.addWidget(switchCheckBox)
        align_button.addLayout(sliders_layout)
        align_button.addWidget(statusBar)

        self.setLayout(align_button)

    def showChangeApiDialog(self):
    
        changeApiDialog = ChangeApiDialog(self)
        
        changeApiDialog.exec()
    
    def closeEvent(self, event: QCloseEvent):

        files_directory = "app/static/files"
        file_path = os.path.join(files_directory, "Latest Background Music Used.txt")
        with open(file_path, 'w') as file:
            file.write("")


        # reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
        #                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        # if reply == QMessageBox.StandardButton.Yes:
        #     # Perform your action before closing
        #     files_directory = "app/static/files"
        #     api_key_file_path = os.path.join(files_directory, "Latest Background Music Used.txt")
        #     with open(api_key_file_path, 'w') as file:
        #         file.write("")
            
        #     event.accept()
        # else:
        #     event.ignore()