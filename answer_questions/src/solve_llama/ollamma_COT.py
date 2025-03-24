import pandas as pd
import re
from ollama import chat  # or from ollama import Ollama if you prefer an OO approach
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




# Parameters
input_csv_path = '/Users/vincentclerc/Documents/Stanford/DCRP-StanfordMath/answer_questions/DATA/DatasetPython5.csv'
output_csv_path = '/Users/vincentclerc/Documents/Stanford/DCRP-StanfordMath/answer_questions/DATA/DatasetPython5_answers-COT.csv'

# Chain of Thought Parameters
N_ITERATIONS = 3  # Number of CoT iterations
SAVE_EVERY = 100  # Save results every 100 questions

# Log start of processing
logging.info(f"Starting the process. Reading input CSV from: {input_csv_path}")

# 1) Read the CSV
df = pd.read_csv(input_csv_path, sep=';', engine='python')
logging.info(f"Input CSV loaded successfully. Total rows: {len(df)}")

# 2) Prepare columns to store results
for i in range(1, N_ITERATIONS + 1):
    df[f"Question_{i}"] = ""
    df[f"Answer_{i}"] = ""
df["Final Snippet"] = ""

# 3) Check if output CSV exists to resume processing
if os.path.exists(output_csv_path):
    logging.info(f"Output CSV found at {output_csv_path}. Loading existing data to resume.")
    df_existing = pd.read_csv(output_csv_path, sep=';', engine='python')
    start_idx = len(df_existing)
    if start_idx >= len(df):
        logging.info("All questions have already been processed.")
        exit()
    df = df.iloc[start_idx:]
    logging.info(f"Resuming from row {start_idx + 1}.")
else:
    logging.info("No existing output CSV found. Starting fresh.")

# 4) Define System Instructions
system_instructions = """You are a helpful physics assistant. 
You will be given a question with numeric variables. 
Provide a thorough, step-by-step solution, but ensure that, at the very end, 
you produce the final numeric result in the format:

<A> [numeric result] [units] <\\A>
"""

# 5) Process each question in the CSV
full_answers = []
final_snippets = []

for idx, row in df.iterrows():
    global_idx = idx  # Adjust if resuming
    logging.info(f"Processing row {global_idx + 1}/{len(df)}...")

    # Extract relevant columns
    question = row["Question"] if "Question" in df.columns else ""
    logging.debug(f"Question: {question}")

    # Initialize messages with system instructions and initial question
    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": question}
    ]

    # Store the initial question
    df.at[idx, "Question_1"] = question

    # Initialize variable to hold the latest answer
    latest_answer = ""

    try:
        for i in range(1, N_ITERATIONS + 1):
            logging.info(f"Sending Question_{i} to Llama API...")
            response = chat(model="llama3.1:latest", messages=messages, stream=False)

            # Extract the answer
            answer = response["message"]["content"]
            logging.debug(f"Response received: {answer}")

            # Store the answer
            df.at[idx, f"Answer_{i}"] = answer

            # Extract the final bit
            final_bit = extract_final_bit(answer)
            logging.info(f"Extracted final bit from Answer_{i}: {final_bit}")

            if i == N_ITERATIONS:
                df.at[idx, "Final Snippet"] = final_bit

            latest_answer = answer  # Update the latest answer

            # Prepare the next question if not the last iteration
            if i < N_ITERATIONS:
                follow_up_question = "Could you verify this answer?"
                df.at[idx, f"Question_{i + 1}"] = follow_up_question
                messages.append({"role": "user", "content": follow_up_question})

    except Exception as e:
        logging.error(f"An error occurred while processing row {global_idx + 1}: {e}")
        # Optionally, fill remaining answers/questions with NaN or a placeholder
        for j in range(i + 1, N_ITERATIONS + 1):
            df.at[idx, f"Question_{j}"] = "Error: Unable to process."
            df.at[idx, f"Answer_{j}"] = "Error: Unable to process."
        df.at[idx, "Final Snippet"] = "Error: Unable to extract."
        continue

    # Save progress every SAVE_EVERY questions
    if (global_idx + 1) % SAVE_EVERY == 0:
        logging.info(f"Saving progress at row {global_idx + 1}/{len(df)}.")
        df.iloc[:global_idx + 1].to_csv(output_csv_path, index=False, sep=';')
        logging.info(f"Progress saved to {output_csv_path}.")

# 6) Save the final results
logging.info("All questions processed. Saving final results.")
df.to_csv(output_csv_path, index=False, sep=';')
logging.info(f"Final results saved to: {output_csv_path}")
