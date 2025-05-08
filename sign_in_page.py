import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout

class SignInPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Smart Parking Lot - Sign In")
        self.setGeometry(100, 100, 300, 400)  # Adjust window size for phone screen
        
        # Set the layout for the sign-in page
        self.layout = QVBoxLayout()

        # Create and style the widgets
        self.title = QLabel("Welcome to Smart Parking Lot")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        
        # Form for username and password input
        self.form_layout = QFormLayout()
        
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.form_layout.addRow("Username:", self.username_input)
        self.form_layout.addRow("Password:", self.password_input)
        
        # Sign-in button
        self.sign_in_button = QPushButton("Sign In", self)
        self.sign_in_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px;")
        self.sign_in_button.clicked.connect(self.on_sign_in)

        # Add widgets to layout
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.sign_in_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.layout)

    def on_sign_in(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "password":
            print("Sign-in successful")
        else:
            print("Invalid username or password")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignInPage()
    window.show()
    sys.exit(app.exec())
