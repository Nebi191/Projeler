# E-Ticaret Django Projesi

Bu proje Django kullanılarak geliştirilmiş basit bir e-ticaret uygulamasıdır.

## Kurulum

1. Projeyi klonlayın veya ZIP dosyasını indirin.

```bash
git clone https://github.com/Nebi191/Projeler.git
cd Projeler


Sanal ortam oluşturun ve aktifleştirin:

python -m venv env
source env/bin/activate    # Windows için: env\Scripts\activate

Gerekli paketleri yükleyin:
pip install -r requirements.txt


Veritabanını oluşturun ve migrate edin:
python manage.py migrate

Örnek ürün verilerini yükleyin:
python manage.py loaddata products.json

Geliştirme sunucusunu başlatın:
python manage.py runserver
