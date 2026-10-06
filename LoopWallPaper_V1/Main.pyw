import threading
from scheduler import Scheduler
from gui import App

def run_background_task():
    # Arka plan motorunu başlatır
    app_scheduler = Scheduler()
    app_scheduler.run()

if __name__ == "__main__":
    # daemon=True parametresi, arayüz çarpıdan kapatıldığında 
    # arka plan işleminin de otomatik sonlanmasını sağlar.
    bg_thread = threading.Thread(target=run_background_task, daemon=True)
    bg_thread.start()

    # Arayüzü başlat
    gui_app = App()
    gui_app.mainloop()