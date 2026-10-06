import customtkinter as ctk
from tkinter import filedialog
from config_manager import ConfigManager
import pystray
from PIL import Image, ImageDraw
import threading

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LoopWallPaper v1")
        self.geometry("450x300")
        
        self.config_manager = ConfigManager()
        self.settings = self.config_manager.load_settings()

        # X (Kapat) tuşunun davranışını değiştir: Kapatma, gizle!
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

        # Klasör Seçimi Arayüzü
        current_dir = self.settings.get("wallpaper_directory", "Seçilmedi")
        self.lbl_folder = ctk.CTkLabel(self, text=f"Mevcut Klasör: {current_dir}", wraplength=400)
        self.lbl_folder.pack(pady=(20, 10))

        self.btn_folder = ctk.CTkButton(self, text="Klasör Seç", command=self.select_folder)
        self.btn_folder.pack(pady=10)

        # Süre Seçimi Arayüzü
        self.lbl_interval = ctk.CTkLabel(self, text="Değişim Süresi (Saniye):")
        self.lbl_interval.pack(pady=(20, 5))

        self.entry_interval = ctk.CTkEntry(self, justify="center")
        self.entry_interval.insert(0, str(self.settings.get("interval_seconds", 3600)))
        self.entry_interval.pack(pady=5)

        # Kaydet Butonu
        self.btn_save = ctk.CTkButton(self, text="Ayarları Kaydet", fg_color="green", hover_color="darkgreen", command=self.save_settings)
        self.btn_save.pack(pady=20)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.settings["wallpaper_directory"] = folder_path
            self.lbl_folder.configure(text=f"Mevcut Klasör: {folder_path}")

    def save_settings(self):
        try:
            new_interval = int(self.entry_interval.get())
            current_settings = self.config_manager.load_settings() 
            
            current_settings["interval_seconds"] = new_interval
            current_settings["wallpaper_directory"] = self.settings.get("wallpaper_directory", "")
            
            self.config_manager.save_settings(current_settings)
            self.settings = current_settings 
            
            self.btn_save.configure(text="Kaydedildi!", fg_color="gray")
            self.after(2000, lambda: self.btn_save.configure(text="Ayarları Kaydet", fg_color="green"))
        except ValueError:
            print("Hata: Lütfen süreye sadece rakam girin!")

    # --- SYSTEM TRAY (GÖREV ÇUBUĞU) İŞLEMLERİ ---

    def create_tray_icon_image(self):
        # Şimdilik dışarıdan .ico yüklemek yerine kodla basit bir ikon (Mavi üzerine sarı LW) çizdiriyoruz
        image = Image.new('RGB', (64, 64), color=(30, 30, 30))
        d = ImageDraw.Draw(image)
        d.text((15, 20), "LW", fill=(0, 150, 255))
        return image

    def hide_window(self):
        self.withdraw() # Ana pencereyi ekrandan sil (ama arkada çalışmaya devam etsin)
        
        # Sağ alt köşe menüsünü oluştur
        menu = pystray.Menu(
            pystray.MenuItem("Arayüzü Göster", self.show_window),
            pystray.MenuItem("Tamamen Kapat", self.quit_window)
        )
        
        image = self.create_tray_icon_image()
        self.tray_icon = pystray.Icon("LoopWallPaper", image, "LoopWallPaper v1", menu)
        
        # Arayüz donmasın diye Tray ikonunu ayrı bir thread (iş parçacığı) içinde başlat
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon, item):
        self.tray_icon.stop() # Tray ikonunu yok et
        self.after(0, self.deiconify) # CustomTkinter penceresini tekrar ekrana getir

    def quit_window(self, icon, item):
        self.tray_icon.stop() 
        self.quit() # Programı belleği temizleyerek kapat