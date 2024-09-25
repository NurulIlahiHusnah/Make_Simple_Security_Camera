import cv2
import time
import datetime

cap = cv2.VideoCapture(0) # untuk mengakses perangkat webcam yang digunakan 

# Mendeteksi wajah dan tubuh
face_cascade = cv2.CascadeClassifier(       
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False # menyimpan status apakah deteksi wajah dan tubuh terjadi 
detection_stopped_time = None # waktu ketika deteksi berhenti 
timer_started = False # menyimpan status apakah timer telah dimulai
SECOND_TO_RECORD_AFTER_DETECTION = 5 # durasi tambahan untuk merekam video setelah selesai (5 detik)

# Menentukan format dan ukuran frame dari video
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"XVID") # 4 kode dalam kurung merupakan jenis format video 

# Melakukan looping untuk mendapat frame dari kamera
while True:
    _, frame = cap.read() # untuk membaca frame dan menanpilkan dilayar 
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5 )
    
# Ketika wajah atau tubuh terdeteksi, mulai merekam, proses perekaman dimulai dan video disimpan 
# dengan nama berdasarkan timestamp saat ini.
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(
                f'{current_time}.avi', fourcc, 20, frame_size )
            print('Started Recording!')
            
# Jika deteksi berhenti: 
# Setelah deteksi berhenti, program akan terus merekam selama 5 detik tambahan. 
# Setelah itu, perekaman dihentikan dan file video ditutup.
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECOND_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("Stop Recording!")
        else:
            timer_started = True
            detection_stopped_time = time.time()
# Jika deteksi terjadi, frame akan disimpan ke dalam file video.            
    if detection:
        out.write(frame)
    # for (x, y, width, height) in faces:
    #     cv2.rectangle(frame,(x, y), (x + width, y + height),(255, 0, 0),3)
    
    cv2.imshow('Camera',frame) # Menampilkan video dari kamera secara real-time.
    
    
    if cv2.waitKey(1) == ord('q'): # Jika pengguna menekan tombol 'q', program akan berhenti.
        break
    
# Melepaskan objek video writer dan kamera serta menutup semua jendela yang ditampilkan.    
out.release()
cap.release()
cv2.destroyAllWindows()