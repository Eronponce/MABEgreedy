import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from EGreedyMAB import EgreedyMAB
from Arm import Arm
import statistics


#mostra a tabela com as escolha dos braços
def mostraTabela(armQuantity):
  coluna1= []
  coluna2 = []
  coluna3 = []
  contador = 0
  for i in armQuantity:
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

def pieChart(choices):
  st.write("### Gráfico de pizza de porcentagem de escolha")
  df = pd.DataFrame(choices).T
  df.columns = [f"Braço {i+1}" for i in range(len(choices))]
  df.index.name = "Execução"

  # Define a custom function to format the value labels
  def format_autopct(value):
      if value == 0:
          return ''
      else:
          return '%1.1f%%' % value
  # Get the non-zero choices and their corresponding labels
  non_zero_choices = [choice for choice in choices if choice != 0]
  non_zero_labels = [label for choice, label in zip(choices, df.columns) if choice != 0]
  # Create the pie chart
  fig1, ax1 = plt.subplots(facecolor='none')
  
  colours1 = ['#26C6DA','#6699fc','#f0a1a2','#fd266f','#7defa1','#ffd16a','#C0CA33','orange','purple']
  
  ax1.pie(non_zero_choices, labels=non_zero_labels, autopct=format_autopct, textprops={'color': 'white'}, colors=colours1,wedgeprops={"edgecolor":"k",'linewidth': 1,'linestyle': '-'})
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

  st.pyplot(fig1)

# mostrar individual por drop   
def frequency(allRewards):
  st.write("### Frequência de recompensas")
  df = pd.DataFrame(allRewards).T
  df.columns = [f"Braço {i+1}" for i in range(len(allRewards))]
  df.index.name = "Execução"
  st.line_chart(df)
  

def averages(rewards,allRewards,regret,execution_times):
 # transforma em int para encontrar moda media e mediana
  allRewards = [[int(val) for val in sublist] for sublist in allRewards]
  mode = []
  for j in range(len(allRewards)):
      if allRewards[j]:
          mode.append(statistics.mode(allRewards[j]))
      else:
          mode.append(None)
  median = [statistics.median(lst) if len(lst) > 0 else None for lst in allRewards]
  std_devs = []
  for j in range(len(allRewards)):
      if len(allRewards[j]) >= 2:
          std_devs.append(statistics.stdev(allRewards[j]))
      else:
          std_devs.append(None)
  
  st.write("### média, mediana, moda, desvio padrão, vezes de execuções e arrependimento das recompensas ")
  df = pd.DataFrame(rewards).T
  df.columns = [f"Braço {i+1}" for i in range(len(rewards))]
  df.index.name = "Braços"
  df = df.rename(index={0: "Média"})
  df.loc["Mediana"] = median
  df.loc["Moda"] = mode
  df.loc["Desvio Padrão"] = std_devs
  df.loc["Vezes de execução"] = execution_times
  sumRegret =[]
  for values in regret:
    sumRegret.append(sum(values))
  df.loc["Arrependimento"] = sumRegret
  st.dataframe(np.transpose(df))



st.sidebar.title("Configurar MAB")
epsilon =  st.sidebar.slider("Epsilon",0.01,1.0)
st.title("MAB em funcionamento")
executions = st.sidebar.number_input("numeros de execuções",min_value= 1,step=1)
maxReward = st.sidebar.number_input("Maximo de recompensa",min_value= 1,step=1)
armQuantity = st.sidebar.number_input("Quantidade de braços",min_value= 1,step=1)



if st.sidebar.button("Executar mab com braços com ranges aleatórios"):
  Arms = Arm(armQuantity,maxReward)  
  fakeRewards = Arm.CreateArms(Arms)   
  mabClass = EgreedyMAB(Arms,armQuantity,executions,epsilon,maxReward)
  rewards,choicesArms,allRewards,regret,execution_times = EgreedyMAB.execute(mabClass)
  mostraTabela(fakeRewards)
  averages(rewards,allRewards,regret,execution_times)
  frequency(allRewards)
  pieChart(choicesArms)
  