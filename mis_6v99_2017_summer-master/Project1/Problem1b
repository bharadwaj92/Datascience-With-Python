'''
/*(b) [10 points] We have provided two data files:
• http://cs229.stanford.edu/ps/ps1/logistic_x.txt
• http://cs229.stanford.edu/ps/ps1/logistic_y.txt
These files contain the inputs (x(i) ∈ R2) and outputs (y(i) ∈ {−1, 1}), respectively for a
binary classification problem, with one training example per row. Implement Newton’s
method for optimizing J(θ), and apply it to fit a logistic regression model to the data.
Initialize Newton’s method with θ = ~0 (the vector of all zeros). What are the coefficients θ
resulting from your fit? (Remember to include the intercept term.)
'''
from urllib.request import urlopen
import numpy as np
from operator import add
import numdifftools


class LogisticRegression():
    theta = [5,5,5]

    def sigmoid(self, x, theta):
        z = np.array([(np.dot(x[i], theta[0:x.shape[1]])) for i in range(len(x))])  ## calculates the sigmoid probability 1/(1+ e^-z) where z = theta1 * x1 + theta2*x2 ... + thetan*xn
        return 1.0 / (1.0 + np.exp(-z))

    def log_likelihood(self, x, y, theta):
        sigmoid_probs = self.sigmoid(x, theta)
        #print(sigmoid_probs)
        return y * np.log(sigmoid_probs) + (1 - y) * np.log(1 - sigmoid_probs)  # defines function that calculates y*log(p) + (1-y)(log(1-p)

    def gradient(self,x, y, theta):
        sigmoid_probs = self.sigmoid(x, theta)
        #print(np.transpose(np.array([y - sigmoid_probs])))
        return np.transpose(np.matmul(np.transpose(x), np.transpose(np.array([sigmoid_probs - y]))))  ## calculates derivate  XT(H(theta) - y)

    def hessian(self,x, theta):
        sigmoid_probs = self.sigmoid(x, theta)
        return np.array(np.matmul(np.transpose(x), np.matmul(np.diag(sigmoid_probs * (1 - sigmoid_probs)), x))) ## Calculates second order derivate of cost function : XT*(diag(H(theta)*(1-H(theta))*X 

    def fit(self, x , y, iterations):
        deltal = np.Infinity
        convergence = 0.00000001
        maxiterations = iterations
        i= 0
        l = self.log_likelihood(x , y , self.theta)
        while( deltal > convergence and i < maxiterations):
            gradients = self.gradient(x , y , self.theta)
            #print(gradients)
            hessians = self.hessian(x , self.theta)
            H_inv = np.linalg.inv(hessians)
            #print(H_inv)
            #delta = H_inv @ gradients.T
            delta = np.dot(H_inv, gradients.T)
            #print(delta)
            self.theta = np.array(list(map(add, gradients, delta))).reshape(3,)
            print(self.theta)
            lnew = self.log_likelihood(x , y , self.theta)
            deltal = l - lnew
            l = lnew
        return self.theta

class DataCleaning():

    def read_data_files(self):
        xarray = []
        yarray = []
        xUrl = "http://cs229.stanford.edu/ps/ps1/logistic_x.txt"
        yUrl = "http://cs229.stanford.edu/ps/ps1/logistic_y.txt"
        textData = urlopen(xUrl)
        for line in textData:
            if (line.strip() != ""):
                line = line.decode('utf-8').strip()
                temp = line.split("  ")
                x = []
                x.append(float(temp[0]))
                x.append(float(temp[1]))
                x.append(1)
                xarray.append(x)
        yData = urlopen(yUrl)
        for line in yData:
            if (line.strip() != ""):
                line = line.decode('utf-8').strip()
                yarray.append(float(line))
        x = np.array(xarray)
        y = np.array(yarray)
        return x , y

if __name__ == "__main__":
    d = DataCleaning()
    x , y  = d.read_data_files()
    lr = LogisticRegression()
    lr.fit(x, y , 1)
