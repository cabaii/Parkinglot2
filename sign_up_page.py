import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout

class DetailsPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Smart Parking Lot - Car Details")
        self.setGeometry(100, 100, 350, 500)  # Adjust window size for phone screen
        
        # Set the layout for the details page
        self.layout = QVBoxLayout()

        # Create and style the widgets
        self.title = QLabel("Enter Car and Driver Details")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        
        # Form for details input
        self.form_layout = QFormLayout()

        # Create input fields for the details
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.car_type_input = QLineEdit(self)
        self.car_type_input.setPlaceholderText("Car Type")
        self.car_type_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.car_make_model_input = QLineEdit(self)
        self.car_make_model_input.setPlaceholderText("Car Make/Model")
        self.car_make_model_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.car_color_input = QLineEdit(self)
        self.car_color_input.setPlaceholderText("Car Color")
        self.car_color_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.vin_number_input = QLineEdit(self)
        self.vin_number_input.setPlaceholderText("VIN Number")
        self.vin_number_input.setStyleSheet("padding: 10px; font-size: 16px;")

        self.license_number_input = QLineEdit(self)
        self.license_number_input.setPlaceholderText("Driver's License Number")
        self.license_number_input.setStyleSheet("padding: 10px; font-size: 16px;")

        # Add the inputs to the form layout
        self.form_layout.addRow("First Name:", self.first_name_input)
        self.form_layout.addRow("Last Name:", self.last_name_input)
        self.form_layout.addRow("Car Type:", self.car_type_input)
        self.form_layout.addRow("Car Make/Model:", self.car_make_model_input)
        self.form_layout.addRow("Car Color:", self.car_color_input)
        self.form_layout.addRow("VIN Number:", self.vin_number_input)
        self.form_layout.addRow("Driver's License Number:", self.license_number_input)
        
        # Submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px;")
        self.submit_button.clicked.connect(self.on_submit)

        # Add widgets to the layout
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.layout)

    def on_submit(self):
        # Collect input data
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        car_type = self.car_type_input.text()
        car_make_model = self.car_make_model_input.text()
        car_color = self.car_color_input.text()
        vin_number = self.vin_number_input.text()
        license_number = self.license_number_input.text()
        
        # For now, print the collected data (this can later be saved or sent somewhere)
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Car Type: {car_type}")
        print(f"Car Make/Model: {car_make_model}")
        print(f"Car Color: {car_color}")
        print(f"VIN Number: {vin_number}")
        print(f"Driver's License Number: {license_number}")
        
        # Optionally, you can show a success message after submission
        print("Details submitted successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DetailsPage()
    window.show()
    sys.exit(app.exec())
