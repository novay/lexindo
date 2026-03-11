from langchain_ollama import OllamaLLM

# Test koneksi ke model fine-tune kamu
try:
    model = OllamaLLM(model="hf.co/nxvay/lexindo_2e:q4_k_m")
    response = model.invoke("Halo, siapa kamu?")
    print("Respon Model:", response)
except Exception as e:
    print("Error:", e)