import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dask.dataframe as dd  # type: ignore
import tempfile
import os

st.set_page_config(page_title='Simple Time Element Analysis', page_icon='img.png')

# ฟังก์ชันวิเคราะห์ DataFrame และคืนค่าผลลัพธ์ที่กรองแล้ว
def analyze_headload(df, active_process_name, state_names):
    filtered_df = df[df['ActiveProcessName'] == active_process_name]
    
    if state_names:
        filtered_df = filtered_df[filtered_df['StateName'].isin(state_names)]
    
    # กรองแถวที่มีค่า 'TargetStateName' เป็น 'None'
    filtered_df = filtered_df[filtered_df['TargetStateName'] != "None"]
    
    return filtered_df

# ฟังก์ชันประมวลผลไฟล์ CSV ขนาดใหญ่ด้วย Dask DataFrame
def process_large_logfile(file_path):
    # อ่าน CSV โดยใช้ Dask DataFrame
    ddf = dd.read_csv(file_path)
    return ddf

def main():
    st.title("Analysis 📊")

    uploaded_file = st.file_uploader('Upload a large CSV file', type='csv')

    if uploaded_file:
        st.text(uploaded_file.name)

        # สร้างไฟล์ชั่วคราว
        temp_file_path = tempfile.NamedTemporaryFile(delete=False).name

        # เขียนไฟล์ที่อัปโหลดไปยังตำแหน่งชั่วคราว
        with open(temp_file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())

        # ประมวลผลไฟล์ล็อกขนาดใหญ่ด้วย Dask DataFrame
        ddf = process_large_logfile(temp_file_path)

        if ddf is not None:
            # แปลง Dask DataFrame เป็น Pandas DataFrame เพื่อใช้สำหรับการเลือกและการพล็อต
            df = ddf.compute()

            # ตัดช่องว่างที่หัวข้อคอลัมน์
            df.columns = df.columns.str.strip()

            # เลือกเกณฑ์การกรองด้วย Pandas DataFrame
            active_process_name = st.selectbox('Select ActiveProcessName', df['ActiveProcessName'].unique())
            
            if active_process_name:
                state_names = df[df['ActiveProcessName'] == active_process_name]['StateName'].unique()
                selected_state_names = st.multiselect('Select StateName(s)', state_names, default=list(state_names))
            else:
                selected_state_names = []
                
            # วิเคราะห์และพล็อตด้วย Pandas DataFrame ตามค่าที่เลือก
            filtered_df = analyze_headload(df, active_process_name, selected_state_names)

            if not filtered_df.empty:
                st.subheader('Filtered Data')
                st.write(filtered_df)

                # คำนวณค่าเฉลี่ย 'Diff or period of time' สำหรับแต่ละ StateName
                avg_diff = filtered_df.groupby('StateName')['Diff or period of time'].mean().reset_index()

                # การพล็อตข้อมูล
                plt.figure(figsize=(10, 6))
                ax = sns.barplot(data=avg_diff, x='StateName', y='Diff or period of time')
                plt.xlabel('StateName')
                plt.ylabel('Avg Diff or period of time')
                plt.title('Average Diff or period of time for selected StateNames')
                plt.xticks(rotation=45, ha='right')  # หมุนตัวหนังสือแกน X เอียง 45 องศาและจัดวางที่ขวา
                
                # ให้ผู้ใช้ป้อนค่าลิมิตเอง
                y_limit = st.number_input('Y-axis limit', min_value=0, value=5000)
                plt.ylim(0, y_limit)
                
                # Annotate max value on the bars
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', xytext=(0, 10), textcoords='offset points')
                
                st.pyplot(plt)
            else:
                st.write("No data available for the selected filters.")

        # ลบไฟล์ที่อัปโหลดแบบชั่วคราว
        os.remove(temp_file_path)

    else:
        st.write("No data available. Please upload log files in this page.")



if __name__ == '__main__':
    main()

st.markdown("""

    <div class="content">
    <p>       </p>
        <p>
            &copy; 2024 By Patharanan P. | For Seagate Korat.
        </p>
    </div>
""", unsafe_allow_html=True)


