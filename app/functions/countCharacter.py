def updateCharacterCount(textEdit, characterCountLabel):
        max_characters = 25000
        current_text = textEdit.toPlainText()
        character_count = len(current_text)
        characterCountLabel.setText(f"Characters: {character_count}/25000")

        if character_count > max_characters:
            textEdit.setPlainText(current_text[:max_characters])
            textEdit.setStyleSheet("QTextEdit { border: 2px solid red; }")
            # textEdit.setReadOnly(True)

        elif (character_count > (max_characters-20)):
            textEdit.setStyleSheet("QTextEdit { border: 2px solid orange; }")
            # textEdit.setReadOnly(False)
        else:
            textEdit.setStyleSheet("")
            # textEdit.setReadOnly(False)
