IoT Device Fingerprinting and Anomaly Detection

Overview

Connected IoT devices, such as smart doorbells and security cameras, are frequently targeted by malware like the Mirai and Gafgyt botnets. This project is a machine learning pipeline designed to fingerprint the normal network behavior of an IoT device and rapidly detect anomalous traffic patterns indicative of a volumetric network attack (e.g., a UDP Flood).

This repository implements a highly optimized XGBoost Classifier that processes network statistical features and identifies malicious traffic with near-perfect precision and recall.

Architecture

The pipeline consists of two primary modules:

preprocess.py (Data Pipeline & Stratification):

Ingests pre-computed network feature datasets (115 statistical features per packet).

Dynamically labels traffic (0 for Benign, 1 for Attack).

Performs a stratified 80/20 train-test split to ensure class balance.

Standardizes the feature space using Scikit-Learn's StandardScaler for optimal gradient boosting convergence.

train.py (Model Training & Evaluation):

Initializes an XGBClassifier tuned for network anomaly detection.

Evaluates the model against the test set, outputting a Confusion Matrix and detailed classification report (Precision, Recall, F1-Score).

Serializes and exports the trained model (.pkl) and scaler parameters for future deployment.

Dataset

This project uses the N-BaIoT Dataset (sourced from the UCI Machine Learning Repository / Kaggle). The data represents real network traffic captured from a Danmini Smart Doorbell.

To run this pipeline locally, you need two specific files from the dataset:

1.benign.csv (Normal device operation)

1.mirai.udp.csv (Active Mirai botnet UDP flood attack)

Note - the numbering before the data set means the following
Device 1: Danmini Smart Doorbell

Device 2: Ennio Smart Doorbell

Device 3: Ecobee Smart Thermostat

Device 4: Philips Baby Monitor

Devices 5, 6, 7: Provision Security Cameras

Devices 8, 9: SimpleHome / Samsung Webcams


Installation & Setup

Clone the repository


Set up the virtual environment

Install dependencies:
pip install pandas numpy scikit-learn xgboost joblib

Prepare the Data:
Create a data/ directory in the root of the project and place the two required CSV files inside it

Usage

To execute the data preprocessing and model training pipeline, run:

python train.py


Results & Insights

The model achieves a 1.00 F1-Score (100% accuracy) on the test set.

While perfect accuracy often indicates overfitting in standard machine learning tasks, it is the expected behavior here. Volumetric DDoS attacks (like Mirai UDP floods) are brute-force events. The sudden shift from a device sending 5 packets a minute to blasting thousands of identical packets per second creates a stark, easily separable mathematical boundary for the XGBoost algorithm.

Future Enhancements

Implementation of an edge-deployable live packet extractor.

Conversion of the XGBoost model to an ultra-lightweight format (like ONNX or TF Lite) for execution directly on constrained IoT hardware.