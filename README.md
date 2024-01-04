# network-traffic-anomaly-detection
This project implements a network traffic anomaly detection mechanism designed to identify anomalous packets amongst the stream of packets in a controlled environment. GMM (Gaussian Mixture Models) and Isolation Forest algorithms were used to detect anomalies.

## Description
The repository includes Exploratory Data Analysis (EDA), pre-processing pipelines, GMM (Gaussian Mixture Models), Isolation Forest, and evaluation metrics to assess performance. 
One of the machines is a Normal Windows PC which has provided benign packets representing normal user activity on a network, the second is the OWASP Broken Web Application which hosts a wide variety of intentionally insecure web applications, and Kali Machine which is used as the primary source of attack traffic in the lab setup, leveraging Kali's extensive set of penetration testing and attack tools.


## Dataset
The dataset used in this project is available on [Kaggle](https://www.kaggle.com/datasets/moradrawashdeh/attack-simulation-lab). Each row in the CSV dataset corresponds to a single network packet, with each column representing one of the fields extracted from that packet. These fields capture a comprehensive view of each packet's metadata and content, providing an extensive base for network traffic analysis.
