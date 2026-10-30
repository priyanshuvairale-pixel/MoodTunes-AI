import csv
import cv2
from deepface import DeepFace
from textblob import TextBlob
import pandas as pd
import tkinter as tk
from tkinter import messagebox


bollywood_songs = [
    ["Title", "Artist", "Year", "Mood"],
    ["Badtameez Dil", "Benny Dayal", 2013, "happy"],
   # ["Tum Ho Toh", "Vishal Mishra", 2025, "natural"],
    ["Bekhayali", "Sachet Tandon", 2019, "sad"],
    ["Saadda Haq", "Mohit Chauhan", 2011, "angry"],
    ["Pehla Nasha", "Udit Narayan", 1992, "romantic"],
    ["Hanuman Chalisa", "Hariharan", 1997, "spiritual"],
    ["Chaiyya Chaiyya", "Sukhwinder Singh", 1998, "energetic"],
    ["Tum Hi Ho", "Arijit Singh", 2013, "romantic"],
    ["Kal Ho Naa Ho", "Sonu Nigam", 2003, "emotional"],
    ["Tera Ban Jaunga", "Akhil Sachdeva", 2019, "romantic"],
    ["Zinda", "Siddharth Mahadevan", 2013, "motivational"],
    ["Tum Ho Toh", "Vishal Mishra", 2025, "natural"]  # Added back
]


with open("songs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(bollywood_songs)

print("Bollywood songs.csv created successfully!")


songs_df = pd.read_csv("songs.csv")


def get_song_by_mood(mood):
   
    mood = mood.lower()
    match = songs_df[songs_df['Mood'].str.lower() == mood]
    if not match.empty:
        return match['Title'].values[0]
    return "No song found for this mood."


def detect_mood_from_face():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            mood = result[0]['dominant_emotion']
            return mood
        except Exception as e:
            return "Error detecting mood"
    return "Camera error"


def detect_mood_from_text(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.2:
        return "happy"
    elif polarity < -0.2:
        return "sad"
    else:
        return "neutral"


def recommend_from_face():
    mood = detect_mood_from_face()
    song = get_song_by_mood(mood)
    messagebox.showinfo("Mood Detected", f"Mood: {mood}\nRecommended Song: {song}")

def recommend_from_text():
    text = text_entry.get()
    mood = detect_mood_from_text(text)
    song = get_song_by_mood(mood)
    messagebox.showinfo("Mood Detected", f"Mood: {mood}\nRecommended Song: {song}")


root = tk.Tk()
root.title("Mood-Based Music Recommender")

tk.Label(root, text="Enter your mood in text:").pack()
text_entry = tk.Entry(root, width=50)
text_entry.pack()

tk.Button(root, text="Recommend from Text", command=recommend_from_text).pack(pady=5)
tk.Button(root, text="Recommend from Face", command=recommend_from_face).pack(pady=5)

root.mainloop()