import streamlit as st
import random 
import pandas as pd
import numpy as np


def pullArm(min,max):
  return random.uniform(min,max)

def MAB(bracosmab,execucoesmab,epsilon):
  resultadosBracos = {}
  
  #cria uma lista para armazenar o melhor braço
  melhorBraco = [0] * len(bracosmab)
  #mostra a tabela com os valores dos bracos
  mostraTabela(bracosmab)
  #começa puxando aleatoriamente na primeira execução
  armRandom = random.randint(0,len(bracosmab) - 1)
  #busca o resultado do braço escolhido aleatoriamente
  result = pullArm(bracosmab[armRandom][0],bracosmab[armRandom][1])
  #armazena o resultado na lista em seu valor, somando 
  melhorBraco[armRandom] = ((result+ melhorBraco[armRandom])/2)
 
  for i in range(execucoesmab):
    randomnumber = random.uniform(0.0,1.0)
    if randomnumber < epsilon:
      armRandom = random.randint(0,9)

      #busca o resultado do braço escolhido aleatoriamente
      result = pullArm(bracosmab[armRandom][0],bracosmab[armRandom][1])
      #armazena o resultado na lista em seu valor, somando 
      
      melhorBraco[armRandom] = ((result+ melhorBraco[armRandom])/2)

      
    else:
      melhorEscolha = np.argmax(melhorBraco)
      result = pullArm(bracosmab[melhorEscolha][0],bracosmab[melhorEscolha][1])
      st.write(result)
      st.write(melhorEscolha)
      resultadosBracos.setdefault(melhorEscolha, []).append(result)
      st.write(resultadosBracos)
      melhorBraco[melhorEscolha] = ((result+ melhorBraco[melhorEscolha])/2)
      
  st.write(melhorBraco)

  



#mostra a tabela com as escolha dos braços
def mostraTabela(bracosDisponiveis):
  coluna1= []
  coluna2 = []
  coluna3 = []
  contador = 0
  for i in bracosDisponiveis:
    contador += 1
    coluna1.append(str(f"braço {contador}°")) 
    coluna2.append(i[0])
    coluna3.append(i[1])
  pd.set_option('display.max_colwidth', None)
  st.write(pd.DataFrame({
    'Braço referente': coluna1,
    'Valor minimo': coluna2,
    'Valor maximo': coluna3,
}).set_index(['Braço referente']))
st.sidebar.title("Configurar MAB")

epsilon =  st.sidebar.slider("Epsilon",0.0,1.0)

st.title("MAB em funcionamento")
execucoes = st.sidebar.number_input("numeros de execuções")
if st.sidebar.button("Executar mab com braços com ranges aleatórios"):
  Arm1min = random.uniform(0,10)
  Arm2min = random.uniform(0,10)
  Arm3min = random.uniform(0,10)
  Arm4min = random.uniform(0,10)
  Arm5min = random.uniform(0,10)
  Arm6min = random.uniform(0,10)
  Arm7min = random.uniform(0,10)
  Arm8min = random.uniform(0,10)
  Arm9min = random.uniform(0,10)
  Arm10min = random.uniform(0,10)
  Arm1max = random.uniform(0,10)+Arm1min
  Arm2max =random.uniform(0,10)+Arm2min
  Arm3max = random.uniform(0,10)+Arm3min
  Arm4max = random.uniform(0,10)+Arm4min
  Arm5max = random.uniform(0,10)+Arm5min
  Arm6max = random.uniform(0,10)+Arm6min
  Arm7max = random.uniform(0,10)+Arm7min
  Arm8max = random.uniform(0,10)+Arm8min
  Arm9max = random.uniform(0,10)+Arm9min
  Arm10max = random.uniform(0,10)+Arm10min
  bracos = [[Arm1min,Arm1max],[Arm2min,Arm2max],[Arm3min,Arm3max],[Arm4min,Arm4max],[Arm5min,Arm5max],[Arm6min,Arm6max],[Arm7min,Arm7max],[Arm8min,Arm8max],[Arm9min,Arm9max],[Arm10min,Arm10max]]
  MAB(bracos,int(execucoes),epsilon)



st.sidebar.write("Expecifique aqui o range de resultados que cada braço pode gerar")
col1,col2  = st.sidebar.columns(2)

with col1:
  st.sidebar.write("Valor")
  Arm1min = st.number_input("Minimal number 1° arm",0.0,10.0)
  Arm2min = st.number_input("Minimal number 2° arm",0.0,10.0)
  Arm3min = st.number_input("Minimal number 3° arm",0.0,10.0)
  Arm4min = st.number_input("Minimal number 4° arm",0.0,10.0)
  Arm5min = st.number_input("Minimal number 5° arm",0.0,10.0)
  Arm6min = st.number_input("Minimal number 6° arm",0.0,10.0)
  Arm7min = st.number_input("Minimal number 7° arm",0.0,10.0)
  Arm8min = st.number_input("Minimal number 8° arm",0.0,10.0)
  Arm9min = st.number_input("Minimal number 9° arm",0.0,10.0)
  Arm10min = st.number_input("Minimal number 10° arm",0.0,10.0)
with col2:
  Arm1max = st.number_input("Maximum number 1° arm",0.0,10.0)
  Arm2max = st.number_input("Maximum number 2° arm",0.0,10.0)
  Arm3max = st.number_input("Maximum number 3° arm",0.0,10.0)
  Arm4max = st.number_input("Maximum number 4° arm",0.0,10.0)
  Arm5max = st.number_input("Maximum number 5° arm",0.0,10.0)
  Arm6max = st.number_input("Maximum number 6° arm",0.0,10.0)
  Arm7max = st.number_input("Maximum number 7° arm",0.0,10.0)
  Arm8max = st.number_input("Maximum number 8° arm",0.0,10.0)
  Arm9max = st.number_input("Maximum number 9° arm",0.0,10.0)
  Arm10max = st.number_input("Maximum number 10° arm",0.0,10.0)


if st.sidebar.button('Executar Algoritmo'):
  bracos = [[Arm1min,Arm1max],[Arm2min,Arm2max],[Arm3min,Arm3max],[Arm4min,Arm4max],[Arm5min,Arm5max],[Arm6min,Arm6max],[Arm7min,Arm7max],[Arm8min,Arm8max],[Arm9min,Arm9max],[Arm10min,Arm10max]]
  MAB(bracos, execucoes)


