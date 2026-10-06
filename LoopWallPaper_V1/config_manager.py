import json
import os

class ConfigManager:
    def __init__(self, config_file="settings.json"):
        self.config_file = config_file

    def load_settings(self):
        # Dosya yoksa varsayılan değerleri döndür ve dosyayı oluştur
        if not os.path.exists(self.config_file):
            default_settings = {
                "wallpaper_directory": "", # Buraya resimlerin olduğu klasör yolunu gireceksin
                "interval_seconds": 3600,  # Örnek: 1 saat = 3600 saniye
                "last_change_time": 0.0,
                "current_image_index": 0
            }
            self.save_settings(default_settings)
            return default_settings

        # Dosya varsa oku
        with open(self.config_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_settings(self, data):
        # Veriyi JSON olarak dosyaya yaz
        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)