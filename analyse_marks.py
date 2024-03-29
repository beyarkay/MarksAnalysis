import glob
import pprint as pp

import matplotlib.pyplot as plt
import numpy as np

# files = ["_data/sta_test_1_dp_list.txt",
#          "_data/sta_test_2_dp_list.txt",
#          "_data/sta_assignment_average.txt",
#          "_data/sta_class_mark.txt"]
#
# files = ["_data/csc_test_1.txt",
#          "_data/csc_test_2.txt",
#          "_data/csc_test_3.txt"]
#
# files = ["_data/sta_test_1.txt",
#          "_data/sta_test_2.txt"]
#
# files = ["_data/sta_test_1.txt",
#          "_data/sta_test_1_dp_list.txt"]
#
# files = ["_data/sta_test_2.txt",
#          "_data/sta_test_2_dp_list.txt"]
#
# file = "_data/csc1016s_assignments.txt"
# file = "_data/csc1016s_averages.txt"
# file = "_data/csc1016s_practical_tests.txt"
file = "_data/sll1074s_exam.txt"

files = [
    # "_data/csc1016s_assignments.txt",
    # "_data/csc1016s_averages.txt",
    # "_data/csc1016s_exam.txt",
    # "_data/csc1016s_practical_tests.txt",
    # "_data/csc1016s_quizes.txt",
    # "_data/csc3003s_exam_2019.txt",
    # "_data/csc_test_1.txt",
    # "_data/csc_test_2.txt",
    # "_data/csc_test_3.txt",
    # "_data/sll1074s_exam.txt",
    # "_data/sta1006_exam.txt",
    # "_data/sta_assignment_average.txt",
    # "_data/sta_class_mark.txt",
    # "_data/sta_dp.txt",
    # "_data/sta_test_1.txt",
    "_data/sta_test_1_dp_list.txt",
    # "_data/sta_test_2.txt",
    "_data/sta_test_2_dp_list.txt",
]

# files = sorted(glob.glob("_data/*.txt"))

COLOURS = ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8',
           '#911eb4', '#f032e6', '#a9a9a9', '#800000', '#9A6324', '#808000', '#469990',
           '#000075', '#fabebe', '#ffd8b1', '#fffac8', '#aaffc3', '#e6beff', '#eeeeee',
           '#111111']
SHOULD_SAVE = True
NUM_BINS = 20
DELIMITER = ","
PERCENTILE_VALUES = [25, 50, 75]  # TODO This isn't dynamic, and only works if len(PERCENTILE_VALUES) == 3


def isfloat(string):
    return string.replace('.', '', 1).isdigit()


def parse_files(files):
    """
    Expects multiple file paths, with data formateed like so:
    ```
        CSC1016S Test 1,35      - Title for the series,full marks
        1234123,24              - ID number, followed by results for each series
        1234323,26.0            - ID number, followed by results for each series
        1234523,14              - ID number, followed by results for each series
        ...
    ```
    :return: grand_title, titles, hundies, percentages
    """
    titles = []
    hundies = []
    percentages = []

    for i, file in enumerate(files):
        pp.pprint("Opening: " + file)
        with open(file, "r") as textfile:
            # Parse the header
            first_line = textfile.readline().split(DELIMITER)
            titles.append(first_line[0])
            hundies.append(float(first_line[1].strip()))

            percentages.append([])
            # Parse the body
            for line in textfile:
                if isfloat(line.split(DELIMITER)[-1].strip()):
                    mark = float(line.split(DELIMITER)[-1].strip())
                    percentages[i].append(np.round(mark / hundies[i] * 100.0, 2))
                elif line.split(DELIMITER)[-1].strip() in ["DPR", "AB", "LOA"]:
                    print("Ommitted: " + line)
                else:
                    print(f"Couldn't parse this line'{line}', as isfloat('{line.split(',')[-1].strip()}') is false")
    grand_title = "\nvs ".join(titles)

    return grand_title, titles, hundies, percentages


def parse_file(file):
    """
    Expects one file, with data formateed like so:
    ```
        CSC Assignments                                 - Title for the graph
        PeopleSoft Number,A1,A2,A3,A4,A5,A6,A7,A9,A10   - Labels for each series of the data
        ,100,100,100,100,100,100,100,100,100            - Totals ('full marks') for each series
        1212393,100,100,100,100,97,85,29,70,100         - ID number, followed by results for each series
        1261168,100,98,90,48,81,81,18,0,0               - ID number, followed by results for each series
        1338826,100,43,15,0,68,18,23,56,0               - ID number, followed by results for each series
        ...
    ```
    :return: grand_title, titles, hundies, percentages
    """
    pp.pprint("Opening: " + file)
    with open(file, "r") as textfile:
        # Parse the header
        grand_title = textfile.readline().strip()
        titles = [title.strip() for title in textfile.readline().split(DELIMITER)[1:]]
        hundies = [float(hundie.strip()) for hundie in textfile.readline().split(DELIMITER) if len(hundie) > 0]
        percentages = [[] for _ in hundies]

        # Parse the body
        ommitted = 0
        for line in textfile:
            marks = []
            if isfloat(line.split(DELIMITER)[-1].strip()):
                marks = [float(line.strip()) for line in line.split(DELIMITER)[1:]]
            elif line.split(DELIMITER)[-1].strip() in ["DPR", "AB", "LOA", "O", "INC", "DE"]:
                print("Ommitted: " + line)
                ommitted += 1
            else:
                print(f"Couldn't parse this line'{line}', as isfloat('{line.split(',')[-1].strip()}') is false")
                ommitted += 1

            for i, mark in enumerate(marks):
                percentages[i].append(np.round(mark / hundies[i] * 100.0, 2))
    print(f"Ommitted: {ommitted}")
    return grand_title, titles, hundies, percentages


