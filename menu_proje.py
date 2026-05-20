import cv2
import mediapipe as mp
import time
import math
import winsound
import threading

# MediaPipe Kurulumu
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Kamera Başlatma
cap = cv2.VideoCapture(1)

# Proje Değişkenleri
active_scene = "Ana Menu"
click_cooldown = 0.8
last_click_time = 0

# Sepet Sistemi
cart = []
total_price = 0

# Sipariş Başarı Ekranı
show_success_message = False
success_start_time = 0

# Bip Sesi
def play_beep():
    threading.Thread(target=winsound.Beep, args=(2000, 100), daemon=True).start()

# Ana Menü Butonları
main_buttons = [
    [15, 140, 115, 220, "Corbalar"],
    [125, 140, 225, 220, "Ana Yemekler"],
    [235, 140, 325, 220, "Tatlilar"],
    [335, 140, 425, 220, "Icecekler"]
]

# Alt Menü İçerikleri
sub_menu_items = {
    "Corbalar": [
        [30, 90, 420, 140, "Mercimek Corbasi", 80],
        [30, 150, 420, 200, "Ezogelin Corbasi", 85],
        [30, 210, 420, 260, "Domates Corbasi", 90],
        [30, 270, 420, 320, "Tavuk Suyu Corba", 95],
        [30, 330, 420, 380, "Kelle Paca Corbasi", 130]
    ],
    "Ana Yemekler": [
        [30, 90, 420, 140, "Izgara Kofte", 240],
        [30, 150, 420, 200, "Tavuklu Pilav", 180],
        [30, 210, 420, 260, "Izgara Somon", 320],
        [30, 270, 420, 320, "Adana Kebab", 260],
        [30, 330, 420, 380, "Karisik Pizza", 210]
    ],
    "Tatlilar": [
        [30, 90, 420, 140, "Baklava (4 Dilim)", 150],
        [30, 150, 420, 200, "Sutlac", 110],
        [30, 210, 420, 260, "Tiramisu", 130],
        [30, 270, 420, 320, "Kunefe", 160],
        [30, 330, 420, 380, "Cikolatali Sufle", 120]
    ],
    "Icecekler": [
        [30, 90, 420, 140, "Kutu Kola", 45],
        [30, 150, 420, 200, "Ayran", 30],
        [30, 210, 420, 260, "Salgam Suyu", 35],
        [30, 270, 420, 320, "Meyve Suyu", 40],
        [30, 330, 420, 380, "Soguk Cay (Ice Tea)", 45]
    ]
}

# Ortak Butonlar
back_button = [30, 405, 150, 460, "Geri"]
checkout_button = [165, 405, 420, 460, "Siparisi Tamamla"]
cancel_btn = [90, 415, 290, 455, "ORDER_CANCEL"]
confirm_btn = [350, 415, 550, 455, "ORDER_CONFIRM"]

hovered_btn = None

print("Parmak Tıklama (Pinch Click) Modu Aktif Edildi!")

