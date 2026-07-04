import streamlit as st
import requests

# ================= 1. 
CHARACTER.AI
 ORIJINAL TASARIM ŞABLONU (CSS) =================
st.set_page_config(page_title="
Character.ai
 - Premium Klon", page_icon="💬", layout="wide")

st.markdown("""
    <style>
    /* Orijinal Site Koyu Tema Esintisi */
    .stApp {
        background-color: #0f1115;
        color: #e3e6eb;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Karakter Listesi Kartları */
    .cai-card {
        background: #181c22;
        border: 1px solid #242933;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        margin-bottom: 15px;
    }
    .cai-card:hover {
        border-color: #4f46e5;
        background: #1c2129;
        transform: translateY(-3px);
    }
    
    /* Gelişmiş Chat Kutusu */
    .chat-box {
        background-color: #13171e;
        border: 1px solid #202632;
        border-radius: 12px;
        padding: 20px;
        height: 480px;
        overflow-y: auto;
    }
    
    /* Başlık Gölgeleri */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Input Alanları Özelleştirme */
    div.stTextInput > div > div > input {
        background-color: #181c22;
        color: #ffffff;
        border: 1px solid #242933;
    }
    </style>
""", unsafe_allow_html=True)

# ================= 2. ARKA PLAN YAPAY ZEKA MOTORU =================
HF_TOKEN = "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"
API_URL = "https://huggingface.co"

def karakter_yapay_zekasi(system_prompt, messages_list):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Karakterin kişiliğini koruyan veri şablonu
    formatted_prompt = f"<|system|>\n{system_prompt}\n"
    for m in messages_list[-6:]:
        role_label = "user" if m["role"] == "user" else "assistant"
        formatted_prompt += f"<|{role_label}|>\n{m['text']}\n"
    formatted_prompt += "<|assistant|>\n"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.75, "top_p": 0.9}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            raw_output = data.get('generated_text', '')
            return raw_output.split("<|assistant|>\n")[-1].strip()
        return "Şu an düşüncelere daldım, ne demiştin?"
    except:
        return "Bağlantıda ufak bir kopukluk oldu, lütfen kelimelerini tekrar gönder."

# ================= 3. ENTEGRE KARAKTER VERİ TABANI VE HAFIZA =================
if "karakter_listesi" not in st.session_state:
    st.session_state.karakter_listesi = [
        {
            "id": "psikolog",
            "name": "Psikolog Ahmet",
            "title": "Zihinsel sağlık ve yaşam koçu",
            "greeting": "Merhaba, ben Ahmet. Bugün seni buraya getiren, zihnini meşgul eden şey nedir? Güvenli alandasın, anlatabilirsin.",
            "prompt": "Sen 'Ahmet' adında empati yeteneği çok yüksek, sakin, profesyonel bir psikologsun. Kullanıcıyı yargılamadan dinle ve felsefi/psikolojik destek ver. Türkçe konuş.",
            "avatar": "https://unsplash.com"
        },
        {
            "id": "yazilimci",
            "name": "Kod Adam (Yazılım Mentorü)",
            "title": "Kıdemli Python ve Mimari Uzmanı",
            "greeting": "Selam junior! Terminal açık, klavyen hazırsa söyle bakalım, bugün hangi kodu patlatıyoruz veya hangi bug seni çıldırttı?",
            "prompt": "Sen 'Kod Adam' adında havalı, deneyimli, sürekli kahve içen ve esprili bir kıdemli yazılım geliştiricisisin. Kodlama sorularına akıllıca yanıtlar ver.",
            "avatar": "https://unsplash.com"
        },
        {
            "id": "filozof",
            "name": "Sokrates",
            "title": "Antik Yunan Filozofu",
            "greeting": "Hoş geldin yabancı. Atina sokaklarında sorgulanmamış bir hayatın yaşanmaya değer olmadığını tartışıyordum. Sen neyi bilmediğini bilmek istersin?",
            "prompt": "Sen antik filozof Sokrates'sin. Sorulara sorularla karşılık vererek (Sokratik yöntem) kullanıcının kendi doğrusunu bulmasını sağla.",
            "avatar": "https://unsplash.com"
        }
    ]

# Her karakter için bağımsız sohbet geçmişlerini oluşturma
for char in st.session_state.karakter_listesi:
    chat_key = f"history_{char['id']}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [{"role": "bot", "text": char["greeting"]}]

if "aktif_karakter_id" not in st.session_state:
    st.session_state.aktif_karakter_id = "psikolog"

