import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dask.dataframe as dd # type: ignore
import tempfile
import os

st.set_page_config(page_title='Simple Time Element Analysis', page_icon='img.png')

# Function to analyze DataFrame and return filtered results
def analyze_headload(df, active_process_name, state_name, target_state_name, controller_level, start_datetime, end_datetime):
    filtered_df = df[df['ActiveProcessName'] == active_process_name]
    
    if state_name:
        filtered_df = filtered_df[filtered_df['StateName'] == state_name]
    if target_state_name:
        filtered_df = filtered_df[filtered_df['TargetStateName'] == target_state_name]
    if controller_level:
        filtered_df = filtered_df[filtered_df['ControllerLevel'] == controller_level]
    if start_datetime and end_datetime:
        filtered_df = filtered_df[(filtered_df['DateTime.Now'] >= start_datetime) & (filtered_df['DateTime.Now'] <= end_datetime)]
    
    return filtered_df


# Function to process large CSV file with Dask
def process_large_logfile(file_path):
    # Read CSV using Dask DataFrame
    ddf = dd.read_csv(file_path, parse_dates=[' DateTime.Now'])
    return ddf

def main():
    st.title("Analysis 📊")

    uploaded_file = st.file_uploader('Upload a large CSV file', type='csv')

    if uploaded_file:
        st.text(uploaded_file.name)

        # Create a temporary file path
        temp_file_path = tempfile.NamedTemporaryFile(delete=False).name

        # Write the uploaded file to a temporary location
        with open(temp_file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())

        # Process large log file with Dask DataFrame
        ddf = process_large_logfile(temp_file_path)

        if ddf is not None:
            # Convert Dask DataFrame to Pandas DataFrame for selection and plotting
            df = ddf.compute()

            # Strip whitespace from column names
            df.columns = df.columns.str.strip()

            # Choose filtering criteria with Pandas DataFrame
            active_process_name = st.selectbox('Select ActiveProcessName', df['ActiveProcessName'].unique())
            
            if active_process_name:
                state_names = df[df['ActiveProcessName'] == active_process_name]['StateName'].unique()
                state_name = st.selectbox('Select StateName', state_names)
            else:
                state_name = None

            if state_name:
                target_state_names = df[(df['ActiveProcessName'] == active_process_name) & (df['StateName'] == state_name)]['TargetStateName'].unique()
                target_state_name = st.selectbox('Select TargetStateName', target_state_names)
            else:
                target_state_name = None

            if target_state_name:
                controller_levels = df[(df['ActiveProcessName'] == active_process_name) & (df['StateName'] == state_name) & (df['TargetStateName'] == target_state_name)]['ControllerLevel'].unique()
                controller_level = st.selectbox('Select ControllerLevel', controller_levels)
            else:
                controller_level = None

            # Add datetime range selection
            min_datetime = df['DateTime.Now'].min()
            max_datetime = df['DateTime.Now'].max()

            # Check if min_datetime is equal to max_datetime
            if min_datetime == max_datetime:
                # If they are equal, adjust max_datetime to be one day later (or earlier, depending on your data)
                max_datetime = min_datetime + pd.Timedelta(days=1)

            # Initialize start_datetime and end_datetime with default values
            start_date = st.date_input('Select start date', min_value=min_datetime.date(), max_value=max_datetime.date(), value=min_datetime.date())
            start_time = st.time_input('Select start time', value=min_datetime.time())
            end_date = st.date_input('Select end date', min_value=min_datetime.date(), max_value=max_datetime.date(), value=max_datetime.date())
            end_time = st.time_input('Select end time', value=max_datetime.time())

            # Combine date and time
            start_datetime = pd.Timestamp.combine(start_date, start_time)
            end_datetime = pd.Timestamp.combine(end_date, end_time)

            # Analyze and plot with Pandas DataFrame based on selected values
            if start_datetime and end_datetime:
                filtered_df = analyze_headload(df, active_process_name, state_name, target_state_name, controller_level, start_datetime, end_datetime)

                if not filtered_df.empty:
                    st.subheader('Filtered Data')
                    st.write(filtered_df)

                    # Plotting the data
                    plt.figure(figsize=(10, 6))
                    sns.lineplot(data=filtered_df, x='DateTime.Now', y='Diff or period of time')
                    plt.xlabel('Date and Time')
                    plt.ylabel('Diff or period of time')
                    plt.title('Diff or period of time for selected filters')
                    st.pyplot(plt)
                else:
                    st.write("No data available for the selected filters.")

        # Remove temporary uploaded file
        os.remove(temp_file_path)

    else:
        st.write("No data available. Please upload log files in the Analysis page.")

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

