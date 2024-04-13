import streamlit as st

from io import BytesIO
import docx
import PyPDF4
from io import BytesIO
import re
import pandas as pd
from pyresparser import ResumeParser



def extract_contact_info(text):




    phone_pattern = r'\b(?:\+\d{1,2}\s)?\d{3}[.-]?\d{3}[.-]?\d{4}\b'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    skills_pattern = r'(?i)\b(?:programming|python|java|javascript|html|css)\b'  # Add more skills as needed

    # Extracting information
    phone_numbers = re.findall(phone_pattern, text)
    email_addresses = re.findall(email_pattern, text)
    skills = re.findall(skills_pattern, text)

    return phone_numbers, email_addresses, skills
def read_pdf(file):
    """
    Function to read text from a PDF file.
    """
    pdf_file = BytesIO(file.read())
    pdf_reader = PyPDF4.PdfFileReader(pdf_file)
    full_text = []
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        full_text.append(page.extractText())
    return '\n'.join(full_text)
def read_docx(file):
    """
    Function to read text from a DOCX file.
    """
    docx_file = BytesIO(file.getvalue())
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)




def main():
    st.title("Upload Resumes Here...")
    all_skills = []
    all_phone_numbers = []
    all_email_addresses = []
    all_pdf_content = []

    uploaded_files = st.file_uploader("Resumes...", accept_multiple_files=True)

    if uploaded_files:
        st.write("Files uploaded:")
        for file in uploaded_files:
            file_details = {"FileName": file.name, "FileType": file.type, "FileSize": file.size}
            st.write(file_details)
            if file.type == "application/pdf":
                # Display PDF content in the Python shell
                pdf_content = read_pdf(file)


                phone_numbers, email_addresses, skills = extract_contact_info(pdf_content)

                phone_numbers = phone_numbers or ['']
                email_addresses = email_addresses or ['']
                skills = skills or ['']
                all_skills.append(skills)
                all_phone_numbers.append(phone_numbers)
                all_email_addresses.append(email_addresses)
                all_pdf_content.append(pdf_content)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # Display DOCX content in the Python shell
                docx_content =  read_docx(file)

                phone_numbers, email_addresses, skills = extract_contact_info(docx_content)

                phone_numbers = phone_numbers or ['']
                email_addresses = email_addresses or ['']
                skills = skills or ['']
                all_skills.append(skills)
                all_phone_numbers.append(phone_numbers)
                all_email_addresses.append(email_addresses)
                all_pdf_content.append(docx_content)
            else:
                st.write("Unsupported file type:", file.type)
        data = {
            'Skills': [item for sublist in all_skills for item in sublist],
            'Phone Numbers': [item for sublist in all_phone_numbers for item in sublist],
            'Email Addresses': [item for sublist in all_email_addresses for item in sublist],
            'PDF Content': all_pdf_content
        }
        df = pd.DataFrame(data)

        # Displaying DataFrame
        st.write("Extracted Information DataFrame:")
        st.write(df)
        st.write('Click on download icon to download dataframe into csv/excel file.')


if __name__ == "__main__":
    main()