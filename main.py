import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.Application.app import create_app

def start_backend():
    print("Backend başlatılıyor...")
    app = create_app()  # 🟢 Flask uygulamasını burada başlat!
    app.run(debug=True, host="127.0.0.1", port=5000)

def initialize_services():
    print("Gerekli servisler kontrol ediliyor...")

def main():
    print("Ana servis başlatılıyor...")
    initialize_services()
    start_backend()
    
if __name__ == "__main__":
    main()

