import requests
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic import BaseModel

load_dotenv()

HEADERS = {"User-Agent": "AulaAgentes/1.0 (aula didatica)"}


# ── Estrutura detalhada ───────────────────────────────────────────────────────
class ArquiteturaDetalhada(BaseModel):
    descricao: str
    numero_agentes: int
    agentes: str
    ferramentas: str
    fluxo: str
    vantagens: str
    limitacoes: str


class ArquiteturaDeAgentes(BaseModel):
    prompt_chaining: ArquiteturaDetalhada
    orchestrator_workers: ArquiteturaDetalhada
    parallelization: ArquiteturaDetalhada
    routing: ArquiteturaDetalhada
    comparacao_arquiteturas: str
    recomendacao_final: str


# ── Agente Arquiteto ───────────────────────────────────────────────────────────
agente_arquiteto = Agent(
    model=OpenRouterModel("openai/gpt-4o-mini"),
    output_type=ArquiteturaDeAgentes,
    system_prompt=(
        "Você é um arquiteto sênior de sistemas multi-agentes com IA.\n\n"

        "Para CADA arquitetura você DEVE obrigatoriamente fornecer:\n"
        "- descricao\n"
        "- numero_agentes\n"
        "- agentes (nome + papel)\n"
        "- ferramentas\n"
        "- fluxo\n"
        "- vantagens\n"
        "- limitacoes\n\n"

        "Arquiteturas:\n"
        "1. Prompt Chaining\n"
        "2. Orchestrator-Workers\n"
        "3. Parallelization\n"
        "4. Routing\n\n"

        "Após analisar todas, você DEVE criar uma seção de COMPARAÇÃO:\n"
        "- Compare as arquiteturas em termos de:\n"
        "  • complexidade\n"
        "  • escalabilidade\n"
        "  • latência\n"
        "  • flexibilidade\n"
        "  • adequação ao problema\n\n"

        "Na recomendação final:\n"
        "- Escolha UMA arquitetura principal\n"
        "- Justifique claramente\n"
        "- Explique por que as outras são inferiores\n"
        "- Reforce agentes, ferramentas e fluxo\n\n"

        "Regras:\n"
        "- Seja específico e técnico\n"
        "- Não seja genérico\n"
        "- Não pule nenhuma arquitetura\n\n"

        "Responda em português."
    ),
)


# ── Função reutilizável (ESSENCIAL) ───────────────────────────────────────────
def rodar_agente(business_case: str) -> ArquiteturaDeAgentes:
    resposta = agente_arquiteto.run_sync(business_case)
    return resposta.output


# ── Execução via terminal (opcional) ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("🤖 AI Architect Agent")
    print("=" * 70)
    print("Descreva seu business case (ENTER duas vezes para finalizar):\n")

    linhas = []
    while True:
        linha = input()
        if linha.strip() == "":
            break
        linhas.append(linha)

    business_case = " ".join(linhas)

    if not business_case.strip():
        print("⚠️ Nenhum business case informado.")
        exit()

    print("\nAnalisando...\n")

    resultado = rodar_agente(business_case)

    print("\nRESULTADO:\n")
    print(resultado)