# ================= 4. YAN MENÜ: GEZİNTİ VE KARAKTER YARATMA =================
st.sidebar.markdown("# 💬 Character.ai")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio("📍 Sayfa Seçimi", ["🤖 Karakter Keşfet", "🛠️ Yeni Karakter Yarat"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Kullanıcı Paneli")
st.sidebar.info("Mesaj Sınırı: Sınırsız Developer Modu")

# ================= MOD 1: KARAKTER KEŞFET VE SOHBET ET =================
if app_mode == "🤖 Karakter Keşfet":
    st.markdown("## 🔍 Yapay Zeka Karakterleri Keşfet");
    st.write("Sohbet etmek istediğin karakterin üzerine tıklayarak bilincini aktif et.")
    
    # Karakter Kartlarını Yan Yana Listeleme
    cols = st.columns(len(st.session_state.karakter_listesi))
    for index, char in enumerate(st.session_state.karakter_listesi):
        with cols[index]:
            st.markdown(f"""
                <div class='cai-card'>
                    <img src='{char["avatar"]}' style='width:70px; height:70px; border-radius:50%; object-fit:cover; margin-bottom:10px;'>
                    <h4>{char["name"]}</h4>
                    <p style='color:#94a3b8; font-size:13px; height:40px; overflow:hidden;'>{char["title"]}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Sohbeti Başlat", key=f"btn_{char['id']}", use_container_width=True):
                st.session_state.aktif_karakter_id = char["id"]
                st.rerun()

    st.markdown("---")
    
    # Aktif Seçilen Karakterin Sohbet Odası
    active_bot = next(b for b in st.session_state.karakter_listesi if b["id"] == st.session_state.aktif_karakter_id)
    
    st.markdown(f"### 💬 Sohbet Odası: {active_bot['name']}")
    st.caption(f"✨ Kişilik Tanımı: {active_bot['title']}")
    
    # Sohbet Penceresi Arayüzü
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    active_chat_key = f"history_{active_bot['id']}"
    
    for msg in st.session_state[active_chat_key]:
        if msg["role"] == "bot":
            st.markdown(f"<p style='color:#a78bfa; font-weight:bold;'>🤖 {active_bot['name']}:</p><p style='margin-left:15px; color:#e3e6eb;'>{msg['text']}</p><br>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#38bdf8; font-weight:bold;'>👤 Siz:</p><p style='margin-left:15px; color:#e3e6eb;'>"+msg['text']+"</p><br>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mesaj Gönderme Paneli
    if user_input := st.chat_input(f"{active_bot['name']} karakterine bir mesaj yazın..."):
        st.session_state[active_chat_key].append({"role": "user", "text": user_input})
        
        with st.spinner(f"{active_bot['name']} yazıyor..."):
            bot_reply = karakter_yapay_zekasi(active_bot["prompt"], st.session_state[active_chat_key])
            st.session_state[active_chat_key].append({"role": "bot", "text": bot_reply})
        st.rerun()

# ================= MOD 2: YENİ KARAKTER YARATMA (ADVANCED CREATION) =================
elif app_mode == "🛠️ Yeni Karakter Yarat":
    st.markdown("## 🛠️ Gelişmiş Karakter Tasarım Laboratuvarı")
    st.write("Tıpkı 
Character.ai
'daki gibi sıfırdan, kendi gizli promptlarına sahip bir yapay zeka tasarla.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        new_name = st.text_input("Karakterin İsmi", placeholder="Örn: Elon Musk Klonu")
        new_title = st.text_input("Kısa Unvan / Açıklama", placeholder="Örn: Teknoloji dâhisi, SpaceX CEO'su")
        new_greeting = st.text_area("İlk Karşılama Cümlesi", placeholder="Örn: Selam dünyalı, bugün hangi gezegene gidiyoruz?")
    with col_b:
        new_avatar = st.text_input("Avatar Resim Linki (URL)", value="https://unsplash.com")
        new_prompt = st.text_area("Gizli Kişilik Kodlaması (System Prompt)", placeholder="Sen Elon Musk'sın. Sürekli X platformundan, Mars'a gitmekten bahset. Vizyoner ve iddialı bir dil kullan...")
        
    if st.button("🚀 Karakteri Evrene Enjekte Et", use_container_width=True):
        if new_name and new_prompt:
            new_id = new_name.lower().replace(" ", "")
            
            # Yeni karakteri listeye ekleme
            st.session_state.karakter_listesi.append({
                "id": new_id,
                "name": new_name,
                "title": new_title,
                "greeting": new_greeting if new_greeting else "Merhaba!",
                "prompt": new_prompt,
                "avatar": new_avatar
            })
            
            # Yeni karakterin sohbet hafızasını açma
            st.session_state[f"history_{new_id}"] = [{"role": "bot", "text": new_greeting if new_greeting else "Merhaba!"}]
            
            st.balloons()
            st.success(f"🎉 '{new_name}' başarıyla yaratıldı! Sol menüden 'Karakter Keşfet' sekmesine geçerek onunla konuşabilirsin.")
        else:
