import numpy as np

def draw_quiver(ax, pos3d, dir3d, color='blue', alpha=1, length=1):
    if not type(pos3d).__module__ == "numpy":
        pos3d = np.array(pos3d)
    if not type(dir3d).__module__ == "numpy":
        dir3d = np.array(dir3d)
    assert(np.isclose(1, np.linalg.norm(dir3d)))
    dir3d = dir3d * (-1)  # need to be done bcs otherwise the arrow goes wrong..
    ax.quiver(
        pos3d[0], pos3d[1], pos3d[2], dir3d[0], \
        dir3d[1], dir3d[2], facecolor='None', \
        length=length, color=color, alpha=alpha)

def plot_cam(ax, pos, R, length=1):
    R = np.transpose(R)
    ax.scatter(pos[0], pos[1], pos[2], color='black')
    draw_quiver(ax, pos, R[:,0], color='blue', length=length)
    draw_quiver(ax, pos, R[:,1], color='red', length=length)
    draw_quiver(ax, pos, R[:,2], color='black', length=length)