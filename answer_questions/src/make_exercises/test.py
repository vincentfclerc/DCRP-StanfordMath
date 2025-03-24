from data_access import load_exercises_from_csv, save_exercises_to_csv
exercises = load_exercises_from_csv('make_exercises/DATA/Dataset.csv')
for ex in exercises:
    print(ex.level_us, ex.level_fr, ex.question, ex.numeric_answer)
    # Perform randomization, computations, etc.
save_exercises_to_csv(exercises, 'make_exercises/DATA/Dataset-formatted.csv')