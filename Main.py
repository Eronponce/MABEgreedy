import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from EGreedyMAB import EgreedyMAB
from Arm import Arm
import statistics


#mostra a tabela com as escolha dos braços
def mostraTabela(arm_quantity):
  coluna1= []
  coluna2 = []
  coluna3 = []
  contador = 0
  for i in arm_quantity:
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
def frequency(all_rewards):
  st.write("### Frequência de recompensas")
  df = pd.DataFrame(all_rewards).T
  df.columns = [f"Braço {i+1}" for i in range(len(all_rewards))]
  df.index.name = "Execução"
  st.line_chart(df)
  

def averages(rewards,all_rewards,regret,execution_times):
 # transforma em int para encontrar moda media e mediana
  all_rewards = [[int(val) for val in sublist] for sublist in all_rewards]
  mode = []
  for j in range(len(all_rewards)):
      if all_rewards[j]:
          mode.append(statistics.mode(all_rewards[j]))
      else:
          mode.append(None)
  median = [statistics.median(lst) if len(lst) > 0 else None for lst in all_rewards]
  std_devs = []
  for j in range(len(all_rewards)):
      if len(all_rewards[j]) >= 2:
          std_devs.append(statistics.stdev(all_rewards[j]))
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
  sum_regret =[]
  for values in regret:
    sum_regret.append(sum(values))
  df.loc["Arrependimento"] = sum_regret
  st.dataframe(np.transpose(df))



st.sidebar.title("Configurar MAB")
epsilon =  st.sidebar.slider("Epsilon",0.01,1.0)
st.title("MAB em funcionamento")
executions = st.sidebar.number_input("numeros de execuções",min_value= 1,step=1)
max_reward = st.sidebar.number_input("Maximo de recompensa",min_value= 1,step=1)
arm_quantity = st.sidebar.number_input("Quantidade de braços",min_value= 1,step=1)



if st.sidebar.button("Executar mab com braços com ranges aleatórios"):
  Arms = Arm(arm_quantity,max_reward)  
  fake_rewards = Arm.CreateArms(Arms)   
  mab_class = EgreedyMAB(Arms,arm_quantity,executions,epsilon,max_reward)
  rewards,choices_arms,all_rewards,regret,execution_times = EgreedyMAB.execute(mab_class)
  mostraTabela(fake_rewards)
  averages(rewards,all_rewards,regret,execution_times)
  frequency(all_rewards)
  pieChart(choices_arms)
  