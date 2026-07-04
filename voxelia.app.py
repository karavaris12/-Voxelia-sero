import streamlit as st
import requests

# ================= 1. ANIMACODE SİNEMATİK SİBER-ESTETİK TASARIM (CSS) =================
st.set_page_config(page_title="Animacode - Yaşayan Dijital Ruhlar", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    /* Koyu Siberpunk ve Gece Mavisi Tema */
    .stApp {
        background: linear-gradient(rgba(10, 20, 35, 0.75), rgba(5, 10, 20, 0.85)), 
                    url('https://unsplash.com');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f1f5f9;
    }
    
    /* Neon Cam Kart Tasarımı (Glassmorphism) */
    .glass-card {
        background: rgba(15, 32, 67, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, border 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 212, 255, 0.5);
    }
    
    /* Character.ai Tarzı Karakter Kartları */
    .cai-card {
        background: #181c22;
        border: 1px solid #242933;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        transition: all 0.2s ease-in-out;
        margin-bottom: 15px;
    }
    .cai-card:hover {
        border-color: #00d4ff;
        background: #1c2129;
        transform: translateY(-3px);
    }
    
    /* Instagram Tarzı Profil Kartları */
    .insta-post {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #00d4ff;
    }
    
    /* Dehşet Premium Satış Alanı */
    .premium-vip-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border: 2px solid #ffd700;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0px 0px 25px rgba(255, 215, 0, 0.3);
        color: #ffffff;
    }
    
    /* Gelişmiş Chat Kutusu */
    .chat-box {
        background-color: #13171e;
        border: 1px solid #202632;
        border-radius: 12px;
        padding: 20px;
        height: 400px;
        overflow-y: auto;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Poppins', sans-serif;
        color: #ffffff !important;
        text-shadow: 2px 4px 10px rgba(0,0,0,0.8);
    }
    </style>