def calculate_statistics(percentages, percentile_values):
    mu = []
    sigma = []
    num = []
    percentiles = []
    for percentage in percentages:
        # Calculate the sample statistics
        mu.append(np.round(np.mean(percentage), 2))
        sigma.append(np.round(np.std(percentage), 2))
        num.append(len(percentage))
        percentiles.append([])
        for j, percentile in enumerate(percentile_values):
            percentiles[-1].append(np.round(np.percentile(percentage, percentile), 2))
    return mu, sigma, num, percentiles


def plot_histogram(axes, percentages, num, num_bins, colours, titles, grand_title):
    # Plot the histograms simultaneously
    legend_items = [r"{}, n={}".format(titles[i], num[i]) for i in range(len(percentages))]

    ax3.hist(x=percentages,
             bins=100,
             color=colours,
             alpha=0.7,
             rwidth=0.85,
             density=True,
             histtype='step',
             cumulative=True,
             range=(0, 100))

    ax3.legend(legend_items,
               loc='best',
               bbox_to_anchor=(1, 0.8),
               fontsize=6,
               handlelength=1).get_frame().set_alpha(0.5)
    ax3.grid(axis='y', alpha=0.5)
    ax3.set_title(f"Cumulative Mark Frequency\ngithub.com/beyarkay/MarksAnalysis", size=15)
    ax3.set_ylabel("Percentile")
    ax3.set_xlabel("Mark %")
    ax3.set_yticks(np.linspace(0, 1, 11))
    ax3.set_xticks(range(0, 101, 10))
    ax3.set_xlim(0, 100)

    n, bins, patches = axes.hist(x=percentages,
                                 bins=num_bins,
                                 color=colours,
                                 alpha=0.7,
                                 rwidth=0.85)
    ax1.set_xticks(bins, range(0, 100 + 1, 100 // num_bins))
    # ax1.set(title=grand_title + f" - Source Code at github.com/beyarkay/MarksAnalysis",
    #         ylabel='Frequency',
    #         xlabel="Mark %")
    ax1.set_title(f"{grand_title}\ngithub.com/beyarkay/MarksAnalysis", size=25)
    ax1.set_ylabel("Frequency")
    ax1.set_xlabel("Mark %")

    ax1.grid(axis='y', alpha=0.5)
    ax1.legend(legend_items,
               loc='best',
               bbox_to_anchor=(1, 0.8),
               fontsize=6,
               handlelength=1).get_frame().set_alpha(0.5)
    ax1.tick_params(axis='both', which='major', labelsize=10)
    ax1.tick_params(axis='both', which='minor', labelsize=8)
    return n


def plot_std_dev(axes, n, percentages, mu, sigma, colours):
    maxfreq = np.max(n)
    height = np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10
    plt.ylim(ymax=height)

    x_pos = []
    y_pos = []
    padding = [0, 0.025]
    for i, test in enumerate(percentages):
        x_pos.append([(mu[i] - sigma[i]) / 100.0, (mu[i] + sigma[i]) / 100.0])
        y_pos.append([0.95 - padding[1] * i, 0.96 - padding[1] * i])
        axes.axvline(mu[i], y_pos[i][0], y_pos[i][1], color=colours[i], ls='-')
        axes.axhspan(y_pos[i][0] * height,
                     y_pos[i][1] * height,
                     x_pos[i][0],
                     x_pos[i][1],
                     color=colours[i % len(colours)],
                     ls='-',
                     alpha=0.6)


def plot_table(mu, sigma, percentiles, colours, titles):
    table_data = [mu,
                  sigma,
                  [percentiles[i][0] for i in range(len(mu))],
                  [percentiles[i][1] for i in range(len(mu))],
                  [percentiles[i][2] for i in range(len(mu))],
                  num]

    table_data_T = [*zip(*table_data)]
    row_labels = titles
    col_labels = ["μ", "σ", "25th", "50th", "75th", "n"]

    scale = 0.7
    # TODO the_table doesn't dynamically resize itself when the data shape
    the_table = ax2.table(cellText=table_data_T,
                          rowLabels=row_labels,
                          colLabels=col_labels,
                          rowColours=colours,
                          bbox=[0.5 - scale / 2, 0.5 - scale / 2, scale, scale])

    ax2.axis(False)
    # ax2.tick_params(
    #     axis='both',  # changes apply to the x-axis
    #     which='both',  # both major and minor ticks are affected
    #     bottom=False,  # ticks along the bottom edge are off
    #     top=False,  # ticks along the top edge are off
    #     left=False,
    #     right=False,
    #     labelbottom=False,
    #     labeltop=False)  # labels along the bottom edge are off


if __name__ == '__main__':


    for file in files:
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(10, 20))

        grand_title, titles, hundies, percentages = parse_file(file)

        mu, sigma, num, percentiles = calculate_statistics(percentages, PERCENTILE_VALUES)

        n = plot_histogram(ax1,
                           percentages,
                           num,
                           NUM_BINS,
                           COLOURS[:len(percentages)],
                           titles,
                           grand_title)

        # plot_std_dev(ax1, n, percentages, mu, sigma, COLOURS)

        plot_table(mu, sigma, percentiles, COLOURS[:len(mu)], titles)

        plt.tight_layout()

        if SHOULD_SAVE:
                graph_title = "graphs/" + grand_title.replace(" ", "_").replace("\n", "_")
                plt.savefig(graph_title, dpi=400, bbox_inches='tight')
                print(f"Graph saved as {graph_title}")
        else:
            plt.show(dpi=400)
