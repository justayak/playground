import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
import math
import cv2

def plot_mats(mats, cols=5, cmap=plt.get_cmap('gray'), size=16):
    """
    plot a set of matrices close to each other
    """
    SUBSTITUTE = np.zeros_like(mats[0])
    rows = []
    currentRow = []
    cols = float(cols)

    def add_to_rows():
        while len(currentRow) < cols:
            currentRow.append(SUBSTITUTE)
        rows.append(np.hstack(currentRow))
    
    for i in range(0, len(mats)):
        M = mats[i]
        minv = np.min(M)
        maxv = np.max(M)
        if minv < 0 or minv > 255 or maxv < 0 or maxv > 255:
            M = translate(M, minv, maxv, 0, 255)

        if i%cols == 0:
            if len(currentRow) > 0:
                add_to_rows()
            currentRow = []
        currentRow.append(M)
    if len(currentRow) > 0:
        add_to_rows()
    I = np.vstack(rows)
    f, ax = plt.subplots(ncols=1)
    f.set_size_inches(size, size)
    ax.imshow(I, cmap=cmap)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
def vectorize(images):
    I = images[0].shape
    channels = 0
    rows = I[0]
    cols = I[1]
    if len(I) == 3:
        R = np.zeros((len(images), I[2], I[0] * I[1]))
        channels = I[2]
    elif len(I) == 2:
        R = np.zeros((len(images), I[0] * I[1]))
    else:
        assert(False)
        
    for i, I in enumerate(images):
        C = []
        if channels > 0:
            for c in range(channels):
                C.append(I[:,:,c])
        
        for r in range(rows):
            if channels > 0:
                for c in range(channels):
                    R[i, c, r*cols:(r*cols+cols)] = C[c][r,:]
            else:
                R[i, r*cols:(r*cols+cols)] = I[r,:]
    
    return R


def un_vectorize(R, square=True, w=None, h=None):
    if w is not None:
        assert(h is not None)
        square = False
    
    channels = 0
    if len(R.shape) == 3:
        channels = R.shape[1]
    elif len(R.shape) != 2:
        assert(False)
        
    if square:
        if channels == 0:
            w = R.shape[1]/2
            h = w
        else:
            w = R.shape[2]/2
            h = w
        
    count = R.shape[0]
    
    Result = []
    
    for i in range(count):
        if channels == 0:
            I = np.zeros((h, w))
            for r in range(h):
                I[r,:] = R[i, r*w:(r*w+w)]
        else:
            I = np.zeros((h, w, channels))
            C = []
            for c in range(channels):
                I_ = np.zeros((h, w))
                for r in range(h):
                    I_[r,:] = R[i, c, r*w:(r*w+w)]
                C.append(I_)
            for i,c in enumerate(C):
                I[:,:, i] = c
        
        Result.append(I)
    
    return Result