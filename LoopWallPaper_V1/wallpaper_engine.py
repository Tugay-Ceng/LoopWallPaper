import os
import ctypes

class WallpaperEngine:
    def __init__(self, directory):
        self.directory = directory

    def get_images(self):
        # Klasör yoksa boş liste dön
        if not os.path.exists(self.directory):
            return []
        
        valid_extensions = ('.png', '.jpg', '.jpeg')
        # Sadece resim dosyalarını filtrele
        images = [f for f in os.listdir(self.directory) if f.lower().endswith(valid_extensions)]
        return images

    def set_wallpaper(self, image_name):
        image_path = os.path.join(self.directory, image_name)
        # Windows için dosya yolunu düzelt (Ters eğik çizgiler vb.)
        image_path = os.path.normpath(image_path)
        
        # Windows arka plan değiştirme API çağrısı
        # 20 = SPI_SETDESKWALLPAPER, 3 = Ayarları kaydet ve sistemi güncelle
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        print(f"Duvar kağıdı değiştirildi: {image_name}")