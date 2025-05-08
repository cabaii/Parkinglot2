import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QFormLayout, QDateEdit, QTimeEdit, QMessageBox, QSpinBox
)
from PyQt6.QtCore import QDate, QTime, Qt


class ReservationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Parking - Quick Reservation")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("Reserve Parking Spot(s)")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.title)

        self.form_layout = QFormLayout()

        # Date and time inputs
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())

        self.spots_input = QSpinBox()
        self.spots_input.setMinimum(1)
        self.spots_input.setMaximum(10)
        self.spots_input.setValue(1)

        # Add fields to the form layout
        self.form_layout.addRow("Reservation Date:", self.date_input)
        self.form_layout.addRow("Reservation Time:", self.time_input)
        self.form_layout.addRow("Number of Spots:", self.spots_input)

        self.layout.addLayout(self.form_layout)

        self.submit_button = QPushButton("Confirm Reservation")
        self.submit_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; font-size: 16px;")
        self.submit_button.clicked.connect(self.submit_reservation)
        self.layout.addWidget(self.submit_button)

    def submit_reservation(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm")
        spots = self.spots_input.value()
        total_cost = spots * 24

        print(f"Reservation confirmed for {spots} spot(s) on {date} at {time}.")
        print(f"Total Cost: ${total_cost}")

        QMessageBox.information(
            self,
            "Reservation Confirmed",
            f"{spots} spot(s) reserved for {date} at {time}.\nTotal cost: ${total_cost}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReservationPage()
    window.show()
    sys.exit(app.exec())
