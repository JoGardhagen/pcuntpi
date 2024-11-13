import time
import math
from gui import update_timer_label, draw_second_hand  # Vi importerar dessa från GUI

# Variabler för att hålla koll på timern
timing = False
start_time = 0
elapsed_time = 0
second_hand = None
saved_times = []
best_time = None  # Håller koll på bästa tiden
MAX_TIME = 15


def update_best_time_label(best_time_label):
    global best_time, saved_times
    if saved_times:
        current_best = min(saved_times)
        if best_time is None or current_best < best_time:
            best_time = current_best
            minutes = int(best_time // 60)
            seconds = int(best_time % 60)
            milliseconds = int((best_time * 1000) % 1000)
            best_time_label.config(text=f"Bästa tiden: {minutes}:{seconds:02d}.{milliseconds:03d}")

def save_time(time_label, canvas, last_race_label, best_time_label, saved_times_label):

    global elapsed_time, saved_times
    if timing:  # Kontrollera om timern är igång
        # Spara tiden i listan
        saved_times.append(elapsed_time)
        
        # Begränsa listan till de senaste fyra tiderna och kalla på reset_timer om fyra tider finns
        if len(saved_times) >= 4:
            stop_timer(time_label, canvas, saved_times_label,last_race_label)

        # Uppdatera etiketter efter att tiden sparats
        update_best_time_label(best_time_label)


# Funktion för att visa de senaste fyra tiderna i GUI
def update_race_collections(last_race_label):
    global saved_times
    if len(saved_times) == 0:
        last_race_label.config(text="")
    else:
        result = "\t\t".join([f"{i+1}: {time:.3f} s" for i, time in enumerate(saved_times)])
        last_race_label.config(text=f"{result}")


# Starta timern
def start_timer(root, canvas, time_label, center_x, center_y, clock_radius, saved_times_label,last_race_label):

    global timing, start_time, elapsed_time
    if not timing:
        timing = True
        start_time = time.time()
        elapsed_time = 0
        update_clock(root, canvas, time_label, center_x, center_y, clock_radius, saved_times_label,last_race_label)


# Stoppa timern
def stop_timer(time_label, canvas, saved_times_label,last_race_label):
    global timing, elapsed_time
    if timing:
        timing = False
        elapsed_time = time.time() - start_time
        reset_timer(time_label, canvas, saved_times_label,last_race_label)  # Återställ etikett och tid


# Uppdatera klockan och sekundvisaren
def update_clock(root, canvas, time_label, center_x, center_y, clock_radius, saved_times_label,last_race_label):
    global elapsed_time, timing, second_hand
    if timing:
        # Beräkna förfluten tid
        elapsed_time = time.time() - start_time

        # Kontrollera om max tid är nådd eller om fyra tider har sparats
        if elapsed_time >= MAX_TIME :
            stop_timer(time_label, canvas, saved_times_label,last_race_label)
            saved_times.clear()
            return  # Avsluta funktionen

        # Om det redan finns en sekundvisare, ta bort den
        if second_hand is not None:
            canvas.delete(second_hand)

        # Rita den nya sekundvisaren och spara dess id så vi kan ta bort den nästa gång
        second_hand = draw_second_hand(canvas, center_x, center_y, clock_radius, elapsed_time)

        # Uppdatera timeretiketten
        update_timer_label(time_label, elapsed_time)

        # Anropa funktionen igen efter 10ms
        root.after(10, update_clock, root, canvas, time_label, center_x, center_y, clock_radius, saved_times_label,last_race_label)

        update_race_collections(last_race_label)


# Uppdatera sparade tider på skärmen
def update_saved_times_label(saved_times_label):
    global saved_times
    if len(saved_times) != 0:
        result = "\n".join([f"{i+1}: {time:.3f} s" for i, time in enumerate(saved_times)])
        saved_times_label.config(text=result)


# Återställ timern och uppdatera etiketter
def reset_timer(time_label, canvas, saved_times_label,last_race_label):
    global timing, elapsed_time, second_hand, saved_times
    timing = False
    elapsed_time = 0

    # Nollställ tidsetiketten om den finns
    if time_label is not None:
        time_label.config(text="00:00.000")

    # Ta bort sekundvisaren om canvas inte är None och second_hand finns
    if canvas is not None and second_hand is not None:
        canvas.delete(second_hand)
        second_hand = None

    # Uppdatera saved_times_label med de senaste sparade tiderna
    update_saved_times_label(saved_times_label)


    # Rensa listan för att möjliggöra nya tider
    saved_times.clear()
    update_race_collections(last_race_label)
