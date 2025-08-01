# Amerika Pazarı Satış Analizi Dashboard

Bu Streamlit uygulaması, Amerika pazarlarındaki satış verilerini detaylı olarak analiz eder ve görselleştirir.

## Özellikler

- 🇺🇸 Amerika pazarlarındaki satış performansı analizi
- 🏆 En çok satan ürünlerin belirlenmesi
- 🏪 Pazar bazında performans karşılaştırması
- 📂 Kategori bazında satış analizi
- 📊 İnteraktif görselleştirmeler
- 📋 Detaylı yönetim raporları

## Analiz Edilen Pazarlar

- AmazonUS
- EtsyDecoroHomeArt
- EtsyIslamicDecorGifts
- EtsyIwa
- EtsyMapwoodA
- EtsyShukran
- ShopifyCfwEn
- ShopifyIslamicEn
- ShopifyShkuranEn
- ShopifyUppEn
- Walmart

## Nasıl Kullanılır

### Yerel Çalıştırma

1. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:
```bash
streamlit run amerika_analiz_app.py
```

### Streamlit Cloud'da Çalıştırma

1. Bu repository'yi fork edin
2. Streamlit Cloud'da yeni bir uygulama oluşturun
3. GitHub repository'nizi bağlayın
4. `amerika_analiz_app.py` dosyasını main file olarak seçin

## Veri Gereksinimleri

Uygulama `sirket_son_1.csv` dosyasını kullanır. Bu dosya aşağıdaki sütunları içermelidir:

- `marketplace_key`: Pazar adı
- `variant_name`: Ürün adı
- `SUM(quantity)`: Satış miktarı

## Dashboard Bölümleri

### 📈 Genel Performans Metrikleri
- Toplam satış miktarı
- Aktif pazar sayısı
- Ürün çeşit sayısı
- Kategori sayısı

### 🏆 En Çok Satan Ürünler
- Top 20 ürün listesi
- Ürün bazında performans analizi

### 🏪 Pazar Performansı
- Pazar bazında satış miktarları
- Pazar payı dağılımları

### 📂 Kategori Analizi
- Kategori bazında performans
- Kategori payı analizi

### 📊 Görselleştirmeler
- İnteraktif bar grafikler
- Heatmap analizleri
- Pie chart'lar

### 📋 Detaylı Rapor
- Özet istatistikler
- Stratejik öneriler
- Ham veri görüntüleme

## Teknolojiler

- **Streamlit**: Web uygulaması framework'ü
- **Pandas**: Veri analizi
- **Plotly**: İnteraktif görselleştirme
- **NumPy**: Sayısal hesaplamalar

## Lisans

MIT License
