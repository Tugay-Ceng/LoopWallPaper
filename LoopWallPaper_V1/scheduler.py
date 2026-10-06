import time
from config_manager import ConfigManager
from wallpaper_engine import WallpaperEngine

class Scheduler:
    def __init__(self):
        self.config_manager = ConfigManager()

    def run(self):
        print("Zamanlayıcı başlatıldı. Arka planda çalışıyor...")
        
        while True:
            settings = self.config_manager.load_settings()
            wall_dir = settings.get("wallpaper_directory", "")
            
            # Eğer klasör yolu boşsa bekle
            if not wall_dir:
                print("Ayarlarda klasör yolu yok. Lütfen settings.json'ı düzenleyin.")
                time.sleep(60)
                continue

            engine = WallpaperEngine(wall_dir)
            images = engine.get_images()

            if not images:
                print("Belirtilen klasörde resim bulunamadı.")
                time.sleep(60)
                continue

            current_time = time.time()
            last_time = settings.get("last_change_time", 0.0)
            interval = settings.get("interval_seconds", 3600)

            # Zaman kontrolü: Geçerli zaman - Son değişim zamanı >= Bekleme süresi
            if (current_time - last_time) >= interval:
                current_index = settings.get("current_image_index", 0)
                
                # Eğer index resim sayısını aştıysa başa dön
                if current_index >= len(images):
                    current_index = 0

                selected_image = images[current_index]
                
                # Resmi değiştir
                engine.set_wallpaper(selected_image)

                # Ayarları güncelle (yeni zamanı ve bir sonraki resim sırasını kaydet)
                settings["last_change_time"] = current_time
                settings["current_image_index"] = current_index + 1
                self.config_manager.save_settings(settings)

            # İşlemciyi (CPU) yormamak için döngüyü 1 dakika uyut. 
            # Arka plan uygulaması sürekli saniyeleri saymamalıdır.
            time.sleep(5)