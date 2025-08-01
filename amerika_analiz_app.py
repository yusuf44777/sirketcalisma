import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Plotly'yi opsiyonel hale getirelim
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly kütüphanesi bulunamadı. Bazı grafikler görüntülenemeyebilir.")

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Amerika Pazarı Satış Analizi",
    page_icon="🇺🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stil ayarları
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #0066cc;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Veriyi yükle ve işle"""
    df = pd.read_csv('sirket_son_1.csv')
    
    # Amerika pazarları
    amerika_pazarlari = [
        'AmazonUS', 'EtsyDecoroHomeArt', 'EtsyIslamicDecorGifts', 
        'EtsyIwa', 'EtsyMapwoodA', 'EtsyShukran', 'ShopifyCfwEn',
        'ShopifyIslamicEn', 'ShopifyShkuranEn', 'ShopifyUppEn', 'Walmart'
    ]
    
    # Mevcut Amerika pazarlarını filtrele
    mevcut_amerika_pazarlari = [pazar for pazar in amerika_pazarlari if pazar in df['marketplace_key'].unique()]
    df_amerika = df[df['marketplace_key'].isin(mevcut_amerika_pazarlari)].copy()
    
    # Kategori bilgisini ekle
    df_amerika['kategori'] = df_amerika['variant_name'].str.split('-').str[0]
    
    return df_amerika, mevcut_amerika_pazarlari

