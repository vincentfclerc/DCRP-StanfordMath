import pandas as pd
import re
from ollama import chat  # or from ollama import Ollama if you prefer an OO approach
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_final_bit(answer: str):
    """
    Utility function to extract the text between <A> and <\A>.
    Returns the content inside <A> ... <\\A>, or an empty string if not found.
    """
    pattern = r"<A>(.*?)<\\A>"
    match = re.search(pattern, answer, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

input_csv_path = '/Users/vincentclerc/Documents/Stanford/DCRP-StanfordMath/answer_questions/DATA/DatasetPython5.csv'
output_csv_path = '/Users/vincentclerc/Documents/Stanford/DCRP-StanfordMath/answer_questions/DATA/DatasetPython5_answers.csv'

# Log start of processing
logging.info(f"Starting the process. Reading input CSV from: {input_csv_path}")

# 1) Read the CSV
df = pd.read_csv(input_csv_path, sep=';', engine='python')  
logging.info(f"Input CSV loaded successfully. Total rows: {len(df)}")

# 2) Prepare columns to store results
full_answers = []
final_snippets = []

# 3) Process each question in the CSV
for idx, row in df.iterrows():
    logging.info(f"Processing row {idx + 1}/{len(df)}...")

    # Extract relevant columns
    question = row["Question"] if "Question" in df.columns else ""
    logging.debug(f"Question: {question}")

    # Additional context or instructions
    instructions = """You are a helpful physics assistant. 
    You will be given a question with numeric variables. 
    Provide a thorough, step-by-step solution, but ensure that, at the very end, 
    you produce the final numeric result in the format:

    <A> [numeric result] [units] <\\A>

    For example:
    Q1
    ...some explanation...
    <A> 14 m <\\A>
    Q2
    ...some explanation...
    <A> 19 kg.m^3 <\\A>
    """

    prompt = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": question}
    ]
    logging.debug(f"Prompt prepared: {prompt}")

    # Call the local Llama API via Ollama
    logging.info("Sending question to Llama API...")
    response = chat(model="llama3.1:latest", messages=prompt, stream=False)

    # The 'response' object is typically a dict with "message".
    full_answer_str = response["message"]["content"]
    logging.debug(f"Response received: {full_answer_str}")

    # Parse out the <A> ... <\A> portion
    final_bit = extract_final_bit(full_answer_str)
    logging.info(f"Extracted final bit: {final_bit}")

    # Store results
    full_answers.append(full_answer_str)
    final_snippets.append(final_bit)

# 4) Add results to DataFrame
df["Full Answer"] = full_answers
df["Final Snippet"] = final_snippets

# 5) Write results back to CSV
logging.info(f"Writing output to: {output_csv_path}")
df.to_csv(output_csv_path, index=False, sep=';')
logging.info("Process completed successfully.")
