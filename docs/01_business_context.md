# Contexto de Negócio — Airline Passenger Satisfaction

## 1. O Problema

### Situação
Companhias aéreas operam em um mercado de margens extremamente estreitas. A satisfação do passageiro é um dos principais drivers de retenção, recomendação e receita recorrente. No entanto, **a maioria das empresas reage à insatisfação depois que ela ocorre** — via reclamações, cancelamentos e avaliações negativas.

### Complicação
Dado o volume de passageiros e a complexidade da operação, **não é viável tratar manualmente cada caso de insatisfação em tempo real**. As equipes de Customer Experience precisam de um sistema que identifique automaticamente passageiros em risco de insatisfação.

### Questão central
> *"Como podemos prever, com base nos dados coletados durante a jornada do passageiro, se ele está satisfeito ou não — e agir proativamente?"*

---

## 2. Contexto Estratégico

| Fator | Impacto |
|-------|---------|
| Custo de aquisição vs. retenção | Reter é 5–7× mais barato que adquirir |
| NPS (Net Promoter Score) | Diretamente ligado à satisfação per-flight |
| Revenue per passenger | Passageiros satisfeitos compram mais ancillaries |
| Reviews online | Afetam diretamente a taxa de conversão de novos clientes |

A indústria de aviação civil movimenta **trilhões de dólares anuais**, e a diferença entre companhias líderes e perdedoras muitas vezes está na **experiência do passageiro**, não na tarifa.

---

## 3. Hipóteses de Negócio

Antes de construir qualquer modelo, as seguintes hipóteses foram formuladas pelo time de negócio:

**H1:** Passageiros em classe executiva tendem a ser mais satisfeitos que os de classe econômica.

**H2:** Viagens a negócios têm maior satisfação que viagens pessoais, pois a empresa paga e o conforto é prioridade.

**H3:** Atrasos na partida têm impacto negativo na satisfação, mas atrasos na chegada têm impacto ainda maior.

**H4:** Serviços digitais (Wi-Fi, check-in online, entretenimento) têm peso crescente na satisfação, especialmente para passageiros mais jovens.

**H5:** Passageiros frequentes (Loyal Customer) têm maior tolerância a falhas de serviço do que novos clientes.

---

## 4. Stakeholders e Casos de Uso

| Stakeholder | Como usa o modelo |
|-------------|------------------|
| **Customer Experience** | Identifica passageiros insatisfeitos em voo para intervenção da tripulação |
| **Operações** | Correlaciona atrasos com queda de satisfação para priorização |
| **Marketing** | Segmenta passageiros para ofertas de recuperação pós-voo |
| **Produto** | Prioriza melhorias de serviço com maior impacto na satisfação |
| **C-Suite** | KPI de satisfação preditiva por rota/aeronave/tripulação |

---

## 5. Critérios de Sucesso

O modelo será considerado bem-sucedido se:

1. **F1-Score ≥ 0.85** no conjunto de teste (equilíbrio entre identificar insatisfeitos sem gerar muitos falsos alarmes)
2. **Gap Treino–Teste < 5pp** (modelo generaliza bem, sem overfitting)
3. **Recall de insatisfação ≥ 0.80** (captura a maioria dos passageiros insatisfeitos)
4. **Tempo de predição < 100ms** por passageiro (viável para uso em tempo real)

---

## 6. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Overfitting em árvores | Alta | Alto | Limitar profundidade, usar ensemble |
| Features correlacionadas | Média | Médio | Análise de correlação, PCA se necessário |
| Desbalanceamento de classes | Média | Alto | Verificar e aplicar SMOTE se necessário |
| Drift de dados em produção | Alta | Alto | Monitoramento periódico e retreinamento |
| Interpretabilidade do modelo | Média | Médio | Preferir modelos interpretáveis ou usar SHAP |

---

## 7. Definição da Variável-Alvo

```
satisfaction = 0  →  Passageiro INSATISFEITO (Neutral or Dissatisfied)
satisfaction = 1  →  Passageiro SATISFEITO (Satisfied)
```

**Por que classificação binária e não multiclasse?**

A escolha binária reflete a realidade operacional: o time de bordo precisa de um sinal claro e acionável — "intervir" ou "não intervir". Nuances de satisfação podem ser capturadas em versões futuras do modelo.

---

## 8. Valor Gerado

Estimativa conservadora de impacto para uma companhia aérea de médio porte:

- **Redução de 10% no churn** de passageiros identificados como insatisfeitos → +$2M/ano em receita recorrente
- **Aumento de 0.5 pontos no NPS** → correlação histórica de +3% em taxa de recompra
- **Economia operacional** em programas reativos de compensação (menos vouchers emitidos às cegas)
