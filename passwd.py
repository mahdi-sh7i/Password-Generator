from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel,
                             QPushButton, QSlider, QSpinBox, QLineEdit)
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from enum import Enum
from PyQt5 import uic
from enum import IntEnum
from math import log2
import secrets
import sys

class Characters(Enum):
    btn_lower = ascii_lowercase
    btn_upper = ascii_uppercase
    btn_digits = digits
    btn_special = punctuation

CHARACTER_NUMBER = {
    'btn_lower': len(Characters.btn_lower.value),
    'btn_upper': len(Characters.btn_upper.value),
    'btn_digits': len(Characters.btn_digits.value),
    'btn_special': len(Characters.btn_special.value)
}

class StrengthToEntropy(IntEnum):
    Excellent = 120
    Strong = 70
    Good = 50
    Weak = 30
    Pathetic = 0

def create_new(length: int, characters: str) -> str:
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_entropy(length: int, character_number: int) -> float:
    if character_number == 0:
        return 0.0  # Avoid division by zero
    return round(length * log2(character_number), 2)

class UI(QMainWindow):
    def __init__(self):  # Corrected from init to __init__
        super(UI, self).__init__()

        # Load The Ui file
        uic.loadUi("passwd.ui", self)

        # Define our widgets
        self.slider_length = self.findChild(QSlider, "slider_length")
        self.spinBox = self.findChild(QSpinBox, "spinBox")
        self.label_strength = self.findChild(QLabel, "label_strength")
        self.line_password = self.findChild(QLineEdit, "line_password")
        self.label_entropy = self.findChild(QLabel, "label_entropy")  # Ensure this label exists in your UI

        # Move The Slider
        self.slider_length.valueChanged.connect(self.slide_it)

        # Connect slider to spinbox
        self.slider_length.valueChanged.connect(self.spinBox.setValue)
        self.spinBox.valueChanged.connect(self.slider_length.setValue)

        #33
        self.btn_visibility.clicked.connect(self.toggle_visibility)

        # Connect buttons to generate password
        for btn_name in Characters:
            button = self.findChild(QPushButton, btn_name.name)
            if button:  # Check if button exists
                button.clicked.connect(self.set_password)

        # Connect refresh button
        self.btn_refresh = self.findChild(QPushButton, "btn_refresh")  # Ensure this button exists in your UI
        if self.btn_refresh:
            self.btn_refresh.clicked.connect(self.refresh_password)

        # Connect copy button
        self.btn_copy = self.findChild(QPushButton, "btn_copy")  # Ensure this button exists in your UI
        if self.btn_copy:
            self.btn_copy.clicked.connect(self.copy_to_clipboard)

        # Set initial password
        self.set_password()

        # Show The App
        self.show()

    def toggle_visibility(self):
        if self.line_password.echoMode() == QLineEdit.Normal:
            self.line_password.setEchoMode(QLineEdit.Password)
            
        else:
            self.line_password.setEchoMode(QLineEdit.Normal)
            

    def slide_it(self, value):
        self.set_password()  # Regenerate password on slider change

    def set_password(self):
        length = self.slider_length.value()
        characters = self.get_characters()

        if characters:  # Ensure characters are selected
            password = create_new(length=length, characters=characters)
            self.line_password.setText(password)
            self.set_entropy(length, len(characters))  # Update entropy after generating a new password
            self.set_strength(password)  # Pass the generated password to set strength

    def refresh_password(self):
        """Refresh the password when the refresh button is clicked."""



        self.set_password()  # Regenerate password on refresh

    def copy_to_clipboard(self):
        """Copy the generated password to the clipboard."""
        password = self.line_password.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(password)

    def get_characters(self) -> str:
        chars = ''
        for btn in Characters:
            button = self.findChild(QPushButton, btn.name)
            if button and button.isChecked():
                chars += btn.value
            
        return chars
    
    def set_entropy(self, length: int, char_num: int) -> None:
        entropy_value = get_entropy(length, char_num)
        self.label_entropy.setText(f'Entropy: {entropy_value} bits')

    def set_strength(self, password: str) -> None:
        length = len(password)
        char_num = len(self.get_characters())

        for strength in StrengthToEntropy:
            if get_entropy(length, char_num) >= strength.value:
                self.label_strength.setText(f'Strength: {strength.name}')
                break  # Exit after finding the first matching strength

# -------------------------------------------------------------

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()


