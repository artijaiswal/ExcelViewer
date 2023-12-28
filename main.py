import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Excel Viewer",
    page_icon="👋",
    layout="wide",
    
)

def intro():
    import streamlit as st

    st.write("# Welcome to Metadata Viewer! 👋")
    st.sidebar.success("Upload a file to view.")

    st.markdown(
        """
        Excel viewer is an app to see data more efficiently in UI. Without scrolling much.

        **👈 Upload the file and read the data , filter it out , check the metadata about the uploaded file.
    """
    )

def ReadFile(uploaded_file):
    df = "null"
    data = "null"
    if(uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        df = ReadWorkSheet(uploaded_file)
        ShowData(df)
    elif(uploaded_file.type == "text/csv"):
        df = ReadCSV(uploaded_file)
        ShowData(df)
    elif(uploaded_file.type == "application/json"):
        data = json.load(uploaded_file)
        ShowJsonData(data)
    else:
        return
    
def DownloadButton(uploaded_file):
    st.sidebar.download_button( 

    label="Open in Excel",

    data=uploaded_file.type,

    file_name=uploaded_file.name,

    mime=uploaded_file.type,
)

def ReadCSV(uploaded_file):
    return pd.read_csv(uploaded_file)
    

def ReadWorkSheet(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    sheet_name = st.sidebar.selectbox("Select Sheet", sheet_names)
    return pd.read_excel(uploaded_file, sheet_name)

def ShowData(df):
    columnTab, dataTab = st.tabs(["Column Details", "Data"])
    with columnTab:
        st.write(df.dtypes)
    with dataTab:
        st.dataframe(df)

def ShowJsonData(jsonData):
    keysList = list(jsonData.keys())
    columnTab, dataTab = st.tabs(["Column Details", "Data"])
    with columnTab:
        st.write(keysList)
    with dataTab:
        st.write(jsonData)
    
    
uploaded_files = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx", "json"], accept_multiple_files=True)

if len(uploaded_files) > 0:

    uploaded_file = st.sidebar.selectbox("Select file for view", uploaded_files, format_func=lambda x: x.name)
    if uploaded_file is not None:
            fileExpander = st.expander("File Metadata")
            with fileExpander:
                st.write(uploaded_file) 
            ReadFile(uploaded_file)
            DownloadButton(uploaded_file)
else:
    intro()