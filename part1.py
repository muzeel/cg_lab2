import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def gray_1(img):
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            pixels[x, y] = (gray, gray, gray)
    return img
def gray_2(img):
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
            pixels[x, y] = (gray, gray, gray)
    return img

def diff(a, b):
    p1, p2 = a.load(), b.load()
    out = Image.new("RGB", a.size)
    po = out.load()
    for x in range(a.width):
        for y in range(a.height):
            r1, g1, b1 = p1[x, y]
            r2, g2, b2 = p2[x, y]
            po[x, y] = (abs(r1-r2), abs(g1-g2), abs(b1-b2))
    return out



def show_hist(ax, canvas, img):
    ax.clear()
    h = img.histogram()
    ax.plot(h[0:256], 'r', lw=0.8)
    ax.plot(h[256:512], 'g', lw=0.8)
    ax.plot(h[512:768], 'b', lw=0.8)
    ax.set_title("Гистограмма", fontsize=9)
    canvas.draw()

def open_file():
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
    if not path:
        return

    orig = Image.open(path).convert("RGB")
    g1 = gray_1(orig.copy())
    g2 = gray_2(orig.copy())
    d  = diff(g1, g2)
    imgs = [orig, g1, g2, d]

    photos.clear()
    for lbl, img in zip(labels, imgs):
        p = img.copy()
        p.thumbnail((280, 280))
        ph = ImageTk.PhotoImage(p)
        photos.append(ph)
        lbl.config(image=ph)

    for ax, canvas, img in zip(axes, canvases, imgs):
        show_hist(ax, canvas, img)

    root.title(path.replace("\\", "/").split("/")[-1])

root = tk.Tk()
names = ["Оригинал", "Серый1", "Серый2", "Разность"]
labels, axes, canvases, photos = [], [], [], []

for i, name in enumerate(names):
    tk.Label(root, text=name, font=("Arial", 11, "bold")).grid(row=0, column=i)

    lbl = tk.Label(root)
    lbl.grid(row=1, column=i, padx=5, pady=5)
    labels.append(lbl)

    fig = Figure(figsize=(3, 2.5))
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=2, column=i, padx=5)
    axes.append(ax)
    canvases.append(canvas)


tk.Button(root, text="Открыть картинку", command=open_file)\
    .grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")

root.mainloop()