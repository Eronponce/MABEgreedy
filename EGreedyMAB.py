import numpy as np
import random as rand

class EgreedyMAB:
	def __init__(self, Arms, arm_quantity, executions, epsilon):
		self.arm_quantity = arm_quantity
		self.Arms = Arms
		self.executions = executions
		self.epsilon = epsilon

	def execute(self):
		# Create a variable for the first interaction
		first_interaction = True
		
		# Instantiate arrays to store rewards for each arm
		rewards = [0] * self.arm_quantity
		choices_arms = [0] * self.arm_quantity
		
		# List to store the regret for each arm
		regret = [[] for _ in range(self.arm_quantity)]
		
		# List to store all the rewards collected for each arm
		all_rewards = [[] for _ in range(self.arm_quantity)]
		
		# List to store the number of times each arm was executed
		execution_times = [0] * self.arm_quantity

		# In each execution, generate a random number according to epsilon and choose an arm
		for i in range(self.executions):
			random_number = rand.uniform(0, 1)
			
			if first_interaction:
				# Choose a random arm for the first interaction
				arm_chosen = rand.randint(0, self.arm_quantity - 1)
				first_interaction = False
			else:
				if random_number > self.epsilon:
					# Exploit: Choose the arm with the highest estimated reward
					arm_chosen = np.argmax(rewards)
				else:
					# Explore: Choose a random arm
					arm_chosen = rand.randrange(len(rewards))

			# Calculate regret for each arm
			expected_rewards = [rewards[i] if choices_arms[i] > 0 else 0 for i in range(self.arm_quantity)]
			best_reward = max(expected_rewards)
			
			for i in range(self.arm_quantity):
				if i == arm_chosen:
					regret[i].append(best_reward - expected_rewards[i])

			# Get the reward for the chosen arm from the Arms class
			temp_reward = self.Arms.GetMakespan(arm_chosen)
			
			# Calculate the updated average reward for the chosen arm
			temp_sum = (rewards[arm_chosen] + temp_reward) / 2
			
			# Increment the execution count for the chosen arm
			execution_times[arm_chosen] += 1
			
			# Update the average reward for the chosen arm
			rewards[arm_chosen] = int(temp_sum)
			
			# Increment the number of times the chosen arm was chosen
			choices_arms[arm_chosen] += 1
			
			# Store the average reward for the chosen arm in all_rewards
			all_rewards[arm_chosen].append(temp_sum)
			
			# Store the rewards for the other arms in all_rewards
			for i in range(self.arm_quantity):
				if i != arm_chosen:
					all_rewards[i].append(rewards[i])
		
		return rewards, choices_arms, all_rewards, regret, execution_times
