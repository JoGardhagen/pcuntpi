import math
import tkinter as tk

# Skapa och uppdatera huvudfönstret
def create_root_window():
    root = tk.Tk()
    root.title("Timer")
    root.config(cursor="none")
    return root

def set_fullscreen(window):
    for _ in range(5):
        window.attributes("-fullscreen", True)
        window.wm_attributes("-topmost", True)
        #window.attributes("-topmost",True)
        window.update_idletasks()
    window.after(1000)

def create_canvas(root, size=200):
    canvas = tk.Canvas(root, width=size, height=size)
    canvas.pack(expand=True)
    return canvas

def add_image(root):
    photo = tk.PhotoImage(file="/home/piroot/Desktop/pcuntpi/logo.png")
    img_label = tk.Label(root, image=photo)
    img_label.image = photo  # Håll referens till bilden
    img_label.pack(side="bottom", fill="x")

def create_timer_label(root):
    label = tk.Label(root, text="0:00.000", font=("Helvetica", 40), fg="black")
    label.pack(pady=20)
    return label

def creat_last_race_label(root):
    last_race_label = tk.Label(root, text="", font=("Helvetica", 20),bg="black", fg="snow")
    last_race_label.pack(pady=10,fill="x")
    return last_race_label

def create_best_time_label(root):
    best_time_label = tk.Label(root, text="Bästa tiden: --:--.---", font=("Helvetica", 20), fg="black")
    best_time_label.pack(anchor="ne", padx=10, pady=10)  # Placera i övre högra hörnet
    return best_time_label

def create_saved_times_label(root):
    saved_times_label = tk.Label(root, text="Föregående Race:", font=("Helvetica", 20), anchor="nw", justify="left")
    saved_times_label.place(x=10, y=10)  # Placera i övre vänstra hörnet
    return saved_times_label

# Uppdatera timeretiketten
def update_timer_label(label, elapsed_time):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)
    label.config(text=f"{minutes}:{seconds:02d}.{milliseconds:03d}")

# Rita sekundvisaren
def draw_second_hand(canvas, center_x, center_y, clock_radius, elapsed_time):
    seconds = elapsed_time % 60
    angle = math.radians(90 - (seconds * 6))
    hand_length = clock_radius - 20
    end_x = center_x + hand_length * math.cos(angle)
    end_y = center_y - hand_length * math.sin(angle)
    second_hand = canvas.create_line(center_x, center_y, end_x, end_y, fill="red", width=2)
    return second_hand

# Rita urtavlan
def draw_clock_face(canvas, center_x, center_y, clock_radius):
    canvas.create_oval(center_x - clock_radius, center_y - clock_radius,
                       center_x + clock_radius, center_y + clock_radius, outline="black", width=2)
    
    for i in range(12):
        angle_deg = i * 30
        angle_rad = math.radians(angle_deg)
        x_outer = center_x + clock_radius * math.cos(angle_rad)
        y_outer = center_y - clock_radius * math.sin(angle_rad)
        x_inner = center_x + (clock_radius - 20) * math.cos(angle_rad)
        y_inner = center_y - (clock_radius - 20) * math.sin(angle_rad)
        canvas.create_line(x_outer, y_outer, x_inner, y_inner, fill="black", width=2)