# Insights e Análise de Resultados

## 1. O que Esperamos Ver

Antes de analisar qualquer número, é útil formular **expectativas baseadas em conhecimento dos algoritmos** — o que torna surpresas ainda mais informativas.

| Algoritmo | Expectativa Treino | Expectativa Teste | Risco Principal |
|-----------|-------------------|-------------------|----------------|
| KNN | Médio-alto (~85%) | Médio (~80%) | Sofrimento da dimensionalidade |
| Decision Tree | Muito alto (~95%+) | Moderado (~83%) | Overfitting forte |
| Random Forest | Alto (~95%) | Alto (~87%) | Gap pequeno, best overall |
| Logistic Regression | Moderado (~82%) | Moderado (~82%) | Underfitting se não-linear |

---

## 2. Padrões Diagnósticos Esperados

### Padrão 1 — Overfitting (Árvore de Decisão)
```
Train F1: 0.980  →  Val F1: 0.870  →  Test F1: 0.865
Gap: 11.5pp  ⚠️ Overfitting detectado
```
A Decision Tree, mesmo com `max_depth=10`, tende a memorizar o conjunto de treino. O gap expressivo entre treino e validação/teste é o diagnóstico clássico de overfitting.

**Implicação de negócio:** Se esse modelo fosse para produção, a performance real seria ~15pp abaixo do que parece no treino.

### Padrão 2 — Estabilidade (Random Forest)
```
Train F1: 0.965  →  Val F1: 0.905  →  Test F1: 0.900
Gap: 6.5pp  ✅ Aceitável — ensemble reduziu variância
```
O Random Forest é o algoritmo que mais se aproxima da "solução equilibrada": alto desempenho no treino, mas com generalização consistente para dados novos.

**Por que?** Cada árvore vê apenas um subconjunto aleatório das features — isso força diversidade e reduz correlação entre os modelos base.

### Padrão 3 — Estabilidade Linear (Logistic Regression)
```
Train F1: 0.825  →  Val F1: 0.820  →  Test F1: 0.818
Gap: 0.7pp  ✅ Quase zero overfitting
```
A Regressão Logística é o modelo mais honesto: o que você vê no treino é o que você get no teste. O custo é a performance absoluta mais baixa — o modelo linear pode não capturar interações complexas entre features.

**Implicação:** Se a relação entre features e satisfação é predominantemente não-linear, a LR sofrerá um teto de performance.

### Padrão 4 — KNN: Comportamento Surpresa
```
Train F1: 0.910  →  Val F1: 0.845  →  Test F1: 0.843
Gap: 6.7pp  ⚠️ Moderado
```
O KNN com k=5 tem um gap moderado porque, em vizinhanças pequenas, ainda há alguma memorização. Aumentar k (ex: k=15) reduziria o gap mas poderia diminuir o desempenho absoluto.

---

## 3. Framework de Análise de Resultados

### O que perguntar ao ler a tabela de resultados:

**Pergunta 1: Qual modelo tem o maior F1-Score no TESTE?**
→ Esse é o melhor modelo para produção.

**Pergunta 2: Qual modelo tem o menor gap Treino–Teste?**
→ Esse é o modelo que mais generaliza. Preferível se o dataset de produção for muito diferente do treino.

**Pergunta 3: Algum modelo tem Recall significativamente mais alto que Precision?**
→ Esse modelo é mais "agressivo" na identificação de insatisfeitos — bom para maximizar detecção, mas gera mais falsos alarmes.

**Pergunta 4: Existe um modelo com Precision alta e Recall baixo?**
→ Esse modelo é "conservador" — só classifica como insatisfeito quando tem alta certeza, mas pode perder muitos casos reais.

---

## 4. Interpretação por Perfil de Uso

### Cenário A: Intervenção de baixo custo (avisar tripulação)
**Prioridade: Recall alto**
- O custo de uma intervenção desnecessária é baixo (conversa, oferta de pontos)
- O custo de perder um insatisfeito é alto (churn)
- **Modelo recomendado:** O que tiver maior Recall no teste

### Cenário B: Intervenção de alto custo (upgrade de classe, voucher)
**Prioridade: Precision alta**
- O custo da intervenção é significativo (upgrade, vale-voucher)
- Queremos ter certeza antes de agir
- **Modelo recomendado:** O que tiver maior Precision no teste

### Cenário C: Relatório gerencial (dashboard de satisfação)
**Prioridade: Accuracy + interpretabilidade**
- Gestores precisam de números confiáveis e explicações
- **Modelo recomendado:** Logistic Regression (coeficientes interpretáveis) ou Random Forest (feature importance)

---

## 5. Insights Estratégicos

### Insight 1 — O valor do ensemble
O Random Forest quase sempre supera árvores individuais. Isso não é coincidência — é uma propriedade matemática do ensemble: a variância média de N modelos descorrelacionados é 1/N da variância de um único modelo.

**Takeaway:** Em projetos com orçamento para apenas um modelo em produção, Random Forest é a escolha padrão mais segura.

### Insight 2 — O mito da acurácia
Um modelo com 93% de acurácia parece excelente. Mas se 90% dos passageiros forem satisfeitos, um modelo idiota que diz "todos satisfeitos" teria 90% de acurácia — e seria inútil. F1-Score é sempre mais informativo.

**Takeaway:** Nunca reporte apenas acurácia em problemas de classificação com classes desbalanceadas.

### Insight 3 — O gap é tão importante quanto a métrica absoluta
Um modelo com 88% de F1 no treino e 87% no teste é melhor do que um com 96% no treino e 88% no teste — mesmo tendo a mesma performance final. O segundo modelo tem 8pp de overfitting que, em dados de produção mais variados, se tornará ainda maior.

**Takeaway:** Sempre reporte Treino, Validação E Teste. O gap conta a história real.

### Insight 4 — Features importam mais que algoritmos
Estudos repetidos no mercado mostram que features de qualidade superam algoritmos sofisticados. Um Random Forest treinado com features ruins perde para uma Regressão Logística treinada com boas features.

**Próximo passo:** Feature importance e feature engineering são prioridades maiores que tuning de hiperparâmetros.

---

## 6. Perguntas Abertas para Próximas Iterações

1. **Quais são as 5 features mais importantes?** (Random Forest feature_importances_ ou SHAP)
2. **Existe desbalanceamento de classes?** Se sim, aplicar SMOTE ou ajustar class_weight
3. **O modelo funciona igualmente para diferentes segmentos?** (Análise por classe, tipo de viagem, faixa etária)
4. **Qual é o limiar ótimo de probabilidade?** (Por padrão 0.5, mas pode ser ajustado para maximizar Recall ou Precision)
5. **Como o modelo performa ao longo do tempo?** (Data drift — estabilidade em dados futuros)
