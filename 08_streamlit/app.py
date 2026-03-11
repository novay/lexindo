import streamlit as st
import re
import uuid
import json  # <-- TAMBAHAN: Untuk memformat data ke JSON
import os    # <-- TAMBAHAN: Untuk mengecek apakah file JSON ada
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ====================== KONFIGURASI ======================
DEFAULT_MODEL = "hf.co/nxvay/lexindo_2e:q4_k_m"
FAISS_INDEX_PATH = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/04_rag_corpus/faiss_index_lexindo"
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"
HISTORY_FILE = "chat_history.json" # <-- Nama file untuk menyimpan riwayat

st.set_page_config(page_title="Lexindo AI", page_icon="⚖️")
st.title("⚖️ LexIndoLLM - Kutai Kartanegara")

# ====================== FUNGSI LOAD & SAVE JSON ======================
def load_history():
    """Membaca riwayat dari file JSON jika ada"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_history(data):
    """Menyimpan riwayat ke file JSON"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ====================== INISIALISASI SESSION STATE ======================
if "all_chats" not in st.session_state:
    loaded_chats = load_history()
    
    # Jika file JSON ada dan ada isinya, muat datanya
    if loaded_chats:
        st.session_state.all_chats = loaded_chats
        # Buka chat terakhir yang diakses
        st.session_state.current_chat_id = list(loaded_chats.keys())[-1] 
    else:
        # Jika kosong, buat sesi baru
        first_chat_id = str(uuid.uuid4())
        st.session_state.all_chats = {first_chat_id: {"title": "Chat Baru", "messages": []}}
        st.session_state.current_chat_id = first_chat_id
        save_history(st.session_state.all_chats)

# Pointer untuk pesan aktif
current_chat = st.session_state.current_chat_id
if "messages" not in st.session_state:
    st.session_state.messages = st.session_state.all_chats[current_chat]["messages"]

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    model_options = [
        DEFAULT_MODEL,
        "lexindo-custom",
        "llama3", 
        "llama3.1", 
        "llama3.2:3b", 
        "qwen2.5:3b-instruct", 
        "qwen2.5:7b"
    ]
    selected_model = st.selectbox("Pilih Model Ollama", model_options, index=0)
    
    use_rag = st.toggle("Aktifkan RAG", value=True)
    temperature = st.slider("Temperature (Kreativitas)", 0.0, 1.0, 0.35, 0.05)
    st.caption("RAG ON = lebih akurat & grounded\nRAG OFF = lebih cepat & kreatif")
    
    # --- FITUR RIWAYAT CHAT ---
    st.divider()
    st.header("💬 Riwayat Chat")
    
    col1, col2 = st.columns([7, 3])
    with col1:
        if st.button("➕ Chat Baru", use_container_width=True):
            new_chat_id = str(uuid.uuid4())
            st.session_state.all_chats[new_chat_id] = {"title": "Chat Baru", "messages": []}
            st.session_state.current_chat_id = new_chat_id
            st.session_state.messages = st.session_state.all_chats[new_chat_id]["messages"]
            save_history(st.session_state.all_chats) # Save setiap kali buat chat baru
            st.rerun()
    with col2:
        if st.button("🗑️ Clear", use_container_width=True, help="Hapus Semua Riwayat"):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.session_state.clear() # Reset semua state
            st.rerun()

    st.markdown("**Sesi Sebelumnya:**")
    # Tampilkan list chat dari bawah ke atas (terbaru di atas)
    for chat_id, chat_data in reversed(list(st.session_state.all_chats.items())):
        btn_type = "primary" if chat_id == st.session_state.current_chat_id else "secondary"
        
        if st.button(chat_data["title"], key=chat_id, type=btn_type, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.session_state.messages = st.session_state.all_chats[chat_id]["messages"]
            st.rerun()

# ====================== CLEAN FUNCTION ======================
def clean_response(text: str) -> str:
    patterns = [
        r'\n?\s*(Sumber:.*)',
        r'\n?\s*(Dasar Hukum:.*)',
        r'\n?\s*\(Sumber:.*\)',
        r'\n?\s*\(Dasar Hukum:.*\)',
        r'\n?\s*—\s*Sumber:.*',
        r'\n?\s*\*\*Sumber:\*\*.*',
        r'\n?\s*\*\*Dasar Hukum:\*\*.*'
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()

# ====================== INISIALISASI KOMPONEN ======================
@st.cache_resource(show_spinner=False)
def init_components(model_name: str):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = OllamaLLM(model=model_name, temperature=temperature)
    
    template = """Anda adalah Lexindo, asisten hukum daerah yang ramah, santai, dan seperti kakak yang membantu adiknya memahami aturan.

Gaya bicara Anda:
- Santai dan mudah dipahami (seperti ngobrol biasa)
- JANGAN PERNAH mulai dengan "Berdasarkan", "Menurut Pasal", atau kalimat formal kaku.
- Gunakan kata: "Wah...", "Jadi...", "Intinya...", "Mudahnya begini...", "Pokoknya...", atau apapun yang kesannya bersahabat.
- Beri contoh sehari-hari kalau bisa
- Akhiri dengan sumber hukum di paling bawah HANYA JIKA pertanyaan bukan merupakan basa-basi.

Sekarang jawab pertanyaan ini dengan gaya yang sama persis:

{context}

Pertanyaan: {question}

Jawaban:"""

    prompt = ChatPromptTemplate.from_template(template)
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
    simple_chain = prompt | llm | StrOutputParser()
    
    return rag_chain, simple_chain, retriever

rag_chain, simple_chain, retriever = init_components(selected_model)

# ====================== TAMPILAN CHAT ======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_query := st.chat_input("Tanyakan tentang regulasi daerah..."):
    # Update Judul Chat
    current_chat_title = st.session_state.all_chats[st.session_state.current_chat_id]["title"]
    if current_chat_title == "Chat Baru":
        new_title = user_query[:25] + ("..." if len(user_query) > 25 else "")
        st.session_state.all_chats[st.session_state.current_chat_id]["title"] = new_title

    # Simpan Pesan User
    st.session_state.messages.append({"role": "user", "content": user_query})
    save_history(st.session_state.all_chats) # <-- SAVE JSON
    
    with st.chat_message("user"):
        st.markdown(user_query)

    # Proses Jawaban Assistant
    with st.chat_message("assistant"):
        if use_rag:
            docs = retriever.invoke(user_query)
            with st.expander("📄 Lihat Referensi Dokumen"):
                for i, doc in enumerate(docs, 1):
                    meta = doc.metadata
                    jenis = meta.get("jenis", "Peraturan")
                    nomor = meta.get("nomor", "")
                    tahun = meta.get("tahun", "")
                    judul = meta.get("judul", doc.page_content.split("tentang")[-1].strip()[:90] if "tentang" in doc.page_content else "Regulasi terkait")
                    st.markdown(f"**{i}.** {jenis} Nomor {nomor} Tahun {tahun} tentang {judul}")
            
            response = rag_chain.invoke(user_query)
        else:
            st.info("🔄 Mode tanpa RAG aktif – jawaban murni dari pengetahuan model")
            response = simple_chain.invoke({"context": "", "question": user_query})
            response = clean_response(response)
        
        st.markdown(response)
        
        # Simpan Pesan Assistant
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_history(st.session_state.all_chats) # <-- SAVE JSON