# Melhorias Aplicadas — `00_improved.py` vs `00.py`

> Esta é a fase final do projeto: documentação técnica de cada melhoria aplicada no script gerado, explicando o **erro original**, o **conceito por trás do problema** e a **solução implementada**.

---

## Visão Geral das Mudanças

| # | Categoria | Arquivo original | Arquivo melhorado | Impacto |
|---|-----------|-----------------|-------------------|---------|
| 1 | Bug | `"\n. Iniciando o ensaio..."` | `"\n4. Iniciando o ensaio..."` | Corretude |
| 2 | Import desnecessário | `from sklearn.preprocessing import StandardScaler` | Removido | Limpeza |
| 3 | Path frágil | `pd.read_csv('X_training.csv')` | Path absoluto via `__file__` | Robustez |
| 4 | Duplicação de código | 12 linhas repetidas × 4 modelos | Função `calcular_metricas()` | Manutenibilidade |
| 5 | Precisão das métricas | `round(..., 3)` | `round(..., 4)` | Granularidade |
| 6 | Análise ausente | Sem análise de gap | Seção 6: Gap Treino→Teste | Valor diagnóstico |
| 7 | Sem exportação | Apenas `print()` | `df.to_csv()` | Usabilidade |
| 8 | Sem identificação do vencedor | Sem resumo | `idxmax()` exibe melhor modelo | Clareza |

---

## Melhoria 1 — Bug de Numeração no Print

### Erro original
```python
# Linha 94 do 00.py
print("\n. Iniciando o ensaio...")
```

### Problema conceitual
O script numera visualmente suas seções (1, 2, 3...) para orientar o usuário durante a execução. Na seção 4, o número foi omitido — o print exibe apenas `". Iniciando o ensaio..."` com um ponto isolado, quebrando a sequência visual e confundindo quem lê a saída.

Embora seja um erro cosmético, em scripts executados por terceiros ou em pipelines de CI/CD, a legibilidade do log é parte da qualidade do entregável.

### Solução aplicada
```python
# 00_improved.py
print("\n4. Iniciando o ensaio...")
```

**Por que isso importa:** Logs claros e sequenciais são a primeira linha de debugging em produção. Um log malformado pode mascarar a etapa onde uma falha ocorreu.

---

## Melhoria 2 — Import Desnecessário (`StandardScaler`)

### Erro original
```python
# Linha 13 do 00.py — importado mas nunca usado
from sklearn.preprocessing import StandardScaler
```

### Problema conceitual
O `StandardScaler` foi importado mas jamais instanciado ou chamado em nenhum ponto do script. Isso é chamado de **dead import** — código morto que aumenta o ruído cognitivo e pode confundir leitores futuros sobre a intenção do autor.

Além disso, importar módulos desnecessários:
1. Aumenta o tempo de inicialização do script (marginal, mas real)
2. Cria confusão sobre se a normalização foi ou não aplicada
3. Viola o princípio de código limpo: "código não deve conter intenções não-executadas"

**Contexto técnico adicional:** O dataset já está normalizado (features em 0–1). Aplicar StandardScaler novamente modificaria a distribuição dos dados de forma incorreta — é possível que o autor tenha cogitado usar o scaler, decidiu não usar (corretamente), mas esqueceu de remover o import.

### Solução aplicada
```python
# StandardScaler removido do 00_improved.py
# Apenas imports efetivamente utilizados permanecem
```

---

## Melhoria 3 — Caminho de Arquivo Frágil (Hard-coded Relative Path)

### Erro original
```python
# Linhas 34-35 do 00.py
X_train_full = pd.read_csv('X_training.csv')
y_train_full = pd.read_csv('y_training.csv')
```

### Problema conceitual
Caminhos relativos em Python são resolvidos com base no **diretório de trabalho atual** (`os.getcwd()`), não no diretório onde o script reside. Isso significa:

```bash
# Funciona:
cd ML-1 && python 00.py

# Falha com FileNotFoundError:
cd /home/user && python ML-1/00.py
python ML-1/00.py  # de qualquer outro diretório
```

