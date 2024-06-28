from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import streamlit as st
import pandas as pd
import csv

st.set_page_config(page_title='Easy Predictive Analysis', page_icon='img.png')

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

def predict_stop_messages(dataframes, selected_file):
    stop_messages_freq = {}
    
    for idx, df in enumerate(dataframes):
        if f'File {idx + 1}' == selected_file:
            stop_messages = df[df['Start/Stop'] == 'stop']['Message'].value_counts()
            stop_messages_freq[selected_file] = stop_messages
    
    return stop_messages_freq

def summarize_stop_messages(stop_messages_freq):
    st.subheader('Summary of Stop Messages')
    
    for file_name, messages_freq in stop_messages_freq.items():
        st.write(f"File: {file_name}")
        df_summary = pd.DataFrame({'Message': messages_freq.index, 'Frequency': messages_freq.values})
        st.table(df_summary)

def train_logistic_regression(dataframes):
    # Concatenate all dataframes into one
    all_data = pd.concat(dataframes, ignore_index=True)

    # Prepare the data
    X = all_data[['TimeTicks(ms)']]  # Independent variable
    y = all_data['Timediff(ms)'] < 999999999  
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Initialize Logistic Regression model
    model = LogisticRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Predict stop status for all data
    all_data['Predicted_Stop_Status'] = model.predict(X)

    return all_data

def main():
    st.title("Predict 📈")
    uploaded_files = st.session_state.get('dataframes', [])

    if not uploaded_files:
        st.write("No data available. Please upload log files on the Analysis page first.")
        return

    log_levels = pd.concat([df['LogLevel'] for df in uploaded_files]).unique().tolist()
    log_levels.insert(0, 'All')

    selected_file = st.selectbox('Select File to Predict', [f'File {idx + 1}' for idx in range(len(uploaded_files))])

    stop_messages_freq = predict_stop_messages(uploaded_files, selected_file)

    summarize_stop_messages(stop_messages_freq)

    st.subheader('Logistic Regression Prediction of Stop Status')
    st.write("Using TimeTicks(ms) as Independent Variable and Timediff(ms) < 999999999 as Dependent Variable")

    # Train and predict using Logistic Regression
    all_data = train_logistic_regression(uploaded_files)

    # Display the result
    st.write(all_data[['TimeTicks(ms)', 'Timediff(ms)', 'Predicted_Stop_Status']])

if __name__ == '__main__':
    main()
