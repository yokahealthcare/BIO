from snake_brain import Brain
from snake_dqn import DQN
import gym
import numpy as np
import matplotlib.pyplot as plt

# setting the parameters
learningRate = 0.001
maxMemory = 5000
gamma = 0.9 # discount value
batchSize = 32
epsilon = 1. # using epsilon-greedy method (this will totally random chooser)
epsilonDecayRate = 0.995


# intitalizing the environment, the Brain and the Experience Replay Memory
env = gym.make('MountainCar-v0')
brain = Brain(2, 3, learningRate)
model = brain.model
DQN = DQN(maxMemory, gamma)

# Starting the game
epoch = 0
currentState = np.zeros((1, 2))
nextState = currentState
totReward = 0 # total reward
rewards = list() # store total rewards from each game

while True:
	epoch += 1

	# play the game
	env.reset()
	currentState = np.zeros((1, 2))
	nextState = currentState
	gameOver = False

	while not gameOver:
		# taking actions
		if np.random.rand() <= epsilon: # smart algorithm epsilon-greedy
			action = np.random.randint(0,3)
		else:
			qvalues = model.predict(currentState)[0]
			action = np.argmax(qvalues)


		# updating the environment
		nextState[0], reward, gameOver, _ = env.step(action)
		env.render() # show the game

		totReward += reward # adding to reward

		# remembering new experience, training the AI and updating current state
		DQN.remember([currentState, action, reward, nextState], gameOver)
		inputs, targets = DQN.getBatches(model, batchSize)
		model.train_on_batch(inputs, targets)

		currentState = nextState

	# lowering the epsilon and displaying the result
	epsilon *= epsilonDecayRate

	rewards.append(totReward)
	print("Epoch : {}; Epsilon : {:.5f}; Total Reward: {:.2f}; Rewards: {:.2f}".format(epoch, epsilon, totReward, rewards[-1]))

	totReward = 0
	#plt.plot(rewards)
	#plt.xlabel("Epoch")
	#plt.ylabel("Rewards")
	#plt.show()

env.close()







