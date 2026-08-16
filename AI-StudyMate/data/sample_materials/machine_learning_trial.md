# Machine Learning Trial Material

## Supervised Learning
Supervised learning uses labelled examples to learn a mapping between inputs and target outputs. Classification predicts discrete categories while regression predicts continuous numerical values.

## Logistic Regression
Logistic regression is a supervised classification algorithm. It estimates the probability of a class using the sigmoid function: p = 1 / (1 + e^-z). A probability threshold can be used to assign a class.

## Decision Trees
A decision tree predicts by repeatedly splitting data according to feature conditions. Internal nodes represent decisions, branches represent outcomes, and leaves represent predictions. Very deep trees can overfit.

## Gradient Descent
Gradient descent minimizes a loss function by updating parameters in the opposite direction of the gradient: theta_new = theta_old - learning_rate * gradient. A very large learning rate can be unstable while a very small learning rate can be slow.

## Neural Networks
A neural network has an input layer, hidden layers and an output layer. Neurons compute weighted sums followed by activation functions.

## Backpropagation
Backpropagation computes gradients of the loss with respect to model parameters using the chain rule from the output layer toward earlier layers. The gradients are used by an optimizer such as gradient descent.

## Classification Metrics
Accuracy is the proportion of correct predictions. Precision measures how many predicted positives are actually positive. Recall measures how many actual positives are identified. F1-score combines precision and recall using their harmonic mean.

## Overfitting
Overfitting occurs when a model learns training data too closely and performs poorly on unseen data. Regularization, simpler models, cross-validation, pruning and more data can reduce overfitting.