def main():
    # Ana başlık
    st.markdown('<div class="main-header">🇺🇸 Amerika Pazarı Satış Analizi</div>', unsafe_allow_html=True)
    
    # Veriyi yükle
    df_amerika, mevcut_amerika_pazarlari = load_data()
    
    # Sidebar
    st.sidebar.markdown("## 📊 Filtreler")
    selected_markets = st.sidebar.multiselect(
        "Pazarları Seçin:",
        options=mevcut_amerika_pazarlari,
        default=mevcut_amerika_pazarlari
    )
    
    # Seçilen pazarlara göre filtreleme
    if selected_markets:
        df_filtered = df_amerika[df_amerika['marketplace_key'].isin(selected_markets)]
    else:
        df_filtered = df_amerika
    
    # Ana metrikler
    st.markdown("## 📈 Genel Performans Metrikleri")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df_filtered['SUM(quantity)'].sum()
        st.metric(
            label="💰 Toplam Satış",
            value=f"{total_sales:,} adet"
        )
    
    with col2:
        total_markets = df_filtered['marketplace_key'].nunique()
        st.metric(
            label="🏪 Aktif Pazar Sayısı",
            value=f"{total_markets} adet"
        )
    
    with col3:
        total_products = df_filtered['variant_name'].nunique()
        st.metric(
            label="📦 Ürün Çeşidi",
            value=f"{total_products:,} adet"
        )
    
    with col4:
        total_categories = df_filtered['kategori'].nunique()
        st.metric(
            label="📂 Kategori Sayısı",
            value=f"{total_categories} adet"
        )
    
    # Tab'ler oluştur
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 En Çok Satan Ürünler", 
        "🏪 Pazar Performansı", 
        "📂 Kategori Analizi", 
        "📊 Görselleştirmeler",
        "📋 Detaylı Rapor"
    ])
    
    with tab1:
        st.markdown("### 🏆 En Çok Satan Ürünler")
        
        # Ürün satış analizi
        urun_satislari = df_filtered.groupby('variant_name')['SUM(quantity)'].sum().reset_index()
        urun_satislari = urun_satislari.sort_values('SUM(quantity)', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Top 20 ürün tablosu
            st.markdown("#### İlk 20 En Çok Satan Ürün")
            top_20 = urun_satislari.head(20)
            top_20_display = top_20.copy()
            top_20_display['Sıra'] = range(1, len(top_20) + 1)
            top_20_display = top_20_display[['Sıra', 'variant_name', 'SUM(quantity)']]
            top_20_display.columns = ['Sıra', 'Ürün Adı', 'Satış Miktarı']
            
            st.dataframe(
                top_20_display,
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.markdown("#### 💡 Önemli İstatistikler")
            top_20_total = top_20['SUM(quantity)'].sum()
            top_20_percentage = (top_20_total / total_sales) * 100
            
            st.markdown(f"""
            <div class="insight-box">
            <strong>İlk 20 Ürün:</strong><br>
            • Toplam Satış: {top_20_total:,} adet<br>
            • Toplam Payı: %{top_20_percentage:.1f}<br>
            • En Çok Satan: {top_20.iloc[0]['variant_name'][:30]}...<br>
            • Satış Miktarı: {top_20.iloc[0]['SUM(quantity)']:,} adet
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🏪 Pazar Performans Analizi")
        
        # Pazar analizi
        pazar_satislari = df_filtered.groupby('marketplace_key')['SUM(quantity)'].sum().reset_index()
        pazar_satislari = pazar_satislari.sort_values('SUM(quantity)', ascending=False)
        pazar_satislari['pazar_payi_%'] = (pazar_satislari['SUM(quantity)'] / pazar_satislari['SUM(quantity)'].sum()) * 100
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Pazar Performans Tablosu")
            pazar_display = pazar_satislari.copy()
            pazar_display.columns = ['Pazar', 'Toplam Satış', 'Pazar Payı (%)']
            pazar_display['Pazar Payı (%)'] = pazar_display['Pazar Payı (%)'].round(1)
            
            st.dataframe(
                pazar_display,
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.markdown("#### 🎯 Pazar Payı Dağılımı")
            if PLOTLY_AVAILABLE:
                fig_pie = px.pie(
                    pazar_satislari, 
                    values='SUM(quantity)', 
                    names='marketplace_key',
                    title="Pazar Payları"
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                # Streamlit native pie chart
                st.subheader("Pazar Payları")
                chart_data = pazar_satislari.set_index('marketplace_key')['SUM(quantity)']
                st.bar_chart(chart_data)
    
    with tab3:
        st.markdown("### 📂 Kategori Bazında Analiz")
        
        # Kategori analizi
        kategori_satislari = df_filtered.groupby('kategori')['SUM(quantity)'].sum().reset_index()
        kategori_satislari = kategori_satislari.sort_values('SUM(quantity)', ascending=False)
        kategori_satislari['kategori_payi_%'] = (kategori_satislari['SUM(quantity)'] / kategori_satislari['SUM(quantity)'].sum()) * 100
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Kategori Performansı")
            kategori_display = kategori_satislari.copy()
            kategori_display.columns = ['Kategori', 'Toplam Satış', 'Kategori Payı (%)']
            kategori_display['Kategori Payı (%)'] = kategori_display['Kategori Payı (%)'].round(1)
            
            st.dataframe(
                kategori_display,
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.markdown("#### 📊 Kategori Satış Grafiği")
            if PLOTLY_AVAILABLE:
                fig_bar = px.bar(
                    kategori_satislari, 
                    x='kategori', 
                    y='SUM(quantity)',
                    title="Kategori Bazında Satış Miktarları",
                    labels={'kategori': 'Kategori', 'SUM(quantity)': 'Satış Miktarı'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                # Streamlit native bar chart
                st.subheader("Kategori Bazında Satış Miktarları")
                chart_data = kategori_satislari.set_index('kategori')['SUM(quantity)']
                st.bar_chart(chart_data)
    
    with tab4:
        st.markdown("### 📊 Detaylı Görselleştirmeler")
        
        # En çok satan ürünler bar chart
        st.markdown("#### 🏆 En Çok Satan 15 Ürün")
        top_15 = urun_satislari.head(15)
        
        if PLOTLY_AVAILABLE:
            fig_products = px.bar(
                top_15, 
                x='SUM(quantity)', 
                y='variant_name',
                orientation='h',
                title="En Çok Satan 15 Ürün",
                labels={'SUM(quantity)': 'Satış Miktarı', 'variant_name': 'Ürün Adı'}
            )
            fig_products.update_layout(height=600)
            st.plotly_chart(fig_products, use_container_width=True)
        else:
            # Streamlit native horizontal bar chart
            chart_data = top_15.set_index('variant_name')['SUM(quantity)'].sort_values(ascending=True)
            st.bar_chart(chart_data, horizontal=True)
        
        # Pazar-Kategori Analizi (tablo olarak)
        st.markdown("#### 🔥 Pazar ve Kategori İlişkisi")
        pazar_kategori = df_filtered.groupby(['marketplace_key', 'kategori'])['SUM(quantity)'].sum().reset_index()
        pazar_kategori_pivot = pazar_kategori.pivot(index='marketplace_key', columns='kategori', values='SUM(quantity)')
        pazar_kategori_pivot = pazar_kategori_pivot.fillna(0)
        
        if PLOTLY_AVAILABLE:
            fig_heatmap = px.imshow(
                pazar_kategori_pivot,
                title="Pazar ve Kategori Bazında Satış Dağılımı",
                labels=dict(x="Kategori", y="Pazar", color="Satış Miktarı"),
                aspect="auto"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            # Tablo olarak göster
            st.subheader("Pazar ve Kategori Bazında Satış Dağılımı")
            st.dataframe(pazar_kategori_pivot, use_container_width=True)
    
    with tab5:
        st.markdown("### 📋 Detaylı Analiz Raporu")
        
        # Özet rapor
        st.markdown("#### 🇺🇸 Amerika Pazarı Satış Analizi Özeti")
        
        # En başarılı veriler
        en_buyuk_pazar = pazar_satislari.iloc[0]
        en_cok_satan_urun = urun_satislari.iloc[0]
        en_basarili_kategori = kategori_satislari.iloc[0]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### 📊 Genel İstatistikler")
            st.markdown(f"""
            • **Toplam Amerika satışı:** {total_sales:,} adet  
            • **Aktif pazar sayısı:** {total_markets} adet  
            • **Farklı ürün çeşidi:** {total_products:,} adet  
            • **Farklı kategori sayısı:** {total_categories} adet  
            """)
            
            st.markdown("##### 🏆 En Başarılı")
            st.markdown(f"""
            • **En büyük pazar:** {en_buyuk_pazar['marketplace_key']} ({en_buyuk_pazar['SUM(quantity)']:,} adet)  
            • **En çok satan ürün:** {en_cok_satan_urun['variant_name'][:40]}... ({en_cok_satan_urun['SUM(quantity)']:,} adet)  
            • **En başarılı kategori:** {en_basarili_kategori['kategori']} ({en_basarili_kategori['SUM(quantity)']:,} adet)  
            """)
        
        with col2:
            st.markdown("##### 💡 Önemli Bulgular")
            top_3_pazar_pay = pazar_satislari.head(3)['pazar_payi_%'].sum()
            top_5_kategori_pay = kategori_satislari.head(5)['kategori_payi_%'].sum()
            
            st.markdown(f"""
            • İlk 3 pazar toplam satışın **%{top_3_pazar_pay:.1f}**'ini oluşturuyor  
            • İlk 20 ürün toplam satışın **%{top_20_percentage:.1f}**'ini oluşturuyor  
            • İlk 5 kategori toplam satışın **%{top_5_kategori_pay:.1f}**'ini oluşturuyor  
            """)
            
            st.markdown("##### 🔍 Stratejik Öneriler")
            st.markdown("""
            • En büyük pazarlarda daha fazla ürün çeşidi sunmayı değerlendirin  
            • Başarılı kategorilerdeki ürün gamını genişletmeyi düşünün  
            • Düşük performanslı pazarlarda strateji gözden geçirilmeli  
            • En çok satan ürünlerin stok yönetimi kritik öneme sahip  
            """)
        
        # Ham veri görüntüleme seçeneği
        if st.checkbox("🗂️ Ham Veriyi Göster"):
            st.markdown("#### Ham Veri")
            st.dataframe(df_filtered, use_container_width=True)
    
    # Alt bilgi
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
    📊 Amerika Pazarı Satış Analizi Dashboard | 
    📅 Analiz Tarihi: Ağustos 2025 | 
    💼 Yönetim Raporu
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
