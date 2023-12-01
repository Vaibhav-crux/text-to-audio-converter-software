from PyQt6.QtWidgets import QDialog, QLabel, QTextEdit, QPushButton, QVBoxLayout, QLineEdit
import os, requests

class ChangeApiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change API")

        self.passwordLabel = QLabel("Enter Password:")
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passwordButton = QPushButton("Submit Password")

        self.label = QLabel("Enter API Key:")
        self.textEdit = QTextEdit()
        self.saveButton = QPushButton("Save")

        layout = QVBoxLayout()
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordLineEdit)
        layout.addWidget(self.passwordButton)
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)

        self.passwordButton.clicked.connect(self.validatePassword)
        self.saveButton.clicked.connect(self.saveApiKey)

        self.label.hide()
        self.textEdit.hide()
        self.saveButton.hide()

    def validatePassword(self):
        correct_password = "skoobVT"
        entered_password = self.passwordLineEdit.text()

        if entered_password == correct_password:
            self.passwordLabel.hide()
            self.passwordLineEdit.hide()
            self.passwordButton.hide()

            self.label.show()
            self.textEdit.show()
            self.saveButton.show()
        else:
            self.passwordLineEdit.clear()

    def saveApiKey(self):

        api_key = self.textEdit.toPlainText()

        headers = {"xi-api-key": api_key}
        url = "https://api.elevenlabs.io/v1/user"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            files_directory = "app/static/files"
            if not os.path.exists(files_directory):
                os.makedirs(files_directory)

            api_key_file_path = os.path.join(files_directory, "ApiKey.txt")
            with open(api_key_file_path, 'w') as file:
                file.write(api_key)

            print("API Key:", api_key)
            self.accept()
        else:
            self.textEdit.setStyleSheet("border: 1px solid red;") 