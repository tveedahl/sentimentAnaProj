import sqlite3
import nltk
import tkinter as tk
from tkinter import messagebox
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

# Download VADER lexicon if needed
nltk.download("vader_lexicon")

def save_to_db(data):
    conn = sqlite3.connect("user_inputs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("INSERT INTO inputs (content) VALUES (?)", (data,))
    conn.commit()
    conn.close()

def submit_input():
    user_text = entry.get()
    if user_text.strip():
        save_to_db(user_text)

        user_inputs = load_inputs_as_tuples()
        sid = SentimentIntensityAnalyzer()

        for row in user_inputs:
            text = row[0]  # Get the actual content string from the tuple
            print(f"Analyzing: {text}")
            scores = sid.polarity_scores(text)
            summary = "\n".join([f"{k.capitalize()}: {v:.2f}" for k, v in scores.items()])
            messagebox.showinfo("Input Saved", f"Sentiment Analysis:\n{summary}")

        entry.delete(0, tk.END)  # Clear entry after saving
    else:
        messagebox.showwarning("Empty Input", "Please enter something.")

def load_inputs_as_tuples():
    conn = sqlite3.connect("user_inputs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM inputs ORDER BY timestamp DESC LIMIT 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

# GUI setup
root = tk.Tk()
root.title("User Input GUI")
root.geometry("500x200")

label = tk.Label(root, text="What's On Your Mind?")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=submit_input)
submit_button.pack(pady=10)

root.mainloop()
