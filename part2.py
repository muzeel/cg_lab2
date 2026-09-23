import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from PIL import Image
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
    #img_array = np.fromfile(file_path, dtype=np.uint8)
    #img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    img = Image.open(file_path).convert("RGB")
except Exception as e:
    raise FileNotFoundError(f"Не удалось прочитать файл: {file_path}\n{e}")

if img is None:
    raise FileNotFoundError(f"Не удалось декодировать изображение: {file_path}")

pixels = img.load()
img_np = np.array(img)


out_r = Image.new("RGB", img.size)
out_g = Image.new("RGB", img.size)
out_b = Image.new("RGB", img.size)

r_vals = []
g_vals = []
b_vals = []


pixels_r = out_r.load()
pixels_g = out_g.load()
pixels_b = out_b.load()
width, height = img.size
for x in range(width):
    for y in range(height):
        r, g, b = pixels[x, y]
        pixels_r[x, y] = (r, 0, 0)
        pixels_g[x, y] = (0, g, 0)
        pixels_b[x, y] = (0, 0, b)
        r_vals.append(r)
        g_vals.append(g)
        b_vals.append(b)

# Создание фигуры с сеткой 2×4 (для изображений и гистограмм)
fig, axes = plt.subplots(2, 4, figsize=(18, 8))

# Верхний ряд: изображения
axes[0, 0].imshow(img)
axes[0, 0].set_title('Исходное изображение')
axes[0, 0].axis('off')

axes[0, 1].imshow(out_r)
axes[0, 1].set_title('Канал R')
axes[0, 1].axis('off')

axes[0, 2].imshow(out_g)
axes[0, 2].set_title('Канал G')
axes[0, 2].axis('off')

axes[0, 3].imshow(out_b)
axes[0, 3].set_title('Канал B')
axes[0, 3].axis('off')

# Нижний ряд: гистограммы
axes[1, 0].hist(r_vals, bins=256, range=[0, 256], color='red')
axes[1, 0].set_title('Гистограмма канала R')
axes[1, 0].set_xlabel('Интенсивность')
axes[1, 0].set_ylabel('Количество пикселей')

axes[1, 1].hist(g_vals, bins=256, range=[0, 256], color='green')
axes[1, 1].set_title('Гистограмма канала G')
axes[1, 1].set_xlabel('Интенсивность')
axes[1, 1].set_ylabel('Количество пикселей')

axes[1, 2].hist(b_vals, bins=256, range=[0, 256], color='blue')
axes[1, 2].set_title('Гистограмма канала B')
axes[1, 2].set_xlabel('Интенсивность')
axes[1, 2].set_ylabel('Количество пикселей')

# 4-я ячейка нижнего ряда не используется - прячем
axes[1, 3].axis('off')

plt.tight_layout()
plt.show()
