import time
import matplotlib.pyplot as plt
from collections import Counter

def get_predictions():
    # Simulate delay
    time.sleep(4)

    # Predictions
    depression_predictions = ['low', 'low']
    emotion_predictions = [
        'angry', 'disgust', 'angry', 'angry', 'happy', 'happy', 'angry', 'fearful', 'angry', 'happy',
        'disgust', 'fearful', 'happy', 'disgust', 'surprised', 'disgust', 'disgust', 'angry', 'angry', 
        'happy', 'happy', 'disgust', 'happy', 'disgust', 'disgust', 'angry', 'angry', 'angry', 'fearful',
        'angry', 'happy', 'fearful', 'fearful', 'disgust', 'angry', 'disgust', 'fearful', 'disgust', 
        'angry', 'angry', 'disgust', 'fearful', 'disgust', 'disgust', 'disgust', 'angry', 'disgust', 
        'happy', 'angry', 'disgust', 'angry', 'fearful'
    ]

    return depression_predictions, emotion_predictions

# Example usage
if __name__ == "__main__":
    depression, emotions = get_predictions()
    
    # Count frequency of each emotion
    emotion_counts = Counter(emotions)

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(emotion_counts.keys(), emotion_counts.values(), color='skyblue')
    plt.title("Emotion Predictions Frequency")
    plt.xlabel("Emotion")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Optional: Print predictions
    print("Depression Predictions:", depression)
    print("Emotion Predictions:", emotions)
