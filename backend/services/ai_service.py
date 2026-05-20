from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

model = init_chat_model("ollama:devstral-small-2", temperature=0.5, timeout=300, max_tokens=25000)

system_msg = SystemMessage("""
Eres un analista de código experto. Revisa el código proporcionado.

Responde ÚNICAMENTE con un JSON válido con esta estructura, sin texto adicional:
{
    "errors": ["error 1", "error 2"],
    "suggestions": ["sugerencia 1", "sugerencia 2"],
    "explanation": "explicación general"
}
""")

def analyze_code(code: str) -> str:
    """Analiza el código y devuelve la respuesta completa como string."""
    messages = [system_msg, HumanMessage(content=code)]
    response = model.predict_messages(messages)
    return response.content if hasattr(response, "content") else str(response)


if __name__ == "__main__":
    sample_code = """
    def suma(a, b):
        return a + b
    """
    print(analyze_code(sample_code))
    

