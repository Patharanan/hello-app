import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dask.dataframe as dd  # type: ignore
import tempfile

st.set_page_config(page_title='Easy Analysis Time Element', page_icon='img.png')

# ฟังก์ชั่นกรองข้อมูลและจัดกลุ่ม
def filter_and_group_data(df, active_process_name, state_target_pairs, time_threshold):
    filtered_df = df[(df['ActiveProcessName'] == active_process_name) & (df[' Diff or period of time'] <= time_threshold)]
    group_df = filtered_df[filtered_df[[' StateName', ' TargetStateName']].apply(tuple, axis=1).isin(state_target_pairs)]
    return group_df

# ฟังก์ชันประมวลผลไฟล์ CSV ขนาดใหญ่ด้วย Dask DataFrame
def process_large_logfile(file_path):
    # อ่าน CSV โดยใช้ Dask DataFrame
    ddf = dd.read_csv(file_path)
    return ddf

def main():
    st.title("Analysis 📊")

    if 'history' not in st.session_state:
        st.session_state.history = []

    uploaded_file = st.file_uploader('Upload a large log file', type='csv')
    time_threshold = st.number_input('Enter maximum Diff or period of time threshold', min_value=1, value=3000)

    # ฟังก์ชันคำนวณค่าเฉลี่ย
    def calculate_avg(df, pairs):
        avg_dict = {}
        for pair in pairs:
            pair_df = df[(df[' StateName'] == pair[0]) & (df[' TargetStateName'] == pair[1])]
            avg_time = pair_df[' Diff or period of time'].mean()
            avg_dict[pair] = round(avg_time, 2)
        return avg_dict

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

            # กำหนดคู่ StateName และ TargetStateName สำหรับกลุ่มต่าง ๆ
            place_hga_pairs = [
                (' WaitForNestReady', ' MoveToAboveNest'),
                (' MoveToAboveNest', ' PlaceHGAToNest'),
                (' PlaceHGAToNest', ' MoveToPostPlace'),
                (' MoveToPostPlace', ' MoveToAboveTray')
            ]
            pick_hga_pairs = [
                (' MoveToAboveTray', ' WaitForHGADemand'),
                (' WaitForHGADemand', ' PrepareEE1ForPick'),
                (' PrepareEE1ForPick', ' PickHGAFromTray'),
                (' PickHGAFromTray', ' MoveToStandbyZ'),
                (' MoveToStandbyZ', ' WaitForNestReady')
            ]
            Nest_EE1_pairs = [
                (" WaitNestRotateComplete"," RotateNestAfterSwap"),
                (" RotateNestAfterSwap"," WaitEE1PlaceComplete"),
                (" WaitEE1PlaceComplete"," PrepareHGA"),
                (" PrepareHGA"," WaitNestRotateComplete")
            ]
            Nest_Rotate_pairs = [
                (" WaitNestEE2Complete"," WaitNestEE1Complete"),
                (" WaitNestEE1Complete"," WaitAcceptControlZone6"),
                (" WaitAcceptControlZone6"," SwapAndRotateNest"),
                (" SwapAndRotateNest"," WaitNestEE2Complete")
            ]
            EE2_pairs = [
                (" MoveToAboveNest"                  , " WaitForNestReady"),
                (" WaitForNestReady"                 , " MoveToPrePickPosition"),
                (" MoveToPrePickPosition"            , " VerifyHGABeforePick"),
                (" VerifyHGABeforePick"              , " PickHGAFromNest"),
                (" PickHGAFromNest"                  , " MoveToAfterPickPosition"),
                (" MoveToAfterPickPosition"          , " MoveToPrePlaceStandby"),
                (" MoveToPrePlaceStandby"            , " MoveToAboveCarrier"),
                (" MoveToAboveCarrier"               , " MoveToPlacePosition"),
                (' MoveToPlacePosition'              , " PlaceHGAToCarrier"),
                (" PlaceHGAToCarrier"                , " MoveToStandbyAfterPlace"),
                (" MoveToStandbyAfterPlace"          , " MoveToAboveNest")
            ]

            # กรองและจัดกลุ่มข้อมูล
            place_hga_df = filter_and_group_data(df, 'Seagate.AAS.HSA.LCA.HLD2.RobotEE1', place_hga_pairs, time_threshold)
            pick_hga_df = filter_and_group_data(df, 'Seagate.AAS.HSA.LCA.HLD2.RobotEE1', pick_hga_pairs, time_threshold)
            Nest_EE1_df = filter_and_group_data(df,'Seagate.AAS.HSA.LCA.HLD2.NestEE1' , Nest_EE1_pairs ,time_threshold)
            Nest_Rotate_df = filter_and_group_data(df,'Seagate.AAS.HSA.LCA.HLD2.NestRotate' , Nest_Rotate_pairs, time_threshold)
            EE2_df = filter_and_group_data(df,'Seagate.AAS.HSA.LCA.HLD2.RobotEE2' , EE2_pairs, time_threshold)

            # คำนวณค่าเฉลี่ยสำหรับแต่ละคู่
            place_hga_avg = calculate_avg(place_hga_df, place_hga_pairs)
            pick_hga_avg = calculate_avg(pick_hga_df, pick_hga_pairs)
            Nest_EE1_avg = calculate_avg(Nest_EE1_df, Nest_EE1_pairs)
            Nest_Rotate_avg = calculate_avg(Nest_Rotate_df, Nest_Rotate_pairs)
            EE2_avg = calculate_avg(EE2_df, EE2_pairs)

            # พล็อตกราฟ
            st.subheader('Place HGA Time Distribution')
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=place_hga_df, y=' Diff or period of time')
            plt.title('Place HGA Time Distribution')
            st.pyplot(plt)

            st.subheader('Pick HGA Time Distribution')
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=pick_hga_df, y=' Diff or period of time')
            plt.title('Pick HGA Time Distribution')
            st.pyplot(plt)
            
            st.subheader('Nest EE1 Time Distribution')
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=Nest_EE1_df, y=' Diff or period of time')
            plt.title('Nest EE1 Time Distribution')
            st.pyplot(plt)
            
            st.subheader('Nest Rotate Time Distribution')
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=Nest_Rotate_df, y=' Diff or period of time')
            plt.title('Nest Rotate Time Distribution')
            st.pyplot(plt)
            
            st.subheader('EE2 Time Distribution')
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=EE2_df, y=' Diff or period of time')
            plt.title('EE2 Time Distribution')
            st.pyplot(plt)

            # แสดงตารางข้อมูล
            st.subheader('Place HGA Data')
            st.dataframe(place_hga_df)
            st.write("Average time for each pair in Place HGA:")
            for pair, avg in place_hga_avg.items():
                st.write(f"{pair}: {avg}")
            st.subheader('Total Average Time for Each Group')
            st.write("Total average time for Place HGA:", round(sum(place_hga_avg.values()), 2))

            st.subheader('Pick HGA Data')
            st.dataframe(pick_hga_df)
            st.write("Average time for each pair in Pick HGA:")
            for pair, avg in pick_hga_avg.items():
                st.write(f"{pair}: {avg}")
            st.subheader('Total Average Time for Each Group')
            st.write("Total average time for Pick HGA:", round(sum(pick_hga_avg.values()), 2))
            
            st.subheader('Nest EE1 Data')
            st.dataframe(Nest_EE1_df)
            st.write("Average time for each pair in Nest EE1:")
            for pair, avg in Nest_EE1_avg.items():
                st.write(f"{pair}: {avg}")
            st.subheader('Total Average Time for Each Group')
            st.write("Total average time for Nest EE1:", round(sum(Nest_EE1_avg.values()), 2))
            
            st.subheader('Nest Rotate Data')
            st.dataframe(Nest_Rotate_df)
            st.write("Average time for each pair in Nest Rotate:")
            for pair, avg in Nest_Rotate_avg.items():
                st.write(f"{pair}: {avg}")
            st.subheader('Total Average Time for Each Group')
            st.write("Total average time for Nest Rotate:", round(sum(Nest_Rotate_avg.values()), 2))
            
            st.subheader('EE2 Data')
            st.dataframe(EE2_df)
            st.write("Average time for each pair in EE2:")
            for pair, avg in EE2_avg.items():
                st.write(f"{pair}: {avg}")
            st.subheader('Total Average Time for Each Group')
            st.write("Total average time for EE2:", round(sum(EE2_avg.values()), 2))

            # เพิ่มข้อมูลที่ประมวลผลลงใน history
            history_entry = {
                'file_name': uploaded_file.name,
                'place_hga_avg': place_hga_avg,
                'pick_hga_avg': pick_hga_avg,
                'Nest_EE1_avg': Nest_EE1_avg,
                'Nest_Rotate_avg': Nest_Rotate_avg,
                'EE2_avg': EE2_avg
            }
            st.session_state.history.append(history_entry)

            # จำกัดจำนวน history ไว้ที่ 5
            if len(st.session_state.history) > 5:
                st.session_state.history.pop(0)

    # แสดง history
    if st.session_state.history:
        st.sidebar.title("History")
        for i, entry in enumerate(st.session_state.history):
            with st.sidebar.expander(f"History {i+1}: {entry['file_name']}"):
                st.write("Average time for Place HGA:")
                for pair, avg in entry['place_hga_avg'].items():
                    st.write(f"{pair}: {avg}")
                st.write("Total average time for Place HGA:", round(sum(entry['place_hga_avg'].values()), 2))

                st.write("Average time for Pick HGA:")
                for pair, avg in entry['pick_hga_avg'].items():
                    st.write(f"{pair}: {avg}")
                st.write("Total average time for Pick HGA:", round(sum(entry['pick_hga_avg'].values()), 2))

                st.write("Average time for Nest EE1:")
                for pair, avg in entry['Nest_EE1_avg'].items():
                    st.write(f"{pair}: {avg}")
                st.write("Total average time for Nest EE1:", round(sum(entry['Nest_EE1_avg'].values()), 2))

                st.write("Average time for Nest Rotate:")
                for pair, avg in entry['Nest_Rotate_avg'].items():
                    st.write(f"{pair}: {avg}")
                st.write("Total average time for Nest Rotate:", round(sum(entry['Nest_Rotate_avg'].values()), 2))

                st.write("Average time for EE2:")
                for pair, avg in entry['EE2_avg'].items():
                    st.write(f"{pair}: {avg}")
                st.write("Total average time for EE2:", round(sum(entry['EE2_avg'].values()), 2))

if __name__ == '__main__':
    main()
