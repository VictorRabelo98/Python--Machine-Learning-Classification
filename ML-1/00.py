# ------------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
#-------------------------------


# Bibliotecas básicas
import pandas as pd
import numpy as np
import warnings

# Divisão e preprocessamento
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ⭐ ALGORITMOS DE CLASSIFICAÇÃO (CORRIGIDO!)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Métricas de Avaliação
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Configurações
warnings.filterwarnings('ignore')

print(" Todas as bibliotecas importadas com sucesso!")


# 1. CARREGAMENTO DOS DADOS
#------------------------------

# Carregar dados de treinamento
X_train_full = pd.read_csv('X_training.csv')
y_train_full = pd.read_csv('y_training.csv')


# Remover coluna 'id' se existir
if 'id' in X_train_full.columns:
    X_train_full = X_train_full.drop('id', axis=1)

# Ajustar formato do y
y_train_full = y_train_full.values.ravel()

print(f"   - Dados carregados: {X_train_full.shape[0]} amostras, {X_train_full.shape[1]} features")
print(f"   - Distribuição das classes: {np.bincount(y_train_full)}")

#-------------------------------
# 2. DIVISÃO DOS DADOS
#-------------------------------

print("\n2. Dividindo os dados em treinamento, validação e teste...")

# Primeiro, separar conjunto de teste (20%)
X_temp, X_test, y_temp, y_test = train_test_split(
    X_train_full, y_train_full, 
    test_size=0.2, 
    random_state=42,
    stratify=y_train_full
)

# Depois, dividir o restante em treino (64%) e validação (16%)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp,
    test_size=0.2,  # 20% de 80% = 16% do total
    random_state=42,
    stratify=y_temp
)

print(f"   - Treinamento: {X_train.shape[0]} amostras ({X_train.shape[0]/X_train_full.shape[0]*100:.1f}%)")
print(f"   - Validação: {X_val.shape[0]} amostras ({X_val.shape[0]/X_train_full.shape[0]*100:.1f}%)")
print(f"   - Teste: {X_test.shape[0]} amostras ({X_test.shape[0]/X_train_full.shape[0]*100:.1f}%)")

#------------------------------
# 3. PREPARAÇÃO DOS MODELOS
#------------------------------
print("\n3. Preparando os algoritmos de classificação...")

# Dicionário com os modelos e seus parâmetros
modelos = {
    'KNN': KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto'),
    'Decision Tree': DecisionTreeClassifier(max_depth=10, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
    'Logistic Regression': LogisticRegression(C=1.0, solver='lbfgs', max_iter=1000, random_state=42)
}

print(f"   - {len(modelos)} algoritmos configurados")


#------------------------------
# 4. TREINAMENTO E AVALIAÇÃO
#------------------------------

print("\n. Iniciando o ensaio...")

# Estruturas para armazenar resultados
resultados_train = []
resultados_val = []
resultados_test = []

# Loop através de cada modelo
for idx, (nome_modelo, modelo) in enumerate(modelos.items(), 1):
    print(f"\n   [{idx}/{len(modelos)}] Treinando: {nome_modelo}")
    
    try:
        # Treinar o modelo
        modelo.fit(X_train, y_train)
        print(f"       Treinamento concluído")
        
        # ===== AVALIAR NO CONJUNTO DE TREINAMENTO =====
        y_pred_train = modelo.predict(X_train)
        acc_train = accuracy_score(y_train, y_pred_train)
        prec_train = precision_score(y_train, y_pred_train, average='weighted', zero_division=0)
        rec_train = recall_score(y_train, y_pred_train, average='weighted', zero_division=0)
        f1_train = f1_score(y_train, y_pred_train, average='weighted', zero_division=0)
        
        resultados_train.append({
            'Algoritmo': nome_modelo,
            'Accuracy': round(acc_train, 3),
            'Precision': round(prec_train, 3),
            'Recall': round(rec_train, 3),
            'F1-Score': round(f1_train, 3)
        })
        
        # ===== AVALIAR NO CONJUNTO DE VALIDAÇÃO =====
        y_pred_val = modelo.predict(X_val)
        acc_val = accuracy_score(y_val, y_pred_val)
        prec_val = precision_score(y_val, y_pred_val, average='weighted', zero_division=0)
        rec_val = recall_score(y_val, y_pred_val, average='weighted', zero_division=0)
        f1_val = f1_score(y_val, y_pred_val, average='weighted', zero_division=0)
        
        resultados_val.append({
            'Algoritmo': nome_modelo,
            'Accuracy': round(acc_val, 3),
            'Precision': round(prec_val, 3),
            'Recall': round(rec_val, 3),
            'F1-Score': round(f1_val, 3)
        })
        
        # ===== AVALIAR NO CONJUNTO DE TESTE =====
        y_pred_test = modelo.predict(X_test)
        acc_test = accuracy_score(y_test, y_pred_test)
        prec_test = precision_score(y_test, y_pred_test, average='weighted', zero_division=0)
        rec_test = recall_score(y_test, y_pred_test, average='weighted', zero_division=0)
        f1_test = f1_score(y_test, y_pred_test, average='weighted', zero_division=0)
        
        resultados_test.append({
            'Algoritmo': nome_modelo,
            'Accuracy': round(acc_test, 3),
            'Precision': round(prec_test, 3),
            'Recall': round(rec_test, 3),
            'F1-Score': round(f1_test, 3)
        })
        
        print(f"       Avaliação concluída")
        
    except Exception as e:
        print(f"       ERRO ao treinar {nome_modelo}: {e}")
        continue


#------------------------------
# 5. EXIBIÇÃO DOS RESULTADOS
#------------------------------

print("\n" + "="*70)
print("RESULTADOS DO ENSAIO - CLASSIFICAÇÃO")
print("="*70)

# Converter para DataFrames
df_train = pd.DataFrame(resultados_train)
df_val = pd.DataFrame(resultados_val)
df_test = pd.DataFrame(resultados_test)

print("\n PERFORMANCE SOBRE OS DADOS DE TREINAMENTO")
print(df_train.to_string(index=True))

print("\n PERFORMANCE SOBRE OS DADOS DE VALIDAÇÃO")

print(df_val.to_string(index=True))

print("\n PERFORMANCE SOBRE OS DADOS DE TESTE")
print(df_test.to_string(index=True))