while cap.isOpened():

    success, image = cap.read()

    if not success:
        continue

    image = cv2.flip(image, 1)

    # Sipariş Başarı Ekranı
    if show_success_message:

        image[:] = (20, 20, 20)

        cv2.putText(image, "SIPARISINIZ ALINDI", (110, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 4)

        cv2.putText(image, "Tesekkur ederiz", (210, 310),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow('Touchless Menu - Profesyonel Otomasyon', image)

        if time.time() - success_start_time >= 3:
            show_success_message = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        continue

    h, w, c = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # Üst Bilgi Barı
    cv2.rectangle(image, (0, 0), (w, 65), (45, 45, 45), -1)

    cv2.putText(image, f"Ekran: {active_scene}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(image, f"Toplam Tutar: {total_price} TL", (360, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 100), 2)

    # Normal Menü Ekranları
    if active_scene != "Siparis_Ozet":

        # Sepet Paneli
        cv2.rectangle(image, (440, 75), (w - 10, 465), (25, 25, 25), -1)
        cv2.rectangle(image, (440, 75), (w - 10, 465), (200, 200, 200), 1)

        cv2.putText(image, "Siparis Sepeti", (455, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        y_pos = 140
        delete_buttons = []

        for idx, item in enumerate(cart[-8:]):

            actual_idx = len(cart) - len(cart[-8:]) + idx
            short_name = item['name'][:12]

            cv2.putText(image, short_name, (445, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (240, 240, 240), 1)

            cv2.putText(image, f"{item['price']}TL", (540, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 255, 100), 1)

            bx1, by1, bx2, by2 = 590, y_pos - 12, 625, y_pos + 4

            if hovered_btn == f"DELETE_ITEM_{actual_idx}":
                cv2.rectangle(image, (bx1, by1), (bx2, by2), (30, 30, 255), -1)
                cv2.rectangle(image, (bx1, by1), (bx2, by2), (255, 255, 255), 1)
            else:
                cv2.rectangle(image, (bx1, by1), (bx2, by2), (50, 50, 200), -1)

            cv2.putText(image, "X", (bx1 + 10, by1 + 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)

            delete_buttons.append([bx1, by1, bx2, by2, actual_idx])
            y_pos += 35

        # Ana Menü
        if active_scene == "Ana Menu":

            for btn in main_buttons:

                x1, y1, x2, y2, label = btn

                if hovered_btn == f"GO_SCENE_{label}":
                    cv2.rectangle(image, (x1, y1), (x2, y2), (180, 80, 80), -1)
                    cv2.rectangle(image, (x1 - 2, y1 - 2),
                                  (x2 + 2, y2 + 2), (100, 255, 100), 2)
                else:
                    cv2.rectangle(image, (x1, y1), (x2, y2), (150, 60, 60), -1)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 1)

                cv2.putText(image, label, (x1 + 5, y1 + 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 2)

        # Alt Menüler
        else:

            for item in sub_menu_items[active_scene]:

                x1, y1, x2, y2, label, price = item

                if hovered_btn == f"ADD_{label}_{price}":
                    cv2.rectangle(image, (x1, y1), (x2, y2), (70, 70, 70), -1)
                    cv2.rectangle(image, (x1 - 2, y1 - 2),
                                  (x2 + 2, y2 + 2), (100, 255, 100), 2)
                else:
                    cv2.rectangle(image, (x1, y1), (x2, y2), (50, 50, 50), -1)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 1)

                cv2.putText(image, label, (x1 + 10, y1 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)

                cv2.putText(image, f"{price} TL", (x1 + 310, y1 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.42, (100, 255, 100), 2)

            # Geri Butonu
            if hovered_btn == "BACK_TO_MAIN":
                cv2.rectangle(image,
                              (back_button[0], back_button[1]),
                              (back_button[2], back_button[3]),
                              (80, 80, 200), -1)

                cv2.rectangle(image,
                              (back_button[0] - 2, back_button[1] - 2),
                              (back_button[2] + 2, back_button[3] + 2),
                              (100, 255, 100), 2)

            else:
                cv2.rectangle(image,
                              (back_button[0], back_button[1]),
                              (back_button[2], back_button[3]),
                              (60, 60, 160), -1)

            cv2.putText(image, "< Geri",
                        (back_button[0] + 30, back_button[1] + 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                        (255, 255, 255), 2)

        # Siparişi Tamamla
        if len(cart) > 0:

            if hovered_btn == "GO_CHECKOUT":
                cv2.rectangle(image,
                              (checkout_button[0], checkout_button[1]),
                              (checkout_button[2], checkout_button[3]),
                              (80, 180, 80), -1)

                cv2.rectangle(image,
                              (checkout_button[0] - 2, checkout_button[1] - 2),
                              (checkout_button[2] + 2, checkout_button[3] + 2),
                              (100, 255, 100), 2)

            else:
                cv2.rectangle(image,
                              (checkout_button[0], checkout_button[1]),
                              (checkout_button[2], checkout_button[3]),
                              (60, 150, 60), -1)

        else:
            cv2.rectangle(image,
                          (checkout_button[0], checkout_button[1]),
                          (checkout_button[2], checkout_button[3]),
                          (70, 85, 70), -1)

        cv2.putText(image, "Siparisi Tamamla",
                    (checkout_button[0] + 30, checkout_button[1] + 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (255, 255, 255), 2)

    # Sipariş Özet Ekranı
    else:

        cv2.rectangle(image, (60, 75), (580, 465), (30, 30, 30), -1)
        cv2.rectangle(image, (60, 75), (580, 465), (100, 255, 100), 2)

        cv2.putText(image, "SIPARIS ADISYON OZETI", (200, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.line(image, (80, 130), (560, 130), (255, 255, 255), 1)

        y_pos = 160

        for idx, item in enumerate(cart[-7:]):

            cv2.putText(image, f"{idx + 1}. {item['name']}",
                        (90, y_pos), cv2.FONT_HERSHEY_SIMPLEX,
                        0.45, (220, 220, 220), 1)

            cv2.putText(image, f"{item['price']} TL",
                        (460, y_pos), cv2.FONT_HERSHEY_SIMPLEX,
                        0.45, (100, 255, 100), 1)

            y_pos += 28

        cv2.line(image, (80, 365), (560, 365), (255, 255, 255), 1)

        cv2.putText(image, f"GENEL TOPLAM: {total_price} TL",
                    (280, 395), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (100, 255, 100), 2)

        # İptal Butonu
        if hovered_btn == "ORDER_CANCEL":
            cv2.rectangle(image,
                          (cancel_btn[0], cancel_btn[1]),
                          (cancel_btn[2], cancel_btn[3]),
                          (70, 70, 200), -1)

            cv2.rectangle(image,
                          (cancel_btn[0] - 2, cancel_btn[1] - 2),
                          (cancel_btn[2] + 2, cancel_btn[3] + 2),
                          (100, 255, 100), 2)

        else:
            cv2.rectangle(image,
                          (cancel_btn[0], cancel_btn[1]),
                          (cancel_btn[2], cancel_btn[3]),
                          (50, 50, 180), -1)

        cv2.putText(image, "Siparisi Iptal Et",
                    (115, 440), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)

        # Onay Butonu
        if hovered_btn == "ORDER_CONFIRM":
            cv2.rectangle(image,
                          (confirm_btn[0], confirm_btn[1]),
                          (confirm_btn[2], confirm_btn[3]),
                          (70, 200, 70), -1)

            cv2.rectangle(image,
                          (confirm_btn[0] - 2, confirm_btn[1] - 2),
                          (confirm_btn[2] + 2, confirm_btn[3] + 2),
                          (100, 255, 100), 2)

        else:
            cv2.rectangle(image,
                          (confirm_btn[0], confirm_btn[1]),
                          (confirm_btn[2], confirm_btn[3]),
                          (50, 180, 50), -1)

        cv2.putText(image, "Siparisi Onayla",
                    (375, 440), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)

    # Pinch Click Sistemi
    is_clicked = False
    target_btn = None
    hovered_btn = None

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            p8 = hand_landmarks.landmark[8]
            p4 = hand_landmarks.landmark[4]

            cx8, cy8 = int(p8.x * w), int(p8.y * h)
            cx4, cy4 = int(p4.x * w), int(p4.y * h)

            distance = math.sqrt((cx8 - cx4) ** 2 + (cy8 - cy4) ** 2)

            # İmleç Rengi
            if distance > 45:
                cursor_color = (255, 255, 0)
            elif 18 <= distance <= 45:
                cursor_color = (0, 255, 255)
            else:
                cursor_color = (0, 0, 255)

            cv2.circle(image, (cx8, cy8), 10, cursor_color, -1)
            cv2.circle(image, (cx8, cy8), 12, (255, 255, 255), 1)

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Hover
            if active_scene != "Siparis_Ozet":

                if active_scene == "Ana Menu":

                    for btn in main_buttons:

                        if btn[0] < cx8 < btn[2] and btn[1] < cy8 < btn[3]:
                            target_btn = f"GO_SCENE_{btn[4]}"
                            hovered_btn = target_btn

                else:

                    for item in sub_menu_items[active_scene]:

                        if item[0] < cx8 < item[2] and item[1] < cy8 < item[3]:
                            target_btn = f"ADD_{item[4]}_{item[5]}"
                            hovered_btn = target_btn

                    if back_button[0] < cx8 < back_button[2] and back_button[1] < cy8 < back_button[3]:
                        target_btn = "BACK_TO_MAIN"
                        hovered_btn = target_btn

                if checkout_button[0] < cx8 < checkout_button[2] and checkout_button[1] < cy8 < checkout_button[3]:

                    if len(cart) > 0:
                        target_btn = "GO_CHECKOUT"
                        hovered_btn = target_btn

                for btn in delete_buttons:

                    if btn[0] < cx8 < btn[2] and btn[1] < cy8 < btn[3]:
                        target_btn = f"DELETE_ITEM_{btn[4]}"
                        hovered_btn = target_btn

            else:

                if cancel_btn[0] < cx8 < cancel_btn[2] and cancel_btn[1] < cy8 < cancel_btn[3]:
                    target_btn = "ORDER_CANCEL"
                    hovered_btn = target_btn

                if confirm_btn[0] < cx8 < confirm_btn[2] and confirm_btn[1] < cy8 < confirm_btn[3]:
                    target_btn = "ORDER_CONFIRM"
                    hovered_btn = target_btn

            # Tıklama
            if distance < 18:

                cv2.circle(image, (cx8, cy8), 15, (0, 255, 0), 3)

                if (time.time() - last_click_time) > click_cooldown:
                    is_clicked = True
                    last_click_time = time.time()

            # Buton İşlemleri
            if is_clicked and target_btn is not None:

                play_beep()

                if target_btn.startswith("GO_SCENE_"):
                    active_scene = target_btn.replace("GO_SCENE_", "")

                elif target_btn == "BACK_TO_MAIN":
                    active_scene = "Ana Menu"

                elif target_btn == "GO_CHECKOUT":
                    active_scene = "Siparis_Ozet"

                elif target_btn.startswith("ADD_"):

                    _, name, price = target_btn.split("_")

                    cart.append({
                        "name": name,
                        "price": int(price)
                    })

                    total_price += int(price)

                elif target_btn.startswith("DELETE_ITEM_"):

                    item_idx = int(target_btn.replace("DELETE_ITEM_", ""))

                    if item_idx < len(cart):
                        total_price -= cart[item_idx]['price']
                        cart.pop(item_idx)

                elif target_btn == "ORDER_CANCEL":

                    cart.clear()
                    total_price = 0
                    active_scene = "Ana Menu"

                elif target_btn == "ORDER_CONFIRM":

                    cart.clear()
                    total_price = 0
                    active_scene = "Ana Menu"

                    show_success_message = True
                    success_start_time = time.time()

                    print("Siparis basariyla mutfaga iletildi!")

    cv2.imshow('Touchless Menu - Profesyonel Otomasyon', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()