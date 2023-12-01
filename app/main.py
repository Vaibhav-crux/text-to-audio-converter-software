import sys
from PySide6 import QtWidgets
import qdarkstyle
from design.gui import MyWidget
from qtpy.QtCore import QCoreApplication, QFile, QTextStream

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setStyleSheet(qdarkstyle.load_stylesheet())


    widget = MyWidget()

    # widget.resize(800, 600)
    widget.showMaximized()
    widget.show()

    sys.exit(app.exec())





'''
import sys
from PySide6 import QtWidgets
import qdarktheme
# from buttonClick import MyWidget
# from sliders import MyWidget
from adding_buttons_horz_vert import MyWidget


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Dark theme including toolbar
    # palette = qdarktheme.load_palette(theme="dark")
    # app.setPalette(palette)

    # Dark theme except toolbar
    qdarktheme.setup_theme()
    

    widget = MyWidget()

    widget.resize(800, 600)
    # widget.showMaximized()
    
    
    widget.show()

    sys.exit(app.exec())
'''
