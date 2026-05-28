import os
import re

import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Zomato Analytics",
    page_icon="🍽️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zealand",
    162: "Philippines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

PRICE_TYPE = {1: "cheap", 2: "normal", 3: "expensive"}


# ---------------------------------------------------------------------------
# Carregamento e pipeline de limpeza — executado UMA vez por sessão
# ---------------------------------------------------------------------------
@st.cache_data
def load_and_process_data() -> pd.DataFrame:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "ProjetoFinal", "zomato.csv")

    df = pd.read_csv(csv_path, encoding="utf-8")

    # Remover colunas com valor único (zero variância analítica)
    cols_to_remove = [col for col in df.columns if df[col].nunique() == 1]
    df = df.drop(columns=cols_to_remove)

    # Remover duplicatas e nulos
    df = df.drop_duplicates()
    df = df.dropna(axis=0, how="any")

    # Normalizar nomes de colunas para snake_case
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
    )

    # Enriquecimento: colunas derivadas
    df["price_type"] = df["price_range"].map(PRICE_TYPE).fillna("gourmet")
    df["country"] = df["country_code"].map(COUNTRIES).fillna("Unknown")
    df["color_name"] = df["rating_color"].map(COLORS).fillna("Unknown")

    # Simplificar culinária para o primeiro tipo listado
    df["cuisines"] = df["cuisines"].astype(str).apply(lambda x: x.split(",")[0].strip())

    return df


df_4 = load_and_process_data()

# ---------------------------------------------------------------------------
# Navegação e filtros
# ---------------------------------------------------------------------------
page = st.radio(
    "Páginas",
    ("Geral", "País", "Cidade", "Restaurantes", "Culinária"),
    horizontal=True,
)

countries_list = sorted(df_4["country"].unique().tolist())
cuisines_list = sorted(df_4["cuisines"].unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Selecione o(s) país(es)", ["Todos"] + countries_list, default="Todos"
)
selected_cuisines = st.sidebar.multiselect(
    "Selecione a(s) culinária(s)", ["Todos"] + cuisines_list, default="Todos"
)

st.sidebar.markdown("---")
st.sidebar.write("Projeto por Victor Rabelo de Campos")

# Aplicar filtros
df_filtered = df_4.copy()

if "Todos" not in selected_countries:
    df_filtered = df_filtered[df_filtered["country"].isin(selected_countries)]

if "Todos" not in selected_cuisines:
    escaped = [re.escape(c) for c in selected_cuisines]
    pattern = "|".join(escaped)
    df_filtered = df_filtered[
        df_filtered["cuisines"].str.contains(pattern, case=False, na=False)
    ]


# ---------------------------------------------------------------------------
# Página: Geral
# ---------------------------------------------------------------------------
if page == "Geral":
    st.title("Análise Geral")
    st.write("Dashboard analisando dados de restaurantes em várias cidades e países.")

    if df_filtered.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Número de Restaurantes", df_filtered["restaurant_name"].nunique())
        col2.metric("Número de Países", df_filtered["country"].nunique())
        col3.metric("Número de Cidades", df_filtered["city"].nunique())

        col4, col5 = st.columns(2)
        col4.metric("Avaliações Feitas", df_filtered["aggregate_rating"].count())
        col5.metric("Tipos de Culinária Registrados", df_filtered["cuisines"].nunique())

        st.subheader("Mapa de Restaurantes")
        if "latitude" in df_filtered.columns and "longitude" in df_filtered.columns:
            map_data = df_filtered[["latitude", "longitude"]].dropna()
            st.map(map_data)
        else:
            st.write("Colunas de latitude/longitude não encontradas no dataset.")


