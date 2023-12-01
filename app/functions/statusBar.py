import os

def cursorPositionChanged(textEdit, statusBar):
    if not hasattr(statusBar, 'save_directory'):
        file_path = os.path.join("app/static/files", "VoiceSaveLocation.txt")
        with open(file_path, 'r') as f:
            statusBar.save_directory = f.readline()

            statusBar.save_directory = statusBar.save_directory.replace("\\", "/")


    cursor = textEdit.textCursor()

    # Get the block number and position within the block
    block_number = cursor.blockNumber() + 1
    column = cursor.positionInBlock() + 1

    # Calculate the row based on the block number
    row = block_number

    spaces = 50 * "\t"

    statusBar.showMessage(f"row: {row} | column: {column} {spaces} Path: {statusBar.save_directory}")
