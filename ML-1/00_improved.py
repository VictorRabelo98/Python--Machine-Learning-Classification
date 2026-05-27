# ============================================================
# AIRLINE PASSENGER SATISFACTION — CLASSIFICAÇÃO ML
# Script melhorado: corrige bugs e organiza saídas do original
# ============================================================

import os
import pandas as pd
import numpy as np
import warnings

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

warnings.filterwarnings('ignore')

print("Todas as bibliotecas importadas com sucesso!")


# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
X_PATH = os.path.join(SCRIPT_DIR, 'X_training.csv')
Y_PATH = os.path.join(SCRIPT_DIR, 'y_training.csv')

X_train_full = pd.read_csv(X_PATH)
y_train_full = pd.read_csv(Y_PATH)

if 'id' in X_train_full.columns:
    X_train_full = X_train_full.drop('id', axis=1)

y_train_full = y_train_full.values.ravel()

print(f"\n1. Dados carregados")
print(f"   - Amostras: {X_train_full.shape[0]}, Features: {X_train_full.shape[1]}")
print(f"   - Distribuição das classes: {np.bincount(y_train_full)}")


# ============================================================
# 2. DIVISÃO DOS DADOS
# ============================================================

print("\n2. Dividindo os dados em treinamento, validação e teste...")

X_temp, X_test, y_temp, y_test = train_test_split(
    X_train_full, y_train_full,
    test_size=0.2,
    random_state=42,
    stratify=y_train_full
)

X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp,
    test_size=0.2,
    random_state=42,
    stratify=y_temp
)

total = X_train_full.shape[0]
print(f"   - Treinamento: {X_train.shape[0]} amostras ({X_train.shape[0]/total*100:.1f}%)")
print(f"   - Validação:   {X_val.shape[0]} amostras ({X_val.shape[0]/total*100:.1f}%)")
print(f"   - Teste:       {X_test.shape[0]} amostras ({X_test.shape[0]/total*100:.1f}%)")


# ============================================================
# 3. PREPARAÇÃO DOS MODELOS
# ============================================================

print("\n3. Preparando os algoritmos de classificação...")

modelos = {
    'KNN': KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto'),
    'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
    'Logistic Regression': LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000, random_state=42),
}

print(f"   - {len(modelos)} algoritmos configurados")


# ============================================================
# 4. TREINAMENTO E AVALIAÇÃO
# ============================================================

print("\n4. Iniciando o ensaio...")

resultados_train = []
resultados_val = []
resultados_test = []


def calcular_metricas(y_true, y_pred, nome_modelo):
    return {
        'Algoritmo': nome_modelo,
        'Accuracy': round(accuracy_score(y_true, y_pred), 4),
        'Precision': round(precision_score(y_true, y_pred, average='weighted', zero_division=0), 4),
        'Recall': round(recall_score(y_true, y_pred, average='weighted', zero_division=0), 4),
        'F1-Score': round(f1_score(y_true, y_pred, average='weighted', zero_division=0), 4),
    }


for idx, (nome_modelo, modelo) in enumerate(modelos.items(), 1):
    print(f"\n   [{idx}/{len(modelos)}] Treinando: {nome_modelo}")

    try:
        modelo.fit(X_train, y_train)
        print(f"       Treinamento concluído")

        resultados_train.append(calcular_metricas(y_train, modelo.predict(X_train), nome_modelo))
        resultados_val.append(calcular_metricas(y_val, modelo.predict(X_val), nome_modelo))
        resultados_test.append(calcular_metricas(y_test, modelo.predict(X_test), nome_modelo))

        print(f"       Avaliação concluída")

    except Exception as e:
        print(f"       ERRO ao treinar {nome_modelo}: {e}")
        continue


# ============================================================
# 5. EXIBIÇÃO DOS RESULTADOS
# ============================================================

print("\n" + "=" * 70)
print("RESULTADOS DO ENSAIO — CLASSIFICAÇÃO DE SATISFAÇÃO DE PASSAGEIROS")
print("=" * 70)

df_train = pd.DataFrame(resultados_train)
df_val = pd.DataFrame(resultados_val)
df_test = pd.DataFrame(resultados_test)

print("\n PERFORMANCE — DADOS DE TREINAMENTO")
print(df_train.to_string(index=False))

print("\n PERFORMANCE — DADOS DE VALIDAÇÃO")
print(df_val.to_string(index=False))

print("\n PERFORMANCE — DADOS DE TESTE")
print(df_test.to_string(index=False))


# ============================================================
# 6. ANÁLISE DE GAP (OVERFITTING DETECTOR)
# ============================================================

print("\n" + "=" * 70)
print("ANÁLISE DE GAP TREINO → TESTE (F1-Score)")
print("=" * 70)

df_gap = df_train[['Algoritmo', 'F1-Score']].copy()
df_gap = df_gap.rename(columns={'F1-Score': 'F1_Treino'})
df_gap['F1_Teste'] = df_test['F1-Score'].values
df_gap['Gap (pp)'] = ((df_gap['F1_Treino'] - df_gap['F1_Teste']) * 100).round(2)
df_gap['Status'] = df_gap['Gap (pp)'].apply(
    lambda g: 'OK' if g <= 5 else ('Atencao' if g <= 10 else 'Overfitting')
)

print(df_gap.to_string(index=False))

print("\n Melhor modelo (F1 no teste):", df_test.loc[df_test['F1-Score'].idxmax(), 'Algoritmo'])


# ============================================================
# 7. EXPORTAR RESULTADOS
# ============================================================

OUTPUT_PATH = os.path.join(SCRIPT_DIR, 'resultados_ensaio.csv')

df_export = pd.concat([
    df_train.assign(Conjunto='Treino'),
    df_val.assign(Conjunto='Validacao'),
    df_test.assign(Conjunto='Teste'),
], ignore_index=True)

df_export.to_csv(OUTPUT_PATH, index=False)
print(f"\n Resultados exportados: {OUTPUT_PATH}")
