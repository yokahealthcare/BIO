import numpy as np

# Experience Replay / Memory + More
class DQN:
    def __init__(self, maxMemory, gamma):
        self.maxMemory = maxMemory
        self.gamma = gamma
        self.memory = list()

    # Adding New Experience
    def remember(self, transition, gameOver):
        """
            VARIABLE INFORMATION:
            
            1. TRANSITION = [currentState, action, reward, nextState]
            
            2. currentState is also array = [11 elements for snake game]

        """
        self.memory.append([transition, gameOver])
        # check the maxMemory and delete the latest memory 
        if len(self.memory) > self.maxMemory:
            del self.memory[0]

    # Getting Batches of Inputs and Targets
    def getBatches(self, model, batchSize):
        lenMemory = len(self.memory)

        numInputs = self.memory[0][0][0].shape[1]
        numOutputs = model.output_shape[-1]


        # Initializing The Inputs and The Targets
        # np.zeros(ROW, COLUMN)
        inputs = np.zeros((min(batchSize, lenMemory), numInputs))
        targets = np.zeros((min(batchSize, lenMemory), numOutputs))

        # Extracting Transistions From Random Experiments
        for i, inx in enumerate(np.random.randint(0, lenMemory, size=min(batchSize, lenMemory))):
            currentState, action, reward, nextState = self.memory[inx][0]
            gameOver = self.memory[inx][1]

            # Updating Inputs and Tragets
            inputs[i] = currentState
            targets[i] = model.predict(currentState)[0] # get only output at index 0
            if gameOver:
                targets[i][action] = reward
            else:
                targets[i][action] = reward + self.gamma * np.max(model.predict(nextState)[0])


        return inputs, targets

        # INPUTS    : is input that goes in neural network
        # TARGETS   : is Q-values goes out neural network