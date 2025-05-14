import numpy as np
import pandas as pd
import cv2
import imutils
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

camera = None

# Function to select an image file using Tkinter file dialog
def select_image():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select an image file using a file explorer
    inputfile = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])

    # Check if the user selected a file
    if inputfile:
        # Read the selected image
        img = cv2.imread(inputfile)
        img_copy = img.copy()  # Make a copy of the image to reset the circle
        imgWidth, imgHeight = img.shape[1], img.shape[0]

        # Read the colors CSV file
        index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
        df = pd.read_csv("C:\\Users\\LENOVO\\Desktop\\color_detection_python_app\\colordetection_code\\colors.csv", header=None, names=index)

        # Initialize variables
        r = g = b = xpos = ypos = 0
        clicked = False
        font = cv2.FONT_HERSHEY_SIMPLEX  # Use a normal font

        # Define the "Close" button position and size
        close_button_pos = (imgWidth - 100, 20)
        close_button_size = (80, 40)

        def getRGBvalue(event, x, y, flags, param):
            nonlocal b, g, r, xpos, ypos, clicked
            if event == cv2.EVENT_LBUTTONDOWN:
                if (close_button_pos[0] <= x <= close_button_pos[0] + close_button_size[0] and
                        close_button_pos[1] <= y <= close_button_pos[1] + close_button_size[1]):
                    root.destroy()
                else:
                    xpos = x
                    ypos = y
                    b, g, r = img[y, x]
                    b = int(b)
                    g = int(g)
                    r = int(r)
                    clicked = True

        def colorname(B, G, R):
            minimum = 10000
            cname = ""
            hex_code = ""
            # Initialize low and high indices for binary search
            low = 0
            high = len(df) - 1
            
            while low <= high:
                mid = (low + high) // 2
                # Calculate the difference between the target color and the current color in the dataset
                d = abs(B - int(df.loc[mid, "B"])) + abs(G - int(df.loc[mid, "G"])) + abs(R - int(df.loc[mid, "R"]))
                
                # Update minimum difference and closest color if a closer color is found
                if d < minimum:
                    minimum = d
                    cname = df.loc[mid, "color_name"]
                    hex_code = df.loc[mid, "hex"]
                
                # If the target color is less than the current color, search the left half
                if (R, G, B) < (int(df.loc[mid, "R"]), int(df.loc[mid, "G"]), int(df.loc[mid, "B"])):
                    high = mid - 1
                # If the target color is greater than the current color, search the right half
                else:
                    low = mid + 1
            
            return cname, hex_code


        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", getRGBvalue)

        run = True
        while run:
            if clicked:
                img = img_copy.copy()  # Reset the image to remove old circle
                # Draw a filled circle with the detected color
                center = (xpos, ypos)
                radius = 120
                cv2.circle(img, center, radius, (b, g, r), -1)
                cname, hex_code = colorname(b, g, r)
                # Choose text color for contrast
                text_color = (255, 255, 255) if (r + g + b) < 600 else (0, 0, 0)
                # Put the color name and hex code inside the circle
                font_scale = 0.8
                thickness = 2
                # Calculate text sizes
                cname_size = cv2.getTextSize(cname, font, font_scale, thickness)[0]
                hex_code_size = cv2.getTextSize(hex_code, font, font_scale, thickness)[0]
                # Calculate positions
                cname_x = xpos - cname_size[0] // 2
                cname_y = ypos - 10
                hex_code_x = xpos - hex_code_size[0] // 2
                hex_code_y = ypos + hex_code_size[1] // 2 + 10  # Add a gap between color name and hex code
                # Put text on the image
                cv2.putText(img, cname, (cname_x, cname_y), font, font_scale, text_color, thickness, cv2.LINE_AA)
                cv2.putText(img, hex_code, (hex_code_x, hex_code_y), font, font_scale, text_color, thickness, cv2.LINE_AA)
                clicked = False

            # Display RGB values at the bottom of the image
            #cv2.putText(img, f'R={r} G={g} B={b}', (10, imgHeight - 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Draw the "Close" button
            #cv2.rectangle(img, close_button_pos, (close_button_pos[0] + close_button_size[0], close_button_pos[1] + close_button_size[1]), (0, 0, 255), -1)
            #cv2.putText(img, 'Close', (close_button_pos[0] + 10, close_button_pos[1] + 25), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow("Image", img)

            if cv2.waitKey(20) & 0xFF == 27:
                break

        cv2.destroyAllWindows()
    else:
        print("No file selected.")  # Inform the user if no file was selected

