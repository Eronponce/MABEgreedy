import random as rand

# Traverse through the number of arms and create fake arms,
# where each arm has a possible reward range for the user
class Arm:
		def __init__(self, arm_quantity):
				self.arm_quantity = arm_quantity
				self.fake_rewards = []
				
		def CreateArms(self):
				fake_arms = []
				for i in range(self.arm_quantity):
						reward_range = []
						
						# Generate two random numbers to define the reward range
						random_number_1 = rand.uniform(0, 100)
						random_number_2 = rand.uniform(random_number_1, 100)
						
						# Append the reward range to the list of fake arms
						reward_range.append(random_number_1)
						reward_range.append(random_number_2)
						fake_arms.append(reward_range)
				
				# Store the fake rewards in the instance variable
				self.fake_rewards = fake_arms
				
				return fake_arms

		# Return a fake reward as if it were the genetic operator
		def GetMakespan(self, arm):
				return rand.uniform(self.fake_rewards[arm][0], self.fake_rewards[arm][1])
