import math

# Ввод исходных данных
print("--- Ввод коэффициентов ---")
a1 = float(input("a1 = "))
b1 = float(input("b1 = "))
a2 = float(input("a2 = "))
b2 = float(input("b2 = "))
a3 = float(input("a3 = "))
b3 = float(input("b3 = "))

print("\n--- Ввод диапазона ---")
x0 = float(input("x0 (старт) = "))
xk = float(input("xk (конец) = "))
dx = float(input("dx (шаг)  = "))

# Вычисление векторов X и Y
x_vec, y_vec = [], []
current_x = x0
while current_x <= xk + (dx * 0.01):
    x_vec.append(current_x)
    y = (a1 * math.sin(b1 * current_x) + 
         a2 * math.sin(b2 * current_x) + 
         a3 * math.sin(b3 * current_x))
    y_vec.append(y)
    current_x += dx

# Вывод таблицы в консоль
print("\n+------------+------------+")
print("|     X      |     Y      |")
print("+------------+------------+")
for x, y in zip(x_vec, y_vec):
    print(f"| {x:10.4f} | {y:10.4f} |")
print("+------------+------------+")

# Ручное создание несжатого BMP
print("\nГенерация графика...")
W, H = 800, 600  # Размеры картинки в пикселях
img = [255] * (W * H * 3) # Белый холст в формате RGB (все байты = 255)

# Масштабирование под размер экрана 800x600
min_x, max_x = min(x_vec), max(x_vec)
min_y, max_y = min(y_vec), max(y_vec)
span_x = (max_x - min_x) if max_x != min_x else 1
span_y = (max_y - min_y) if max_y != min_y else 1

# Функция рисования пикселя
def set_pixel(x, y):
    if 0 <= x < W and 0 <= y < H:
        idx = (y * W + x) * 3
        img[idx] = 255   # Синий цвет (B)
        img[idx+1] = 0   # Зелёный цвет (G)
        img[idx+2] = 0   # Красный цвет (R) 

# Функция рисования сплошной линии (Алгоритм Брезенхема)
def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while True:
        set_pixel(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# Переводим координаты векторов в пиксели экрана
pixels = []
for x, y in zip(x_vec, y_vec):
    px = int((x - min_x) / span_x * (W - 60)) + 30
    py = int((y - min_y) / span_y * (H - 60)) + 30
    pixels.append((px, py))

# Соединяем точки линиями, чтобы график не ломался
for i in range(len(pixels) - 1):
    draw_line(pixels[i][0], pixels[i][1], pixels[i+1][0], pixels[i+1][1])

# Запись структуры BMP-файла
row_size = (W * 3 + 3) & ~3
pixel_data_size = row_size * H
file_size = 54 + pixel_data_size

header = bytearray(54) # Пустая заготовка под заголовок из 54 байт.
header[0:2] = b'BM' # Тип файла BMP BitMap
header[2:6] = file_size.to_bytes(4, 'little') # Размер файла целиком
header[10:14] = (54).to_bytes(4, 'little')
header[14:18] = (40).to_bytes(4, 'little')
header[18:22] = W.to_bytes(4, 'little')
header[22:26] = H.to_bytes(4, 'little')
header[26:28] = (1).to_bytes(2, 'little')
header[28:30] = (24).to_bytes(2, 'little') # Указываем на отсутствие сжатия (3 байта на пиксель)
header[34:38] = pixel_data_size.to_bytes(4, 'little')

with open("graph.bmp", "wb") as f:
    f.write(header) # Сначала пишем 54 байта заголовка
    for r in range(H):
        row = bytearray(row_size)
        for c in range(W):
            idx = (r * W + c) * 3
            row[c*3] = img[idx]
            row[c*3+1] = img[idx+1]
            row[c*3+2] = img[idx+2]
        f.write(row) # Построчно выгружаем пиксели

print("График успешно сохранен в файл: graph.bmp")

# Автоматическое открытие картинки на экране
import os
import platform
try:
    if platform.system() == "Windows":
        os.startfile("graph.bmp")
except Exception:
    print("Не удалось открыть файл автоматически, но он сохранен в папке проекта.")
