import numpy as np
import helper
import warnings
import pandas as pd
import os
import sys


warnings.filterwarnings('ignore')

# TODO: change test_num
print('test num:')
for line in sys.stdin:
    test_num = int(line.rstrip())
    break
# print('percentage:')
# for line in sys.stdin:
#     perct = float(line.rstrip())
#     break
perct = 0.05
mod = 'lsl'

filename = 'data/retrospective_ova_JHU_proteome_sort_common_gene_7061.txt'
data, gene, sample = helper.getNormData(filename)
row, col = data.shape
# perct = 0.05
miss_row, miss_col = helper.pickMissIndex(row, col, perct, test_num)
# ALL missing values in pred are 0.0
pred = data.copy()
pred[miss_row, miss_col] = 0.0
pred[np.isnan(data)] = float('nan')

# Average imputation
avg = False
if avg:
    held = pred.copy()
    for d in pred:
        d[d == 0.0] = np.nanmean(d[np.nonzero(d)])
    perf = helper.performance(pred, data, held)
    print(perct, perf)

model = True
if model:
    fold = 5
    # ALL missing values in pred are 0.0
    pred = np.nan_to_num(pred)
    index = helper.crossValidation(fold, data.shape[1], test_num)

    hold_out_ftr = True
    average = False
    new_sample = []
    total_result = []
    total_held = []
    total_true = []
    out_f, clf = helper.getFileModel(
        hold_out_ftr, average, perct, test_num, mod)

    for idx in index:
        for sp in sample[idx]:
            new_sample.append(sp)
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
        total_held.append(result.copy())
        # original data with 5 fold
        total_true.append(data[:, idx])

        if average:
            # missing values in features are average values
            for tr, te in zip(train, test):
                tr[tr == 0] = np.nanmean(tr[np.nonzero(tr)])
                te[te == 0] = np.nanmean(te[np.nonzero(te)])
            # if all values are missing in the feature, fill them with 0
            train = np.nan_to_num(train)
            test = np.nan_to_num(test)

        for i in range(train.shape[0]):
            temp_idx = (~np.isnan(targets[i]))
            target = targets[i][temp_idx]
            feature = np.delete(train, i, 0)[:, temp_idx]
            # train
            if target.shape[0] is not 0:    
                clf.fit(np.transpose(feature), target)
            # test
            miss_pos = (result[i] == 0)
            feature = np.delete(test, i, 0)
            result[i][miss_pos] = clf.predict(np.transpose(feature))[miss_pos]
        
        total_result.append(result)
        print('done')

    total_result = np.concatenate(total_result, axis=1)
    total_held = np.concatenate(total_held, axis=1)
    total_true = np.concatenate(total_true, axis=1)

    helper.outputFile(total_result, out_f, gene, new_sample)
    helper.outputFile(total_held,
        'output/per_{}/held_{}.txt'.format(perct, test_num), gene, new_sample)
    helper.outputFile(total_true,
        'output/true_{}.txt'.format(test_num), gene, new_sample)

