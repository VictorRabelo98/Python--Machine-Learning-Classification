# Metodologia — Processo de Criação do Projeto

## 1. Framework Metodológico

Este projeto segue uma versão adaptada do **CRISP-DM** (Cross-Industry Standard Process for Data Mining), o framework mais adotado em projetos de Machine Learning aplicado.

```
┌─────────────────────────────────────────────────────┐
│                    CRISP-DM                         │
│                                                     │
│  1. Entendimento     2. Entendimento     3. Prep.   │
│     do Negócio  →→→   dos Dados   →→→   dos Dados  │
│         ↑                                    ↓      │
│  6. Deploy     ←←←  5. Avaliação   ←←←  4. Model. │
└─────────────────────────────────────────────────────┘
```

---

## 2. Fase 1 — Entendimento do Negócio

### Objetivo definido
Classificar passageiros como **satisfeitos (1)** ou **insatisfeitos (0)** com base em 25 atributos coletados durante a jornada de voo.

### Tipo de problema
- **Supervised Learning** — rótulos disponíveis no dataset
- **Binary Classification** — duas classes de saída
- **Batch processing** — predições em lote, não em tempo real (nesta versão)

### Métrica-alvo
**F1-Score (weighted)** como métrica primária, por:
1. Capturar tanto Precision quanto Recall
2. Lidar adequadamente com possível desbalanceamento de classes
3. Ser mais informativa que Accuracy em problemas de classificação binária

---

## 3. Fase 2 — Entendimento dos Dados

### Inspeção inicial
```python
X_train_full.shape     # (72515, 25)
y_train_full.shape     # (72515,) após ravel()
np.bincount(y)         # [n_insatisfeitos, n_satisfeitos]
```

### Características identificadas
| Característica | Status |
|---------------|--------|
| Missing values | Não detectados |
| Feature scaling | Pré-aplicada (valores 0–1) |
| Encoding categórico | Pré-aplicado (one-hot) |
| Coluna de ID | Presente → removida |
| Target format | Necessita `.ravel()` para array 1D |

### Decisões tomadas
- **Não reaplicar normalização:** Os dados já estão normalizados (0–1), portanto aplicar StandardScaler novamente seria redundante e potencialmente prejudicial
- **Remover coluna 'id':** Identificador sem valor preditivo — adicionar apenas ruído ao modelo

---

## 4. Fase 3 — Preparação dos Dados

### Pipeline de preparação

```python
# Passo 1: Carregamento
X = pd.read_csv('X_training.csv')
y = pd.read_csv('y_training.csv')

# Passo 2: Limpeza
X = X.drop('id', axis=1)        # Remove coluna sem poder preditivo
y = y.values.ravel()             # Converte DataFrame → array 1D

# Passo 3: Split estratificado (mantém proporção de classes)
X_temp, X_test = train_test_split(X, test_size=0.20, stratify=y)
X_train, X_val = train_test_split(X_temp, test_size=0.20, stratify=y_temp)
```

### Por que dividir em três conjuntos?

| Conjunto | Tamanho | Papel |
|---------|---------|-------|
| **Treino** | 64% | Ajustar os parâmetros do modelo |
| **Validação** | 16% | Comparar modelos e selecionar o melhor |
| **Teste** | 20% | Simular performance em dados nunca vistos |

**Regra de ouro:** O conjunto de teste nunca deve influenciar nenhuma decisão de modelagem. Ele é o "oráculo imparcial" — consultado apenas uma vez, no final.

---

## 5. Fase 4 — Modelagem

### Critérios de seleção dos algoritmos

Os quatro algoritmos foram escolhidos por representarem **paradigmas diferentes** de aprendizado:

| Paradigma | Algoritmo | Motivo da inclusão |
|-----------|-----------|-------------------|
| Instance-based | KNN | Baseline não-paramétrico |
| Árvore única | Decision Tree | Interpretabilidade máxima |
| Ensemble | Random Forest | Maior robustez esperada |
| Linear | Logistic Regression | Baseline linear interpretável |

### Configuração dos hiperparâmetros

Os hiperparâmetros foram definidos como valores **razoáveis e conservadores** para um estudo inicial:

```python
# KNN: k=5 é o default mais comum e funciona bem para datasets médios
KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto')

# Decision Tree: depth=10 limita crescimento mas ainda permite capturar padrões
DecisionTreeClassifier(max_depth=10, random_state=42)

# Random Forest: 100 árvores é suficiente para estabilidade de estimativas
RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

# Logistic Regression: lbfgs é estável para datasets médios; max_iter=1000 evita não-convergência
LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000, random_state=42)
```

**`random_state=42`**: Garante reprodutibilidade — qualquer pessoa que execute o código obtém exatamente os mesmos resultados.

---

## 6. Fase 5 — Avaliação

### Métricas calculadas para cada modelo × cada conjunto

```
Para cada (modelo, conjunto):
  ├── Accuracy  = acertos / total
  ├── Precision = VP / (VP + FP)  [média ponderada]
  ├── Recall    = VP / (VP + FN)  [média ponderada]
  └── F1-Score  = 2 × (P × R) / (P + R)  [média ponderada]
```

### Como interpretar os resultados

**Diagnóstico de overfitting:**
```
Se Treino >> Validação ≈ Teste → Overfitting (modelo memorizou)
Se Treino ≈ Validação ≈ Teste  → Bom ajuste (modelo generalizou)
Se Treino ≈ Validação << Teste → Underfitting (modelo simples demais)
```

**Qual métrica priorizar?**
- Em problema de retenção: priorize **Recall** (capturar todos os insatisfeitos, mesmo com alguns falsos alarmes)
- Em problema de intervenção custosa: priorize **Precision** (só intervir quando tiver certeza)
- Na ausência de contexto claro: use **F1-Score** como compromisso

---

## 7. Decisões Técnicas Documentadas

| Decisão | Justificativa |
|---------|--------------|
| Não aplicar StandardScaler | Dados já normalizados (0–1) |
| `average='weighted'` nas métricas | Pondera por suporte de cada classe, mais justo para desbalanceamento |
| `zero_division=0` nas métricas | Evita erros quando uma classe não tem predições |
| `stratify=y` no split | Mantém proporção de classes em todos os subconjuntos |
| `warnings.filterwarnings('ignore')` | Elimina avisos de convergência do solver que não afetam os resultados |
| `random_state=42` | Reprodutibilidade universal |
| Try/except por modelo | Isola falhas — um modelo com erro não interrompe a avaliação dos demais |

---

## 8. Limitações Reconhecidas

1. **Sem otimização de hiperparâmetros:** Os parâmetros são razoáveis, mas não ótimos. GridSearchCV poderia melhorar 2–5pp em F1.

2. **Sem cross-validation:** A divisão train/val/test é dependente do `random_state`. K-Fold estratificado daria estimativas mais estáveis.

3. **Sem análise de features:** Não sabemos quais features são mais importantes — informação crítica para o negócio.

4. **Sem detecção de outliers:** Dados anômalos (atrasos extremos, avaliações 0 em todas as categorias) não foram tratados.

5. **Sem análise de erro:** Não sabemos quais passageiros o modelo erra sistematicamente — podem revelar padrões não capturados.
