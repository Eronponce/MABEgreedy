import random as rand


#Percore pelo numero de braços criando falsos braços, onde cada   
# um tem um range possivel de recompensar o usuário
class Arm:
  def __init__(self,arm_quantity,max_reward):
    self.arm_quantity = arm_quantity
    self.max_reward = max_reward
    self.fake_rewards = []
      
  def CreateArms(self):
    fake_arms = []
    for i in range(self.arm_quantity):
      reward_range = []
      random_number_1 = rand.uniform(0,self.max_reward)
      random_number_2 = rand.uniform(random_number_1,self.max_reward)
      reward_range.append(random_number_1)
      reward_range.append(random_number_2)
      fake_arms.append(reward_range)
    self.fake_rewards = fake_arms
    return(fake_arms)
  
  #retorna uma recompensa falsa como se fosse o operador genetico
  def GetMakespan(self,arm):
    return rand.uniform(self.fake_rewards[arm][0],self.fake_rewards[arm][1])
  
