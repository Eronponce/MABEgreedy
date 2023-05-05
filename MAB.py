import streamlit as st
import random as rand
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#percore pelo numero de braços criando falsos braços, onde cada   
# um tem um range possivel de recompensar o usuário
def fakeArm(bracos,maxReward):
  fakeArms = []
  for i in range(bracos):
    rewardRange = []
    randomNumber1 = rand.uniform(0,maxReward)
    randomNumber2 = rand.uniform(randomNumber1,maxReward)
    rewardRange.append(randomNumber1)
    rewardRange.append(randomNumber2)
    fakeArms.append(rewardRange)
  return (fakeArms)

#retorna uma recompensa falsa como se fosse o operador genetico
def fakePull(arm):
  return rand.uniform(fakeRewards[arm][0],fakeRewards[arm][1])

def mab(bracos,execucoes,epsilon):
  #cria uma variavel para a primeira iteração
  firstInteraction = True
  #instancia array de recompensas determinando cada braço
  rewards = [0] * bracos
  choicesArms = [0] * bracos
  allRewards = [[] for _ in range(bracos)]
  #Em cada execução ele gera um numero aleatorio conforme o 
  # epsilon e armazena a soma em rewards[]
  for i in range(execucoes):
    randomNumber = rand.uniform(0,epsilon)
    if firstInteraction:
      armChoosen = rand.randint(0,bracos-1)
      firstInteraction = False
    else:
      if randomNumber < epsilon:
        armChoosen = rand.randint(0,bracos-1)
      else:
        armChoosen = np.argmax(rewards)
    tempReward = fakePull(armChoosen)
    tempSum =(rewards[armChoosen] +tempReward)/2
    #Guarda media das recompensas
    rewards[armChoosen] = tempSum
    #Guarda quantas vezes braço foi puxado
    choicesArms[armChoosen] += 1
    #Guarda todas as recompensas coletadas
    allRewards[armChoosen].append(tempSum)
  return(rewards,choicesArms,allRewards)
        
        

#streamlit


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

def mostraDados(reward,choices,allrewards):
  st.write("### Frequência de recompensas")
  df = pd.DataFrame(allrewards).T
  df.columns = [f"Braço {i+1}" for i in range(len(allrewards))]
  df.index.name = "Execução"
  st.line_chart(df)
  
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

  # Find the index of the largest non-zero choice
  max_choice = max(choices)
  explode_index = choices.index(max_choice)

  # Create a list of values for the explode parameter
  explode = [0] * len(choices)
  explode[explode_index] = 0.1
  st.write(ex)
  ax1.pie(non_zero_choices, labels=non_zero_labels, autopct=format_autopct, textprops={'color': 'white'}, explode=explode)
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

  st.pyplot(fig1)


  #Traceback (most recent call last):
  File "C:\Users\eronp\.conda\envs\MABEgreedy\lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 565, in _run_script
    exec(code, module.__dict__)
  File "C:\Users\eronp\.conda\envs\MABEgreedy\MAB.py", line 148, in <module>
    mostraDados(rewards,choicesArms,allRewards)
  File "C:\Users\eronp\.conda\envs\MABEgreedy\MAB.py", line 105, in mostraDados
    ax1.pie(non_zero_choices, labels=non_zero_labels, autopct=format_autopct, textprops={'color': 'white'}, explode=explode)
  File "C:\Users\eronp\.conda\envs\MABEgreedy\lib\site-packages\matplotlib\__init__.py", line 1472, in inner
    return func(ax, *map(sanitize_sequence, args), **kwargs)
  File "C:\Users\eronp\.conda\envs\MABEgreedy\lib\site-packages\matplotlib\axes\_axes.py", line 3211, in pie
    raise ValueError("'explode' must be of length 'x'")

  # Create a DataFrame from the reward data
  df = pd.DataFrame(reward).T
  df.columns = [f"Braço {i+1}" for i in range(len(reward))]
  df.index.name = "Execução"

  # Create a bar chart of the average reward for each arm
  plt.bar(df.columns, df.values[0])

  # Set chart title and axis labels
  plt.title("Recompensa média de cada braço")
  plt.xlabel("Braços")
  plt.ylabel("Recompensa média")

  # Display the chart
  st.write(plt.show())
  
  st.write(np.median(reward))



  

 


st.sidebar.title("Configurar MAB")
epsilon =  st.sidebar.slider("Epsilon",0.0,1.0)
st.title("MAB em funcionamento")
execucoes = st.sidebar.number_input("numeros de execuções",min_value= 1,step=1)
maxReward = st.sidebar.number_input("Maximo de recompensa",min_value= 1,step=1)
quantidadeBracos = st.sidebar.number_input("Quantidade de braços",min_value= 1,step=1)
if st.sidebar.button("Executar mab com braços com ranges aleatórios"):
  fakeRewards = fakeArm(quantidadeBracos,maxReward)            
  rewards,choicesArms,allRewards = mab(quantidadeBracos,execucoes,epsilon)
  mostraTabela(fakeRewards)
  mostraDados(rewards,choicesArms,allRewards)