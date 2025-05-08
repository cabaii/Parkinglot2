import sys
import random
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QGridLayout, QTableWidget, QTableWidgetItem, QLineEdit,
    QFrame
)
from PyQt6.QtCore import Qt, QTimer

CAR_TYPES = ["Sedan", "SUV", "Truck", "Van", "Coupe"]

def generate_license_plate():
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3)) + \
           "".join(random.choices("0123456789", k=3))

def generate_car_type():
    return random.choice(CAR_TYPES)


class LoginPage(QWidget):
    def __init__(self, switch_function):
        super().__init__()
        layout = QVBoxLayout()

        title = QLabel("Admin Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")

        login_button = QPushButton("Sign In")
        login_button.clicked.connect(self.check_credentials)

        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.error_label)
        layout.addWidget(login_button)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(100, 150, 100, 150)
        self.setLayout(layout)
        self.switch_function = switch_function

    def check_credentials(self):
        if self.username_input.text() == "SWE admin" and self.password_input.text() == "Parking":
            self.switch_function()
        else:
            self.error_label.setText("Invalid credentials")


class Dashboard(QWidget):
    def __init__(self, liveview_page):
        super().__init__()
        layout = QGridLayout()
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(5)
        layout.setContentsMargins(20, 0, 20, 0)

        self.stats = {
            "Vehicles Parked": QLabel(),
            "Lots Available": QLabel(),
            "Cars Today": QLabel(),
            "Avg. Time in Lot": QLabel("1h 32m")
        }

        for i, (title, label) in enumerate(self.stats.items()):
            box = self.create_info_box(title, label)
            layout.addWidget(box, i // 2, i % 2)

        self.setLayout(layout)
        self.liveview_page = liveview_page
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_stats)
        self.update_timer.start(2000)

    def create_info_box(self, title, value_label):
        box = QFrame()
        box.setFixedHeight(220)
        box.setStyleSheet("""
            QFrame {
                background-color: #0078d7;
                border: none;
                border-radius: 12px;
            }
            QLabel {
                color: white;
            }
            QLabel#title {
                font-weight: 700;
                font-size: 18px;
            }
            QLabel#value {
                font-size: 26px;
                font-weight: bold;
                margin-top: 5px;
            }
        """)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(15, 10, 15, 10)
        vbox.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("title")
        value_label.setObjectName("value")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox.addWidget(title_label)
        vbox.addWidget(value_label)
        box.setLayout(vbox)

        return box

    def update_stats(self):
        occupied = sum(1 for status in self.liveview_page.slot_statuses if status['occupied'])
        available = len(self.liveview_page.slot_statuses) - occupied
        cars_today = self.liveview_page.cars_today

        self.stats["Vehicles Parked"].setText(str(occupied))
        self.stats["Lots Available"].setText(str(available))
        self.stats["Cars Today"].setText(str(cars_today))


class LiveView(QWidget):
    def __init__(self, history_page):
        super().__init__()
        layout = QGridLayout()
        layout.setSpacing(10)
        self.slots = []
        self.slot_statuses = []
        self.cars_today = 0
        self.history_page = history_page

        for i in range(20):
            slot_label = QLabel(f"Slot {i + 1}")
            slot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            slot_label.setFixedSize(200, 120)
            layout.addWidget(slot_label, i // 5, i % 5)
            self.slots.append(slot_label)
            self.slot_statuses.append({"occupied": False, "plate": "", "type": "", "entry": None})

        self.setLayout(layout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slots)
        self.timer.start(3000)

    def update_slots(self):
        for i, slot_label in enumerate(self.slots):
            if random.random() < 0.4:
                is_occupied = not self.slot_statuses[i]['occupied']
                if is_occupied:
                    plate = generate_license_plate()
                    car_type = generate_car_type()
                    entry_time = datetime.now()
                    self.slot_statuses[i] = {
                        "occupied": True, "plate": plate,
                        "type": car_type, "entry": entry_time
                    }
                    self.history_page.add_entry(plate, car_type, entry_time)
                    self.cars_today += 1
                else:
                    if self.slot_statuses[i]['entry']:
                        exit_time = datetime.now()
                        plate = self.slot_statuses[i]['plate']
                        self.history_page.update_exit_time(plate, exit_time)
                    self.slot_statuses[i] = {"occupied": False, "plate": "", "type": "", "entry": None}

            status = self.slot_statuses[i]
            if status['occupied']:
                slot_label.setText(f"{status['plate']}\n{status['type']}")
                slot_label.setStyleSheet("background-color: red; color: white; border-radius: 6px; font-weight: bold;")
            else:
                slot_label.setText(f"Slot {i + 1}")
                slot_label.setStyleSheet("background-color: green; color: white; border-radius: 6px; font-weight: bold;")


class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["License Plate", "Car Type", "Entry Time", "Exit Time", "Status"])
        layout.addWidget(self.table)
        self.entries = {}
        self.setLayout(layout)

    def add_entry(self, plate, car_type, entry_time):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.entries[plate] = row
        self.table.setItem(row, 0, QTableWidgetItem(plate))
        self.table.setItem(row, 1, QTableWidgetItem(car_type))
        self.table.setItem(row, 2, QTableWidgetItem(entry_time.strftime("%Y-%m-%d %H:%M:%S")))
        self.table.setItem(row, 3, QTableWidgetItem("--"))
        self.table.setItem(row, 4, QTableWidgetItem("In"))

    def update_exit_time(self, plate, exit_time):
        row = self.entries.get(plate)
        if row is not None:
            self.table.setItem(row, 3, QTableWidgetItem(exit_time.strftime("%Y-%m-%d %H:%M:%S")))
            self.table.setItem(row, 4, QTableWidgetItem("Out"))


class ParkingDashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        heading = QLabel("🅿️ Parking System")
        heading.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dashboard_btn = QPushButton("Dashboard")
        liveview_btn = QPushButton("Live View")
        history_btn = QPushButton("History")
        for btn in (dashboard_btn, liveview_btn, history_btn):
            btn.setStyleSheet("background-color: #005fa3; color: white; padding: 10px; font-size: 16px;")

        self.stack = QStackedWidget()
        self.history_page = HistoryPage()
        self.liveview_page = LiveView(self.history_page)
        self.dashboard_page = Dashboard(self.liveview_page)
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.liveview_page)
        self.stack.addWidget(self.history_page)

        dashboard_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        liveview_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.liveview_page))
        history_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.history_page))

        sidebar.addWidget(heading)
        sidebar.addWidget(dashboard_btn)
        sidebar.addWidget(liveview_btn)
        sidebar.addWidget(history_btn)
        sidebar.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setStyleSheet("background-color: #0078d7;")

        layout.addWidget(sidebar_widget, 1)
        layout.addWidget(self.stack, 3)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Top-level stacked widget
    top_level_stack = QStackedWidget()

    # Create dashboard and login page
    dashboard = ParkingDashboard()
    login_page = LoginPage(lambda: top_level_stack.setCurrentWidget(dashboard))

    top_level_stack.addWidget(login_page)
    top_level_stack.addWidget(dashboard)
    top_level_stack.setCurrentWidget(login_page)

    top_level_stack.setWindowTitle("Admin Dashboard - Parking Lot Management")
    top_level_stack.resize(1000, 700)
    top_level_stack.show()

    sys.exit(app.exec())
