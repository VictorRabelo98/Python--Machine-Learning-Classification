# Airline Passenger Satisfaction — ML Classification Study

> **Problema de negócio:** Uma companhia aérea precisa identificar, com antecedência, quais passageiros estão insatisfeitos com seus serviços para agir proativamente na retenção e melhoria da experiência de voo.

---

## Sumário

- [Contexto & Storytelling](#contexto--storytelling)
- [Problema de Negócio](#problema-de-negócio)
- [Solução Proposta](#solução-proposta)
- [Stack Tecnológica](#stack-tecnológica)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dataset](#dataset)
- [Algoritmos Avaliados](#algoritmos-avaliados)
- [Metodologia](#metodologia)
- [Como Executar](#como-executar)
- [Resultados & Insights](#resultados--insights)
- [Próximos Passos](#próximos-passos)

---

## Contexto & Storytelling

Em um mercado aéreo cada vez mais competitivo, a satisfação do passageiro deixou de ser um diferencial e passou a ser um requisito de sobrevivência. Pesquisas do setor indicam que **adquirir um novo cliente custa de 5 a 7 vezes mais** do que reter um cliente existente.

A empresa fictícia **AirSatisfy Airlines** enfrenta um dilema clássico: seus dados operacionais revelam que aproximadamente metade dos passageiros deixa os voos sem registrar feedback. Desses, uma parcela significativa não retorna para uma segunda compra. O time de Customer Experience identificou o padrão, mas sem capacidade de prever *qual* passageiro está na iminência de se tornar um detrator.

Este projeto nasce dessa dor real: **construir um modelo preditivo capaz de classificar automaticamente a satisfação do passageiro** com base nos atributos coletados durante o voo — de conforto do assento ao Wi-Fi de bordo — antes mesmo que o passageiro desembarque.

---

## Problema de Negócio

| Dimensão | Detalhe |
|----------|---------|
| **Setor** | Aviação Civil / Customer Experience |
| **Tipo** | Classificação Binária |
| **Variável-alvo** | `satisfaction` → `0` (Insatisfeito) / `1` (Satisfeito) |
| **Volume de dados** | 72.515 registros de passageiros |
| **Features disponíveis** | 25 atributos de serviço e perfil do passageiro |

**Perguntas de negócio respondidas pelo modelo:**

1. Qual perfil de passageiro tende à insatisfação?
2. Quais atributos de serviço mais influenciam a satisfação?
3. Com qual precisão conseguimos prever a satisfação antes do desembarque?
4. Qual algoritmo oferece o melhor equilíbrio entre desempenho e interpretabilidade?

---

## Solução Proposta

A solução é um **estudo comparativo de algoritmos de classificação**, onde quatro modelos de Machine Learning são treinados, validados e testados sob as mesmas condições, permitindo escolher o mais adequado para produção.

```
Dados Brutos → Pré-processamento → Split (64/16/20) → Treinamento → Avaliação → Comparação → Insight
```

**Critérios de escolha do melhor modelo:**
- Maior F1-Score no conjunto de teste (equilíbrio entre Precision e Recall)
- Menor gap entre treino e teste (controle de overfitting)
- Interpretabilidade para o time de negócio

---

## Stack Tecnológica

| Camada | Tecnologia | Versão Recomendada |
|--------|------------|-------------------|
| Linguagem | Python | ≥ 3.9 |
| Manipulação de dados | pandas | ≥ 1.5 |
| Computação numérica | NumPy | ≥ 1.23 |
| Machine Learning | scikit-learn | ≥ 1.2 |
| Ambiente | Jupyter / VSCode | — |

---

## Estrutura do Projeto

```
Python--Machine-Learning-Classification/
│
├── README.md                        # Documentação principal (este arquivo)
├── LICENSE                          # Licença MIT
│
├── docs/                            # Documentação técnica detalhada
│   ├── 01_business_context.md       # Contexto de negócio aprofundado
│   ├── 02_stack_and_architecture.md # Stack e arquitetura técnica
│   ├── 03_storytelling.md           # Narrativa do projeto
│   ├── 04_methodology.md            # Metodologia e decisões técnicas
│   ├── 05_insights_and_results.md   # Insights e análise dos resultados
│   └── 06_code_improvements.md      # Melhorias aplicadas ao código
│
└── ML-1/
    ├── 00.py                        # Script original de classificação
    ├── 00_improved.py               # Script melhorado (sem erros)
    ├── X_training.csv               # Features (72.515 amostras × 25 features)
    └── y_training.csv               # Labels (0=Insatisfeito, 1=Satisfeito)
```

---

## Dataset

### Origem
Dataset de satisfação de passageiros de companhia aérea com features pré-processadas (normalizadas e codificadas).

### Dimensões
- **Amostras:** 72.515 registros
- **Features:** 25 atributos (após remoção do ID)
- **Target:** Binário (0/1)

### Categorias de Features

| Categoria | Features |
|-----------|---------|
| **Perfil do passageiro** | `customer_type`, `age`, `class`, `gender_Female`, `gender_Male` |
| **Viagem** | `flight_distance`, `type_of_travel_*` |
| **Serviços de bordo** | `inflight_wifi_service`, `food_and_drink`, `seat_comfort`, `inflight_entertainment`, `on_board_service`, `leg_room_service`, `inflight_service`, `cleanliness` |
| **Experiência no aeroporto** | `departure_arrival_time_convenient`, `ease_of_online_booking`, `gate_location`, `online_boarding`, `checkin_service`, `baggage_handling` |
| **Pontualidade** | `departure_delay_in_minutes`, `arrival_delay_in_minutes` |

---

## Algoritmos Avaliados

| Algoritmo | Parâmetros-chave | Característica |
|-----------|-----------------|----------------|
| **KNN** (k=5) | `weights='uniform'` | Baseado em distância, sem treinamento explícito |
| **Decision Tree** | `max_depth=10` | Alta interpretabilidade, propenso a overfitting |
| **Random Forest** | `n_estimators=100`, `max_depth=10` | Ensemble robusto, menor variância |
| **Logistic Regression** | `C=1.0`, `solver='lbfgs'` | Modelo linear, alta interpretabilidade |

---

## Metodologia

### Divisão dos Dados (Estratificada)

```
72.515 amostras totais
│
├── Treino   → 51.689 amostras (64%)  — aprendizado dos padrões
├── Validação → 12.922 amostras (16%) — ajuste e seleção do modelo
└── Teste    →  14.503 amostras (20%) — avaliação final imparcial
```

A estratificação garante que a proporção de classes (0/1) seja mantida em todos os subconjuntos.

### Métricas de Avaliação

| Métrica | O que mede | Quando priorizar |
|---------|-----------|-----------------|
| **Accuracy** | % de acertos totais | Classes balanceadas |
| **Precision** | Qualidade dos positivos previstos | Evitar falsos alarmes |
| **Recall** | Cobertura dos positivos reais | Evitar falsos negativos |
| **F1-Score** | Média harmônica Precision/Recall | Classes desbalanceadas |

---

## Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/VictorRabelo98/Python--Machine-Learning-Classification.git
cd Python--Machine-Learning-Classification/ML-1

# 2. Instale as dependências
pip install pandas numpy scikit-learn

# 3. Execute o script original
python 00.py

# 4. Execute o script melhorado (recomendado)
python 00_improved.py
```

---

## Resultados & Insights

> Os resultados completos e análise detalhada estão em [`docs/05_insights_and_results.md`](docs/05_insights_and_results.md).

**Insight estratégico principal:** O Random Forest, com seu ensemble de 100 árvores de decisão, tende a apresentar o melhor equilíbrio entre precisão e generalização neste tipo de dataset — especialmente por lidar bem com features de diferentes escalas e correlacionadas.

**Risco identificado:** Modelos como KNN e Decision Tree apresentam maior risco de overfitting neste volume de dados, o que pode ser diagnosticado pelo gap entre métricas de treino e teste.

---

## Próximos Passos

- [ ] Análise exploratória de dados (EDA) com visualizações
- [ ] Otimização de hiperparâmetros (GridSearchCV / Optuna)
- [ ] Feature importance e SHAP values
- [ ] Cross-validation (K-Fold Estratificado)
- [ ] Curvas ROC e AUC por modelo
- [ ] Exportação dos modelos treinados (joblib)
- [ ] API de predição (FastAPI ou Flask)
- [ ] Dashboard de monitoramento de performance

---

## Licença

MIT License — © 2025 VictorRabelo98
