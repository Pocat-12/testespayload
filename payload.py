import tkinter as tk

# 1. Setup the main hidden controller
root = tk.Tk()
root.withdraw()

# Load your image once
image = tk.PhotoImage(file="hacked.png") 

# 2. Create a function that handles the delay loop
def spawn_window(g):
    if g > 0:
        # Create the pop-up
        window = tk.Toplevel(root)
        window.title("PAYLOAD_EXECUTED__" + str(g))
        
        # Position it
        x_offset = 100 + (g * 300 % 1080)
        y_offset = 100 + (g * 300 % 720)
        window.geometry(f"1000x560+{x_offset}+{y_offset}")

        # Add image
        label = tk.Label(window, image=image)
        label.pack(pady=0)
        label.image = image 

        # 3. Instead of sleep, tell Tkinter to run this function again 
        # after 200 milliseconds (0.2 seconds) with the next 'g' value
        root.after(200, spawn_window, g - 1)

# 4. Start the chain reaction with your starting 'g' value
starting_g = 100
spawn_window(starting_g)

# 5. Keep the program alive
root.mainloop()
