import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


class HSVApp:
    def __init__(self, root):
        self.root = root
        root.title("BGR -> HSV -> RGB")

        self.img_bgr = None
        self.hsv_base = None
        self.result_bgr = None

        tk.Button(root, text="Открыть изображение",
                  command=self.open_image).pack(fill="x")
        tk.Button(root, text="Сохранить результат",
                  command=self.save_image).pack(fill="x")

        self.dh = self._make_slider("Оттенок (H)", -180, 180)
        self.ds = self._make_slider("Насыщенность (S)", -255, 255)
        self.dv = self._make_slider("Яркость (V)", -255, 255)

        self.label = tk.Label(root)
        self.label.pack()

    def _make_slider(self, text, lo, hi):
        frame = tk.Frame(self.root)
        frame.pack(fill="x")
        tk.Label(frame, text=text, width=18, anchor="w").pack(side="left")
        var = tk.IntVar(value=0)
        scale = tk.Scale(frame, from_=lo, to=hi, orient="horizontal",
                         variable=var, command=lambda _: self.update())
        scale.pack(side="right", fill="x", expand=True)
        return var

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return
        self.img_bgr = cv2.imread(path, cv2.IMREAD_COLOR)
        self.hsv_base = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2HSV)
        self.update()

    def hsv_to_rgb(self,h, s, v):
        hf = (h * 2.0) % 360.0
        sf = s / 255.0
        vf = v / 255.0
        c = vf * sf
        x = c * (1.0 - abs((hf / 60.0) % 2.0 - 1.0))
        m = vf - c

        if hf < 60:
            rp, gp, bp = c, x, 0.0
        elif hf < 120:
            rp, gp, bp = x, c, 0.0
        elif hf < 180:
            rp, gp, bp = 0.0, c, x
        elif hf < 240:
            rp, gp, bp = 0.0, x, c
        elif hf < 300:
            rp, gp, bp = x, 0.0, c
        else:
            rp, gp, bp = c, 0.0, x

        return (int(round((rp + m) * 255)),
                int(round((gp + m) * 255)),
                int(round((bp + m) * 255)))

    def update(self):
        if self.hsv_base is None:
            return
        dh, ds, dv = self.dh.get(), self.ds.get(), self.dv.get()
        h_img, w_img = self.hsv_base.shape[:2]

        img = Image.new("RGB", (w_img, h_img))
        po = img.load()
        for y in range(h_img):
            for x in range(w_img):
                h = int(self.hsv_base[y, x, 0])
                s = int(self.hsv_base[y, x, 1])
                v = int(self.hsv_base[y, x, 2])

                h = (h + dh) % 180
                s = max(0, min(255, s + ds))
                v = max(0, min(255, v + dv))

                po[x, y] = self.hsv_to_rgb(h, s, v)

        self.result_bgr = np.array(img)[:, :, ::-1].copy()

        preview = img.copy()
        preview.thumbnail((700, 500))
        self.tk_img = ImageTk.PhotoImage(preview)
        self.label.config(image=self.tk_img)

    def save_image(self):
        if self.result_bgr is None:
            messagebox.showwarning("Внимание", "Сначала откройте изображение")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            cv2.imwrite(path, self.result_bgr)
            messagebox.showinfo("Готово", f"Сохранено: {path}")


if __name__ == "__main__":
    root = tk.Tk()
    HSVApp(root)
    root.mainloop()