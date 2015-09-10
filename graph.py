import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

def get_datarow(datafile, row_name):
    with open(datafile) as csv_file:
        r = csv.reader(csv_file, delimiter=',')
        header = True
        xcor = 0
        x_column = []

        for row in r:
            if header:
                xval_set = False

                for title in row:
                    if row_name != title and not xval_set:
                        xcor += 1
                    elif row_name == title:
                        xval_set = True

                if not xval_set:
                    raise NameError('Invalid Row Name: ' + row_name)

                header = False
            else:
                x_column.append(row[xcor])

    return x_column

def create_double_graph(datafile, xcol, ycol1, ycol2, outdir='.'):
    fig, ax1 = plt.subplots()
    try:
        xdata = get_datarow(datafile, xcol)
        y1data = get_datarow(datafile, ycol1)
        y2data = get_datarow(datafile, ycol2)
    except NameError as e:
        print(e)
        return e  # for logging elsewhere
    ax1.plot(xdata, y1data, 'b-', linewidth=3.0)
    ax1.set_xlabel(xcol)

    ax1.set_ylabel(ycol1, color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    
    ax2 = ax1.twinx()
    ax2.plot(xdata, y2data, 'r-', linewidth=3.0)
    ax2.set_ylabel(ycol2, color='r')
    for tl in ax2.get_yticklabels():
            tl.set_color('r')
    
    graph_title = xcol + ' vs ' + ycol1 + ' and ' + ycol2
    plt.title(graph_title)
    plt.savefig(outdir + '/' + graph_title + '.png', bbox_inches='tight')
    plt.close()
    return True


def multi_graph(datafile, xcol, ycols, outdir='.'):
    if len(ycols) == 2:
        return create_double_graph(datafile, xcol, ycols[0], ycols[1], 
                outdir=outdir)
    
    try:
        xdata = get_datarow(datafile, xcol)
    except NameError as e:
        print(e)
        return e  # TODO: logging
    graph_title = xcol + ' vs ' 
    for ycol in ycols:
        graph_title += ycol + ', '
        try:
            ydata = get_datarow(datafile, ycol)
        except NameError as e:
            print(e)
            return e

        plt.plot(xdata, ydata, label=ycol, linewidth=3.0)
    
    plt.title(graph_title[:-2])
    plt.xlabel(xcol)
    plt.legend(bbox_to_anchor=(1.4, 1.0))
    plt.savefig(outdir + '/' + graph_title[:-2] + '.png', bbox_inches='tight')
    plt.close()
    return True

if __name__ == "__main__":
    multi_graph(sys.argv[1], 'record_id', ['voltage', 'current']) 
