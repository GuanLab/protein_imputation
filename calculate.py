import numpy as np
from helper import getNormData, performance, correlation
import warnings


warnings.filterwarnings('ignore')

def calculate(fold, perct, is_nrmse):
    result = []
    models = ['svr', 'lsl', 'lr', 'dt']
    for model in models:
        r = []
        for i in range(fold):
            held, gene, sample = getNormData('result/per_{}/data_{}.txt'.format(perct, i))
            result, gene, sample = getNormData('result/per_{}/{}_{}.txt'.format(perct, model, i))
            true, gene, sample = getNormData('result/data_{}.txt'.format(i))
            num_missing = []
            for h in held:
                num_missing.append(np.sum(h == 0))
            if is_nrmse:
                r.append(performance(result, true, np.array(num_missing)))
            else:
                r.append(correlation(result, true, held))
        result.append(r)
    return result
