import streamlit as st
import pandas as pd

st.set_page_config(page_title='Simple Time Element Analysis', page_icon='img.png')

# ฟังก์ชันสำหรับคำนวณค่าทางสถิติ
def compute_statistics(df):
    # แปลงคอลัมน์ Date และ Time เป็นรูปแบบ datetime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    # คำนวณค่าทางสถิติ
    log_level_counts = df['LogLevel'].value_counts()
    timediff_mean = df['Timediff(ms)'].mean()
    timediff_median = df['Timediff(ms)'].median()
    message_counts = df['Message'].value_counts()

    return log_level_counts, timediff_mean, timediff_median, message_counts

def main():
    st.title("Data📂")
    
    # Display Table Data
    if 'dataframes' in st.session_state:
        file_names = st.session_state['file_names']
        dataframes = st.session_state['dataframes']
        for idx, df in enumerate(dataframes):
            file_name = file_names[idx]
            st.subheader(f"{file_name}")

            # Load custom CSS for DataFrame styling
            st.markdown("""
                <style>
                    table.dataframe {
                        width: 100%;
                    }
                </style>
            """, unsafe_allow_html=True)

            st.dataframe(df)

            # คำนวณค่าทางสถิติและแสดงผล
            log_level_counts, timediff_mean, timediff_median, message_counts = compute_statistics(df)

            st.write('**Count by LogLevel**')
            st.write(log_level_counts)
            
            st.write('**Message Frequencies**')
            st.write(message_counts)
                        
            st.write('**Mean Timediff(ms)**:', timediff_mean)
            st.write('**Median Timediff(ms)**:', timediff_median)

if __name__ == "__main__":
    main()

st.markdown("""
    <div class="content">
    <p>       </p>
        <p>
            &copy; 2024 By Patharanan P. | For Seagate Korat.
        </p>
    </div>
""", unsafe_allow_html=True)
