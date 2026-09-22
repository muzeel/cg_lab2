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

    def update(self):
        if self.hsv_base is None:
            return
        h, s, v = cv2.split(self.hsv_base.astype(np.int16))
        h = (h + self.dh.get()) % 180
        s = np.clip(s + self.ds.get(), 0, 255)
        v = np.clip(v + self.dv.get(), 0, 255)
        hsv_mod = cv2.merge([h, s, v]).astype(np.uint8)
        self.result_bgr = cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR)

        rgb = cv2.cvtColor(self.result_bgr, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        img.thumbnail((700, 500))
        self.tk_img = ImageTk.PhotoImage(img)
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