import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import random
import os
from io import BytesIO

st.set_page_config(page_title='Easy Analysis Time Element', page_icon='img.png')


# convert file log to csv write 7 column 
def convert_log_to_csv(input_file):
    output_file = input_file.replace('.log', '.csv')
    with open(input_file, 'r') as log_file:
        log_lines = log_file.readlines()

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Date', 'Time', 'TimeTicks(ms)', 'LogLevel', 'Start/Stop', 'Message', 'Timediff(ms)'])
        for line in log_lines[1:]:
            parts = line.strip().split('\t')
            if len(parts) == 7:
                writer.writerow(parts)

    return output_file


# analyze file from upload  custom message custom log level fix y limit
def analyze_and_plot(dataframes, log_level, selected_messages, y_limit, target_values):
    filtered_dfs = []
    combined_df = pd.DataFrame()

    for idx, df in enumerate(dataframes):
        if log_level == 'All':
            filtered_df = df[df['Message'].isin(selected_messages) & (df['Timediff(ms)'] <= y_limit)]
        else:
            filtered_df = df[(df['LogLevel'] == log_level) & df['Message'].isin(selected_messages) & (df['Timediff(ms)'] <= y_limit)]
        filtered_dfs.append(filtered_df)
        combined_df = pd.concat([combined_df, filtered_df], ignore_index=True)

    st.subheader('Analysis Plots')

    num_files = len(dataframes)
    file_colors = {idx: (random.random(), random.random(), random.random()) for idx in range(num_files)}

    for idx, df in enumerate(filtered_dfs):
        file_name = f"File {idx + 1}"  # เลือกใช้ชื่อของไฟล์ที่อัปโหลด

        st.subheader(f'{file_name}')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))  # ปรับขนาดของ subplot เป็น (15, 10)

        # Bar Plot
        sns.barplot(x='Timediff(ms)', y='Message', data=df, ax=ax1, color=file_colors[idx])
        for msg in df['Message'].unique():
            max_val_bar = df[df['Message'] == msg]['Timediff(ms)'].max()
            x_pos = df[df['Message'] == msg]['Timediff(ms)'].median()
            ax1.annotate(f'{msg} Max: {max_val_bar}', xy=(x_pos, msg), xytext=(5, 5),
                         textcoords='offset points', fontsize=10, ha='left', va='center', color='black', 
                         bbox=dict(facecolor='white', alpha=0.8))
        for msg, target in target_values.items():
            if msg in df['Message'].unique():
                ax1.scatter(target, msg, color='red', marker='o', s=100, label='Target Value')
        ax1.set_title('Bar Plot')
        ax1.set_xlabel('Time Difference (ms)')
        ax1.set_ylabel('Message')
        ax1.legend()

        # Violin Plot
        sns.violinplot(x='Timediff(ms)', y='Message', data=df, ax=ax2, color=file_colors[idx])
        for msg in df['Message'].unique():
            max_val_violin = df[df['Message'] == msg]['Timediff(ms)'].max()
            x_pos = df[df['Message'] == msg]['Timediff(ms)'].median()
            ax2.annotate(f'{msg} Max: {max_val_violin}', xy=(x_pos, msg), xytext=(5, 5),
                         textcoords='offset points', fontsize=10, ha='left', va='center', color='black',
                         bbox=dict(facecolor='white', alpha=0.8))
        for msg, target in target_values.items():
            if msg in df['Message'].unique():
                ax2.scatter(target, msg, color='red', marker='o', s=100, label='Target Value')
        ax2.set_title('Violin Plot')
        ax2.set_xlabel('Time Difference (ms)')
        ax2.set_ylabel('Message')
        ax2.legend()

        plt.subplots_adjust(wspace=0.5)  # ปรับระยะห่างระหว่าง subplot

        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Combined Plot
    st.subheader('Combined Analysis Plot')
    combined_fig, (ax1_comb, ax2_comb) = plt.subplots(1, 2, figsize=(15, 10))  # ปรับขนาดของ subplot เป็น (15, 10)

    # Bar Plot for combined data
    sns.barplot(x='Timediff(ms)', y='Message', data=combined_df, ax=ax1_comb)
    for msg in combined_df['Message'].unique():
        max_val_bar_comb = combined_df[combined_df['Message'] == msg]['Timediff(ms)'].max()
        x_pos_comb = combined_df[combined_df['Message'] == msg]['Timediff(ms)'].median()
        ax1_comb.annotate(f'{msg} Max: {max_val_bar_comb}', xy=(x_pos_comb, msg), xytext=(5, 5),
                     textcoords='offset points', fontsize=10, ha='left', va='center', color='black', 
                     bbox=dict(facecolor='white', alpha=0.8))
    for msg, target in target_values.items():
        if msg in combined_df['Message'].unique():
            ax1_comb.scatter(target, msg, color='red', marker='o', s=100, label='Target Value')
    ax1_comb.set_title('Combined Bar Plot')
    ax1_comb.set_xlabel('Time Difference (ms)')
    ax1_comb.set_ylabel('Message')
    ax1_comb.legend()

    # Violin Plot for combined data
    sns.violinplot(x='Timediff(ms)', y='Message', data=combined_df, ax=ax2_comb)
    for msg in combined_df['Message'].unique():
        max_val_violin_comb = combined_df[combined_df['Message'] == msg]['Timediff(ms)'].max()
        x_pos_comb = combined_df[combined_df['Message'] == msg]['Timediff(ms)'].median()
        ax2_comb.annotate(f'{msg} Max: {max_val_violin_comb}', xy=(x_pos_comb, msg), xytext=(5, 5),
                     textcoords='offset points', fontsize=10, ha='left', va='center', color='black',
                     bbox=dict(facecolor='white', alpha=0.8))
    for msg, target in target_values.items():
        if msg in combined_df['Message'].unique():
            ax2_comb.scatter(target, msg, color='red', marker='o', s=100, label='Target Value')
    ax2_comb.set_title('Combined Violin Plot')
    ax2_comb.set_xlabel('Time Difference (ms)')
    ax2_comb.set_ylabel('Message')
    ax2_comb.legend()

    plt.subplots_adjust(wspace=2)  # ปรับระยะห่างระหว่าง subplot

    plt.xticks(rotation=45)
    st.pyplot(combined_fig)

    return combined_fig

