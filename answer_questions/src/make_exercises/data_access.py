import csv
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Exercise:
    """
    Represents a single exercise.
    """
    level_us: str
    level_fr: str
    question: str
    test_answer: str
    numeric_answer: Optional[float]
    units_1: str
    units_2: str
    units_3: str


def load_exercises_from_csv(csv_path: str) -> List[Exercise]:
    """
    Reads a CSV of exercises and returns a list of Exercise objects.
    The CSV is assumed to have the following header columns:
    - Level US
    - Level FR
    - Question
    - Test Answer
    - Numeric answer
    - Units 1
    - Units 2
    - Units 3

    Args:
        csv_path: Path to the exercises CSV file.

    Returns:
        A list of Exercise objects parsed from the CSV.
    """
    exercises = []
    
    with open(csv_path, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Extract the basic fields
            level_us = row.get('Level US', '').strip()
            level_fr = row.get('Level FR', '').strip()
            question = row.get('Question', '').strip()
            test_answer = row.get('Test Answer', '').strip()
            numeric_answer_str = row.get('Numeric answer', '').strip()

            # Convert the numeric answer to a float if possible; otherwise None
            try:
                numeric_answer = float(numeric_answer_str)
            except ValueError:
                numeric_answer = None

            units_1 = row.get('Units 1', '').strip()
            units_2 = row.get('Units 2', '').strip()
            units_3 = row.get('Units 3', '').strip()
            
            # Create and store the Exercise object
            ex = Exercise(
                level_us=level_us,
                level_fr=level_fr,
                question=question,
                test_answer=test_answer,
                numeric_answer=numeric_answer,
                units_1=units_1,
                units_2=units_2,
                units_3=units_3
            )
            exercises.append(ex)

    return exercises


def save_exercises_to_csv(exercises: List[Exercise], csv_path: str) -> None:
    """
    Saves a list of Exercise objects back to a CSV file with the same column structure.
    
    Args:
        exercises: The list of Exercise objects to write.
        csv_path: Path to the output CSV file.
    """
    fieldnames = [
        'Level US',
        'Level FR',
        'Question',
        'Test Answer',
        'Numeric answer',
        'Units 1',
        'Units 2',
        'Units 3'
    ]
    
    with open(csv_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for ex in exercises:
            # Convert numeric_answer back to string
            numeric_answer_str = (
                str(ex.numeric_answer) if ex.numeric_answer is not None else ""
            )
            
            writer.writerow({
                'Level US': ex.level_us,
                'Level FR': ex.level_fr,
                'Question': ex.question,
                'Test Answer': ex.test_answer,
                'Numeric answer': numeric_answer_str,
                'Units 1': ex.units_1,
                'Units 2': ex.units_2,
                'Units 3': ex.units_3
            })
