class PythonGradientDescent:
    def __init__(self):
        self.learningRate = 0.01
        self.maxIterations = 5000
        self.costHistory = []
        self.performedIterations = 0
        self.weights = []
        self.bias = 0

    def is_nan(self, num):
        return num != num

    def initialize_weights_with_zeros(self, size):
        self.weights = [0] * size

    def fit(self, input_matrix, actual_values):
        self.initialize_weights_with_zeros(len(input_matrix[0]))

        self.costHistory = []
        self.costHistory.append(self.cost_function(input_matrix, actual_values))

        self.performedIterations = 0

        while not self.has_converged() and self.performedIterations <= self.maxIterations:
            self.update_weights(input_matrix, actual_values)
            self.costHistory.append(self.cost_function(input_matrix, actual_values))
            self.performedIterations += 1

    def cost_function(self, input_matrix, actual_values):
        predicted_values = self.hypothesis_function(input_matrix)
        squared_errors = [(actual_values[i] - predicted_values[i]) ** 2 for i in range(len(actual_values))]
        return sum(squared_errors) / len(squared_errors) / 2

    def has_converged(self):
        if len(self.costHistory) == 0:
            return False
        if len(self.costHistory) < 2:
            return False
        precision = 1e-10

        current_cost = self.costHistory[len(self.costHistory) - 1]
        previous_cost = self.costHistory[len(self.costHistory) - 2]

        difference = current_cost - previous_cost

        if difference > 0 or self.is_nan(difference):
            raise Exception("Model is starting to diverge")

        return (abs(current_cost) < precision) or (abs(difference) < precision)

    def update_weights(self, input_matrix, actual_values):
        predicted_output_vector = self.hypothesis_function(input_matrix)

        cost_derivative = self.cost_derivative(predicted_output_vector, actual_values)
        weight_derivative = self.weight_derivative(input_matrix, cost_derivative)

        bias_derivative = self.bias_derivative(cost_derivative)

        learning_rate_times_weight_derivative = [x * self.learningRate for x in weight_derivative]

        self.weights = [(self.weights[i] - learning_rate_times_weight_derivative[i]) for i in range(len(self.weights))]
        self.bias = self.bias - (self.learningRate * bias_derivative)

    def cost_derivative(self, predicted_output_vector, target_output_vector):
        derivatives = []
        for i in range(len(predicted_output_vector)):
            derivative = predicted_output_vector[i] - target_output_vector[i]
            derivatives.append(derivative)
        return derivatives

    def bias_derivative(self, cost_derivative):
        return sum(cost_derivative) / len(cost_derivative)

    def weight_derivative(self, inputMatrix, costDerivativeVector):
        weightDerivative = []
        for i in range(len(inputMatrix)):
            rowTimesVector = [inputMatrix[i][j] * costDerivativeVector[i] for j in range(len(inputMatrix[i]))]
            weightDerivative.append(rowTimesVector)

        answer = []
        for column in range(len(weightDerivative[0])):
            sum = 0
            for row in weightDerivative:
                sum += row[column]
            answer.append(sum)
        return [(element / len(costDerivativeVector)) for element in answer]

    def predict(self, inputMatrix):
        return self.hypothesis_function(inputMatrix)

    def hypothesis_function(self, inputMatrix):
        return self.weighted_sum(inputMatrix)

    def weighted_sum(self, inputMatrix):
        weightedSum = []
        for i in range(len(inputMatrix)):
            listsMultiplication = [inputMatrix[i][j] * self.weights[j] for j in range(len(self.weights))]
            weightedSum.append(sum(listsMultiplication) + self.bias)
        return weightedSum
