import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import random
import os
from io import BytesIO
import base64

# Set the icon and title for the web app
st.set_page_config(page_title='Easy Analysis Time Element', page_icon='img.png')
st.sidebar.image('logo.png', use_column_width=True)

# Sidebar with logo
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-image: url('logo.png');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 100px; /* Adjust height as needed */
        }
    </style>
""", unsafe_allow_html=True)


# Main title with icon and rainbow text
st.markdown("""
    <style>
        .rainbow-text {
            background-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
            -webkit-background-clip: text;
            color: transparent;
            font-size: 2em;
        }
        .blue-text {
            color: #2e6e99;
            font-size: 2em;
        }
        .indent { padding-left: 1em; }
    </style>
    <h1 class="rainbow-text">Easy Analysis Time Element</h1>
    """, unsafe_allow_html=True)

# Section: Introduction to Easy Analysis Time Element
st.markdown("""
    <h2 class="blue-text">What is Easy Analysis Time Element?</h2>
    <div style="font-size: 1.25em;">
        <p class="indent">The cycle time of machines in the production process is the main factor that makes OEE effective.</p>
        <p class="indent">Therefore, controlling the cycle time to meet the target requires analysis of machine data. Data analysis is therefore important in order to concretely understand machine errors that occur and solve that problem directly.</p>
    </div>
    """, unsafe_allow_html=True)

# Section: How to Use Easy Analysis Time Element
st.markdown("""
    <h2 class="blue-text">How to use Easy Analysis Time Element?</h2>
    <div style="font-size: 1.25em;">
        <p class="indent">Using the website is straightforward. On the analytics page, you must upload the files you want to analyze. Once the file is uploaded, you will find that a menu appears on the right side of the screen. The menu includes options for Loglevel, Process Filter, and Time Difference Limit (ms). When selecting a process, an input target value for the selected process will appear. The numerical values will then be plotted on the graph.</p>
    </div>
    """, unsafe_allow_html=True)


# st.markdown("""
#     <h2 class="blue-text">All Pages</h2>
#     <div style="font-size: 1.25em;">
#         <p class="indent">1. Headload All Page.  
#          Verify 17 Module with</p>
#         <p class="indent">2. Headload Specific Page.</p>
#         <p class="indent">3. Normal Page.</p>
#         <p class="indent">4. Prediction Page.</p>
#         <p class="indent">5. Show data Page.</p>

#     </div>
#     """, unsafe_allow_html=True)


# Section: Basic Features
# st.markdown("""
#     <h2 class="blue-text">Basic Features</h2>
#     <div style="font-size: 1.25em;">
#         <p class="indent">1. Upload log files on the Analysis page.</p>
#         <p class="indent">2. Filter logs by loglevel on the Analysis page.</p>
#         <p class="indent">3. Filter processes on the Analysis page.</p>
#         <p class="indent">4. Adjust the time difference limit (ms) on the Analysis page.</p>
#         <p class="indent">5. Set target values for plotting on the Analysis page.</p>
#         <p class="indent">6. Plot graphs based on user selection on the Analysis page.</p>
#         <p class="indent">7. Export graphs on the Analysis page.</p>
#         <p class="indent">8. Display data frames on the Data page.</p>
#     </div>
#     """, unsafe_allow_html=True)
