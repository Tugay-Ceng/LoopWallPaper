# LoopWallPaper v1

LoopWallPaper, belirlediğiniz bir klasördeki görselleri okuyarak masaüstü arka planınızı kendi belirlediğiniz zaman aralıklarıyla (saniye bazında) otomatik olarak değiştiren, arka planda çalışan bir Windows masaüstü uygulamasıdır.

## Özellikler
* **Asenkron Zamanlayıcı Motor:** Sistemi (CPU/RAM) yormayan, Windows API (`ctypes`) tabanlı hafif arka plan döngüsü.
* **Modern Arayüz (GUI):** CustomTkinter ile tasarlanmış karanlık tema kontrol paneli.
* **System Tray (Görev Çubuğu) Desteği:** Ana pencere kapatıldığında arka planda çalışmaya devam eder ve sağ alt köşedeki tepsi ikonundan (pystray) yönetilebilir.
* **Kalıcı Bellek Yönetimi:** Ayarlar ve son değişim zamanı yapılandırma dosyalarında saklanır; program yeniden başlatılsa bile döngü kaldığı yerden devam eder.

## Gereksinimler ve Kurulum
Projeyi çalıştırmak için sisteminizde Python yüklü olmalıdır.

1. Depoyu klonlayın:
   `git clone https://github.com/KullaniciAdin/LoopWallPaper.git`
2. Gerekli kütüphaneleri yükleyin:
   `pip install customtkinter pystray pillow`
3. Siyah konsol ekranı olmadan doğrudan arayüzle başlatmak için `main.pyw` dosyasına çift tıklayın.