# from statistics import mean
from IPython import display
import matplotlib.pyplot as plt

plt.ion()


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('training')
    plt.xlabel('number of games')
    plt.ylabel('score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)


plot([1, 2, 3], [1, 4, 9])
