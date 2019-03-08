import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from argparse import ArgumentParser
from scipy import sparse
from scipy import linalg
import sys

parser = ArgumentParser(description= 'send input files')
parser.add_argument('train_feat', type=str)
parser.add_argument('train_target', type=str)
parser.add_argument('dev_feat', type=str)
parser.add_argument('dev_target', type=str)

args = parser.parse_args()

train_data = []
train_row = []
train_col = []

dev_data = []
dev_row = []
dev_col = []

#calculate number of columns matrix. (meaning: n x m ----- it'll return m)
def getCols(filename):
    with open(filename) as fileobj:
        line = fileobj.readline()
        line_list = line.split(' ')
    return len(line_list)
#calculate number of rows matrix. (maining: n x m ----- it'll return n)
def getRows(filename):
    with open(filename) as fileobj:
        counter = 0
        for line in fileobj:
            counter += 1
    return counter
# return double array that is in the same order as in the file
def createMatrixTrain(filename):
    with open(filename) as fileobj:
        for line in fileobj:
            line_list = line.split(' ')
            train_row.append(float(line_list[0]))
            train_col.append(float(line_list[1]))
            train_data.append(float(line_list[2]))

def createMatrixDev(filename):
    with open(filename) as fileobj:
        for line in fileobj:
            line_list = line.split(' ')
            dev_row.append(float(line_list[0]))
            dev_col.append(float(line_list[1]))
            dev_data.append(float(line_list[2]))


def createArray(filename):
    newArray = []
    string = ''
    with open(filename) as fileobj:
        for line in fileobj:
            line_list = line.split(' ')
            for i in range(len(line_list)):
                newArray.append(float(line_list[i]))
    return newArray



# turn files into double arrays
createMatrixTrain(args.train_feat)
t_data = np.asarray(train_data)
t_row = np.asarray(train_row)
t_col = np.asarray(train_col)


train_targ = createArray(args.train_target)
t_targ = np.asarray(train_targ)
print("train_targ", len(train_targ))

dev_set = createMatrixDev(args.dev_feat)
d_data = np.asarray(dev_data)
d_row = np.asarray(dev_row)
d_col = np.asarray(dev_col)


dev_targ = createArray(args.dev_target)
d_targ = np.asarray(dev_targ)
print("dev_targ", len(dev_targ))

training_set = sparse.coo_matrix((t_data, (t_row, t_col) ), shape=(len(train_targ),75000)).tocsc()
development_set = sparse.coo_matrix((d_data, (d_row, d_col) ), shape=(len(dev_targ),75000)).tocsc()

lasso = linear_model.Lasso(alpha=0.1)
lasso.fit(training_set, train_targ)

my_pred = reg.predict(development_set)

print('Coefficients: \n', r.coef_)

print('mean squared error: %.2f' % mean_squared_error(dev_targ, my_pred))

print('variance score: %.2f' % r2_score(dev_targ, my_pred))
