import matplotlib.pyplot as p
import numpy as np


def plot(title, data, show=False):

    fig, ax = p.subplots()
    xbound = 120
    ybound = 3

    # Plot stddev for each bootstrap realization

    bootstrapped_x = None
    bootstrapped_y = None
    stddevs_by_nresps = {}
    for station in data:
        # id = station['id']
        nresps = station['n']
        # nresamples = station['nresamples']
        stddev = station['stddev']
        # print('%s: n=%i (%i) s=%.2f' % (id, nresps, nresamples, stddev))

        # Save bootstrapped scatter points (grey dots)
        # y = station['stddevs']
        # x = np.full(y.shape, fill_value=nresps)
        y = station['stddev']
        x = nresps
        if bootstrapped_x is None:
            bootstrapped_x = x
            bootstrapped_y = y
        else:
            bootstrapped_x = np.append(bootstrapped_x, x)
            bootstrapped_y = np.append(bootstrapped_y, y)

        # Save mean of stddev
        if nresps in stddevs_by_nresps:
            stddevs_by_nresps[nresps].append(stddev)
        else:
            stddevs_by_nresps[nresps] = [stddev]

    # Plot scatterplot (grey dots)
    ax.scatter(bootstrapped_x, bootstrapped_y, c='grey', s=5, alpha=0.25, label='Bootstrapped STDDEV')

    # Plot mean stddev for each nresp bin (black dots)
    mean_x = []
    mean_y = []
    for nresps, stddev in stddevs_by_nresps.items():
        mean_x.append(nresps)
        mean_stddevs = np.nanmean(np.array(stddev))
        mean_y.append(mean_stddevs)

    print(mean_x)
    print(mean_y)
    ax.scatter(mean_x, mean_y, c='black', s=20, label='Mean STDDEV for each nresp')

    # Plot DYFI stddev calculation (WGRW11)

    dyfi_x = np.linspace(1, xbound, 500)
    dyfi_y = np.exp(dyfi_x * (-1/24.02)) * 0.25 + 0.09
    ax.plot(dyfi_x, dyfi_y, c='black', label='DYFI computed STDDEV')

    ax.set_title(title)
    ax.set_xlabel('Number of responses', fontsize=15)
    ax.set_ylabel('Stddev of intensity', fontsize=15)
    ax.set_xbound(lower=1, upper=xbound)
    ax.set_ybound(lower=0, upper=ybound)
    ax.legend()

    ax.grid(True)
    fig.tight_layout()
    if show:
        p.show()
    return fig