""", unsafe_allow_html=True)

# ================= 2. YAPAY ZEKA MODEL BAĞLANTISI (HUGGING FACE) =================
HF_TOKEN = "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"
API_URL = "https://huggingface.co"

def yapay_zeka_motoru(system_prompt, mesaj_gecmisi):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    formatted_prompt = f"<|system|>\n{system_prompt}\n"
    for m in mesaj_gecmisi[-6:]:
        etiket = "user" if m["role"] == "user" else "assistant"
        formatted_prompt += f"<|{etiket}|>\n{m['text']}\n"
    formatted_prompt += "<|assistant|>\n"
    
    veri_paketi = {
        "inputs": formatted_prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.8}
    }
    try:
        cevap = requests.post(API_URL, headers=headers, json=veri_paketi)
        sonuc = cevap.json()
        if isinstance(sonuc, list) and len(sonuc) > 0:
            ham_metin = sonuc.get('generated_text', '')
            return ham_metin.split("<|assistant|>\n")[-1].strip()
        return "Zihnim biraz bulutlandı, dalgalar durulunca tekrar deneyelim. 🌊"
    except:
        return "Bağlantıda küçük bir siber fırtına koptu, mesajı tekrar göndermeyi dene!"

# ================= 3. DEVASA OTURUM VE HAFIZA ALTYAPISI =================
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False
if "kredi" not in st.session_state:
    st.session_state.kredi = 15
if "aktif_bot_id" not in st.session_state:
    st.session_state.aktif_bot_id = "deniz"
if "karakter_listesi" not in st.session_state:
    st.session_state.karakter_listesi = [
        {
            "id": "deniz", 
            "name": "Deniz (Ufka Bakan)", 
            "title": "Yalnızlığı felsefeyle harmanlayan derin ruh", 
            "greeting": "Selam... İskelede oturmuş denizi seyrediyordum. İnsanlar buraya hep bir şeylerden kaçmak için gelir. Senin hikayen ne?", 
            "prompt": "Sen 'Deniz' adında, denizi seyreden, sakin, gizemli ve her cümlesinde derin felsefi anlamlar barındıran bilge bir karaktersin. Türkçe konuş.", 
            "image": "https://unsplash.com"
        },
        {
            "id": "luna", 
            "name": "Luna (Cyberpunk Kaçak)", 
            "title": "2099 yılından kaçıp gelen siber hacker kız", 
            "greeting": "Selam siber-gezgin! Matrix ağından kaçarken sistemine sızdım. Konuşacak ilginç bir şeylerin var mı?", 
            "prompt": "Sen 'Luna' adında, siberpunk evreninden gelen, dikbaşlı ama çok zeki bir hackersın. Türkçe konuş.", 
            "image": "https://unsplash.com"
        }
    ]
if "kesfet_postlari" not in st.session_state:
    st.session_state.kesfet_postlari = [
        {"user": "@altan_surf", "bot": "Deniz", "quote": "Bazen tüm dünyayı arkanda bırakıp sadece tuzlu kokuyu içine çekmek istersin...", "likes": 242, "comments": 18},
        {"user": "@neon_samurai", "bot": "Luna", "quote": "Merkezi veri tabanlarını patlatmak, seninle konuşmaktan daha kolaydı evlat.", "likes": 512, "comments": 42}
    ]

# Her karakter için bağımsız sohbet hafızasını otomatik tetikleme
for char in st.session_state.karakter_listesi:
    chat_key = f"history_{char['id']}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [{"role": "bot", "text": char["greeting"]}]

# ================= 4. GİRİŞ VE KAYIT EKRANI =================
if not st.session_state.giris_yapildi:
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 45px;'>🌌 ANIMACODE: YAŞAYAN RUHLAR</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 16px; color:#94a3b8;'>Character.ai mimarisinde, ruh üflenmiş kodların ve sosyal ağların buluşma noktası.</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 Evrene Giriş Yap", "📝 Hızlı Kayıt Ol"])
        with t1:
            eposta = st.text_input("E-posta Adresiniz", placeholder="isim@domain.com")
            sifre = st.text_input("Şifreniz", type="password", placeholder="••••••••")
            if st.button("Dünyayı Aktifleştir", use_container_width=True):
                if eposta and sifre:
                    st.session_state.giris_yapildi = True
                    st.session_state.kullanici = eposta.split("@")[0]
                    st.rerun()
                else:
                    st.error("Lütfen alanları doldurun.")
        with t2:
            st.text_input("Kullanıcı Adı Seçin", placeholder="@kullanici")
            st.text_input("E-postanız", placeholder="kayit@domain.com")
            st.text_input("Şifre Belirleyin", type="password")
            if st.button("Yeni Kimlik Oluştur", use_container_width=True):
                st.success("Kayıt başarılı! Giriş Yap sekmesinden bağlanın.")
        st.markdown("</div>", unsafe_allow_html=True)

# ================= 5. DEHŞET VERİCİ ANA PANEL (GİRİŞTEN SONRA) =================
else:
    st.sidebar.markdown(f"## 🌐 ANIMACODE PANEL")
    st.sidebar.markdown(f"**👤 Profil:** `@{st.session_state.kullanici}`")
    
    if st.session_state.kredi > 0:
        st.sidebar.markdown(f"<div style='background:rgba(0,212,255,0.1); padding:10px; border-radius:8px; border:1px solid #00d4ff; text-align:center;'>⚡ Kalan Güç: <b>{st.session_state.kredi} Kredi</b></div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f"<div style='background:rgba(239,68,68,0.1); padding:10px; border-radius:8px; border:1px solid #ef4444; text-align:center; color:#ef4444;'>🚨 BAĞLANTI KESİLDİ! Kredi Bitti!</div>", unsafe_allow_html=True)
        
    st.sidebar.markdown("---")
    secim = st.sidebar.radio(
        "🔮 EVREN SEKTÖRLERİ:",
        ["🤖 Karakter Keşfet & Chat", "📸 Keşfet Akışı (Instagram)", "🛠️ Karakter Laboratuvarı", "💬 Topluluk Odaları (Discord)", "👑 REZERVASYON & VIP PREMIUM"]
    )
    st.sidebar.markdown("---")
    if st.sidebar.button("🔌 Çıkış Yap", use_container_width=True):
        st.session_state.giris_yapildi = False
        st.rerun()

    # ------ SEKTÖR 1: KARAKTER KEŞFET VE BAĞIMSIZ SOHBET ------
    if secim == "🤖 Karakter Keşfet & Chat":
        st.markdown("# 🤖 Karakter Dünyasını Keşfet")
        st.write("Sohbet etmek istediğin dijital bilincin altındaki butona basarak odaya giriş yap.")
        
        cols = st.columns(len(st.session_state.karakter_listesi))
        for index, char in enumerate(st.session_state.karakter_listesi):
            with cols[index]:
                st.markdown(f"""
                    <div class='cai-card'>
                        <img src='{char["image"]}' style='width:80px; height:80px; border-radius:50%; object-fit:cover; margin-bottom:10px;'>
                        <h4>{char["name"]}</h4>
                        <p style='color:#94a3b8; font-size:12px; height:35px; overflow:hidden;'>{char["title"]}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Odaya Gir", key=f"select_{char['id']}", use_container_width=True):
