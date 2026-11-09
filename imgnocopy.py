import os
import shutil
import threading
import time
import sys
import subprocess
import tkinter as tk
import random
import socket
import classify
loop = False
print("Starting the payload...")
# Simulate some startup delay
def startup():
    pass

def background_task():
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temporary folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    print("Resource path initialized...")
    

    # Example usage in your application:
    # Instead of: image_path = "logo.png"
    image_path = resource_path("hacked.png")

    # 1. Setup the main hidden controller
    root = tk.Tk()
    root.withdraw()

    # Load your image once
    image = tk.PhotoImage(file=f"{image_path}") 

    # 2. Create a function that handles the delay loop
    def spawn_window(g):
          # Random delay between 1 and 3 seconds
        if g > 0:
        # Create the pop-up
            window = tk.Toplevel(root)
            window.title("PAYLOAD_EXECUTED__" + str(g))
            
            print(f"Spawned window with g={g}")
        # Position it
            x_offset = 1 + ( random.randint(1, 1080))
            y_offset = 1 + ( random.randint(1, 720))
            window.geometry(f"1000x560+{x_offset}+{y_offset}")

        # Add image
            label = tk.Label(window, image=image)
            label.pack(pady=0)
            label.image = image 

        # 3. Instead of sleep, tell Tkinter to run this function again 
        # after 200 milliseconds (0.2 seconds) with the next 'g' value
            root.after(300, spawn_window, g - 1)

    starting_g = 100
    spawn_window(starting_g)
    # 5. Keep the program alive
    root.mainloop()







thread1 = threading.Thread(target=background_task)
time.sleep(random.randint(1, 2))
thread1.start()
 # Wait for the background task to initialize
thread2 = threading.Thread(target=background_task)
thread2.start()
time.sleep(1) 