# Function to start video feed from camera
def start_video_feed():
    global camera
    camera = cv2.VideoCapture(0)

    r = g = b = xpos = ypos = 0

    index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
    df = pd.read_csv("C:\\Users\\LENOVO\\Desktop\\color_detection_python_app\\colordetection_code\\colors.csv", names=index, header=None)

    # Initialize clicked to False
    clicked = False

    def getColorName(B, G, R):
        minimum = 10000
        cname = ""
        hex_code = ""
        # Initialize low and high indices for binary search
        low = 0
        high = len(df) - 1
        
        while low <= high:
            mid = (low + high) // 2
            # Calculate the difference between the target color and the current color in the dataset
            d = abs(B - int(df.loc[mid, "B"])) + abs(G - int(df.loc[mid, "G"])) + abs(R - int(df.loc[mid, "R"]))
            
            # Update minimum difference and closest color if a closer color is found
            if d < minimum:
                minimum = d
                cname = df.loc[mid, "color_name"]
                hex_code = df.loc[mid, "hex"]
            
            # If the target color is less than the current color, search the left half
            if (R, G, B) < (int(df.loc[mid, "R"]), int(df.loc[mid, "G"]), int(df.loc[mid, "B"])):
                high = mid - 1
            # If the target color is greater than the current color, search the right half
            else:
                low = mid + 1
        
        return cname, hex_code


    def draw_circle(frame, center, radius, color):
        cv2.circle(frame, center, radius, color, -1)

    def identify_color(event, x, y, flags, param):
        nonlocal b, g, r, xpos, ypos, clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            xpos = x
            ypos = y
            b, g, r = frame[y, x]
            b = int(b)
            g = int(g)
            r = int(r)
            clicked = True

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', identify_color)

    while True:
        (grabbed, frame) = camera.read()
        frame = imutils.resize(frame, width=1200)
        kernal = np.ones((5, 5), "uint8")

        # Draw the circle around the mouse cursor
        draw_circle(frame, (xpos, ypos), 120, (b, g, r))

        # Get color name and hex code
        if clicked:
            color_name, hex_code = getColorName(b, g, r)
        else:
            color_name, hex_code = "", ""

        # Calculate text size and position
        text_size, _ = cv2.getTextSize(color_name, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        text_x = xpos - text_size[0] // 2
        text_y = ypos + text_size[1] // 2

        # Display color name centered within circle
        cv2.putText(frame, color_name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Display hex code centered below color name
        hex_size, _ = cv2.getTextSize(hex_code, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        hex_x = xpos - hex_size[0] // 2
        hex_y = text_y + hex_size[1] + 10
        cv2.putText(frame, hex_code, (hex_x, hex_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('image', frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

        if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
            break

    camera.release()
    cv2.destroyAllWindows()

# Create a Tkinter root window
root = tk.Tk()
root.title("Color Detection")

# Set window size to full screen
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}+0+0")

# Define window closing protocol
root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

# Define custom styles for buttons
style = ttk.Style(root)
style.theme_use("clam")
style.configure('Orange.TButton', foreground='green', font=('Helvetica', 12, 'bold'))
style.configure('Blue.TButton', foreground='blue', font=('Helvetica', 12, 'bold'))
style.configure('Heading.TLabel', foreground='red', font=('Helvetica', 50, 'bold'))

# Create a frame for the GUI
frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)
# Open and resize the background image to fit the window
background_image = Image.open("C:\\Users\\LENOVO\\Desktop\\color_detection_python_app\\colordetection_code\\Backgroundimage.jpg")
background_image = background_image.resize((window_width, window_height))
background_image = ImageTk.PhotoImage(background_image)
background_label = tk.Label(frame, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()  
# Add a heading label
heading_label = ttk.Label(frame, text="COLOR DETECTION", style='Heading.TLabel', padding="10 10 10 10")
heading_label.pack()

  
# Create a frame for buttons
button_frame = ttk.Frame(frame)
button_frame.pack()

# Load and resize the images for buttons
btn_image1_img = ImageTk.PhotoImage(Image.open("C:\\Users\\LENOVO\\Desktop\\color_detection_python_app\\colordetection_code\\image1.jpg").resize((100, 100), Image.BILINEAR))
btn_image2_img = ImageTk.PhotoImage(Image.open("C:\\Users\\LENOVO\\Desktop\\color_detection_python_app\\colordetection_code\\image2.jpg").resize((100, 100), Image.BILINEAR))

# Create buttons with images
btn_image = ttk.Button(button_frame, image=btn_image1_img, command=select_image, style='Orange.TButton')
btn_image.image = btn_image1_img  # Keep a reference to avoid garbage collection
btn_image.grid(row=0, column=0, padx=50)

btn_video = ttk.Button(button_frame, image=btn_image2_img, command=start_video_feed, style='Blue.TButton')
btn_video.image = btn_image2_img  # Keep a reference to avoid garbage collection
btn_video.grid(row=0, column=1, padx=50)

# Create labels for button names
label1 = ttk.Label(button_frame, text="UPLOAD IMAGE")
label1.grid(row=1, column=0)

label2 = ttk.Label(button_frame, text="OPEN CAMERA")
label2.grid(row=1, column=1)

# Start the Tkinter event loop
root.mainloop()
