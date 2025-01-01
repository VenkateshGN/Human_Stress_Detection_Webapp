import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# JSON-like data
data = {
    "depression": ["low", "high"],
    "emotion": [
        "angry", "disgust", "angry", "angry", "happy", "happy", "angry", "fearful",
        "angry", "happy", "disgust", "fearful", "happy", "disgust", "surprised",
        "disgust", "disgust", "angry", "angry", "happy", "happy", "disgust",
        "happy", "disgust", "disgust", "angry", "angry", "angry", "fearful",
        "angry", "happy", "fearful", "fearful", "disgust", "angry", "disgust",
        "fearful", "disgust", "angry", "angry", "disgust", "fearful", "disgust",
        "disgust", "disgust", "angry", "disgust", "happy", "angry", "disgust",
        "angry", "fearful"
    ]
}

def analyze_emotions():
    """
    Analyzes the emotion data and generates both bar and line charts for the frequencies.
    
    Returns:
        chart_details (dict): A dictionary containing the chart paths and emotion counts.
    """
    # Count occurrences of each emotion
    emotion_counts = Counter(data["emotion"])

    # Generate a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(emotion_counts.keys(), emotion_counts.values(), color='skyblue')
    plt.title('Emotion Frequencies', fontsize=16)
    plt.xlabel('Emotions', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the bar chart
    bar_chart_path = "static/images/emotion_bar_chart.png"
    plt.savefig(bar_chart_path)
    plt.close()

    # Create a line graph with x-axis as time (in seconds)
    time_in_seconds = np.arange(0, len(data["emotion"]))  # Time intervals (0, 1, 2, ..., n)
    emotion_freq = [emotion_counts.get(emotion, 0) for emotion in data["emotion"]]  # Frequency of each emotion at each second

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(time_in_seconds, emotion_freq, color='orange', marker='o', linestyle='-', linewidth=2, markersize=5)
    plt.title('Emotion Frequency Over Time', fontsize=16)
    plt.xlabel('Time (seconds)', fontsize=14)
    plt.ylabel('Emotion Frequency', fontsize=14)
    plt.grid(True)

    # Save the line chart
    line_chart_path = "static/images/emotion_line_chart.png"
    plt.savefig(line_chart_path)
    plt.close()

    # Generate the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(emotion_counts.values(), labels=emotion_counts.keys(), autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title('Emotion Distribution', fontsize=16)

    # Save the pie chart
    pie_chart_path = "static/images/emotion_pie_chart.png"
    plt.savefig(pie_chart_path)
    plt.close()

    # Return chart details
    chart_details = {
        "bar_chart_path": bar_chart_path,
        "line_chart_path": line_chart_path,
        "pie_chart_path": pie_chart_path,  # Return the pie chart path
        "counts": dict(emotion_counts)
    }

    return chart_details
