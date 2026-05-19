from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

model = init_chat_model("ollama:devstral-small-2", temperature=0.5, timeout=300, max_tokens=25000)

system_msg = SystemMessage("""
Eres un analista de código experto. Revisa el código proporcionado y da un análisis 
claro sobre funciones, problemas potenciales, estilo, seguridad y mejoras.
""")

def analyze_code(code: str):
    for chunk in model.stream([system_msg, HumanMessage(code)]):
        print(chunk.content, end="", flush=True)  


if __name__ == "__main__":
    sample_code = """
    def suma(a, b):
        return a + b
    """
    analyze_code(sample_code)
    

    