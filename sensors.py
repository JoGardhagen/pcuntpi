import tkinter as tk
import cv2
import numpy as np
import time
from hardware import read_gpio

# Variabler för att hålla reda på föregående tillstånd av sensorer
last_ir_state = None  # För IR-sensorn
last_beam_state = None  # För ljusstrålebrytaren

# Kolla IR-sensorn och starta timer om reflektion upptäcks (flankdetektering)
def check_ir_sensor(root, start_timer_callback):
    global last_ir_state
    current_state = read_gpio(17)  # Läs aktuellt tillstånd från IR-sensorn

    # Om tillståndet har förändrats (från LOW till HIGH eller vice versa)
    if last_ir_state is None:  # Första gången vi kollar, sätt föregående tillstånd
        last_ir_state = current_state
        print(f"IR sensor state: {current_state}")
        print(f"Beam breaker sensor state: {current_state}")
    elif current_state != last_ir_state:  # Om tillståndet har ändrats
        if current_state == 1:  # IR-sensorn aktiverad
            start_timer_callback()  # Starta timern när IR-sensorn aktiveras
        last_ir_state = current_state  # Uppdatera föregående tillstånd
    
    # Efteranropa sig själv för kontinuerlig övervakning
    root.after(50, check_ir_sensor, root, start_timer_callback)

# Kolla ljusstrålebrytaren och spara tiden vid brytning (flankdetektering)
def check_beam_breaker_sensor(root, save_time_callback):
    global last_beam_state
    current_state = read_gpio(27)  # Läs aktuellt tillstånd från ljusstrålebrytaren

    # Om tillståndet har förändrats (från LOW till HIGH eller vice versa)
    if last_beam_state is None:  # Första gången vi kollar, sätt föregående tillstånd
        last_beam_state = current_state
        print(f"IR sensor state: {current_state}")
        print(f"Beam breaker sensor state: {current_state}")
    elif current_state != last_beam_state:  # Om tillståndet har ändrats
        if current_state == 1:  # Ljusstrålen har brutits
            save_time_callback()  # Spara tiden när strålen bryts
        last_beam_state = current_state  # Uppdatera föregående tillstånd
    
    # Efteranropa sig själv för kontinuerlig övervakning
    root.after(50, check_beam_breaker_sensor, root, save_time_callback)


def check_camera_goal(root,callback,max_passages):
    cap = cv2.VideoCapture(0)  
    time.sleep(2)

    # Ta en referensbild
    ret, frame = cap.read()
    if not ret:
        print("Kameran kunde inte starta.")
        cap.release()
        return
    
    ref = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    line_y = 450  
    threshold= 8000
    passage_count = 0

    while passage_count < max_passages:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(ref, gray)
        _, thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)
        line = np.sum(thresh[line_y, :])

        if line > threshold:
            print("bil registrerad av kameran!")
            callback()  # Anropa callback-funktionen n�r m�llinjen passeras
            passage_count += 1  # �ka r�knaren f�r passeringar
            print(f"Passering {passage_count}/{max_passages}")
            time.sleep(1)  # Pausa f�r att undvika att vi f�ngar samma g�ng om och om igen (kan justeras)

        # L�gg till en kort paus f�r att inte blockera Tkinter-tr�den
        time.sleep(0.05)
    cap.release()
    cv2.destroyAllWindows()