Este é um dos bugs mais comuns em scripts Python que manipulam arquivos — parece funcionar durante o desenvolvimento (quando se está sempre no diretório certo), mas quebra em ambientes de produção, Docker containers, CI/CD pipelines e quando chamado por outros scripts.

### Solução aplicada
```python
# 00_improved.py
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
X_PATH = os.path.join(SCRIPT_DIR, 'X_training.csv')
Y_PATH = os.path.join(SCRIPT_DIR, 'y_training.csv')

X_train_full = pd.read_csv(X_PATH)
y_train_full = pd.read_csv(Y_PATH)
```

**Como funciona:**
- `__file__` → caminho absoluto do script atual
- `os.path.abspath()` → resolve symlinks e paths relativos
- `os.path.dirname()` → extrai apenas o diretório
- `os.path.join()` → constrói o path de forma portável (funciona em Windows e Linux)

**Por que isso importa:** O script agora funciona corretamente independente de onde for chamado — de qualquer diretório, em qualquer sistema operacional.

---

## Melhoria 4 — Eliminação de Duplicação de Código

### Erro original
```python
# 00.py — bloco repetido 3 vezes (train, val, test), dentro de um loop com 4 modelos
# = 12 blocos praticamente idênticos de cálculo de métricas

y_pred_train = modelo.predict(X_train)
acc_train = accuracy_score(y_train, y_pred_train)
prec_train = precision_score(y_train, y_pred_train, average='weighted', zero_division=0)
rec_train = recall_score(y_train, y_pred_train, average='weighted', zero_division=0)
f1_train = f1_score(y_train, y_pred_train, average='weighted', zero_division=0)

resultados_train.append({
    'Algoritmo': nome_modelo,
    'Accuracy': round(acc_train, 3),
    ...
})
# [repetido identicamente para val e test]
```

### Problema conceitual
Este padrão viola o princípio **DRY — Don't Repeat Yourself**: se a lógica de cálculo de métricas precisar mudar (ex.: adicionar uma nova métrica, mudar o parâmetro `average`), a mudança precisaria ser aplicada em 3 lugares diferentes — com alto risco de inconsistência.

Além disso, a legibilidade sofre: o corpo do loop tem ~45 linhas onde as 3 últimas seções são praticamente cópias com renomeação de variáveis.

### Solução aplicada
```python
# 00_improved.py — função extraída, chamada 3 vezes
def calcular_metricas(y_true, y_pred, nome_modelo):
    return {
        'Algoritmo': nome_modelo,
        'Accuracy': round(accuracy_score(y_true, y_pred), 4),
        'Precision': round(precision_score(y_true, y_pred, average='weighted', zero_division=0), 4),
        'Recall': round(recall_score(y_true, y_pred, average='weighted', zero_division=0), 4),
        'F1-Score': round(f1_score(y_true, y_pred, average='weighted', zero_division=0), 4),
    }

# Uso dentro do loop:
resultados_train.append(calcular_metricas(y_train, modelo.predict(X_train), nome_modelo))
resultados_val.append(calcular_metricas(y_val, modelo.predict(X_val), nome_modelo))
resultados_test.append(calcular_metricas(y_test, modelo.predict(X_test), nome_modelo))
```

**Redução:** O corpo do loop passou de ~45 linhas para ~7 linhas, mantendo a mesma funcionalidade.

---

## Melhoria 5 — Granularidade das Métricas (3 vs 4 casas decimais)

### Erro original
```python
'Accuracy': round(acc_train, 3)  # ex: 0.876
```

### Problema conceitual
Arredondar para 3 casas decimais (milésimos) é adequado para apresentação, mas pode mascarar diferenças entre modelos próximos. Por exemplo:
- Modelo A: 0.8764 → arredondado para 0.876
- Modelo B: 0.8755 → arredondado para 0.876

Com 3 casas, os dois parecem idênticos. Com 4 casas, a diferença de 0.0009 é visível.

