import pickle
import pandas as pd

# função para fazer perguntas
def fazer_perguntas(modelo, node, feature_names):
    if node < 0:
        return None

    left_child = modelo.tree_.children_left[node]
    right_child = modelo.tree_.children_right[node]

    if left_child == -1 and right_child == -1:
        class_index = modelo.tree_.value[node].argmax()
        return [str(modelo.classes_[class_index])]

    feature = modelo.tree_.feature[node]
    threshold = modelo.tree_.threshold[node]
    feature_name = feature_names[feature]

    return str(feature_name)

def carregar_csv():
    # adquirindo as colunas para perguntas
    data = pd.read_csv('Training_Tg.csv',sep = ';')
    return data.drop('prognosis', axis=1)

def carregar_ia():
    # carregando modelo de ia treinado
    with open('decision_tree.pkl', 'rb') as arquivo:
        return pickle.load(arquivo)
