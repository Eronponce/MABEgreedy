import numpy as np
import random as rand

class EgreedyMAB:
  def __init__(self,Arms,arm_quantity,executions,epsilon,max_reward):
    self.arm_quantity = arm_quantity
    self.Arms = Arms
    self.executions = executions
    self.epsilon = epsilon
    self.max_reward = max_reward
     

  def execute(self):
    #cria uma variavel para a primeira iteração
    first_interaction = True
    #instancia array de recompensas determinando cada braço
    rewards = [0] * self.arm_quantity
    choices_arms = [0] * self.arm_quantity
    regret = [[] for _ in range(self.arm_quantity)] 
    all_rewards = [[] for _ in range(self.arm_quantity)]
    execution_times = [0] * self.arm_quantity
    #Em cada execução ele gera um numero aleatorio conforme o 
    # epsilon e armazena a soma em rewards[]
    for i in range(self.executions):
      random_number = rand.uniform(0,1)
      if first_interaction:
        arm_choosen = rand.randint(0,self.arm_quantity-1)
        first_interaction = False
      else:
        if random_number > self.epsilon:  
          arm_choosen = np.argmax(rewards)
        else:
    
          arm_choosen = rand.randrange(len(rewards))

        # calculate regret for each arm
      expected_rewards = [rewards[i] if choices_arms[i] > 0 else 0 for i in range(self.arm_quantity)]
      best_reward = max(expected_rewards)
      for i in range(self.arm_quantity):
        if i == arm_choosen:
          regret[i].append(best_reward - expected_rewards[i])
      
      temp_reward = self.Arms.GetMakespan(arm_choosen)
      temp_sum =(rewards[arm_choosen] +temp_reward)/2
      execution_times[arm_choosen] +=1
      #Guarda media das recompensas
      rewards[arm_choosen] = temp_sum
      #Guarda quantas vezes braço foi puxado
      choices_arms[arm_choosen] += 1
      #Guarda todas as recompensas coletadas
      
      for i in range(self.arm_quantity):
        
        if i == arm_choosen:
          all_rewards[arm_choosen].append(temp_sum)
        else:
         
          all_rewards[i].append((rewards[i]))
    return(rewards,choices_arms,all_rewards,regret,execution_times)
  



