import streamlit as st
import os
import re
from collections import Counter


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="AI Tutor Bahasa Indonesia",
    page_icon="📘",
    layout="wide"
)


# =========================================================
# TEMA BIRU DAN SILVER ELEGANT
# =========================================================

st.markdown("""
<style>
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background Utama: Gradient Soft Silver to White */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 50%, #F1F5F9 100%);
    }

    /* Streamlit Header Bar */
    [data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.8) !important;
        backdrop-filter: blur(8px);
    }

    /* Header Main Container */
    .main-header-container {
        background: linear-gradient(135deg, #0F2C59 0%, #1A5F7A 100%);
        padding: 32px 30px;
        border-radius: 20px;
        color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(15, 44, 89, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 25px;
    }

    .main-title {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 34px !important;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }

    .subtitle {
        color: #CBD5E1;
        font-size: 15px;
        font-weight: 400;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    /* Badge Label (Silver/Metallic Style) */
    .badge-silver {
        display: inline-block;
        background: linear-gradient(135deg, #E2E8F0 0%, #94A3B8 100%);
        color: #0F2C59;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    /* =====================================================
       SIDEBAR (Dark Blue & Silver Highlights)
       ===================================================== */

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A192F 0%, #0F2C59 50%, #1E3A8A 100%);
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] code {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #38BDF8 !important;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 6px;
        padding: 2px 6px;
    }

    [data-testid="stSidebar"] hr {
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
    }

    /* =====================================================
       CARDS & CONTAINERS
       ===================================================== */

    .card-container {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(15, 44, 89, 0.05);
        margin-bottom: 24px;
    }

    .section-title {
        color: #0F2C59;
        font-size: 19px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Text Area Styling */
    textarea {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 15px !important;
        transition: all 0.2s ease-in-out;
    }

    textarea:focus {
        border-color: #1A5F7A !important;
        box-shadow: 0 0 0 3px rgba(26, 95, 122, 0.15) !important;
    }

    [data-testid="stTextArea"] label {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    /* Button Styling (Silver Gradient with Blue Accent on Hover) */
    .stButton > button {
        background: linear-gradient(135deg, #0F2C59 0%, #1A5F7A 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        height: 48px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(15, 44, 89, 0.2);
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1A5F7A 0%, #0F2C59 100%) !important;
        box-shadow: 0 6px 18px rgba(15, 44, 89, 0.3);
        transform: translateY(-1px);
    }

    /* Answer Box (Silver & Metallic Blue Accordance) */
    .answer-box {
        background-color: #FFFFFF;
        border-left: 5px solid #0F2C59;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        color: #1E293B;
        line-height: 1.8;
        font-size: 15px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }

    /* Source Box (Metallic Accent) */
    .source-box {
        background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 12px 18px;
        color: #0F2C59;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 20px;
    }

    /* Expander Styling */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    [data-testid="stExpander"] summary {
        color: #0F2C59 !important;
        font-weight: 600 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 13px;
        padding: 24px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# KONFIGURASI DATABASE
# =========================================================

FOLDER_DATABASE = "database"


# =========================================================
# FUNGSI MEMBACA DATABASE TXT
# =========================================================

def baca_database():
    data = []
    if not os.path.exists(FOLDER_DATABASE):
        os.makedirs(FOLDER_DATABASE)

    daftar_file = os.listdir(FOLDER_DATABASE)
    for nama_file in daftar_file:
        if nama_file.lower().endswith(".txt"):
            lokasi_file = os.path.join(FOLDER_DATABASE, nama_file)
            try:
                with open(lokasi_file, "r", encoding="utf-8") as file:
                    isi = file.read()
                data.append({
                    "nama_file": nama_file,
                    "isi": isi
                })
            except Exception as error:
                st.error(f"Gagal membaca {nama_file}: {error}")

    return data


# =========================================================
# MEMBERSIHKAN TEKS & STOPWORDS
# =========================================================

def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks.strip()


STOPWORDS = {
    "yang", "dan", "di", "ke", "dari", "pada", "dengan", "untuk", "dalam",
    "adalah", "itu", "ini", "atau", "apa", "bagaimana", "mengapa", "sebutkan",
    "jelaskan", "jelaskanlah", "tentang", "suatu", "sebuah", "secara",
    "merupakan", "dapat", "akan", "sebagai", "oleh", "lebih", "juga",
    "tidak", "tersebut"
}


def ambil_kata_kunci(pertanyaan):
    teks = bersihkan_teks(pertanyaan)
    kata = teks.split()
    return [item for item in kata if len(item) > 2 and item not in STOPWORDS]


# =========================================================
# SISTEM PENILAIAN RELEVANSI
# =========================================================

def hitung_relevansi(pertanyaan, isi):
    kata_kunci = ambil_kata_kunci(pertanyaan)
    if not kata_kunci:
        return 0

    teks_database = bersihkan_teks(isi)
    kata_database = teks_database.split()
    frekuensi = Counter(kata_database)

    skor = 0
    for kata in kata_kunci:
        if kata in frekuensi:
            jumlah = min(frekuensi[kata], 10)
            skor += jumlah

    # Bonus jika frasa pertanyaan lengkap muncul
    pertanyaan_bersih = bersihkan_teks(pertanyaan)
    if pertanyaan_bersih in teks_database:
        skor += 20

    # Bonus jika kata kunci muncul di awal materi
    baris_awal = teks_database[:500]
    for kata in kata_kunci:
        if kata in baris_awal:
            skor += 5

    return skor


def cari_materi(pertanyaan, database):
    hasil = []
    for data in database:
        skor = hitung_relevansi(pertanyaan, data["isi"])
        if skor > 0:
            hasil.append({
                "nama_file": data["nama_file"],
                "isi": data["isi"],
                "skor": skor
            })

    hasil.sort(key=lambda x: x["skor"], reverse=True)
    return hasil


# =========================================================
# MEMBUAT POTONGAN MATERI
# =========================================================

def ambil_potongan_relevan(pertanyaan, isi, jumlah_maksimal=1200):
    kata_kunci = ambil_kata_kunci(pertanyaan)
    paragraf = re.split(r"\n\s*\n|\r\n", isi)
    paragraf_relevan = []

    for p in paragraf:
        p_bersih = bersihkan_teks(p)
        skor = sum(1 for kata in kata_kunci if kata in p_bersih)
        if skor > 0:
            paragraf_relevan.append((skor, p.strip()))

    paragraf_relevan.sort(key=lambda x: x[0], reverse=True)

    hasil = ""
    for skor, p in paragraf_relevan:
        if len(hasil) + len(p) <= jumlah_maksimal:
            hasil += p + "\n\n"

    if not hasil.strip():
        hasil = isi[:jumlah_maksimal]

    return hasil.strip()


# =========================================================
# LOAD DATABASE
# =========================================================

database = baca_database()


# =========================================================
# HEADER APLIKASI
# =========================================================

st.markdown("""
<div class="main-header-container">
    <div class="main-title">AI Tutor Bahasa Indonesia</div>
    <div class="subtitle">Pusat pembelajaran mandiri Tata Bahasa & Kebahasaan berbasis Knowledge Base internal.</div>
    <span class="badge-silver">📘 Pembelajaran Bahasa Indonesia</span>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("### 📚 Knowledge Base")
    st.write("Database memuat otomatis file `.txt` dari direktori:")
    st.code("database/")
    
    st.write(f"Total materi dimuat: **{len(database)}** file")
    st.divider()

    if len(database) > 0:
        st.markdown("#### 📖 Daftar Materi Available")
        for data in database:
            nama = data["nama_file"].replace(".txt", "").replace("_", " ").title()
            st.write(f"• {nama}")
    else:
        st.warning("Belum ada file TXT ditemukan di direktori `database/`.")


# =========================================================
# FORM PERTANYAAN & HASIL
# =========================================================

st.markdown('<div class="section-title">💬 Ajukan Pertanyaan</div>', unsafe_allow_html=True)

pertanyaan = st.text_area(
    "Masukkan topik atau pertanyaan Anda:",
    placeholder="Contoh: Apa yang dimaksud dengan kalimat efektif dan sebutkan cirinya?",
    height=110
)

tombol = st.button("🔍 CARI JAWABAN", use_container_width=True)

if tombol:
    if not pertanyaan.strip():
        st.warning("Mohon ketik pertanyaan Anda terlebih dahulu.")
    elif len(database) == 0:
        st.error("Database kosong. Harap tambahkan file TXT ke folder `database/`.")
    else:
        with st.spinner("🔎 Mencari referensi relevan..."):
            hasil = cari_materi(pertanyaan, database)

        if len(hasil) > 0:
            hasil_utama = hasil[0]
            st.success("✓ Materi relevan ditemukan!")

            st.markdown('<div class="section-title">💡 Jawaban</div>', unsafe_allow_html=True)
            
            jawaban = ambil_potongan_relevan(pertanyaan, hasil_utama["isi"])
            jawaban_html = jawaban.replace("\n", "<br>")

            st.markdown(f"""
            <div class="answer-box">
                {jawaban_html}
            </div>
            """, unsafe_allow_html=True)

            # Sumber Materi Utama
            st.markdown('<div class="section-title">📚 Sumber Utama</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="source-box">
                📄 <b>{hasil_utama['nama_file']}</b>
            </div>
            """, unsafe_allow_html=True)

            # Materi Terkait Lainnya
            if len(hasil) > 1:
                st.markdown('<div class="section-title">📑 Referensi Terkait Lainnya</div>', unsafe_allow_html=True)
                for item in hasil[1:4]:
                    with st.expander(f"📘 {item['nama_file']}"):
                        potongan = ambil_potongan_relevan(pertanyaan, item["isi"], 800)
                        st.write(potongan)
        else:
            st.warning("Maaf, materi yang cocok belum ditemukan di database.")
            st.info("Saran: Coba gunakan kata kunci umum seperti *'kalimat'*, *'paragraf'*, atau *'ejaan'*.")


# =========================================================
# FOOTER
# =========================================================

st.divider()
st.markdown("""
<div class="footer">
    <b>AI Tutor Bahasa Indonesia</b> • Powered by Python & Streamlit<br>
    <span style="color: #94A3B8;">Navy & Silver Metallic Theme Edition</span>
</div>
""", unsafe_allow_html=True)