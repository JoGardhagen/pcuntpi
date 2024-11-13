from gui import (create_root_window, set_fullscreen, add_image, create_timer_label,
                 create_canvas,draw_clock_face,creat_last_race_label,
                 create_best_time_label,create_saved_times_label)
from timer_logic import start_timer, stop_timer,save_time,update_best_time_label
from sensors import check_ir_sensor, check_beam_breaker_sensor
from hardware import setup_gpio, cleanup_gpio
from time import sleep


def close_app(root, event=None):
    cleanup_gpio()  # Stäng av GPIO först
    root.destroy()  # Stäng Tkinter-applikationen

def main():
    setup_gpio()
    root = create_root_window()
    set_fullscreen(root)
    best_time_label = create_best_time_label(root)
    saved_times_label = create_saved_times_label(root)
    add_image(root)
    canvas = create_canvas(root, size=200)
    center_x = 100  # Justera dessa värden baserat på din canvas storlek
    center_y = 100
    clock_radius = 90

    # Rita urtavlan på canvasen
    draw_clock_face(canvas, center_x, center_y, clock_radius)
    lastRaceLabel =  creat_last_race_label(root)   
    timer_label = create_timer_label(root)


    center_x = 100  # Justera dessa värden baserat på din canvas storlek
    center_y = 100
    clock_radius = 90

    # Bind mellanslagstangenten för att starta timern
    root.bind("<space>", lambda event: start_timer(root, canvas, timer_label, center_x, center_y, clock_radius, saved_times_label,lastRaceLabel))


    # Bind enter-tangenten för att spara tiden
    root.bind("<Return>", lambda event: save_time(timer_label, canvas, lastRaceLabel, best_time_label, saved_times_label))


    # Bind Escape-tangenten för att stänga programmet
    root.bind("<Escape>", lambda event: close_app(root,event))

    # Starta övervakning av sensorer
    check_ir_sensor(root, lambda: start_timer(root, canvas, timer_label, center_x, center_y, clock_radius, saved_times_label, lastRaceLabel))
    check_beam_breaker_sensor(root, lambda: save_time(timer_label, canvas, lastRaceLabel, best_time_label, saved_times_label))


    root.mainloop() 

if __name__ == "__main__":
    #sleep(5)
    main()