# Stack Tecnológica e Arquitetura

## 1. Visão Geral da Stack

```
┌─────────────────────────────────────────────────────────┐
│                   CAMADA DE DADOS                       │
│  CSV (X_training.csv + y_training.csv)                  │
│  pandas.read_csv → DataFrames                           │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│               CAMADA DE PRÉ-PROCESSAMENTO               │
│  • Remoção de colunas irrelevantes (id)                 │
│  • Conversão de Series para array 1D (ravel)            │
│  • Divisão estratificada (train_test_split × 2)         │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                CAMADA DE MODELAGEM                      │
│  ┌──────────┐ ┌───────────────┐ ┌───────────────────┐  │
│  │   KNN    │ │ Decision Tree │ │  Random Forest    │  │
│  │ (k=5)   │ │  (depth=10)   │ │ (100 trees,d=10) │  │
│  └──────────┘ └───────────────┘ └───────────────────┘  │
│                      ┌─────────────────────┐            │
│                      │ Logistic Regression │            │
│                      │  (C=1, lbfgs)      │            │
│                      └─────────────────────┘            │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                CAMADA DE AVALIAÇÃO                      │
│  • Accuracy  • Precision  • Recall  • F1-Score          │
│  • 3 conjuntos: Train / Validation / Test               │
│  • Saída: DataFrames comparativos                       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Tecnologias Detalhadas

### Python 3.9+
**Por quê Python?**
- Ecossistema de Machine Learning mais maduro do mercado
- Sintaxe clara e produtiva para exploração de dados
- Ampla adoção em times de Data Science

### pandas ≥ 1.5
**Papel:** Carregamento, manipulação e apresentação dos dados
- `read_csv()` — carregamento dos datasets
- `DataFrame.drop()` — remoção da coluna ID
- `DataFrame.to_string()` — formatação dos resultados
- `DataFrame` — estruturação dos resultados por modelo

### NumPy ≥ 1.23
**Papel:** Operações numéricas de suporte
- `np.bincount()` — contagem da distribuição de classes
- Base numérica subjacente ao scikit-learn

### scikit-learn ≥ 1.2
**Papel:** Motor de Machine Learning
- `train_test_split` — divisão estratificada dos dados
- `KNeighborsClassifier` — algoritmo baseado em distância
- `DecisionTreeClassifier` — árvore de decisão simples
- `RandomForestClassifier` — ensemble de árvores
- `LogisticRegression` — modelo linear probabilístico
- `accuracy_score`, `precision_score`, `recall_score`, `f1_score` — métricas

---

## 3. Algoritmos em Detalhe

### KNN (K-Nearest Neighbors)
```python
KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto')
```
| Aspecto | Detalhe |
|---------|---------|
| **Paradigma** | Instance-based / Lazy learning |
| **Funcionamento** | Classifica baseado nos 5 vizinhos mais próximos |
| **Vantagem** | Simples, sem fase de treinamento explícita |
| **Desvantagem** | Lento na predição com grandes datasets, sensível à escala |
| **Risco** | Sofrimento da dimensionalidade com 25 features |

### Decision Tree
```python
DecisionTreeClassifier(max_depth=10, random_state=42)
```
| Aspecto | Detalhe |
|---------|---------|
| **Paradigma** | Divisão recursiva baseada em impureza |
| **Funcionamento** | Aprende regras `if/else` sobre features |
| **Vantagem** | Alta interpretabilidade, visualizável |
| **Desvantagem** | Propenso a overfitting sem limitação de profundidade |
| **Risco** | `max_depth=10` pode ainda ser alto para 25 features |

### Random Forest
```python
RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
```
| Aspecto | Detalhe |
|---------|---------|
| **Paradigma** | Ensemble de árvores com bagging |
| **Funcionamento** | 100 árvores em subamostras aleatórias, votação majoritária |
| **Vantagem** | Alta acurácia, robusto a overfitting, feature importance nativa |
| **Desvantagem** | Caixa-preta, mais lento que árvore única |
| **Risco** | Baixo — é o mais robusto dos quatro algoritmos |

### Logistic Regression
```python
LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000, random_state=42)
```
| Aspecto | Detalhe |
|---------|---------|
| **Paradigma** | Modelo linear com função sigmoide |
| **Funcionamento** | Estima probabilidade de satisfação via combinação linear |
| **Vantagem** | Interpretável, rápido, coeficientes com significado |
| **Desvantagem** | Assume linearidade, pode subestimar padrões complexos |
| **Risco** | Pode ter performance inferior se relações forem não-lineares |

---

## 4. Estratégia de Divisão dos Dados

```
Total: 72.515 amostras
         │
         ├──────────────────────────────┐
         ▼                              ▼
    X_temp (80%)                   X_test (20%)
    57.012 amostras               14.503 amostras
         │
         ├──────────────┬──────────────┐
         ▼              ▼
    X_train (80%)   X_val (20%)
    45.609 amostras  11.403 amostras
```

> **Nota:** Os números exatos dependem da distribuição das classes. O uso de `stratify` garante proporção idêntica de classes em todos os subconjuntos.

**Por que 64/16/20 e não 70/30?**
- O conjunto de validação (16%) serve para **comparação e seleção** de modelos sem contaminar o teste
- O teste (20%) é mantido completamente isolado até a avaliação final
- Esta divisão permite diagnosticar overfitting via gap Treino→Validação→Teste

---

## 5. Pipeline de Execução

```
INÍCIO
  ↓
Importar bibliotecas
  ↓
Carregar CSV → DataFrame
  ↓
Remover coluna 'id'
  ↓
Converter target para array 1D
  ↓
Split estratificado 1: (80% temp / 20% test)
  ↓
Split estratificado 2: (80% train / 20% val)
  ↓
Para cada modelo em {KNN, DT, RF, LR}:
  ├── fit(X_train, y_train)
  ├── predict(X_train) → métricas_train
  ├── predict(X_val)   → métricas_val
  └── predict(X_test)  → métricas_test
  ↓
Consolidar resultados em DataFrames
  ↓
Exibir tabelas comparativas
  ↓
FIM
```

---

## 6. Dependências (requirements.txt)

```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
```

---

## 7. Ambiente Recomendado

| Configuração | Mínimo | Recomendado |
|-------------|--------|-------------|
| Python | 3.9 | 3.11+ |
| RAM | 4 GB | 8 GB |
| CPU | 2 cores | 4+ cores |
| Armazenamento | 500 MB | 1 GB |
| IDE | VS Code | Jupyter Lab + VS Code |
