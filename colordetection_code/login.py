import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import subprocess
from PIL import Image, ImageTk

# Function to create a new user
def create_user():
    new_username = entry_new_username.get()
    new_password = entry_new_password.get()
    
    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (new_username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        messagebox.showerror("Error", "Username already exists!")
    elif new_username and new_password:
        # Add new user to the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
        conn.commit()
        messagebox.showinfo("Success", "New user created successfully!")
        entry_new_username.delete(0, tk.END)
        entry_new_password.delete(0, tk.END)
        dialog_create_user.pack_forget()  # Close the dialog after creating the user
    else:
        messagebox.showerror("Error", "Username or password cannot be empty!")

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check if username and password are correct
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Successful", "Click OK to continue!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        root.withdraw()  # Hide the login window
        subprocess.Popen(["python", "colormain.py"])  # Open another Python file
        root.deiconify()  # Show the login window again
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Connect to SQLite database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)''')
conn.commit()

# Create the main window
root = tk.Tk()
root.title("Login Page")

# Customize colors
bg_color = "white"  # light pink
text_color = "white"  # dark purple
button_bg = "green"  # light purple
button_fg = "white"  # white text color for buttons

root.configure(bg=bg_color)

# Set window size to full screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Load and set the background image
bg_image = Image.open("backgroundimage.jpg")
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame to contain login details
frame_login = tk.Frame(root, bg="lightgray", bd=2, relief=tk.RAISED)
frame_login.pack(padx=20, pady=20)

# Username Label and Entry
label_username = tk.Label(frame_login, text="Username:", bg="#536872", fg=text_color, font=("Arial", 16))
label_username.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_username = tk.Entry(frame_login, font=("Arial", 16))
entry_username.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Password Label and Entry
label_password = tk.Label(frame_login, text="Password:", bg="#5f9ea0", fg=text_color, font=("Arial", 16))
label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_password = tk.Entry(frame_login, show="*", font=("Arial", 16))
entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

# Login Button
button_login = tk.Button(root, text="Login", command=login, bg="red", fg=button_fg, font=("Arial", 14), relief=tk.RAISED)
button_login.pack(pady=(0, 10), padx=20, fill="y")

# Create a frame for creating a new user
dialog_create_user = tk.Frame(root, bg="lightgray", bd=2, relief=tk.RAISED)

# Username Label and Entry for new user
label_new_username = tk.Label(dialog_create_user, text="New Username:", bg="#536872")
label_new_username.grid(row=0, column=0, padx=10, pady=5)
entry_new_username = tk.Entry(dialog_create_user)
entry_new_username.grid(row=0, column=1, padx=10, pady=5)

# Password Label and Entry for new user
label_new_password = tk.Label(dialog_create_user, text="New Password:", bg="#5f9ea0")
label_new_password.grid(row=1, column=0, padx=10, pady=5)
entry_new_password = tk.Entry(dialog_create_user, show="*")
entry_new_password.grid(row=1, column=1, padx=10, pady=5)

# Create Button for new user
button_create = tk.Button(dialog_create_user, text="Create User", bg="blue", command=create_user)
button_create.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# New User Button
button_new_user = tk.Button(root, text="Create New User", command=lambda: dialog_create_user.pack(), bg=button_bg, fg=button_fg, font=("Arial", 14), relief=tk.RAISED)
button_new_user.pack(pady=(0, 10), padx=20, fill="y")

# Run the application
root.mainloop()

# Close database connection when the application exits
conn.close()
