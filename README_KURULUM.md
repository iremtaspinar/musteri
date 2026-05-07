# Müşteri Takip Web Başlangıç Paketi

Bu paket Tkinter sürümünden web sisteme geçiş için hazırlanmış başlangıç altyapısıdır.

## Özellikler
- Django web uygulaması
- PostgreSQL hazır bağlantı
- Bulut dosya saklama için S3/Supabase Storage uyumlu yapı
- Müşteri, işler, işlem adımları, randevu
- Gelen/Giden Evrak modülü
- Gider belge yükleme
- Kesilen faturalar modülü
- Kullanıcı işlem logları
- Excel export

## İlk test kurulumu
```powershell
cd musteri_takip_web_baslangic
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py init_default_processes
python manage.py runserver
```

Aç:
```text
http://127.0.0.1:8000/
```

## Canlı mimari
```text
Web uygulaması
↓
PostgreSQL
↓
Private bulut belge depolama
↓
Günlük yedekleme
```

Canlıya geçerken `DATABASE_URL` ve storage bilgileri `.env` içine girilecek.
