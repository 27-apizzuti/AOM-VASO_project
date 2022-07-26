"""
Created on Sat Oct  2 13:52:50 2021
from: https://gist.github.com/hitvoice/36cf44689065ca9b927431546381a3f7

@author: apizz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def cm_analysis(y_true, y_pred, filename, labels, ymap=None, figsize=(10,10)):
    """
    Generate matrix plot of confusion matrix with pretty annotations.
    The plot image is saved to disk.
    args:
      y_true:    true label of the data, with shape (nsamples,)
      y_pred:    prediction of the data, with shape (nsamples,)
      filename:  filename of figure file to save
      labels:    string array, name the order of class labels in the confusion matrix.
                 use `clf.classes_` if using scikit-learn models.
                 with shape (nclass,).
      ymap:      dict: any -> string, length == nclass.
                 if not None, map the labels & ys to more understandable strings.
                 Caution: original y_true, y_pred and labels must align.
      figsize:   the size of the figure plotted.
    """
    if ymap is not None:
        y_pred = [ymap[yi] for yi in y_pred]
        y_true = [ymap[yi] for yi in y_true]
        labels = [ymap[yi] for yi in labels]
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_perc = cm / cm_sum.astype(float) * 100
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_perc[i, j]
            if i == j:
                s = cm_sum[i]
                annot[i, j] = '%.1f%%\n%d/%d' % (p, c, s)
            elif c == 0:
                annot[i, j] = ''
            else:
                annot[i, j] = '%.1f%%\n%d' % (p, c)
    cm = pd.DataFrame(cm, index=labels, columns=labels)
    cm.style.set_properties(**{
    'font-size': '100pt'})
    cm.index.name = 'AVG labels'
    cm.columns.name = 'Predicted CV labels'
    # TPR and PPV
    x = np.asarray(cm)
    TPR = np.diag(x) / np.sum(x, axis=1)
    PPV = np.transpose(np.diag(x) / np.sum(x, axis=0))
    TPR = TPR.round(decimals=2)
    PPV = PPV.round(decimals=2)
    fig, ax = plt.subplots(figsize=figsize)
    plt.suptitle('TPR: {},\n PPV: {}'.format(TPR, PPV))
    sns.heatmap(cm, annot=annot, fmt='', ax=ax, cbar=False)
    plt.savefig(filename)
