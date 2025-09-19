import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from main import custom_encrypt, custom_decrypt

def hide_message(img_path, message, out_path, key):
    message = custom_encrypt(message, key) + chr(0)
    binary_msg = ''.join([format(ord(c), '08b') for c in message])
    img = Image.open(img_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = list(img.getdata())
    if len(binary_msg) > len(pixels) * 3:
        raise ValueError("Image is too small to hold the message.")
    new_pixels = []
    idx = 0
    for pixel in pixels:
        r, g, b = pixel
        if idx < len(binary_msg): r = (r & ~1) | int(binary_msg[idx]); idx += 1
        if idx < len(binary_msg): g = (g & ~1) | int(binary_msg[idx]); idx += 1
        if idx < len(binary_msg): b = (b & ~1) | int(binary_msg[idx]); idx += 1
        new_pixels.append((r, g, b))
    img.putdata(new_pixels)
    img.save(out_path)
    messagebox.showinfo("Success", f"Message hidden in {out_path}")

def extract_message(img_path, key):
    img = Image.open(img_path)
    pixels = list(img.getdata())
    binary_msg = ""
    for pixel in pixels:
        for color in pixel:
            binary_msg += str(color & 1)
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    message = ""
    for char in chars:
        decoded = chr(int(char, 2))
        if decoded == chr(0): break
        message += decoded
    return custom_decrypt(message, key)

class StegoCryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StegoCrypt - Hidden Message Encryptor")
        self.img_path = ""
        tk.Label(root, text="Message:").grid(row=0, column=0, padx=5, pady=5)
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(root, text="Key:").grid(row=1, column=0, padx=5, pady=5)
        self.key_entry = tk.Entry(root, width=10)
        self.key_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.choose_btn = tk.Button(root, text="Choose Image", command=self.choose_image)
        self.choose_btn.grid(row=2, column=0, padx=5, pady=5)
        self.hide_btn = tk.Button(root, text="Hide Message", command=self.do_hide)
        self.hide_btn.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.extract_btn = tk.Button(root, text="Extract Message", command=self.do_extract)
        self.extract_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def choose_image(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.bmp")])
        if self.img_path:
            messagebox.showinfo("Image Selected", f"Selected: {self.img_path}")

    def do_hide(self):
        if not self.img_path:
            messagebox.showerror("Error", "No image selected.")
            return
        out_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        message = self.message_entry.get()
        try:
            key = int(self.key_entry.get())
            hide_message(self.img_path, message, out_path, key)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def do_extract(self):
        if not self.img_path:
            messagebox.showerror("Error", "No image selected.")
            return
        try:
            key = int(self.key_entry.get())
            msg = extract_message(self.img_path, key)
            messagebox.showinfo("Extracted Message", msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoCryptApp(root)
    root.mainloop()