# ---------------------------------------------------------------------------
# Página: País
# ---------------------------------------------------------------------------
elif page == "País":
    st.title("Análise por País")

    if df_filtered.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
    else:
        # Pergunta 1
        st.header("1. Qual o país com mais cidades registradas?")
        country_city = df_filtered.groupby("country")["city"].nunique().sort_values(ascending=False)
        st.bar_chart(country_city.head(5), height=300)
        st.write(f"**{country_city.idxmax()}** — {country_city.max()} cidades.")

        # Pergunta 2
        st.header("2. Top 5 países com mais restaurantes registrados")
        country_rest = df_filtered.groupby("country")["restaurant_name"].nunique().nlargest(5)
        st.bar_chart(country_rest, height=300)
        st.write(f"**{country_rest.idxmax()}** — {country_rest.max()} restaurantes.")

        # Pergunta 3
        st.header("3. Top 5 países com mais restaurantes com nível de preço 4 (gourmet)")
        price4 = df_filtered[df_filtered["price_range"] == 4]
        if not price4.empty:
            cp4 = price4.groupby("country")["restaurant_name"].nunique().nlargest(5)
            st.bar_chart(cp4, height=300)
            st.write(f"**{cp4.idxmax()}** — {cp4.max()} restaurantes gourmet.")
        else:
            st.info("Nenhum restaurante com preço nível 4 nos filtros selecionados.")

        # Cards — perguntas 4-7
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Maior diversidade culinária")
            cuis_country = df_filtered.groupby("country")["cuisines"].nunique()
            if not cuis_country.empty:
                col1.metric("País", cuis_country.idxmax())
                col1.metric("Tipos de culinária", cuis_country.max())

        with col2:
            st.subheader("Mais avaliações")
            rating_country = df_filtered.groupby("country")["aggregate_rating"].count()
            if not rating_country.empty:
                col2.metric("País", rating_country.idxmax())
                col2.metric("Total de avaliações", rating_country.max())

        with col3:
            st.subheader("Mais delivery")
            delivery_df = df_filtered[df_filtered["has_online_delivery"] == 1]
            if not delivery_df.empty:
                del_country = delivery_df.groupby("country")["restaurant_name"].nunique()
                col3.metric("País", del_country.idxmax())
                col3.metric("Restaurantes com delivery", del_country.max())

        with col4:
            st.subheader("Mais reservas")
            reservas_df = df_filtered[df_filtered["has_table_booking"] == 1]
            if not reservas_df.empty:
                res_country = reservas_df.groupby("country")["restaurant_name"].nunique()
                col4.metric("País", res_country.idxmax())
                col4.metric("Restaurantes com reserva", res_country.max())

        # Perguntas 8-11
        st.header("8. Top 5 países com maior volume de avaliações")
        avg_vol = df_filtered.groupby("country")["aggregate_rating"].count().nlargest(5)
        st.bar_chart(avg_vol, height=300)

        st.header("9. Top 5 países com maior nota média")
        avg_rating = df_filtered.groupby("country")["aggregate_rating"].mean().nlargest(5)
        st.bar_chart(avg_rating, height=300)

        st.header("10. Top 5 países com menor nota média")
        min_rating = df_filtered.groupby("country")["aggregate_rating"].mean().nsmallest(5)
        st.bar_chart(min_rating, height=300)

        st.header("11. Média de preço do prato para dois por país")
        cost_country = df_filtered.groupby("country")["average_cost_for_two"].mean().nlargest(5)
        st.bar_chart(cost_country, height=300)


# ---------------------------------------------------------------------------
# Página: Cidade
# ---------------------------------------------------------------------------
elif page == "Cidade":
    st.title("Análise por Cidade")

    if df_filtered.empty:
        st.error("Nenhum dado disponível após aplicar os filtros selecionados.")
    else:
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            st.subheader("Mais restaurantes")
            by_city = df_filtered["city"].value_counts()
            if not by_city.empty:
                st.metric("Cidade", by_city.idxmax())
                st.metric("Restaurantes", by_city.max())

        with col2:
            st.subheader("Mais restaurantes nota > 4")
            high = df_filtered[df_filtered["aggregate_rating"] > 4]["city"].value_counts()
            if not high.empty:
                st.metric("Cidade", high.idxmax())
                st.metric("Restaurantes", high.max())
            else:
                st.info("Nenhum restaurante com nota acima de 4.")

        with col3:
            st.subheader("Mais restaurantes nota < 2.5")
            low = df_filtered[df_filtered["aggregate_rating"] < 2.5]["city"].value_counts()
            if not low.empty:
                st.metric("Cidade", low.idxmax())
                st.metric("Restaurantes", low.max())
            else:
                st.info("Nenhum restaurante com nota abaixo de 2.5.")

        with col4:
            st.subheader("Maior ticket médio p/ dois")
            avg_cost = df_filtered.groupby("city")["average_cost_for_two"].mean()
            if not avg_cost.empty:
                st.metric("Cidade", avg_cost.idxmax())
                st.metric("Valor Médio", f"{avg_cost.max():.2f}")

        st.header("5. Top 5 cidades com maior diversidade culinária")
        cuis_city = df_filtered.groupby("city")["cuisines"].nunique().nlargest(5)
        st.bar_chart(cuis_city, height=300)

        st.header("6. Cidade com mais restaurantes que fazem reservas")
        booking = df_filtered[df_filtered["has_table_booking"] == 1]["city"].value_counts()
        if not booking.empty:
            st.write(f"**{booking.idxmax()}** — {booking.max()} restaurantes.")
        else:
            st.info("Nenhum restaurante com reservas nos filtros selecionados.")

        st.header("7. Cidade com mais restaurantes que fazem entregas (is_delivering_now)")
        delivering = df_filtered[df_filtered["is_delivering_now"] == 1]["city"].value_counts()
        if not delivering.empty:
            st.write(f"**{delivering.idxmax()}** — {delivering.max()} restaurantes.")
        else:
            st.info("Nenhum restaurante entregando agora nos filtros selecionados.")

        st.header("8. Cidade com mais restaurantes que aceitam pedidos online")
        online = df_filtered[df_filtered["has_online_delivery"] == 1]["city"].value_counts()
        if not online.empty:
            st.write(f"**{online.idxmax()}** — {online.max()} restaurantes.")
        else:
            st.info("Nenhum restaurante com pedidos online nos filtros selecionados.")


