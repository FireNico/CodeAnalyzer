from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from langchain.chat_models import init_chat_model

model = init_chat_model(
    "ollama:devstral-small-2",
    temperature=0.5,
    timeout=300,
    max_tokens=25000,
)

class CodeAnalyzerAgent:
    def __init__(self, llm=None):
        self.llm = llm or OpenAI(temperature=0)
        self.tools = self._build_tools()
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
        )

    def _build_tools(self):
        def analyze(code: str) -> str:
            prompt = PromptTemplate(
                input_variables=["code"],
                template=(
                    "Eres un analista de código. Revisa el siguiente código y da un análisis claro "
                    "sobre funciones, problemas potenciales, estilo, seguridad y mejoras.\n\n"
                    "Código:\n{code}\n\n"
                    "Análisis:"
                ),
            )
            chain = LLMChain(llm=self.llm, prompt=prompt)
            return chain.run(code=code)

        return [
            Tool(
                name="code_analyzer",
                func=analyze,
                description=(
                    "Analiza fragmentos de código y entrega recomendaciones, defectos y explicaciones."
                ),
            )
        ]

    def analyze(self, code: str) -> str:
        return self.agent.run(input=code)


if __name__ == "__main__":
    sample_code = """
    def suma(a, b):
        return a + b
    """
    agent = CodeAnalyzerAgent(model)
    print(agent.analyze(sample_code))