Em datasets de 72.515 amostras, essa diferença corresponde a ~65 predições corretas a mais — relevante para comparação.

### Solução aplicada
```python
'Accuracy': round(accuracy_score(y_true, y_pred), 4)  # ex: 0.8764
```

---

## Melhoria 6 — Análise de Gap (Diagnóstico de Overfitting)

### Ausente no original
O script original exibe 3 tabelas separadas mas não compara explicitamente os valores, deixando ao leitor o trabalho de calcular o gap manualmente.

### Problema conceitual
O gap entre métricas de treino e teste é o principal indicador de overfitting — um dos problemas mais comuns e mais custosos em Machine Learning aplicado. Não sinalizá-lo automaticamente significa que o usuário pode selecionar um modelo com alto overfitting sem perceber.

### Solução aplicada
```python
# 00_improved.py — Seção 6
df_gap = df_train[['Algoritmo', 'F1-Score']].copy()
df_gap = df_gap.rename(columns={'F1-Score': 'F1_Treino'})
df_gap['F1_Teste'] = df_test['F1-Score'].values
df_gap['Gap (pp)'] = ((df_gap['F1_Treino'] - df_gap['F1_Teste']) * 100).round(2)
df_gap['Status'] = df_gap['Gap (pp)'].apply(
    lambda g: 'OK' if g <= 5 else ('Atencao' if g <= 10 else 'Overfitting')
)
```

**Output gerado:**
```
Algoritmo          F1_Treino  F1_Teste  Gap (pp)  Status
KNN                    0.XXX     0.XXX      X.XX    OK/Atencao/Overfitting
Decision Tree          0.XXX     0.XXX      X.XX    ...
Random Forest          0.XXX     0.XXX      X.XX    ...
Logistic Regression    0.XXX     0.XXX      X.XX    ...
```

---

## Melhoria 7 — Exportação dos Resultados para CSV

### Ausente no original
O script original só exibe resultados no terminal via `print()`. Após a execução, os dados são perdidos.

### Problema conceitual
Em ambiente profissional, resultados de ML precisam ser:
1. **Persistidos** — para comparação com versões futuras do modelo
2. **Rastreáveis** — para auditoria e reprodutibilidade
3. **Consumíveis** — por outros sistemas (dashboards, relatórios, planilhas)

Um script que só printa resultados não atende nenhum desses requisitos.

### Solução aplicada
```python
# 00_improved.py — Seção 7
df_export = pd.concat([
    df_train.assign(Conjunto='Treino'),
    df_val.assign(Conjunto='Validacao'),
    df_test.assign(Conjunto='Teste'),
], ignore_index=True)

df_export.to_csv(OUTPUT_PATH, index=False)
```

O arquivo `resultados_ensaio.csv` é salvo no mesmo diretório do script (usando o path absoluto da Melhoria 3), com todas as métricas organizadas por conjunto.

---

## Melhoria 8 — Identificação Automática do Melhor Modelo

### Ausente no original
O script original não indica qual modelo ganhou o ensaio.

### Solução aplicada
```python
print("Melhor modelo (F1 no teste):", df_test.loc[df_test['F1-Score'].idxmax(), 'Algoritmo'])
```

**Por que F1 no teste e não no treino?**
Porque o conjunto de teste simula dados novos — é o único indicador confiável de performance em produção. Selecionar o melhor modelo pelo treino é a forma clássica de cometer overfitting na seleção de modelo.

---

## Resumo de Impacto

| Categoria de Melhoria | Quantidade | Impacto |
|----------------------|-----------|---------|
| Bugs corrigidos | 2 (numeração + path) | Corretude funcional |
| Código morto removido | 1 (StandardScaler) | Limpeza e clareza |
| Refatoração | 1 (função de métricas) | Manutenibilidade |
| Features adicionadas | 3 (gap, export, vencedor) | Valor para o usuário |
| **Total** | **7 melhorias** | |

> **Importante:** O arquivo `00.py` (original) não foi modificado. Todas as melhorias estão exclusivamente em `00_improved.py`. O original serve como referência histórica e base de comparação.
