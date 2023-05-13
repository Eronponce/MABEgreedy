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
  
  #retorna uma recompensa falsa como se fosse o operador genetico
  def GetMakespan(self,arm):
    return rand.uniform(self.fakeRewards[arm][0],self.fakeRewards[arm][1])
  
