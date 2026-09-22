import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# Диалоговое окно выбора файла
root = Tk()
root.withdraw()
root.attributes('-topmost', True)

file_path = filedialog.askopenfilename(
    title='Выберите изображение',
    filetypes=[
        ('Изображения', '*.jpg *.jpeg *.png *.bmp *.tif *.tiff *.webp'),
        ('Все файлы', '*.*')
    ]
)
root.destroy()

if not file_path:
    print('Файл не выбран. Выход.')
    raise SystemExit

# Чтение файла с поддержкой кириллицы в пути
try:
    img_array = np.fromfile(file_path, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
except Exception as e:
    raise FileNotFoundError(f"Не удалось прочитать файл: {file_path}\n{e}")

if img is None:
    raise FileNotFoundError(f"Не удалось декодировать изображение: {file_path}")

# OpenCV читает в BGR
b, g, r = cv2.split(img)

# Сбор трёх цветных изображений (только один канал ненулевой)
zeros = np.zeros_like(b)
img_r = cv2.merge([zeros, zeros, r])
img_g = cv2.merge([zeros, g, zeros])
img_b = cv2.merge([b, zeros, zeros])

# Создание фигуры с сеткой 2×4 (для изображений и гистограмм)
fig, axes = plt.subplots(2, 4, figsize=(18, 8))

# Верхний ряд: изображения
axes[0, 0].imshow(cv2.cvtColor(img,   cv2.COLOR_BGR2RGB))
axes[0, 0].set_title('Исходное изображение')
axes[0, 0].axis('off')

axes[0, 1].imshow(cv2.cvtColor(img_r, cv2.COLOR_BGR2RGB))
axes[0, 1].set_title('Канал R')
axes[0, 1].axis('off')

axes[0, 2].imshow(cv2.cvtColor(img_g, cv2.COLOR_BGR2RGB))
axes[0, 2].set_title('Канал G')
axes[0, 2].axis('off')

axes[0, 3].imshow(cv2.cvtColor(img_b, cv2.COLOR_BGR2RGB))
axes[0, 3].set_title('Канал B')
axes[0, 3].axis('off')

# Нижний ряд: гистограммы
axes[1, 0].hist(r.ravel(), bins=256, range=[0, 256], color='red')
axes[1, 0].set_title('Гистограмма канала R')
axes[1, 0].set_xlabel('Интенсивность')
axes[1, 0].set_ylabel('Количество пикселей')

axes[1, 1].hist(g.ravel(), bins=256, range=[0, 256], color='green')
axes[1, 1].set_title('Гистограмма канала G')
axes[1, 1].set_xlabel('Интенсивность')
axes[1, 1].set_ylabel('Количество пикселей')

axes[1, 2].hist(b.ravel(), bins=256, range=[0, 256], color='blue')
axes[1, 2].set_title('Гистограмма канала B')
axes[1, 2].set_xlabel('Интенсивность')
axes[1, 2].set_ylabel('Количество пикселей')

# 4-я ячейка нижнего ряда не используется - прячем
axes[1, 3].axis('off')

plt.tight_layout()
plt.show()