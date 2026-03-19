import streamlit as st
from agent import rodar_agente

st.set_page_config(
    page_title="AI Architect Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Architect Agent")
st.markdown("Transforme um business case em uma arquitetura de agentes")

# Input
business_case = st.text_area(
    "Descreva seu business case:",
    height=200,
    placeholder="Ex: Automatizar atendimento ao cliente..."
)

# Botão
if st.button("Analisar", type="primary"):

    if not business_case.strip():
        st.warning("Por favor, insira um business case.")
    else:
        with st.spinner("Analisando arquitetura..."):

            resultado = rodar_agente(business_case)

        st.success("Análise concluída!")

        # função para mostrar arquitetura
        def mostrar(arch):
            st.markdown("### 📌 Descrição")
            st.write(arch.descricao)

            st.markdown("### 👥 Número de agentes")
            st.write(arch.numero_agentes)

            st.markdown("### 🧠 Agentes e papéis")
            st.write(arch.agentes)

            st.markdown("### 🛠️ Ferramentas")
            st.write(arch.ferramentas)

            st.markdown("### 🔄 Fluxo")
            st.write(arch.fluxo)

            st.markdown("### ✅ Vantagens")
            st.write(arch.vantagens)

            st.markdown("### ⚠️ Limitações")
            st.write(arch.limitacoes)

        # Tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Prompt Chaining",
            "Orchestrator-Workers",
            "Parallelization",
            "Routing",
            "Comparação",
            "Recomendação"
        ])

        with tab1:
            mostrar(resultado.prompt_chaining)

        with tab2:
            mostrar(resultado.orchestrator_workers)

        with tab3:
            mostrar(resultado.parallelization)

        with tab4:
            mostrar(resultado.routing)

        with tab5:
            st.markdown("## 📊 Comparação entre arquiteturas")
            st.write(resultado.comparacao_arquiteturas)

        with tab6:
            st.markdown("## ⭐ Recomendação Final")
            st.write(resultado.recomendacao_final)



            
