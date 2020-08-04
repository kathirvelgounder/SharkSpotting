import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time
import cv2
from PIL import Image
from datetime import time as clock


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
    'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


def main():

    st.sidebar.title("What to do")
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["Show home", "See Summary", "Track Sharks"])
    if app_mode == "Show home":
        display_intro()
    elif app_mode == "See Summary":
        show_summary()
    elif app_mode == "Track Sharks":
        run_the_app()


def get_file_content_as_string(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    return lines


def display_intro():
    home = get_file_content_as_string("intro.txt")
    for line in home:
        next_line = st.markdown(line)

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data 

def show_summary():
    st.title('Summary')
    st.subheader('Totals')
    "Sharks:      2" 
    "People:     16"
    "Dolphins:    3"
    "Boats:       1"
    "Seals:       0"

    show_map()

    st.subheader('Raw data')
    data = pd.DataFrame({
        'objects' : ['shark', 'shark1', 'shark2', 'shark2'],
        'lat' : [33.75600311, 33.75417011, 33.76153611, 33.75666011],
        'lon' : [-118.19445711, -118.18651411, -118.17570711, -118.17360711],
        'time' : ['0:12:23', '0:32:10', '1:04:46', '1:13:07']
    })
    st.dataframe(data)


def show_map():
    data = pd.DataFrame({
        'objects' : ['shark', 'shark1', 'shark2', 'shark2'],
        'lat' : [33.75600311, 33.75417011, 33.76153611, 33.75666011],
        'lon' : [-118.19445711, -118.18651411, -118.17570711, -118.17360711]
    })
    st.map(data)


def draw_img():
    #image = Image.open('shark.png')
    image1 = cv2.imread('shark.png')
    overlay = image1.copy()
    output = image1.copy()
    cv2.rectangle(overlay, (1400, 400), (1525, 725), (0, 0, 255), 5)
    cv2.addWeighted(overlay, 0.5, output, 1 - 0.5, 0, output)
    st.image(output, use_column_width=True, format='JPEG')


def run_the_app():
    # sample data for rendering
    # TO DO:
    #   - draw_image
    #   - fix time slider
    st.title('Shark Spottings')
    show_map()    

    st.title('Video')
    draw_img()

    vid_h = 2
    vid_m = 12
    vid_s = 41
    t = st.slider("", max_value=clock(vid_h, vid_m, vid_s), value=clock(vid_h, vid_m, vid_s))


if __name__ == "__main__":
    main()
