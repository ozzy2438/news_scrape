# 🤖 Selenium Web Scraper

## 📋 Genel Bakış
Bu proje, modern web sitelerinden veri çekme işlemlerini otomatikleştirmek için Selenium WebDriver ve Python kullanılarak geliştirilmiş güçlü bir web scraping çözümüdür. Dinamik web sayfalarından veri toplama, CSV ve PDF formatlarında raporlama özellikleri sunar.

## ✨ Özellikler
- 🚀 Selenium WebDriver ile otomatik web gezinme
- ⚙️ YAML dosyası ile yapılandırılabilir parametreler
- 🎯 CSS selektörleri ile dinamik veri çekme
- 🧹 Gelişmiş veri temizleme ve işleme yetenekleri
- 📊 CSV ve PDF formatlarında veri dışa aktarma
- 📝 Kapsamlı hata yönetimi ve loglama
- 🕶️ Headless (arka planda) çalışma desteği
- 🔄 Otomatik sayfa geçişleri ve dinamik içerik yükleme

## 🛠️ Teknolojiler
- Python 3.9+
- Selenium WebDriver
- Pandas
- ReportLab
- PyYAML
- Chrome/Chromium WebDriver

## 🚀 Kurulum

### 📋 Ön Koşullar
- Python 3.9 veya daha yeni bir sürüm
- Google Chrome veya Chromium tarayıcı
- Chrome versiyonunuza uygun ChromeDriver

### ⚡ Hızlı Başlangıç

1. Repository'yi klonlayın:
```bash
git clone https://github.com/yourusername/selenium_web_scraper.git
cd selenium_web_scraper
```

2. Sanal ortam oluşturun (önerilen):
```bash
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## 🔧 Yapılandırma
`config/config.yaml` dosyasını düzenleyerek scraper davranışını özelleştirebilirsiniz:

```yaml
# Tarayıcı Ayarları
headless: true
timeout: 15

# Çıktı Ayarları
output_dir: output

# Scraping Ayarları
max_pages: 10
wait_time: 3
```

## 💻 Kullanım

### 🌟 Temel Kullanım
```python
from src.scraper import WebScraper

# Scraper'ı başlat
scraper = WebScraper()

# Scraping işlemini çalıştır
scraper.run_scraper(
    url="https://example.com",
    output_name="output/results.csv"
)
```

### 🔥 Gelişmiş Kullanım
```python
# Özel konfigürasyon dosyası ile başlat
scraper = WebScraper(config_path='custom_config.yaml')

# Özel parametrelerle çalıştır
scraper.run_scraper(
    url="https://example.com",
    output_name="output/detailed_results.csv",
    max_pages=20
)
```

## 📁 Proje Yapısı
```
selenium_web_scraper/
├── src/
│   ├── scraper.py          # Ana scraping motoru
│   └── example.py          # Örnek kullanımlar
├── config/
│   ├── config.py           # Konfigürasyon işleyici
│   └── config.yaml         # Ayar dosyası
├── utils/
│   ├── data_processor.py   # Veri işleme araçları
│   └── pdf_generator.py    # PDF rapor oluşturucu
├── output/                 # Çıktı dosyaları
├── Dockerfile             # Docker yapılandırması
└── requirements.txt       # Python bağımlılıkları
```

## 🐳 Docker ile Kullanım
Docker ile çalıştırmak için:

```bash
# Docker imajını oluştur
docker build -t web-scraper .

# Containeri çalıştır
docker run -v $(pwd)/output:/app/output web-scraper
```

## 🚨 Hata Yönetimi
Scraper şu durumları otomatik olarak yönetir:
- 🌐 Bağlantı hataları
- ⏱️ Zaman aşımı istisnaları
- 🎯 Geçersiz selektörler
- 📊 Veri işleme hataları
- 📁 Dosya I/O hataları

## 📊 Veri İşleme Özellikleri
`data_processor.py` modülü şunları içerir:
- 📝 Metin temizleme ve normalleştirme
- 🔢 Sayısal değer çıkarma
- 📈 DataFrame oluşturma ve manipülasyon
- 🔄 Özel veri dönüşümleri

## 📋 Lisans
Bu proje MIT Lisansı altında lisanslanmıştır - Detaylar için LICENSE dosyasına bakın.

## 🤝 Katkıda Bulunma
1. Repository'yi forklayın
2. Yeni bir feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'inizi push edin
5. Pull Request oluşturun

## 💬 Destek
- 📫 Bug raporları için Issues bölümünü kullanın
- 💡 Öneriler için Pull Request gönderin
- ❓ Sorularınız için Discussions bölümünü kullanın

## 👏 Teşekkürler
- 🌟 Selenium ekibine
- 🐍 Python topluluğuna
- 🤝 Tüm katkıda bulunanlara

---
Geliştirici: [Your Name](https://github.com/yourusername)
