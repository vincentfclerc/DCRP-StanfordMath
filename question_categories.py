import pandas as pd
import re



# Load the ODS file

file_path = './DATA/Dataset.ods'

ods_data = pd.read_excel(file_path, engine='odf')

# Define potential keywords for categorization

categories_keywords = {

    "Kinematics": ["speed", "velocity", "acceleration", "distance", "time", "travel"],
    "Dynamics": ["force", "mass", "acceleration", "Newton"],
    "Thermodynamics": ["temperature", "heat", "energy", "Carnot", "adiabatic"],
    "Electricity and Magnetism": ["charge", "current", "voltage", "electric", "photon"],
    "Waves and Optics": ["wavelength", "frequency", "light", "wave"],
    "Astrophysics": ["star", "planet", "orbit", "luminosity", "black hole", "Schwarzschild"],
    "Fluid Mechanics": ["fluid", "pipe", "flow", "rate"],
    "Work and Energy": ["work", "energy", "power"],
    "Chemistry": ["chemical", "reaction"],
    "General Math": ["ratio", "percentage", "convert", "calculate"],
    "Statistical Mechanics": ["entropy", "isothermal", "adiabatic"],
    "Quantum Mechanics": ["electron", "potential well", "quantum"],
    "Finance": ["interest", "deposit", "rate"],
    "Medicine": ["medication", "dose", "patient"]
}

# Create a function to categorize a question
def categorize_question(question):
    if pd.isnull(question):
        return "Uncategorized"
    question_lower = question.lower()
    for category, keywords in categories_keywords.items():
        if any(re.search(rf'\b{keyword}\b', question_lower) for keyword in keywords):
            return category
    return "Uncategorized"
# Apply categorization to the questions
ods_data['Category'] = ods_data['Question'].apply(categorize_question)
# Summarize the categories
category_summary = ods_data['Category'].value_counts().reset_index()
category_summary.columns = ['Category', 'Count']

