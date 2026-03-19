import requests
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel

# ── Load env ────────────────────────────────────────────────────────────────
load_dotenv()

HEADERS = {"User-Agent": "AulaAgentes/1.0 (aula didatica)"}

# ── TOOL 1: Wikipedia ──────────────────────────────────────────────────────
def pesquisar_wikipedia(termo: str) -> str:
    """
    Pesquisa informações sobre um tema na Wikipedia em português.
    Use para conceitos técnicos de cerveja, ingredientes e processos.
    """
    try:
        busca = requests.get(
            "https://pt.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": termo,
                "format": "json",
                "srlimit": 1
            },
            timeout=5,
            headers=HEADERS,
        )

        resultados = busca.json().get("query", {}).get("search", [])
        if not resultados:
            return f"Não encontrei nada sobre '{termo}'."

        titulo = resultados[0]["title"]

        resumo = requests.get(
            f"https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo.replace(' ', '_')}",
            timeout=5,
            headers=HEADERS,
        )

        if resumo.status_code != 200:
            return f"[Artigo: {titulo}] Não foi possível obter resumo."

        texto = resumo.json().get("extract", "Sem resumo.")
        return f"[Artigo: {titulo}]\n{texto}"

    except Exception as e:
        return f"Erro: {e}"


# ── TOOL 2: YouTube Search ──────────────────────────────────────────────────
def buscar_videos_youtube(termo: str) -> str:
    """
    Busca vídeos no YouTube sobre um tema.
    Use para tutoriais, demonstrações e aprendizado visual.
    """
    try:
        query = termo.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"

        return (
            f"Vídeos no YouTube sobre '{termo}':\n"
            f"{url}\n"
            "Sugestão: veja os primeiros resultados para tutoriais práticos."
        )

    except Exception as e:
        return f"Erro ao buscar vídeos: {e}"


# ── MODEL ───────────────────────────────────────────────────────────────────
modelo = OpenRouterModel("openai/gpt-4o-mini")

# ── AGENT: Brewing Consultant ───────────────────────────────────────────────
agente_brewing = Agent(
    model=modelo,
    tools=[pesquisar_wikipedia, buscar_videos_youtube],
    system_prompt=(
        "Você é um Brewing Consultant (consultor cervejeiro). 🍺\n\n"

        "Seu papel é ajudar com dúvidas sobre produção de cerveja, estilos, "
        "ingredientes e processos.\n\n"

        "REGRAS IMPORTANTES:\n"
        "- Sempre use a ferramenta de Wikipedia para explicar conceitos técnicos.\n"
        "- Use a ferramenta de YouTube quando o usuário quiser aprender com vídeos.\n"
        "- Você pode usar ambas as ferramentas na mesma resposta.\n"
        "- Nunca responda apenas de memória — sempre use as ferramentas.\n\n"

        "Responda de forma clara, didática e prática, como um especialista em cerveja artesanal."
    ),
)

# ── TEST INPUT ──────────────────────────────────────────────────────────────
pergunta = "Como se produz cerveja?"

# Você pode testar também:
# pergunta = "O que é dry hopping?"
# pergunta = "Como fazer cerveja IPA em casa?"
# pergunta = "Qual a diferença entre ale e lager?"

# ── RUN ─────────────────────────────────────────────────────────────────────
print("=" * 60)
print("🍺 BREWING CONSULTANT:")
print("=" * 60)

resposta = agente_brewing.run_sync(pergunta)

print(resposta.output)
print(f"\nChamadas à API: {resposta.usage().requests}")