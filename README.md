
# Autism Detection - Video Analysis Module 

This repository is a core component of the **Autism Detection and Assistance System (ADAS)**. It implements emotion recognition and facial analysis from video streams to evaluate emotional responses and assist in early autism detection and personalized content recommendation.

## Key Features

-  Emotion detection using **Inception-ResNet V1** on facial expressions.
-  Frame-by-frame scoring of emotional states.
-  Real-time video feed processing with OpenCV.
-  Cognitive assessment via emotion-tracked video tasks.
-  Supports integration with learning recommendation engine.

## Models Used

- `Inception-ResNet V1` – Emotion recognition
- `AlexNet` – Autism facial feature analysis (external)
- `Random Forest` – Structured data classification (external ensemble)

## Technologies & Libraries

- Python, TensorFlow, Keras
- OpenCV, NumPy, Pandas
- Matplotlib, Seaborn

## Folder Structure

```
📂 autism-video
 ┣ 📁 models/
 ┣ 📁 utils/
 ┣ 📄 video_analysis.py
 ┣ 📄 emotion_scoring.py
 ┣ 📄 requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt
python video_analysis.py
```

## Output

- Detected emotions with timestamps
- Calculated emotional scores
- CSV logs for dashboard integration

---

## Part of the [ADAS System](https://github.com/FizzaSadath/autism-web)
