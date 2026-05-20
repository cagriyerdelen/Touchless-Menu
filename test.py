import cv2
import mediapipe as mp

# MediaPipe el algılama modülleri
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Web kamerasını başlat 
cap = cv2.VideoCapture(1)

print("Kamera açılıyor... Kapatmak için klavyeden 'q' tuşuna basın.")

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Kameradan görüntü alınamadı.")
            continue

        # Görüntüyü aynalayıp RGB'ye çeviriyoruz
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Elleri tespit et
        results = hands.process(image_rgb)

        # El tespit edildiyse ekrana iskelet çizgilerini çiz
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS)

        # Sonucu ekranda göster
        cv2.imshow('Touchless Menu - Temiz Baslangic Testi', image)
        
        # 'q' tuşuna basılırsa döngüyü kır
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()