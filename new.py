import cv2
import numpy as np

# Загрузка фонового изображения
background_image = cv2.imread('background.png')

# Загрузка логотипа
logo_image = cv2.imread('logo.png')

# Загрузка видеофайла
video_capture = cv2.VideoCapture('video.mp4')

# Установка размера видео
video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Установка размера круглого видео
circle_video_size = 300

# Создание окна для вывода
cv2.namedWindow('Output', cv2.WINDOW_NORMAL)

while True:
    # Чтение кадра из видеофайла
    ret, frame = video_capture.read()
    
    if not ret:
        break

    # Обрезка видео до круга
    circle_frame = np.zeros((circle_video_size, circle_video_size, 3), dtype=np.uint8)
    center_x = circle_video_size // 2
    center_y = circle_video_size // 2
    radius = circle_video_size // 2
    for y in range(circle_video_size):
        for x in range(circle_video_size):
            dx = x - center_x
            dy = y - center_y
            if dx * dx + dy * dy <= radius * radius:
                circle_frame[y, x] = frame[y, x]

    # Уменьшение размера круглого видео
    resized_circle_frame = cv2.resize(circle_frame, (circle_video_size // 2, circle_video_size // 2))

    # Вывод названия
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = 'Название мероприятия'
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = (background_image.shape[1] - text_size[0]) // 2
    text_y = 50
    cv2.putText(background_image, text, (text_x, text_y), font, 1, (255, 255, 255), 2)

    # Вывод логотипа
    logo_x = 10
    logo_y = 10
    background_image[logo_y:logo_y + logo_image.shape[0], logo_x:logo_x + logo_image.shape[1]] = logo_image

    # Вывод круглого видео
    video_x = (background_image.shape[1] - resized_circle_frame.shape[1]) // 2
    video_y = (background_image.shape[0] - resized_circle_frame.shape[0]) // 2
    background_image[video_y:video_y + resized_circle_frame.shape[0], video_x:video_x + resized_circle_frame.shape[1]] = resized_circle_frame

    # Вывод результата
    cv2.imshow('Output', background_image)

    # Ожидание нажатия клавиши
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
video_capture.release()
cv2.destroyAllWindows()
