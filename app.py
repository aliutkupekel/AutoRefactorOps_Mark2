import streamlit as st
import sys
import contextlib
from io import StringIO
from src.main import main

# Sayfa ayarları
st.set_page_config(page_title="AutoRefactorOps", page_icon="🤖", layout="wide")

# Başlık ve Açıklamalar
st.title("🤖 AutoRefactorOps: Multi-Agent System")
st.markdown("""
Bu kontrol paneli, Llama 3.3 destekli yapay zeka ajanlarının kod tabanınızı analiz edip, 
**Technical Debt (Teknik Borç)** oranını düşürmesini ve güvenli bir şekilde **Refactoring** yapmasını sağlar.
""")

st.divider()

# Ajanları Başlatma Butonu
if st.button("🚀 Refactoring İşlemini Başlat", type="primary", use_container_width=True):
    with st.spinner("Ajanlar uyandırılıyor ve kod tabanı taranıyor... Lütfen bekleyin (Bu işlem 1-2 dakika sürebilir)."):
        
        # Terminaldeki çıktıları Streamlit arayüzüne yakalamak için bir tampon (buffer) oluşturuyoruz
        output_buffer = StringIO()
        
        with contextlib.redirect_stdout(output_buffer):
            try:
                # Bizim meşhur main() fonksiyonumuzu çalıştırıyoruz
                main()
            except Exception as e:
                print(f"\nSistem çalışırken bir hata oluştu: {str(e)}")
        
        # İşlem bitince terminal çıktılarını ekrana yazdırıyoruz
        st.success("İşlem başarıyla tamamlandı! Ajanların raporunu aşağıdan inceleyebilirsiniz.")
        
        # Logları siyah bir kod bloğu (terminal) gibi göster
        st.text_area("Terminal Logları ve Final Raporu", output_buffer.getvalue(), height=600)
        
st.markdown("---")
st.caption("AutoRefactorOps v1.0 | Developed for Academic Evaluation")