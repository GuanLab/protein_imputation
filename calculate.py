import numpy as np
from matplotlib import pyplot as plt
from helper import getNormData, performance, correlation, outputFile
import warnings


warnings.filterwarnings('ignore')


def calculate(perct, is_nrmse, test_num):
    models = ['svr', 'lsl', 'lr', 'dt', 'pred']
    for model in models:
        perf = []
        for test in range(test_num):
            held, gene, sample = getNormData('output/per_{}/held_{}.txt'.format(perct, test))
            # held, gene, sample = getNormData('output/sub_0/held_{}.txt'.format(test))
            result, gene, sample = getNormData('output/per_{}/{}_{}.txt'.format(perct, model, test))
            # result, gene, sample = getNormData('output/sub_0/{}_{}.txt'.format(model, test))
            true, gene, sample = getNormData('output/true_{}.txt'.format(test))
            if is_nrmse:
                perf.append(performance(result, true, held))
            else:
                perf.append(correlation(result, true, held, False))
        print(perf)

def plot(perct, clr):
    model = 'lr'
    held, gene, sample = getNormData('output/per_{}/held_0.txt'.format(perct))
    result, gene, sample = getNormData('output/per_{}/{}_0.txt'.format(perct, model))
    true, gene, sample = getNormData('output/true_0.txt')

    held = np.ndarray.flatten(held)
    r = np.ndarray.flatten(result)[held == 0.0]
    t = np.ndarray.flatten(true)[held == 0.0]
    plt.style.use('ggplot')
    plt.plot(t, r, '.', color=clr, alpha=0.5)
    plt.xlabel('Observed Data', fontsize=20, color='black')
    plt.ylabel('Predicted Data', fontsize=20, color='black')
    # plt.title(str(perct*100)+'%', fontsize=20)


# calculate(0.2, False, 10)

plot(0.08,'teal')
plot(0.05,'tomato')
plt.plot([1,8],[1,8],color='black',linewidth=0.8)
plt.show()

