# 📷 Camera Feed Quality Detection System

A CNN-based surveillance monitoring system that automatically 
detects camera tampering in real time.

## Features
- Detects 6 conditions: Normal, Blur, Blank, Occlusion, Low Light, Haze
- 98.62% validation accuracy
- 10 second tampering confirmation before alert
- Real time alert system with timestamps
- Supports image and video upload

## Tech Stack
Python | TensorFlow | Keras | OpenCV | Streamlit

## Dataset
26,836 custom recorded images across 6 categories

## How to Run
pip install -r requirements.txt
streamlit run app.py

## Author
Ravishankar Balikai | ECE | KLS Gogte Institute of Technology
