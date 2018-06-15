import numpy as np
import helper
from sklearn import svm, linear_model
from sklearn.tree import DecisionTreeRegressor
import warnings
import pandas as pd
import os


warnings.filterwarnings('ignore')

filename = 'data/retrospective_ova_JHU_proteome_sort_common_gene_7061.txt'
data, gene, sample = helper.getNormData(filename)
row, col = data.shape
perct = 0.1
miss_row, miss_col = helper.pickMissIndex(row, col, perct)
# ALL missing values in pred are 0.0
pred = data.copy()
pred[miss_row, miss_col] = 0.0
pred[np.isnan(data)] = float('nan')

# Average imputation
avg = False
if avg:
    num_missing = []
    for d in pred:
        num_missing.append(np.sum(d == 0.0))
        d[d == 0.0] = np.nanmean(d[np.nonzero(d)])
    perf = helper.performance(pred, data, np.array(num_missing))
    print(perf)

model = True
if model:
    fold = 5
    # ALL missing values in pred are 0.0
    pred = np.nan_to_num(pred)
    index = helper.crossValidation(fold, data.shape[1])

    hold_out_ftr = True
    average = True

    for f, idx in enumerate(index):
        targets = np.delete(data, idx, 1)
        if hold_out_ftr:
            # 5% data are taken away in the feature
            # original missing values in target are filled with 0
            train = np.delete(pred, idx, 1)
        else:
            # 5% data are NOT taken away in the feature
            # original missing values in target are filled with 0
            # missing values are 0 in training feature
            train = np.nan_to_num(np.delete(data, idx, 1))
        test = pred[:, idx]
        result = pred[:, idx].copy()
        result[np.isnan(data[:, idx])] = float('nan')
        # 5 fold cross validation, values held out are 0
        f_name = 'result/per_{}/data_{}.txt'.format(perct, f)
        helper.outputFile(result, f_name, gene, list(sample[idx]))
        # original data with 5 fold
        f_name = 'result/data_{}.txt'.format(f)
        helper.outputFile(data[:, idx], f_name, gene, list(sample[idx]))

        if average:
            # missing values in features are average values
            for tr, te in zip(train, test):
                tr[tr == 0] = tr[np.nonzero(tr)].mean()
                te[te == 0] = te[np.nonzero(te)].mean()
            # if all values are missing in the feature, fill them with 0
            train = np.nan_to_num(train)
            test = np.nan_to_num(test)

        num_missing = []
        out_f, clf = helper.getFileModel(hold_out_ftr, average, perct, f, 'svr')

        for i in range(train.shape[0]):
            temp_idx = (~np.isnan(targets[i]))
            target = targets[i][temp_idx]
            feature = np.delete(train, i, 0)[:, temp_idx]
            # train
            if target.shape[0] is not 0:    
                clf.fit(np.transpose(feature), target)
            # test
            miss_pos = (result[i] == 0)
            num_missing.append(np.sum(miss_pos))
            feature = np.delete(test, i, 0)
            result[i][miss_pos] = clf.predict(np.transpose(feature))[miss_pos]

        helper.outputFile(result, out_f, gene, list(sample[idx]))
        perf = helper.performance(result, data[:, idx], np.array(num_missing))
        print(perf)
