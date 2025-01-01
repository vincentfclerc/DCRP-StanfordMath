import pandas as pd



# Load the ODS file

file_path = 'DCRP-StanfordMath/DATA/Dataset.ods'

ods_data = pd.read_excel(file_path, engine='odf')



# Generate LaTeX code from the dataset

latex_preamble = r"""\documentclass{article}
\usepackage{graphicx} % Required for inserting images
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts,amsthm}
\usepackage{lmodern}
\usepackage{setspace}

\title{questions-stanfordMath}
\author{vincent.clerc.ucbl }
\date{December 2024}

\begin{document}
"""

latex_end = r"\end{document}"

# Generate the body of the document
latex_body = ""
for index, row in ods_data.iterrows():
    question = row['Question'].replace('_x000c_', '') if pd.notnull(row['Question']) else ''
    test_answer = row['Test Answer'].replace('_x000c_', '') if pd.notnull(row['Test Answer']) else ''
    
    section = f"\\section{{}}\n{question}\n\n{test_answer}\n\n"
    latex_body += section

# Combine all parts
latex_document = latex_preamble + latex_body + latex_end

# Save LaTeX code to a file
latex_file_path = 'DCRP-StanfordMath/TEX/questions_stanfordMath.tex'
with open(latex_file_path, 'w') as latex_file:
    latex_file.write(latex_document)

# Provide download link
latex_file_path
