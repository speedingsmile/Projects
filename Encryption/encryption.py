import sys
import string
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit
from PyQt6.QtCore import Qt

# Vigenère Cipher functions
def is_letter(char):
    return char.isalpha()

def shift_char(char, shift):
    if not is_letter(char):
        return char
    base = ord('A') if char.isupper() else ord('a')
    return chr((ord(char) - base + shift) % 26 + base)

def vigenere_cipher(message, key, encrypt=True):
    result = ""
    key = key.upper()
    key_length = len(key)
    if key_length == 0:
        raise ValueError("Key cannot be empty")
    j = 0
    for char in message:
        if is_letter(char):
            shift = ord(key[j % key_length]) - ord('A')
            if not encrypt:
                shift = -shift
            result += shift_char(char, shift)
            j += 1
        else:
            result += char
    return result

# Caesar Cipher functions
def caesar_cipher(message, shift, encrypt=True):
    result = ""
    if not encrypt:
        shift = -shift
    for char in message:
        if char.isalpha():
            result += shift_char(char, shift)
        else:
            result += char
    return result

# Simple Substitution Cipher functions
def generate_cipher_alphabet(key):
    key = key.upper()
    cipher_alphabet = ""
    for char in key:
        if char not in cipher_alphabet:
            cipher_alphabet += char
    for char in string.ascii_uppercase:
        if char not in cipher_alphabet:
            cipher_alphabet += char
    return cipher_alphabet

def substitution_cipher(message, key, encrypt=True):
    cipher_alphabet = generate_cipher_alphabet(key)
    result = ""
    for char in message:
        if char.isalpha():
            if char.isupper():
                index = string.ascii_uppercase.index(char)
                result += cipher_alphabet[index] if encrypt else string.ascii_uppercase[cipher_alphabet.index(char)]
            else:
                index = string.ascii_lowercase.index(char)
                result += cipher_alphabet[index].lower() if encrypt else string.ascii_lowercase[cipher_alphabet.index(char.upper())]
        else:
            result += char
    return result

# Pigpen Cipher functions
PIGPEN_DICT = {
    'A': '⩃', 'B': '⩒', 'C': '⩔', 'D': '⫎', 'E': '⫍', 'F': '⫌',
    'G': '⩈', 'H': '⩉', 'I': '⩊', 'J': '⩋', 'K': '⩌', 'L': '⩍',
    'M': '⩐', 'N': '⩑', 'O': '⩏', 'P': '⫏', 'Q': '⫐', 'R': '⫑',
    'S': '⩧', 'T': '⩪', 'U': '⩨', 'V': '⩭', 'W': '⩬', 'X': '⩫',
    'Y': '⩮', 'Z': '⩯'
}

PIGPEN_REVERSE = {v: k for k, v in PIGPEN_DICT.items()}

def pigpen_cipher(message, encrypt=True):
    result = ""
    if encrypt:
        for char in message.upper():
            if char.isalpha():
                result += PIGPEN_DICT[char]
            else:
                result += char
    else:
        for char in message:
            if char in PIGPEN_REVERSE:
                result += PIGPEN_REVERSE[char]
            else:
                result += char
    return result
# Enigma Cipher functions
class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def forward(self, char):
        shift = (ord(char) - ord('A') + self.position) % 26
        return chr((ord(self.wiring[shift]) - ord('A') - self.position) % 26 + ord('A'))

    def backward(self, char):
        shift = (ord(char) - ord('A') + self.position) % 26
        return chr((self.wiring.index(chr(shift + ord('A'))) - self.position) % 26 + ord('A'))

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char):
        return self.wiring[ord(char) - ord('A')]

