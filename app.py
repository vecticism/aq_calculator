import streamlit as st
from unidecode import unidecode
import pandas as pd

# Apply Alphanumeric Qabbala
def alphanumeric_qabbala_sum(text):
    qabbala_values = {chr(i + 96): i + 9 for i in range(1, 27)}
    qabbala_values.update({str(i): i for i in range(10)})
    text = unidecode(text)  # Normalize the text to replace accented characters
    standardized_text = ''.join(char.lower() for char in text if char.isalnum())  # Standardize text: remove non-alphanumeric and convert to lowercase
    return sum(qabbala_values[char] for char in standardized_text)

# Sanitize text for Excel
def sanitize_text(text):
    # Remove characters not allowed in Excel cells
    return ''.join(char for char in text if char not in ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x0B', '\x0C', '\x0E', '\x0F', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1A', '\x1B', '\x1C', '\x1D', '\x1E', '\x1F'])

# Process text and calculate AQ values
def process_text(input_text):
    lines = input_text.split('\n')
    results = []
    for line in lines:
        sanitized_line = sanitize_text(line)
        aq_value = alphanumeric_qabbala_sum(sanitized_line)
        results.append((sanitized_line, aq_value))
    return results

# Save results to Excel
def save_to_excel(results):
    df = pd.DataFrame(results, columns=['Line', 'AQ Value'])
    df.to_excel('aq_values.xlsx', index=False)
    return 'aq_values.xlsx'

# Save results to plain text
def save_to_text(results):
    file_path = 'aq_values.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        for line, aq_value in results:
            f.write(f"{line} | AQ Value: {aq_value}\n")
    return file_path

# Streamlit UI
st.title("Alphanumeric Qabbala Calculator")

text_input = st.text_area("Enter text:", height=300)

if st.button("Calculate AQ Values"):
    results = process_text(text_input)
    st.write("Results:")
    for line, aq_value in results:
        st.write(f"{line} | AQ Value: {aq_value}")

    st.write("Download Options:")
    if st.button("Export to Excel"):
        file_path = save_to_excel(results)
        st.write(f"Saved to {file_path}")
        st.download_button(
            label="Download Excel",
            data=open(file_path, 'rb').read(),
            file_name='aq_values.xlsx'
        )
    if st.button("Export to Text"):
        file_path = save_to_text(results)
        st.write(f"Saved to {file_path}")
        st.download_button(
            label="Download Text",
            data=open(file_path, 'rb').read(),
            file_name='aq_values.txt'
        )
