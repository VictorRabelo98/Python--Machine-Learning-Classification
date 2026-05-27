# Storytelling — A Jornada do Passageiro Insatisfeito

## Prólogo: O Custo do Silêncio

Era uma terça-feira comum no hub da AirSatisfy Airlines. Às 22h47, o voo AS-2031 pousava no aeroporto de destino com 23 minutos de atraso. Entre os 189 passageiros, 47 deles já haviam tomado a decisão silenciosa que nenhum gestor veria em planilha alguma: **nunca mais voar com essa companhia**.

Eles não reclamariam no balcão. Não ligariam para o SAC. Simplesmente abririam um app concorrente na próxima vez que precisassem viajar.

Esse é o problema invisível que custou à indústria aérea **US$ 35 bilhões em receita perdida** em 2023 — não por reclamações, mas por silêncio.

---

## Capítulo 1: A Crise de Dados que a AirSatisfy Não Sabia que Tinha

A diretora de Customer Experience da AirSatisfy, Dra. Marina Ferreira, recebeu em sua mesa um relatório que a perturbou: **a taxa de recompra havia caído 8% em 18 meses**, mas o NPS declarado nos formulários pós-voo havia subido 3 pontos.

*Como passageiros dizem estar satisfeitos e param de voar?*

A resposta estava nos dados que ninguém havia analisado: **os 68% de passageiros que nunca preencheram o formulário de satisfação**. Esses eram os verdadeiros insatisfeitos — os que simplesmente desapareceram.

A equipe de dados foi convocada. A missão: construir um modelo capaz de prever satisfação **a partir do comportamento observável**, não do feedback declarado.

---

## Capítulo 2: O Dataset como Espelho da Experiência

Os engenheiros de dados revelaram o tesouro escondido na operação: **72.515 registros de passageiros** com dados coletados passivamente durante suas jornadas.

Cada linha do dataset era uma história comprimida em números:

```
Passageiro #34.891:
  → Classe Econômica, Viagem a Negócios, 45 anos
  → Wi-Fi: 2/5, Entretenimento: 3/5, Assento: 2/5
  → Atraso na chegada: 47 minutos
  → Satisfação: 0 (Insatisfeito)
```

```
Passageiro #67.204:
  → Classe Executiva, Viagem a Negócios, 38 anos
  → Wi-Fi: 5/5, Entretenimento: 5/5, Assento: 5/5
  → Atraso na chegada: 0 minutos
  → Satisfação: 1 (Satisfeito)
```

Os padrões estavam lá. Faltava o algoritmo para enxergá-los.

---

## Capítulo 3: A Escolha dos Algoritmos — Quatro Abordagens para um Problema

O cientista de dados Victor Rabelo decidiu não apostar em um único modelo. A estratégia foi comparar **quatro perspectivas algorítmicas diferentes** sobre o mesmo problema:

### O Algoritmo do Vizinho (KNN)
*"Me diga com quem você anda e eu te direi se você está satisfeito."*

O KNN não aprende regras — ele memoriza. Para classificar um passageiro, encontra os 5 passageiros mais similares no histórico e pergunta: "O que eles eram?" É como um concierge que, ao ver um novo hóspede, lembra de outros hóspedes parecidos e projeta a experiência.

**Risco:** Com 25 dimensões, "similar" se torna um conceito elástico — a maldição da dimensionalidade.

### A Árvore das Decisões (Decision Tree)
*"Se o Wi-Fi é ruim E o assento é desconfortável E houve atraso, então: insatisfeito."*

A árvore de decisão é o algoritmo mais humano de todos: ela aprende regras `se-então` que qualquer pessoa de negócio pode entender. O risco é que, sem limitação, ela memoriza o treinamento até decorar os dados — o famoso overfitting.

**Risco:** Com `max_depth=10`, há 10 níveis de perguntas. Isso ainda permite memorizações indesejadas.

### A Floresta dos Sábios (Random Forest)
*"100 perspectivas diferentes sobre o mesmo passageiro, decidindo por votação."*

O Random Forest não é um modelo — é uma democracia de modelos. Cada árvore vê uma amostra diferente dos dados e uma seleção diferente de features. A decisão final é a votação da maioria. Essa diversidade intencional é o que o torna robusto.

**Vantagem:** Quase sempre o melhor dos quatro neste tipo de problema.

### O Modelo da Probabilidade (Logistic Regression)
*"Cada serviço tem um peso. A soma dos pesos determina a probabilidade de satisfação."*

A Regressão Logística é o economista dos algoritmos: assume que a satisfação é uma combinação linear dos atributos e estima os pesos de cada um. Simples, transparente e interpretável — mas pode falhar onde as relações são complexas e não-lineares.

**Vantagem:** Coeficientes revelam diretamente o impacto de cada feature.

---

## Capítulo 4: O Ensaio — Onde Cada Modelo Prova seu Valor

O ensaio foi desenhado com rigor científico:

1. **Conjunto de treino (64%):** Onde os modelos aprendem
2. **Conjunto de validação (16%):** Onde comparamos modelos sem viés
3. **Conjunto de teste (20%):** O veredicto final — dados que nenhum modelo jamais viu

A divisão estratificada garantiu que a proporção de satisfeitos e insatisfeitos fosse idêntica nos três conjuntos. Sem essa garantia, um modelo poderia parecer excelente por simplesmente chegar em um subconjunto com mais casos fáceis.

---

## Capítulo 5: O Diagnóstico dos Resultados

Ao final do ensaio, as tabelas revelaram padrões previsíveis e surpreendentes.

**O que as tabelas nos dizem:**

- **Gap Treino–Teste alto:** O modelo está memorizando, não aprendendo. Sinal de overfitting.
- **Métricas de treino ≈ teste:** O modelo aprendeu padrões reais e generalizáveis.
- **Recall baixo:** Muitos passageiros insatisfeitos estão sendo classificados como satisfeitos — o pior cenário para o negócio.

---

## Capítulo 6: O Insight que Mudou a Conversa

Quando Victor apresentou os resultados para a Dra. Marina, a primeira pergunta não foi sobre acurácia. Foi:

*"Qual modelo me diz POR QUE o passageiro está insatisfeito, não apenas QUE ele está?"*

Essa pergunta revelou a limitação do estudo: **predizer satisfação é só o começo**. O verdadeiro valor está em entender **quais features mais contribuem para a insatisfação** — e isso exige um próximo passo: análise de feature importance e SHAP values.

O modelo não é o produto final. É a porta de entrada para uma conversa mais profunda com os dados.

---

## Epílogo: O Modelo Como Ferramenta de Empatia

Três meses após o deploy do modelo em produção, a equipe de bordo passou a receber alertas discretos sobre passageiros classificados como "alto risco de insatisfação" antes do desembarque. A intervenção era simples: um reconhecimento, uma oferta de pontos de fidelidade, uma conversa humana.

A taxa de churn entre os passageiros identificados caiu 12%.

Mas o dado mais surpreendente não foi esse. Foi descobrir que **47% dos passageiros classificados como insatisfeitos nunca haviam reclamado** — eles simplesmente não sabiam que a companhia se importava.

O modelo não substituiu o atendimento humano. Ele permitiu que o atendimento humano chegasse onde mais importava.

---

*"Dados sem narrativa são apenas números. Narrativa sem dados é apenas opinião. A combinação das duas é estratégia."*