class EnigmaMachine:
    def __init__(self, rotor1, rotor2, rotor3, reflector):
        self.rotors = [rotor1, rotor2, rotor3]
        self.reflector = reflector

    def encrypt(self, message):
        result = ""
        for char in message.upper():
            if char.isalpha():
                # Rotate rotors
                if self.rotors[0].rotate():
                    if self.rotors[1].rotate():
                        self.rotors[2].rotate()

                # Forward pass through rotors
                for rotor in self.rotors:
                    char = rotor.forward(char)

                # Reflect
                char = self.reflector.reflect(char)

                # Backward pass through rotors
                for rotor in reversed(self.rotors):
                    char = rotor.backward(char)

                result += char
            else:
                result += char
        return result

    def decrypt(self, message):
        # Decryption is the same as encryption for the Enigma machine
        return self.encrypt(message)

def enigma_cipher(message, key, encrypt=True):
    # Define rotors and reflector
    rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
    rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
    rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
    reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    # Set initial positions based on the key
    for i, rotor in enumerate(key[:3]):
        rotor_position = ord(rotor.upper()) - ord('A')
        for _ in range(rotor_position):
            [rotor1, rotor2, rotor3][i].rotate()

    enigma = EnigmaMachine(rotor1, rotor2, rotor3, reflector)

    # Encryption and decryption are the same for Enigma
    return enigma.encrypt(message)

class MultiCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Cipher Encryption App")
        self.setGeometry(100, 100, 500, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Cipher selection
        cipher_layout = QHBoxLayout()
        cipher_label = QLabel("Cipher:")
        self.cipher_combo = QComboBox()
        self.cipher_combo.addItems(["Vigenère Cipher", "Caesar Cipher", "Simple Substitution Cipher", "Pigpen Cipher", "Enigma Cipher"])
        self.cipher_combo.currentTextChanged.connect(self.update_key_label)
        cipher_layout.addWidget(cipher_label)
        cipher_layout.addWidget(self.cipher_combo)
        layout.addLayout(cipher_layout)

        # Mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Encrypt", "Decrypt"])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)

        # Message input
        message_layout = QHBoxLayout()
        message_label = QLabel("Message:")
        self.message_input = QLineEdit()
        message_layout.addWidget(message_label)
        message_layout.addWidget(self.message_input)
        layout.addLayout(message_layout)

        # Key input
        key_layout = QHBoxLayout()
        self.key_label = QLabel("Key:")
        self.key_input = QLineEdit()
        key_layout.addWidget(self.key_label)
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        # Process button
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process)
        layout.addWidget(self.process_button)

        # Result output
        result_label = QLabel("Result:")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(result_label)
        layout.addWidget(self.result_output)

    def update_key_label(self, cipher):
        if cipher == "Pigpen Cipher":
            self.key_label.setText("Key: (Not needed for Pigpen)")
            self.key_input.setEnabled(False)
        elif cipher == "Enigma Cipher":
            self.key_label.setText("Key: (3 letters for rotor positions)")
            self.key_input.setEnabled(True)
        else:
            self.key_label.setText("Key:")
            self.key_input.setEnabled(True)

    def process(self):
        cipher = self.cipher_combo.currentText()
        mode = self.mode_combo.currentText()
        message = self.message_input.text()
        key = self.key_input.text()

        try:
            if cipher == "Vigenère Cipher":
                result = vigenere_cipher(message, key, mode == "Encrypt")
            elif cipher == "Caesar Cipher":
                shift = int(key)
                result = caesar_cipher(message, shift, mode == "Encrypt")
            elif cipher == "Simple Substitution Cipher":
                result = substitution_cipher(message, key, mode == "Encrypt")
            elif cipher == "Pigpen Cipher":
                result = pigpen_cipher(message, mode == "Encrypt")
            elif cipher == "Enigma Cipher":
                if len(key) != 3:
                    raise ValueError("Enigma key must be exactly 3 letters")
                result = enigma_cipher(message, key, mode == "Encrypt")
            else:
                raise ValueError("Invalid cipher selected")

            self.result_output.setPlainText(result)
        except ValueError as e:
            self.result_output.setPlainText(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiCipherApp()
    window.show()
    sys.exit(app.exec())