# ---------------------------------------------------------------------------
# Página: Restaurantes
# ---------------------------------------------------------------------------
elif page == "Restaurantes":
    st.title("Análise de Restaurantes")

    if df_filtered.empty:
        st.error("Nenhum dado disponível após aplicar os filtros selecionados.")
    else:
        st.header("1. Top 5 Restaurantes com Maior Quantidade de Avaliações")
        top_votes = df_filtered[["restaurant_name", "votes"]].sort_values("votes", ascending=False).head(5)
        if not top_votes.empty:
            st.bar_chart(top_votes.set_index("restaurant_name")["votes"], height=300)

        st.header("2. Top 5 Restaurantes com Maior Nota Média")
        top_ratings = df_filtered[["restaurant_name", "aggregate_rating"]].sort_values(
            "aggregate_rating", ascending=False
        ).head(5)
        if not top_ratings.empty:
            st.bar_chart(top_ratings.set_index("restaurant_name")["aggregate_rating"], height=300)

        st.header("3. Top 5 Restaurantes com Maior Ticket para Duas Pessoas")
        top_cost = df_filtered[["restaurant_name", "average_cost_for_two"]].sort_values(
            "average_cost_for_two", ascending=False
        ).head(5)
        if not top_cost.empty:
            st.bar_chart(top_cost.set_index("restaurant_name")["average_cost_for_two"], height=300)

        st.header("4. Restaurante brasileiro com menor média de avaliação")
        br = df_filtered[df_filtered["cuisines"].str.contains("Brazilian", case=False, na=False)]
        if not br.empty:
            r = br.loc[br["aggregate_rating"].idxmin()]
            st.write(f"**{r['restaurant_name']}** — nota {r['aggregate_rating']:.2f}")
        else:
            st.info("Nenhum restaurante de culinária brasileira encontrado.")

        st.header("5. Restaurante brasileiro no Brasil com maior média de avaliação")
        br_br = df_filtered[
            df_filtered["cuisines"].str.contains("Brazilian", case=False, na=False)
            & (df_filtered["country"] == "Brazil")
        ]
        if not br_br.empty:
            r = br_br.loc[br_br["aggregate_rating"].idxmax()]
            st.write(f"**{r['restaurant_name']}** — nota {r['aggregate_rating']:.2f}")
        else:
            st.info("Nenhum restaurante de culinária brasileira no Brasil encontrado.")

        st.header("6. Delivery impacta o volume de avaliações?")
        with_del = df_filtered[df_filtered["has_online_delivery"] == 1]
        no_del = df_filtered[df_filtered["has_online_delivery"] == 0]
        if not with_del.empty and not no_del.empty:
            m_with = with_del["votes"].mean()
            m_no = no_del["votes"].mean()
            col1, col2 = st.columns(2)
            col1.metric("Com delivery — média de avaliações", f"{m_with:.0f}")
            col2.metric("Sem delivery — média de avaliações", f"{m_no:.0f}")
            if m_with > m_no:
                st.success("Sim — restaurantes com delivery têm mais avaliações na média.")
            else:
                st.info("Não — restaurantes sem delivery têm mais avaliações na média.")
        else:
            st.info("Dados insuficientes para comparação.")

        st.header("7. Reservas influenciam o ticket médio?")
        with_book = df_filtered[df_filtered["has_table_booking"] == 1]
        no_book = df_filtered[df_filtered["has_table_booking"] == 0]
        if not with_book.empty and not no_book.empty:
            m_with = with_book["average_cost_for_two"].mean()
            m_no = no_book["average_cost_for_two"].mean()
            col1, col2 = st.columns(2)
            col1.metric("Com reserva — ticket médio p/ dois", f"{m_with:.2f}")
            col2.metric("Sem reserva — ticket médio p/ dois", f"{m_no:.2f}")
            if m_with > m_no:
                st.success("Sim — restaurantes com reserva têm ticket médio maior.")
            else:
                st.info("Não — restaurantes sem reserva têm ticket médio maior.")
        else:
            st.info("Dados insuficientes para comparação.")

        st.header("8. Japonês vs BBQ nos EUA — qual custa mais?")
        us = df_filtered[df_filtered["country"] == "United States of America"]
        jpn = us[us["cuisines"].str.contains("Japanese", case=False, na=False)]
        bbq = us[us["cuisines"].str.contains("BBQ", case=False, na=False)]
        if not jpn.empty and not bbq.empty:
            m_jpn = jpn["average_cost_for_two"].mean()
            m_bbq = bbq["average_cost_for_two"].mean()
            col1, col2 = st.columns(2)
            col1.metric("Japonês — ticket médio p/ dois", f"{m_jpn:.2f}")
            col2.metric("BBQ — ticket médio p/ dois", f"{m_bbq:.2f}")
            if m_jpn > m_bbq:
                st.success("Japonês é mais caro que BBQ nos EUA.")
            else:
                st.info("BBQ é mais caro que Japonês nos EUA.")
        else:
            st.info("Dados insuficientes para comparação entre japonês e BBQ nos EUA.")


