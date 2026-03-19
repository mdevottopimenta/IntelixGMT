import requests
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic import BaseModel

load_dotenv()

HEADERS = {"User-Agent": "AulaAgentes/1.0 (aula didatica)"}


# ── Output estruturado mais completo ───────────────────────────────────────────
class ArquiteturaDetalhada(BaseModel):
    descricao: str
    numero_agentes: int
    agentes: str
    ferramentas: str
    fluxo: str


class ArquiteturaDeAgentes(BaseModel):
    prompt_chaining: ArquiteturaDetalhada
    orchestrator_workers: ArquiteturaDetalhada
    parallelization: ArquiteturaDetalhada
    routing: ArquiteturaDetalhada
    recomendacao_final: str


# ── Agente Arquiteto ───────────────────────────────────────────────────────────
agente_arquiteto = Agent(
    model=OpenRouterModel("openai/gpt-4o-mini"),
    output_type=ArquiteturaDeAgentes,
    system_prompt=(
        "Você é um arquiteto sênior de sistemas multi-agentes com IA.\n\n"

        "Você deve analisar um business case e projetar arquiteturas completas.\n\n"

        "Para CADA arquitetura, você DEVE obrigatoriamente fornecer:\n"
        "- descricao: explicação aplicada ao problema\n"
        "- numero_agentes: número total de agentes\n"
        "- agentes: lista com nome + papel de cada agente\n"
        "- ferramentas: quais ferramentas/sistemas cada agente usa\n"
        "- fluxo: passo a passo de execução\n\n"

        "Arquiteturas:\n"
        "1. Prompt Chaining\n"
        "2. Orchestrator-Workers\n"
        "3. Parallelization\n"
        "4. Routing\n\n"

        "Regras:\n"
        "- Seja específico e concreto\n"
        "- Nunca seja genérico\n"
        "- Sempre defina agentes reais (ex: 'Agente de Análise Financeira')\n"
        "- Ferramentas devem ser plausíveis (ex: API, banco de dados, CRM, etc.)\n\n"

        "Na recomendação final você DEVE:\n"
        "- Escolher UMA arquitetura principal\n"
        "- Justificar claramente\n"
        "- Reforçar número de agentes, papéis e ferramentas\n\n"

        "Responda em português."
    ),
)


# ── Função para exibir resultado ──────────────────────────────────────────────
def exibir_bloco(nome, arquitetura: ArquiteturaDetalhada):
    separador = "=" * 70

    print(f"\n{separador}")
    print(nome)
    print(separador)

    print("\n📌 Descrição:")
    print(arquitetura.descricao)

    print("\n👥 Número de agentes:")
    print(arquitetura.numero_agentes)

    print("\n🧠 Agentes e papéis:")
    print(arquitetura.agentes)

    print("\n🛠️ Ferramentas:")
    print(arquitetura.ferramentas)

    print("\n🔄 Fluxo:")
    print(arquitetura.fluxo)


def exibir_analise(resultado: ArquiteturaDeAgentes, business_case: str):
    separador = "=" * 70

    print(separador)
    print("BUSINESS CASE")
    print(separador)
    print(business_case)

    exibir_bloco("ARQUITETURA 1 — PROMPT CHAINING", resultado.prompt_chaining)
    exibir_bloco("ARQUITETURA 2 — ORCHESTRATOR-WORKERS", resultado.orchestrator_workers)
    exibir_bloco("ARQUITETURA 3 — PARALLELIZATION", resultado.parallelization)
    exibir_bloco("ARQUITETURA 4 — ROUTING", resultado.routing)

    print(f"\n{separador}")
    print("⭐ RECOMENDAÇÃO FINAL")
    print(separador)
    print(resultado.recomendacao_final)


# ── Input interativo ──────────────────────────────────────────────────────────
def obter_business_case() -> str:
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

    return " ".join(linhas)


# ── Execução ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    business_case = obter_business_case()

    if not business_case.strip():
        print("⚠️ Nenhum business case informado.")
        exit()

    print("\nAnalisando...\n")

    resposta = agente_arquiteto.run_sync(business_case)

    exibir_analise(resposta.output, business_case)

