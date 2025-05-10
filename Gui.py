from typing import List, Tuple
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from gui_functions import get_highest_score, save_to_csv


class MainWindow(QWidget):
    """
    Main GUI window for the Student Grading System.
    Allows user input of student name, number of attempts, scores,
    and saves the highest score to a CSV file.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Student Grading System")
        self.setGeometry(100, 100, 300, 200)

        self.score_inputs: List[Tuple[QLabel, QLineEdit]] = []
        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the user interface layout and widgets."""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)

        self.name_label = QLabel("Student Name:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.attempts_label = QLabel("Number of Attempts:")
        self.attempts_input = QLineEdit()
        self.layout.addWidget(self.attempts_label)
        self.layout.addWidget(self.attempts_input)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.generate_score_inputs)
        self.layout.addWidget(self.next_button)

        self.grade_button = QPushButton("Grade Student")
        self.grade_button.clicked.connect(self.grade_student)
        self.grade_button.hide()

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.hide()

        self.setLayout(self.layout)

    def generate_score_inputs(self) -> None:
        """
        Generates input fields dynamically based on the number of attempts entered.
        Clears any existing score inputs and repositions buttons and labels.
        """
        try:
            num_attempts = int(self.attempts_input.text())
            if not (1 <= num_attempts <= 4):
                raise ValueError("Attempts must be between 1 and 4.")
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Please enter a number from 1 to 4.")
            return

        for label, input_field in self.score_inputs:
            self.layout.removeWidget(label)
            label.deleteLater()
            self.layout.removeWidget(input_field)
            input_field.deleteLater()
        self.score_inputs.clear()

        self.layout.removeWidget(self.grade_button)
        self.grade_button.hide()
        self.layout.removeWidget(self.status_label)
        self.status_label.hide()

        for i in range(num_attempts):
            score_label = QLabel(f"Score for Attempt {i + 1}:")
            score_input = QLineEdit()
            score_input.setPlaceholderText("e.g. 85")
            self.layout.addWidget(score_label)
            self.layout.addWidget(score_input)
            self.score_inputs.append((score_label, score_input))

        self.next_button.hide()

        self.layout.addWidget(self.grade_button)
        self.grade_button.show()
        self.layout.addWidget(self.status_label)

    def grade_student(self) -> None:
        """
        Gathers input, calculates the final grade (highest score),
        saves to CSV, and displays a submission status.
        """
        try:
            name = self.name_input.text().strip()
            if not name:
                QMessageBox.warning(self, "Missing Name", "Please enter the student's name.")
                return

            try:
                scores: List[int] = [int(input_field.text()) for _, input_field in self.score_inputs]
            except ValueError:
                QMessageBox.critical(self, "Invalid Scores", "All scores must be integers.")
                return

            final_score = get_highest_score(scores)
            save_to_csv(name, scores, final_score)

            self.status_label.setText("Submitted")
            self.status_label.show()

        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An error occurred: {str(e)}")
