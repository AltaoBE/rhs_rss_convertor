import streamlit as st
import os
import pandas as pd
import time  # Import the time module
from data_extractor import DynamicFieldCSVReader  # Assuming the class is saved as dynamic_field_csv_reader.py

st.set_page_config(page_title="RSS/RHS Data Extractor", page_icon="🧪")
# Set the directory where the CSV format files are stored
CSV_FORMAT_FILES_DIR = './assets'
PASSWORD = ('9'*8) + "."  # Set your password here


def list_csv_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.csv')]


def save_uploaded_file(directory, uploadedfile):
    with open(os.path.join(directory, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return os.path.join(directory, uploadedfile.name)


def delete_file(directory, filename):
    os.remove(os.path.join(directory, filename))
    return not os.path.exists(os.path.join(directory, filename))


def customize_css():
    st.markdown("""
    <style>
    .stApp {
    background-image: url("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn.wallpapersafari.com%2F23%2F52%2Fe1npmx.jpg&f=1&nofb=1&ipt=7101b445b825a0f62ecc3b66b9324186efccbaf88aa0e86618796e3e3d8b8071&ipo=images");
    background-size: cover;
    }
    .stDeployButton{
    display: none;
    }
    header{
    display: none;
    }
    </style>
        """, unsafe_allow_html=True)


customize_css()
st.image('https://altao.com/file/2017/02/altao.png', width=300, )

# # Sidebar Scrapy Settings
# st.sidebar.image('logo.png', width=200)

# Streamlit app setup
st.title('RHS/RSS Data Extractor')

# List CSV files in the directory for the user to select for processing
csv_files = list_csv_files(CSV_FORMAT_FILES_DIR)
selected_csv = st.selectbox('Select the format CSV file for processing:', csv_files, key="process_selector")

st.markdown('---')
# File uploader for the user to upload RHS or RSS text file
uploaded_file = st.file_uploader("Upload the RHS or RSS text file for processing", type=['txt'], key="data_uploader")

# Exclusion list input
exclusion_list_input = st.text_input("Enter items to exclude from the excel file, separated by commas:",
                                     "Filler1, Filler2")
exclusion_list = exclusion_list_input.split(",")

# Button to process the uploaded text file
if st.button('Process'):
    if uploaded_file is not None and selected_csv:
        st.empty()
        # st.image('./img/loader.gif', width=300)
        st.info('Please wait...')


        # st.snow()

        # Save the uploaded file to the server
        saved_file_path = save_uploaded_file("input", uploaded_file)

        # Process the file using DynamicFieldCSVReader
        csv_path = os.path.join(CSV_FORMAT_FILES_DIR, selected_csv)
        format_reader = DynamicFieldCSVReader(csv_path)

        output_excel_path = f'./output/{uploaded_file.name.split(".")[0]}_extracted.xlsx'

        # Generate the Excel file
        format_reader.generate_excel(output_excel_path, saved_file_path, exclusion_list)
        st.empty()  # Clear the processing message
        st.success('Processing complete. Download the Excel file below.')
        st.balloons()
        with open(output_excel_path, "rb") as file:
            btn = st.download_button(
                label="Download Excel",
                data=file,
                file_name=f'{uploaded_file.name.split(".")[0]}_extracted.xlsx',
                mime="application/vnd.ms-excel"
            )
    else:
        st.error('Please upload a RHS/RSS text file and select a CSV format.')

st.markdown('---')
st.title('CSV Format File management')
# Password protection for uploading/deleting format files
password_input = st.text_input("Enter password to upload/delete CSV format files:", type="password")

# Section to upload a new CSV format file
if password_input == PASSWORD:
    format_file_uploader = st.file_uploader("Upload new CSV format file", type=['csv'], key="format_uploader")
    if format_file_uploader is not None:
        saved_format_file_path = save_uploaded_file(CSV_FORMAT_FILES_DIR, format_file_uploader)
        st.success(f"Successfully uploaded {format_file_uploader.name}.")

    # Section to delete an existing CSV format file
    csv_files = list_csv_files(CSV_FORMAT_FILES_DIR)
    selected_file_to_delete = st.selectbox('Select a CSV format file to delete:', [None] + csv_files,
                                           key="delete_selector")
    if st.button('Delete selected CSV file'):
        if selected_file_to_delete:
            if delete_file(CSV_FORMAT_FILES_DIR, selected_file_to_delete):
                st.success(f"Successfully deleted {selected_file_to_delete}.")
                csv_files.remove(selected_file_to_delete)  # Update the list to reflect the deletion
                csv_files = list_csv_files(CSV_FORMAT_FILES_DIR)
            else:
                st.error("Failed to delete the file.")
        else:
            st.error("Please select a file to delete.")

# Additional app information and styles
st.markdown('---')
st.markdown('**About:** This tool is designed to extract data from RHS/RSS files')
st.markdown(
    '**Note:** Please ensure the uploaded file and the format CSV file are in the correct format for optimal results.')

hide_streamlit_style = """
                <style>
                #MainMenu {display: none;}
                footer {display: none;}
                #root header{display: none;}
                .stDecoration{display: none;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add copyright notice
st.markdown('---')
st.markdown('__Made by **Altao** © 2023/2024__', unsafe_allow_html=True)
