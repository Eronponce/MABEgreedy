import numpy as np
import random as rand

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
      
      tempReward = self.Arms.GetMakespan(armChoosen)
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
    return(rewards,choicesArms,allRewards,regret,execution_times)
  



