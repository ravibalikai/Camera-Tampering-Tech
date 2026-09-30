# 📷 Camera Feed Quality Detection System

### Real-Time Camera Tampering Detection Using CNN

An end-to-end computer vision and deep learning project that automatically detects camera feed quality issues and tampering conditions in real time.

The system classifies camera frames into six categories and provides alerts when a tampering condition is detected.

## 🎯 Project Objective

The objective of this project is to automatically monitor surveillance camera feeds and identify conditions that can affect camera reliability, including blur, blank frames, occlusion, low light, and haze.

## 🔍 Detection Categories

The CNN model classifies camera frames into six conditions:

- Normal
- Blur
- Blank
- Occlusion
- Low Light
- Haze

## 📊 Dataset

- **26,836 custom-recorded images**
- **6 classification categories**
- Images collected for different camera quality and tampering conditions.

## 🧠 Model

A Convolutional Neural Network (CNN) was developed using TensorFlow and Keras for image classification.

### Model Performance

- **Validation Accuracy: 98.62%**

The system also uses a **10-second confirmation period** before generating a tampering alert to reduce false alarms caused by temporary camera disturbances.

## ⚙️ Key Features

- Real-time camera feed monitoring
- Six-class camera condition classification
- 10-second tampering confirmation
- Timestamped alerts
- Image upload support
- Video upload support
- Interactive Streamlit interface

## 🛠️ Technologies Used

- Python
- TensorFlow
- Keras
- OpenCV
- NumPy
- Pandas
- Matplotlib
- Streamlit
## 📂 Project Structure

```text
Camera-Tampering-Tech/
│
├── app.py
├── major.ipynb
├── requirements.txt
└── README.md
├── major.ipynb
├── requirements.txt
└── README.md
