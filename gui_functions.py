import csv
import os
from typing import List


def get_highest_score(scores: List[int]) -> int:
    return max(scores)


def save_to_csv(name: str, scores: List[int], final_score: int) -> None:
    file_exists = os.path.exists("grades.csv")
    with open("grades.csv", mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Student Name", "Score 1", "Score 2", "Score 3", "Score 4", "Final"])

        # Ensure exactly 4 score fields (pad with empty strings if fewer)
        padded_scores = scores + [""] * (4 - len(scores))
        row = [name] + padded_scores + [final_score]
        writer.writerow(row)