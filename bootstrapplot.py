import matplotlib.pyplot as p
import numpy as np


def plot(title, data):

    fig, ax = p.subplots()
    xbound = 120
    ybound = 3

    # Plot stddev for each boostrap realization

    stddevs_by_nresps = {}
    for station in data:
        # id = station['id']
        nresps = station['n']
        # nresamples = station['nresamples']
        stddev = station['stddev']
        # print('%s: n=%i (%i) s=%.2f' % (id, nresps, nresamples, stddev))

        stddevs = station['stddevs']
        x = np.full(stddevs.shape, fill_value=nresps)
        ax.scatter(x, stddevs, c='grey', s=5, alpha=0.25)
        if nresps in stddevs_by_nresps:
            stddevs_by_nresps[nresps].append(stddev)
        else:
            stddevs_by_nresps[nresps] = [stddev]

    # Plot mean stddev for each nresp bin

    mean_x = []
    mean_y = []
    for nresps, stddevs in stddevs_by_nresps.items():
        mean_x.append(nresps)
        mean_stddevs = np.array(stddevs).mean()
        mean_y.append(mean_stddevs)

    ax.scatter(mean_x, mean_y, c='black', s=10)

    # Plot DYFI stddev calculation (WGRW11)

    dyfi_x = np.linspace(1, xbound, 500)
    dyfi_y = np.exp(dyfi_x * (-1/24.02)) * 0.25 + 0.09
    p.plot(dyfi_x, dyfi_y, c='black')

    ax.set_title(title)
    ax.set_xlabel('Number of responses', fontsize=15)
    ax.set_ylabel('Stddev of intensity', fontsize=15)
    ax.set_xbound(lower=1, upper=xbound)
    ax.set_ybound(lower=0, upper=ybound)

    ax.grid(True)
    fig.tight_layout()
    p.show()
