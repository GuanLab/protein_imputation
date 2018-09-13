import numpy as np
from matplotlib import pyplot as plt
from helper import getRealData, getNormData, performance, correlation
from helper import performanceAll, outputFile, summary
from scipy.stats import pearsonr, spearmanr
import warnings


warnings.filterwarnings('ignore')


# def correlation(result, true):
#     pearson = []
#     spearman = []
#     for r, t in zip(result, true):
#         if np.sum(~np.isnan(r)) > 5:
#             pearson.append(pearsonr(r[~np.isnan(r)], t[~np.isnan(t)])[0])
#             spearman.append(spearmanr(r[~np.isnan(r)], t[~np.isnan(t)])[0])
#     print('pearson: ', np.nanmean(pearson), 'spearman: ', np.nanmean(spearman))


def calculate(perct, is_nrmse, test_num):
    models = ['svr', 'lsl', 'lr', 'dt']
    # models = ['lr']
    for model in models:
        perf = []
        for test in range(test_num):
            # held, gene, sample = getNormData('output/per_{}/held_{}.txt'.format(perct, test))
            held, gene, sample = getNormData('output/full_avg/held_{}.txt'.format(test))
            # result, gene, sample = getNormData('output/per_{}/{}_{}.txt'.format(perct, model, test))
            result, gene, sample = getNormData('output/full_avg/{}_{}.txt'.format(model, test))
            true, gene, sample = getNormData('output/true_{}.txt'.format(test))
            if is_nrmse:
                perf.append(performance(result, true, held))
            else:
                # True: Pearson; False: Spearman
                perf.append(correlation(result, true, held, True))
        print(perf)

def plotPred(perct, clr):
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

def getPerformance(model, perct):
    """ Performance of EACH gene. """
    test_num = 10
    for test in range(test_num):
        held, gene, sample = getNormData('output/per_{}/held_{}.txt'.format(perct, test))
        result, gene, sample = getNormData('output/per_{}/{}_{}.txt'.format(perct, model, test))
        true, gene, sample = getNormData('output/true_{}.txt'.format(test))
        perf = performanceAll(result, true, held)
        outputFile(perf.T, 'perfs/{}_{}.txt'.format(model, test), gene, [str(test)])

def combine(model, perct):
    # Performance of gene that does not have missing value is nan
    test_num = 10
    perfs = []
    for test in range(test_num):
        # perf.shape = (num_gene, 1)
        perf, gene, num = getNormData('perfs/{}_{}.txt'.format(model, test))
        perfs.append(perf)
    perfs = np.hstack(perfs)
    outputFile(perfs, 'perfs/{}_{}.txt'.format(model, perct),
        gene, list(range(test_num)))

def plotPerf(model, col):
    perct = [0.05, 0.08, 0.1, 0.2]
    plt.style.use('ggplot')
    f, axis = plt.subplots(4, 1, sharex=True)
    for ax, p in zip(axis, perct): 
        perf = getRealData('results/{}_{}.txt'.format(model, p))
        ax.plot(perf['perf_avg'], perf[col], '.', color='#8c5eb6', alpha=0.5)
        ax.set_title('{}%'.format(int(p*100)), color='black', fontsize=12)
        corr = pearsonr(perf[col], perf['perf_avg'])[0]
        print(p, corr)
        # ax.text(-1.5, 0.4, format(corr, '.3f'), color='black')
    axis[3].set_xlabel('NRMSE', fontsize=15, color='black')
    axis[1].set_ylabel('Missing Ratio', fontsize=15, color='black')
    # plt.text(-0.5, -0.1, col, ha='center', fontsize=15, color='black')
    # plt.tight_layout(pad=0.5)
    plt.show()

# getPerformance('lr', 0.2)
# combine('lr',0.2)
calculate(0.05, True, 10)

# plotPerf('lr', 'miss_ratio')
