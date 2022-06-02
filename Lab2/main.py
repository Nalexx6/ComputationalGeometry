import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt
from delaune import Delaunay

if __name__ == "__main__":
    points = np.array([[4, 8],
                     [6, 7],
                     [6, 1],
                     [1, 9],
                     [8, 7],
                     [5, 8],
                     [5, 2]])

    delaune_test = Delaunay(points)
    tri1 = delaune_test.triangulation

    tri = scipy.spatial.Delaunay(points)
    plt.triplot(points[:, 0], points[:, 1], tri.simplices, 'k-o',
                label='Delaunay triangulation scipy')

    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(handles=[h[0]], labels=[l[0]])

    # stack graphs horizontally
    for i in range(len(points)):
        points[i][0] += 20

    plt.triplot(points[:, 0], points[:, 1], tri1, 'k-o',
                label='Delaunay triangulation')
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(handles=[h[0]], labels=[l[0]])
    plt.show()
