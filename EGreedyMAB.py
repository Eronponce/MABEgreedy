import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import random as rand


#Percore pelo numero de braços criando falsos braços, onde cada   
# um tem um range possivel de recompensar o usuário
class Arm:
  def __init__(self,armQuantity,maxReward):
    self.armQuantity = armQuantity
    self.maxReward = maxReward
    self.fakeRewards = []
      
  def CreateArms(self):
    fakeArms = []
    for i in range(self.armQuantity):
      rewardRange = []
      randomNumber1 = rand.uniform(0,self.maxReward)
      randomNumber2 = rand.uniform(randomNumber1,self.maxReward)
      rewardRange.append(randomNumber1)
      rewardRange.append(randomNumber2)
      fakeArms.append(rewardRange)
    self.fakeRewards =fakeArms
    return(fakeArms)

  def GetMakespan(self,arm):
    return rand.uniform(self.fakeRewards[arm][0],self.fakeRewards[arm][1])
  

#retorna uma recompensa falsa como se fosse o operador genetico
class EgreedyMAB:
  def __init__(self,Arms,armQuantity,executions,epsilon,maxReward):
    self.armQuantity = armQuantity
    self.Arms = Arms
    self.executions = executions
    self.epsilon = epsilon
    self.maxReward = maxReward
     

  def execute(self):
    #cria uma variavel para a primeira iteração
    firstInteraction = True
    #instancia array de recompensas determinando cada braço
    rewards = [0] * self.armQuantity
    choicesArms = [0] * self.armQuantity
    regret = [[] for _ in range(self.armQuantity)] 
    allRewards = [[] for _ in range(self.armQuantity)]
    execution_times = [0] * self.armQuantity
    #Em cada execução ele gera um numero aleatorio conforme o 
    # epsilon e armazena a soma em rewards[]
    for i in range(self.executions):
      randomNumber = rand.uniform(0,1)
      if firstInteraction:
        armChoosen = rand.randint(0,self.armQuantity-1)
        firstInteraction = False
      else:
        if randomNumber > self.epsilon:  
          armChoosen = np.argmax(rewards)
        else:
    
          armChoosen = rand.randrange(len(rewards))

        # calculate regret for each arm
      expected_rewards = [rewards[i] if choicesArms[i] > 0 else 0 for i in range(self.armQuantity)]
      best_reward = max(expected_rewards)
      for i in range(self.armQuantity):
        if i == armChoosen:
          regret[i].append(best_reward - expected_rewards[i])
      
      tempReward = Arm.GetMakespan(self.Arms,armChoosen)
      tempSum =(rewards[armChoosen] +tempReward)/2
      execution_times[armChoosen] +=1
      #Guarda media das recompensas
      rewards[armChoosen] = tempSum
      #Guarda quantas vezes braço foi puxado
      choicesArms[armChoosen] += 1
      #Guarda todas as recompensas coletadas
      
      for i in range(self.armQuantity):
        
        if i == armChoosen:
          allRewards[armChoosen].append(tempSum)
        else:
         
          allRewards[i].append((rewards[i]))
    return(rewards,choicesArms,allRewards,regret,fakeRewards,execution_times)
  




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
  
  st.write("### Média,Moda,Mediana, regret padrão das recompensas e desvio ")
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
  df.loc["Regret"] = sumRegret
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
  rewards,choicesArms,allRewards,regret,fakeRewards,execution_times = EgreedyMAB.execute(mabClass)
  mostraTabela(fakeRewards)
  averages(rewards,allRewards,regret,execution_times)
  frequency(allRewards)
  pieChart(choicesArms)
  