""" Generate training and testing set. """
import random
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn import svm, linear_model
from sklearn.tree import DecisionTreeRegressor


def getRealData(filename):
    """ Read gene data from file. """
    df = pd.read_csv(filename, index_col=0, sep='\t')
    return df

def getNormData(filename):
    """ Read data from file and set values to positive. 
        Missing values in original data are filled with nan. """
    df = getRealData(filename)
    data = np.array(df)
    d_min = data[~np.isnan(data)].min()
    if d_min < 0:
        data += ((-1.01) * d_min)
    return data, df.index.tolist(), np.array(df.columns.tolist())

def outputFile(data, filename, rows, cols):
    df = pd.DataFrame(data, index=rows, columns=cols)
    df.index.name="Gene_ID"
    df.to_csv(filename, sep="\t")

def pickMissIndex(row, column, percentage):
    """ Return array of row and column of simulated miising positions
        of the data matrix. """
    random.seed(169722497)
    idx_row = []
    idx_col = []
    for i in range(int(row * column * percentage)):
        index = int(row * column * random.random())
        idx_row.append(int(index / column))
        idx_col.append(int(index % column))
    return np.array(idx_row), np.array(idx_col)

# def holdOutLow(data, percentage):
#     random.seed(3620582)
#     avg = np.nanmean(data, axis=1)
#     ref = avg.mean()

def crossValidation(fold, column):
    """ Return a list of cross validation sets. """
    random.seed(243183448)
    index = list(range(column))
    random.shuffle(index)
    sets = []
    size = int(column / fold) + 1
    for i in range(fold):
        sets.append(index[i * size: min((i + 1) * size, column + 1)])
    return np.array(sets)

def getFileModel(hold_out_feature, average, perct, idx, mdl):
    """ Return the path the result is output to and the machine
        learning model. """
    # cat = ''
    # if hold_out_feature and not average:
    #     cat = 'sub_0'
    # elif hold_out_feature and average:
    #     cat = 'sub_avg'
    # elif not hold_out_feature and not average:
    #     cat = 'full_0'
    # else:
    #     cat = 'full_avg'
    cat = 'per_{}'.format(perct)
    print('method: '+cat+'\tmodel: '+mdl)
    models = {
        'svr': svm.SVR(),
        'lsl': linear_model.LassoLars(),
        'lr': linear_model.LinearRegression(),
        'dt': DecisionTreeRegressor()
    }
    filename = 'result/'+cat+'/'+mdl+'_'+str(idx)+'.txt'
    return filename, models[mdl]

def performance(result, true, num_missing):
    """ Calculate nrmse as performance of imputation.
        Only take missing values that are manually taken out into consideration.
        (i.e. Missings in original data are ignored.) """
    error = true - result
    error[np.isnan(error)] = 0.0
    rmse = (error ** 2).sum(axis=1)
    t_diff = []
    for t in true:
        if len(t[np.isnan(t)]) is not len(t):
            t_max = t[~np.isnan(t)].max()
            t_min = t[~np.isnan(t)].min()
            t_diff.append(t_max - t_min)
        else:
            t_diff.append(0.0)
    t_diff = np.array(t_diff)
    nrmse = np.sqrt(rmse / num_missing)  / t_diff
    nrmse[num_missing == 0] = 0.0 # no missing value
    nrmse[t_diff == 0.0] = 0.0 # all missings are true missings
    return nrmse.mean()


def correlation(result, true, held):
    """ Calculate Pearson correlation of missing values.
        Only take missing values that are manually taken out into consideration.
        (i.e. Missings in original data are ignored.) """
    corr = []
    for r, t, h in zip(result, true, held):
        miss_pos = (h == 0.0)
        if np.sum(miss_pos) > 2:
            prs = pearsonr(r[miss_pos], t[miss_pos])[0]
            # corr.append(prs/(np.sum(miss_pos)-1))
            corr.append(prs)
    corr = np.array(corr)[~np.isnan(np.array(corr))]
    return np.mean(corr)

