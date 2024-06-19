import streamlit as st
from unidecode import unidecode
import pandas as pd
from io import BytesIO
import nltk

nltk.download('punkt')

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
def process_text(input_text, mode):
    if mode == 'Prose':
        sentences = nltk.sent_tokenize(input_text)
        results = [(sanitize_text(sentence), alphanumeric_qabbala_sum(sanitize_text(sentence))) for sentence in sentences]
    else:  # Poetry
        lines = input_text.split('\n')
        results = [(sanitize_text(line), alphanumeric_qabbala_sum(sanitize_text(line))) for line in lines if line.strip()]
    return results

# Save results to Excel
def save_to_excel(results):
    df = pd.DataFrame(results, columns=['Line/Sentence', 'AQ Value'])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
    buffer.seek(0)
    return buffer

# Save results to plain text
def save_to_text(results):
    text_output = "\n".join(f"{line} | AQ Value: {aq_value}" for line, aq_value in results)
    return text_output.encode()

# Streamlit UI
st.title("Alphanumeric Qabbala Calculator")

# Add a toggle button for prose or poetry
mode = st.radio("Select mode:", ('Poetry (calculates by line breaks)', 'Prose (calculates by end of sentence)'))

text_input = st.text_area("Enter text:", height=300)

if st.button("Calculate AQ Values"):
    results = process_text(text_input, 'Prose' if 'Prose' in mode else 'Poetry')
    st.write("Results:")
    for line, aq_value in results:
        st.write(f"{line} | AQ Value: {aq_value}")

    st.write("Download Options:")

    # Create download buttons for Excel and Text files
    excel_data = save_to_excel(results)
    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name='aq_values.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    text_data = save_to_text(results)
    st.download_button(
        label="Download Text",
        data=text_data,
        file_name='aq_values.txt',
        mime='text/plain'
    )