# ---------------------------------------------------------------------------
# Página: Culinária
# ---------------------------------------------------------------------------
elif page == "Culinária":
    st.title("Análise por Culinária")

    if df_filtered.empty:
        st.error("Nenhum dado disponível após aplicar os filtros selecionados.")
    else:
        def best_worst_cuisine(label: str, keyword: str):
            subset = df_filtered[df_filtered["cuisines"].str.contains(keyword, case=False, na=False)]
            if subset.empty:
                st.info(f"Nenhum restaurante de culinária {label} encontrado.")
                return
            best = subset.loc[subset["aggregate_rating"].idxmax()]
            worst = subset.loc[subset["aggregate_rating"].idxmin()]
            col1, col2 = st.columns(2)
            col1.metric(f"Melhor {label}", best["restaurant_name"], f"Nota {best['aggregate_rating']:.2f}")
            col2.metric(f"Pior {label}", worst["restaurant_name"], f"Nota {worst['aggregate_rating']:.2f}")

        st.header("Italiana")
        best_worst_cuisine("Italiana", "Italian")

        st.header("Americana")
        best_worst_cuisine("Americana", "American")

        st.header("Árabe")
        best_worst_cuisine("Árabe", "Arabian")

        st.header("Japonesa")
        best_worst_cuisine("Japonesa", "Japanese")

        st.header("Caseira (Home)")
        best_worst_cuisine("Caseira", "Home")

        st.header("11. Culinária com maior ticket médio para dois")
        avg_cost = df_filtered.groupby("cuisines")["average_cost_for_two"].mean()
        if not avg_cost.empty:
            st.write(f"**{avg_cost.idxmax()}** — ticket médio {avg_cost.max():.2f}")

        st.header("12. Culinária com maior nota média")
        avg_rating = df_filtered.groupby("cuisines")["aggregate_rating"].mean()
        if not avg_rating.empty:
            st.write(f"**{avg_rating.idxmax()}** — nota média {avg_rating.max():.2f}")

        st.header("13. Culinária com mais restaurantes com delivery e reserva")
        both = df_filtered[
            (df_filtered["has_online_delivery"] == 1) & (df_filtered["has_table_booking"] == 1)
        ].copy()
        if not both.empty:
            cuisine_counts = both["cuisines"].value_counts()
            st.write(f"**{cuisine_counts.idxmax()}** — {cuisine_counts.max()} restaurantes.")
        else:
            st.info("Nenhum restaurante com delivery e reserva simultâneos nos filtros selecionados.")
