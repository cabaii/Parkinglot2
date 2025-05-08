import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QGridLayout, QLineEdit, QFormLayout, QSpinBox, QTimeEdit, QDateEdit
)
from PyQt6.QtCore import Qt, QTimer, QDate, QTime
from datetime import datetime
import random


class LiveView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setSpacing(10)
        self.slots = []
        self.statuses = [False] * 20  # False = free, True = occupied

        for i in range(20):
            label = QLabel(f"Slot {i + 1}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedSize(200, 120)
            layout.addWidget(label, i // 5, i % 5)
            self.slots.append(label)

        self.setLayout(layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slots)
        self.timer.start(3000)

    def update_slots(self):
        for i, label in enumerate(self.slots):
            if random.random() < 0.4:
                self.statuses[i] = not self.statuses[i]
            if self.statuses[i]:
                label.setText("Occupied")
                label.setStyleSheet("background-color: red; color: white; border-radius: 6px; font-weight: bold;")
            else:
                label.setText(f"Slot {i + 1}")
                label.setStyleSheet("background-color: green; color: white; border-radius: 6px; font-weight: bold;")


class PaymentPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        layout.setContentsMargins(100, 50, 100, 50)

        self.card_number = QLineEdit()
        self.card_number.setPlaceholderText("1234 5678 9012 3456")
        self.expiry_date = QLineEdit()
        self.expiry_date.setPlaceholderText("MM/YY")
        self.cvv = QLineEdit()
        self.cvv.setPlaceholderText("CVV")
        self.cvv.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Card Number:", self.card_number)
        layout.addRow("Expiration Date:", self.expiry_date)
        layout.addRow("CVV:", self.cvv)
        self.setLayout(layout)


class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        layout.setContentsMargins(100, 50, 100, 50)

        self.username = QLineEdit()
        self.car_type = QLineEdit()
        self.car_make = QLineEdit()
        self.license_plate = QLineEdit()

        layout.addRow("Username:", self.username)
        layout.addRow("Car Type:", self.car_type)
        layout.addRow("Car Make:", self.car_make)
        layout.addRow("License Plate:", self.license_plate)
        self.setLayout(layout)


class ReservationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        layout.setContentsMargins(100, 50, 100, 50)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())

        self.spots_spinbox = QSpinBox()
        self.spots_spinbox.setMinimum(1)
        self.spots_spinbox.setMaximum(5)

        layout.addRow("Reservation Date:", self.date_edit)
        layout.addRow("Reservation Time:", self.time_edit)
        layout.addRow("Number of Spots:", self.spots_spinbox)

        self.setLayout(layout)


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QWidget()
        sidebar.setStyleSheet("background-color: #0078d7; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)
        heading = QLabel("🚗 User Panel")
        heading.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        sidebar_layout.addWidget(heading)

        button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 18px;
                padding: 12px 8px;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
        """

        liveview_btn = QPushButton("Live View")
        liveview_btn.setStyleSheet(button_style)
        payment_btn = QPushButton("Payment")
        payment_btn.setStyleSheet(button_style)
        profile_btn = QPushButton("Profile")
        profile_btn.setStyleSheet(button_style)
        reservation_btn = QPushButton("Reservation")
        reservation_btn.setStyleSheet(button_style)

        sidebar_layout.addWidget(liveview_btn)
        sidebar_layout.addWidget(payment_btn)
        sidebar_layout.addWidget(profile_btn)
        sidebar_layout.addWidget(reservation_btn)
        sidebar_layout.addStretch()

        # Pages
        self.stack = QStackedWidget()
        self.live_view = LiveView()
        self.payment_page = PaymentPage()
        self.profile_page = ProfilePage()
        self.reservation_page = ReservationPage()

        self.stack.addWidget(self.live_view)
        self.stack.addWidget(self.payment_page)
        self.stack.addWidget(self.profile_page)
        self.stack.addWidget(self.reservation_page)

        liveview_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.live_view))
        payment_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.payment_page))
        profile_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.profile_page))
        reservation_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.reservation_page))

        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(self.stack, 3)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserInterface()
    window.setWindowTitle("Parking Lot - User")
    window.resize(1000, 700)
    window.show()
    sys.exit(app.exec())
