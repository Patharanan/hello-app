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
st.set_page_config(page_title='Simple Time Element Analysis', page_icon='img.png')
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
            font-size: 3em;
        }
        .blue-text {
            color: #2e6e99;
            font-size: 2em;
        }
        .indent { padding-left: 1em; }
        .content { font-size: 1.25em; }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2e6e99;
            color: white;
            text-align: center;
            padding: 10px 0;
        }
    </style>
    <h1 class="rainbow-text">Simple Time Element Analysis</h1>
""", unsafe_allow_html=True)

# Section: Introduction to Easy Analysis Time Element
st.markdown("""
    <h2 class="blue-text">What is Simple Time Element Analysis?</h2>
    <div class="content">
        <p>
            Cycle time of machines in the production process is the main factor that makes OEE effective. Therefore, control
            Cycle Time to achieve the goal must therefore rely on machine data analysis. Data analysis is therefore important in
            Understanding concrete machine errors and solving them directly
        </p>
    </div>
""", unsafe_allow_html=True)

# Section: How to Use Easy Analysis Time Element
st.markdown("""
    <h2 class="blue-text">How to use Simple Time Element Analysis?</h2>
    <div class="content">
        <h3>HL All Page</h3>
        <p class="indent">
            This page allows users to upload CSV files up to 200MB in size. If the file is too large,
            It is recommended to remove columns that are not required in the analysis, such as `FunctionName`, `GetTikCount`,
            and `Xtralnfo` to enable a successful upload. On this page an overview of the processes is provided.
            There are 17 modules in total, allowing users to check which processes are in each module.
            There is an abnormality. Users can also adjust the value of the Y axis to keep the graph at the appropriate scale.
        </p>
        <h3>HL Group Page</h3>
        <p class="indent">
            This page allows you to group modules and processes of interest to see the Cycle Time of each group. Which includes:
            <ul>
                <li>Seagate.AAS.HSA.LCA.HLD2.RobotEE1:
                Place HGA group: sub-processes include `WaitForNestReady`, `MoveToAboveNest`, `PlaceHGAToNest`, `MoveToPostPlace`
                Pick HGA group: sub-processes include `MoveToAboveTray`, `WaitForHGADemand`, `PrepareEE1ForPick`, `PickHGAFromTray`, `MoveToStandbyZ`
                </li>
                <li>Seagate.AAS.HSA.LCA.HLD2.NestEE1: Subprocesses include: `WaitNestRotateComplete`, `RotateNestAfterSwap`, `WaitEE1PlaceComplete`, `PrepareHGA`</li>
                <li>Seagate.AAS.HSA.LCA.HLD2.NestRotate: Subprocesses include: `WaitNestEE2Complete`, `WaitNestEE1Complete`, `WaitAcceptControlZone6`, `SwapAndRotateNest`</li>
                <li>Seagate.AAS.HSA.LCA.HLD2.RobotEE2: Subprocesses include: `MoveToAboveNest`, `WaitForNestReady`, `MoveToPrePickPosition`, `VerifyHGABeforePick`, `PickHGAFromNest`, `MoveToAfterPickPosition`, `MoveToPrePlaceStandby`, `MoveToAboveCarrier`, `MoveToPlacePosition`, `PlaceHGAToCarrier `, `MoveToStandbyAfterPlace`</li>
            </ul>
        </p>
        <h3>HL Specific Page</h3>
        <p class="indent">
            Page for viewing details of various modules and sub-processes. during the specified time Users can select the time period they want to view to see the running time of that process.
        </p>
        <h3>Normal Page</h3>
        <p class="indent">
            This page is for Verifying Data of BSE, SWG, Reflow, VTAAP, and RSW machines. The work process is as follows:
            <ol>
                    <li>Upload log file</li>
                    <li>Select loglevel</li>
                    <li>In the Message field, all messages at that loglevel will be displayed.</li>
                    <li>Users can choose to import or export text as needed.</li>
                    <li>Enter the target value to compare with the maximum value of that process.</li>
                    <li>Use the slider menu to configure the `timediff(ms)` sets a value that does not exceed the calculation to eliminate errors. The resulting graph is displayed on the right side of the screen.</li>
            </ol>
        <h3>Data Page</h3>
        <p class="indent">
            It is a page linked to the Normal page. It displays information about 
            files uploaded on the Normal page in a table format so that it can be verified for accuracy.
        </p>
    </div>
""", unsafe_allow_html=True)


# Section: About
st.markdown("""

    <div class="content">
    <p>       </p>
        <p>
            &copy; 2024 By Patharanan P. | For Seagate Korat.
        </p>
    </div>
""", unsafe_allow_html=True)


# # Footer
# st.markdown("""
#     <div class="footer">
#         <p>&copy; 2024 Simple Time Element Analysis.</p>
#     </div>
# """, unsafe_allow_html=True)
