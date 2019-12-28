import numpy as np

class NeuralNetwork():

    def __init__(self):
        # Seed the random number generator
        #np.random.seed(1)

        # todo: possibly change this to output list of neural networks equal to number of ufos

        # Set input layer synaptic weights to a 1x3 matrix and hidden layer biases to a 1x6 matrix
        self.weights_input = 2 * np.random.random((1, 3)) - 1  # from -1 to 1
        self.biases_hidden = 2 * np.random.random((1, 6)) - 1  # from -1 to 1

        # Set hidden layer synaptic weights to a 1x6 matrix and output layer biases to a 1x2 matrix
        self.weights_hidden = 2 * np.random.random((1, 6)) - 1  # from -1 to 1
        self.biases_output = 2 * np.random.random((1, 2)) - 1  # from -1 to 1

    def print_state(self):
        # input
        print("-------------------\nInitial input weights: ")
        print(self.weights_input)
        print("Initial hidden biases: ")
        print(self.biases_hidden)

        # hidden
        print("Initial hidden weights: ")
        print(self.weights_hidden)
        print("Initial output biases: ")
        print(self.biases_output)
        print("-------------------")

    @staticmethod
    def sigmoid(x):
        """
        Takes in weighted sum of the inputs and normalizes
        them through between 0 and 1 through a sigmoid function
        """
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_derivative(x):
        """
        The derivative of the sigmoid function used to
        calculate necessary weight adjustments
        """
        return x * (1 - x)

    def think(self, inputs):
        """
        Pass inputs through the neural network to get output
        """
        inputs = inputs.astype(float)
        hidden_layer_nodes = np.empty([1, 6])
        output = np.empty([1, 2])

        # Get hidden layer values
        for i, weight in enumerate(hidden_layer_nodes.flatten()):
            summation = 0
            for j, feature in enumerate(inputs.flatten()):
                summation += self.weights_input[0][j]*feature
            summation += self.biases_hidden[0][i]
            hidden_layer_nodes[0][i] = self.sigmoid(summation)

        # Get output layer values
        for i, weight in enumerate(output.flatten()):
            summation = 0
            for j, feature in enumerate(hidden_layer_nodes.flatten()):
                summation += self.weights_hidden[0][j]*feature
            summation += self.biases_output[0][i]
            output[0][i] = self.sigmoid(summation)

        return output

class NeuralNetworkTrainer():

    def __init__(self, amount):
        self.NumberOfNN = amount
        self.NNList = [NeuralNetwork() for count in range(self.NumberOfNN)]
        self.generation = 1

    def train(self, dead_parents):
        print("Top of generation " + str(self.generation) + " was a score of " + str(dead_parents[self.NumberOfNN-1][1]))
        dead_parents[self.NumberOfNN-1][0].print_state()
        #self.print_generation()
        self.generation += 1

        randomChildern = self.NumberOfNN//4
        parentsWithChildern = dead_parents[randomChildern:]

        # create overwrite NNList with new generation
        self.NNList = []
        self.NNList = [NeuralNetwork() for count in range(randomChildern)]

        for parent in parentsWithChildern:
            num = np.random.randint(1, 18)
            if num <= 3:
                # change input weights
                indexToChange = num - 1
                parent[0].weights_input[0][indexToChange] = 2 * np.random.random() - 1

            num = np.random.randint(1, 18)
            if num > 3 and num <= 9:
                # change hidden biases
                indexToChange = num - 4
                parent[0].biases_hidden[0][indexToChange] = 2 * np.random.random() - 1

            num = np.random.randint(1, 18)
            if num > 9 and num <=15:
                # change hidden weights
                indexToChange = num - 10
                parent[0].weights_hidden[0][indexToChange] = 2 * np.random.random() - 1

            num = np.random.randint(1, 18)
            if num > 15:
                # change output biases
                indexToChange = num - 16
                parent[0].biases_output[0][indexToChange] = 2 * np.random.random() - 1

            self.NNList.append(parent[0])

    def print_generation(self):
        print("=======================================GENERATION " + str(self.generation) + "================================================")
        for NN in self.NNList:
            NN.print_state()
        print("==========================================================================================================================")





if __name__ == "__main__":
    neural_network = NeuralNetwork()
    neural_network.print_state()

    A = str(input("Input 1: "))
    B = str(input("Input 2: "))
    C = str(input("Input 3: "))

    print("output data: ")
    print(neural_network.think(np.array([A, B, C])))

