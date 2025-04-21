import cv2
import time

def setup_camera():
    # Starta kameran (standard �r 0, men kan �ndras om du har flera kameror)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Kameran kunde inte starta.")
        return

    print("Kameran �r i inst�llningsl�ge. Justera kameran och tryck ESC f�r att avsluta.")

    while True:
        # L�s en bild fr�n kameran
        ret, frame = cap.read()
        if not ret:
            print("Misslyckades med att l�sa bild fr�n kameran.")
            break

        # Rita en linje p� kamerabilden f�r att representera m�llinjen
        line_position = int(frame.shape[0] / 2)  # Justera detta f�r att st�lla in linjens position vertikalt
        color = (0, 255, 0)  # Linjens f�rg, gr�n h�r
        thickness = 3  # Tjocklek p� linjen

        # Rita en linje horisontellt i mitten av bilden
        cv2.line(frame, (0, line_position), (frame.shape[1], line_position), color, thickness)

        # Visa bilden p� sk�rmen med linjen
        cv2.imshow("Kamera Setup - Justera kameran och tryck ESC f�r att avsluta", frame)

        # V�nta p� tangenttryckning
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Om ESC trycks, avsluta setup
            break

        # L�gg till lite f�rdr�jning f�r att h�lla videostr�mmen mjuk
        time.sleep(0.03)

    cap.release()
    cv2.destroyAllWindows()
    print("Kamerainst�llning avslutad.")
