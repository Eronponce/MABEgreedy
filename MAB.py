import streamlit as st
import random as rand
import numpy as np
import pandas as pd

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
    #instancia array de recompensas determinando cada braço
    rewards = [0] * bracos
    choicesArms = [0] * bracos
    allRewards = [None] * bracos
    #Em cada execução ele gera um numero aleatorio conforme o 
    # epsilon e armazena a soma em rewards[]
    for i in range(execucoes):
        randomNumber = rand.uniform(0,epsilon)
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
        tempRewards = []
        tempRewards.append(allRewards[armChoosen])
        tempRewards.append(tempSum)
         #Guarda todas as recompensas coletadas
        allRewards[armChoosen] = tempRewards
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

def MostrarInfo(allRewards, quantidadeBracos):
  # create a list of column names for the DataFrame
  column_names = [f"Arm {i+1}" for i in range(quantidadeBracos)]

  # create a list to store the rewards for each arm at each time step
  reward_data = [[] for _ in range(quantidadeBracos)]

  # loop through the nested list of rewards and extract the rewards for each arm at each time step
  for arm_rewards in allRewards:
      for i, reward in enumerate(arm_rewards):
          if reward is not None:
              reward_data[i].append(reward[1])
          else:
              reward_data[i].append(None)

  # create a pandas DataFrame with the reward data
  reward_df = pd.DataFrame(reward_data, columns=column_names)

  # display the DataFrame
  st.line_chart(reward_df)



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
    MostrarInfo(allRewards,quantidadeBracos)