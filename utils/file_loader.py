import pandas as pd
import PyPDF2

def read_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif uploaded_file.name.endswith('.txt'):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        return df.to_string(index=False)
    else:
        return "Unsupported file format"

# import pandas as pd
# import fitz  # PyMuPDF

# def read_uploaded_file(uploaded_file):
#     if uploaded_file.name.endswith('.pdf'):
#         try:
#             text = []
#             # Read the uploaded file as bytes and pass to fitz
#             with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
#                 for page in doc:
#                     text.append(page.get_text())
#             return "\n".join(text)
#         except Exception as e:
#             return f"Error reading PDF file: {e}"
    
#     elif uploaded_file.name.endswith('.txt'):
#         try:
#             return uploaded_file.read().decode("utf-8")
#         except Exception as e:
#             return f"Error reading TXT file: {e}"
    
#     elif uploaded_file.name.endswith('.csv'):
#         try:
#             df = pd.read_csv(uploaded_file)
#             return df.to_string(index=False)
#         except Exception as e:
#             return f"Error reading CSV file: {e}"
    
#     else:
#         return "Unsupported file format"
