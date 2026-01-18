# SpaceCode-26
Classifying Asteroids as Harmful or not using ML

# 🛡️ The Sentinel Shield: Near-Earth Comet (NEC) Classification

## 🌌 Background: The Planetary Defense Mission

Our solar system is a cosmic shooting gallery. Among the millions of objects orbiting the Sun, **Near-Earth Objects (NEOs)**—specifically comets and asteroids—pose a unique challenge to Earth’s safety. While most bypass our planet at safe distances, a select few are designated as **Potentially Hazardous Objects (PHOs)**.

Identifying these threats early using orbital mechanics is the first line of defense for our planet.

### What makes an object "Hazardous"?

According to NASA/JPL CNEOS standards, a "Hazardous" classification is typically triggered by two critical physical thresholds:

* **Proximity:** A Minimum Orbit Intersection Distance (**MOID**) of **0.05 AU** or less.
* **Size/Magnitude:** An Absolute Magnitude of **22.0** or brighter (suggesting the object is large enough, approx. 140 meters, to cause significant regional damage).

---

## 🎯 Objective

The goal of this project is to develop a **supervised machine learning model** to automate the **Hazardous Classification** of Near-Earth Comets and Asteroids.

This system predicts whether a celestial body is a "Potentially Hazardous" threat based on its orbital elements and physical properties, focusing on maximizing **Recall** to ensure no threats are missed.

---

## 📂 Dataset Description

We utilize a high-dimensional dataset containing orbital parameters of objects observed from **1950 to 2025**.

### Key Features

| Feature Category | Description |
| --- | --- |
| **Physical Properties** | Absolute Magnitude, Estimated Diameter |
| **Orbital Shape & Tilt** | Eccentricity, Inclination, Semi-Major Axis, Perihelion/Aphelion distances |
| **Proximity Metrics** | Minimum Orbit Intersection Distance (MOID), Miss Distance |
| **Dynamics** | Relative Velocity, Orbital Period, Jupiter Tisserand Invariant |
| **Reliability** | Orbit Uncertainty, Orbit Determination Date |

---

## 🛠️ Project Workflow & Tasks

### 1. Data Exploration (EDA)

* Investigate the correlation between **Absolute Magnitude** and the "Hazardous" label.
* Analyze orbital families (e.g., highly eccentric orbits) to detect patterns in hazardous objects.

### 2. Preprocessing

* **High-Cardinality Management:** Handling unique identifiers (Names/IDs).
* **Class Imbalance Strategy:** Hazardous objects are statistically rare. We employ techniques (e.g., SMOTE, Class Weights, Undersampling) to balance the dataset.

### 3. Model Training

* Implementation of various classification algorithms (e.g., Random Forest, XGBoost, Logistic Regression).

### 4. Evaluation

* **Primary Metric:** **Recall** (Sensitivity). Minimizing False Negatives is the priority because missing a hazardous object is catastrophic compared to a false alarm.
* **Secondary Metric:** AUC-ROC score to measure separability.

---


## 📊 Deliverables

This repository contains:

1. **`Sentinel_Shield_Pipeline.ipynb`**: A well-commented, end-to-end pipeline covering data cleaning, EDA, preprocessing, model training, and evaluation.
2. **`Technical_Report.pdf`**: A summary strategy document focusing on handling class imbalance and interpreting model results.

---

## 📈 Results Summary

* **Best Model:** 0 False Negatives
* **Recall Score:** 1.00
* **AUC-ROC:** 0.999817

> **Note:** The high recall ensures that the model acts as an effective "net," catching nearly all potential threats for further human verification.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request for any feature enhancements or bug fixes.

---
## Dataset Link: https://drive.google.com/file/d/1BN6ro6Qtfd4j7tUtlrgVzZ_Ts3axj6v0/view
