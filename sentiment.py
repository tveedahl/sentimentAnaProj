import sqlite3
import nltk
import tkinter as tk
from tkinter import messagebox

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
        #Determine user input sentiment here
        user_inputs = load_inputs_as_dicts()
        for item in user_inputs:
            print(user_inputs)
        messagebox.showinfo("Input Saved", f"The User Sentient So Far Suggests: {user_inputs}")
        entry.delete(0, tk.END)  # Clear entry after saving
    else:
        messagebox.showwarning("Empty Input", "Please enter something.")

def load_inputs_as_dicts():
    conn = sqlite3.connect("user_inputs.db")
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM inputs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    results = [dict(row) for row in rows]  # Convert Row objects to dicts
    conn.close()
    return results

# Create the main window
root = tk.Tk()
root.title("User Input GUI")
root.geometry("3000x1000")

# Create a label
label = tk.Label(root, text="Enter something:")
label.pack(pady=5)

# Create a text entry field
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit_input)
submit_button.pack(pady=10)

# Run the application
root.mainloop()
