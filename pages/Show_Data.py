import streamlit as st
import pandas as pd

st.set_page_config(page_title='Easy Analysis Time Element', page_icon='img.png')

def main():
    st.title("Data📂")
    st.write("Display data here")
    
    # Display Table Data all 
    if 'dataframes' in st.session_state:
        dataframes = st.session_state['dataframes']
        for idx, df in enumerate(dataframes):
            st.subheader(f"DataFrame {idx + 1}")
            st.dataframe(df)  # Display full DataFrame
    else:
        # When no data is available
        st.write("No data available. Please upload log files in the Analysis page.")

if __name__ == "__main__":
    main()




