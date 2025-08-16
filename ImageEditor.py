import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Resim Kırpma Aracı")
        self.root.geometry("900x700")

        
        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.tk_image = None
        
        
        self.crop_rect = None
        self.start_x = None
        self.start_y = None
        self.crop_coords = None

        
        self.create_widgets()

    def create_widgets(self):
        
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(control_frame, text="Resim Aç", command=self.open_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Kırp ve Kaydet", command=self.save_cropped_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Sıfırla", command=self.reset).pack(side=tk.LEFT, padx=5)
        
       
        ttk.Label(control_frame, text="Oran:").pack(side=tk.LEFT, padx=(20, 5))
        self.aspect_ratio = tk.StringVar(value="Serbest")
        ratio_options = ["Serbest", "Kare (1:1)", "Hikaye (9:16)", "Manzara (16:9)", "1080x1920"]
        self.ratio_combobox = ttk.Combobox(control_frame, textvariable=self.aspect_ratio, values=ratio_options, state="readonly")
        self.ratio_combobox.pack(side=tk.LEFT, padx=5)

        
        self.canvas = tk.Canvas(self.root, bg="gray", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

       
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def open_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png *.bmp *.gif"), ("Tüm Dosyalar", "*.*")]
        )
        if not self.image_path:
            return

        self.reset()
        self.original_image = Image.open(self.image_path)
        
        
        max_width = 800
        max_height = 600
        self.original_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        self.display_image = self.original_image.copy() 
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        
        
        self.canvas.config(width=self.display_image.width, height=self.display_image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def on_mouse_down(self, event):
        if not self.tk_image: return
        
        
        self.start_x = event.x
        self.start_y = event.y

        
        if self.crop_rect:
            self.canvas.delete(self.crop_rect)
        self.crop_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline="red", width=2, dash=(4, 4)
        )

    def on_mouse_drag(self, event):
        if not self.crop_rect: return

        cur_x, cur_y = event.x, event.y
        width = cur_x - self.start_x
        height = cur_y - self.start_y
        
        
        ratio_str = self.aspect_ratio.get()
        if ratio_str != "Serbest":
            if ratio_str == "Kare (1:1)":
                ratio = 1.0
            elif ratio_str == "Hikaye (9:16)":
                ratio = 16.0 / 9.0
            elif ratio_str == "Manzara (16:9)":
                ratio = 9.0 / 16.0
            elif ratio_str == "1080x1920":
                ratio = 1920.0 / 1080.0
            
            
            height = width * ratio
            cur_y = self.start_y + height
            
        
        self.canvas.coords(self.crop_rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_mouse_up(self, event):
        if not self.crop_rect: return
        self.crop_coords = self.canvas.coords(self.crop_rect)

    def save_cropped_image(self):
        if not self.crop_coords or not self.image_path:
            messagebox.showwarning("Uyarı", "Lütfen önce bir resim açın ve bir alan seçin.")
            return

        
        original_opened = Image.open(self.image_path)
        
        
        scale_x = original_opened.width / self.display_image.width
        scale_y = original_opened.height / self.display_image.height

       
        x1 = self.crop_coords[0] * scale_x
        y1 = self.crop_coords[1] * scale_y
        x2 = self.crop_coords[2] * scale_x
        y2 = self.crop_coords[3] * scale_y
        
        final_coords = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

        cropped_image = original_opened.crop(final_coords)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG dosyası", "*.png"), ("JPEG dosyası", "*.jpg"), ("Tüm Dosyalar", "*.*")],
            initialfile="kirpilmis_resim.png"
        )

        if save_path:
            cropped_image.save(save_path)
            messagebox.showinfo("Başarılı", f"Resim başarıyla '{save_path}' konumuna kaydedildi.")

    def reset(self):
        self.canvas.delete("all")
        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.tk_image = None
        self.crop_rect = None
        self.crop_coords = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()