def fig_to_bytes(fig):
    img_bytes = BytesIO()
    fig.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    return img_bytes

def main():
    st.title("Analysis 📊")
    uploaded_files = st.file_uploader('Upload multiple log files', type='log', accept_multiple_files=True)

    dataframes = []
    log_levels = []
    selected_messages = []
    y_limit = 10000
    target_values = {}

    if uploaded_files:
        for idx, uploaded_file in enumerate(uploaded_files):
            file_key = f"file_uploader_{idx}_{uploaded_file.name}"
            st.text(uploaded_file.name)

            with open(uploaded_file.name, 'wb') as f:
                f.write(uploaded_file.getvalue())

            csv_file = convert_log_to_csv(uploaded_file.name)
            df = pd.read_csv(csv_file)
            dataframes.append(df)
            os.remove(uploaded_file.name)

        # Store the dataframes in session state
        st.session_state['dataframes'] = dataframes

        log_levels = pd.concat([df['LogLevel'] for df in dataframes]).unique().tolist()
        log_levels.insert(0, 'All')

        log_level = st.sidebar.selectbox('Log Level', log_levels)

        if log_level == 'All':
            messages = pd.concat([df['Message'] for df in dataframes]).unique().tolist()
        else:
            messages = pd.concat([df[df['LogLevel'] == log_level]['Message'] for df in dataframes]).unique().tolist()

        st.sidebar.subheader('Filters')
        selected_messages = st.sidebar.multiselect('Message filter', messages, default=messages)
        y_limit = st.sidebar.slider('Time Difference Limit (ms)', min_value=0, max_value=20000, value=10000)

        for msg in selected_messages:
            target_values[msg] = st.sidebar.number_input(f'Target value for {msg}', min_value=0.0, step=0.01)

        combined_fig = analyze_and_plot(dataframes, log_level, selected_messages, y_limit, target_values)

        if st.button('Export Graph'):
            img_bytes = fig_to_bytes(combined_fig)
            st.download_button(label='Download Graph', data=img_bytes, file_name='plot.png', mime='image/png')

    else:
        st.write("Upload log files to display data.")

if __name__ == '__main__':
    main()
