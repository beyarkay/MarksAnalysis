import pprint as pp
import random

import matplotlib.pyplot as plt
import numpy as np

# files = ["_data/sta_class_mark.txt",
#          "_data/sta_test1.txt",
#          "_data/sta_test2.txt",
#          "_data/sta_assignment_average.txt"]

files = ["_data/csc_test_1.txt",
         "_data/csc_test_2.txt",
         "_data/csc_test_3.txt"]
COLOURS = ['#EC204F', '#FF922C', '#FEED47', '#71CFBD', '#C7C69C', '#DFDEB3']
SHOULD_SAVE = True

NUM_BINS = 20
hundies = []
titles = []
percentages = []
tests = []
mu = []
sigma = []
num = []
PERCENTILE_VALUES = [25, 50, 75]
percentiles = []

for i, file in enumerate(files):
    pp.pprint("Opening: " + file)
    with open(file, "r") as textfile:
        first_line = textfile.readline().split(",")
        if len(first_line[0]) < 200:  # check to see that the file is formatted properly
            hundies.append(float(first_line[0]))
            titles.append(first_line[1].strip())
        else:
            raise Exception("The first line should contain a title and total, but instead it contains: '{}'".format(
                ",".join(first_line)))

        tests.append([])
        for line in textfile:
            one_student = [float(question) for question in line.strip().lower().split(",")[1:] if len(question) > 0]
            tests[i].append(one_student)
    percentages.append([np.round(student[-1] / hundies[i] * 100.0, 1) for student in tests[i] if len(student) > 0])
    mu.append(
        np.round(np.mean(percentages[i]), 2))
    sigma.append(
        np.round(np.std(percentages[i]), 2))
    num.append(len(percentages[i]))
    percentiles.append([])
    for j, percentile in enumerate(PERCENTILE_VALUES):
        percentiles[-1].append(np.percentile(percentages[i], percentile))


n, bins, patches = plt.hist(x=percentages,
                            bins=NUM_BINS,
                            color=COLOURS[:len(percentages)],
                            alpha=0.7,
                            rwidth=0.85)
plt.xticks(bins, range(0, 100 + 1, 100 // NUM_BINS))

x_pos = []
y_pos = []

maxfreq = np.max(n)
height = np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10
plt.ylim(ymax=height)

padding = [0, 0.025]
for i, test in enumerate(tests):
    x_pos.append([(mu[i] - sigma[i]) / 100.0, (mu[i] + sigma[i]) / 100.0])
    y_pos.append([0.95 - padding[1] * i, 0.96 - padding[1] * i])
    plt.axvline(mu[i], y_pos[i][0], y_pos[i][1], color=COLOURS[i], ls='-')
    plt.axhspan(y_pos[i][0] * height,
                y_pos[i][1] * height,
                x_pos[i][0],
                x_pos[i][1],
                color=COLOURS[i % len(COLOURS)],
                ls='-',
                alpha=0.6)

plt.title(" \nvs ".join(titles), fontsize=10)
plt.grid(axis='y', alpha=0.5)
# legend_items = [r"{} $\mu={}$, $\sigma={}$, n={}".format(titles[i], np.round(mu[i], 2), np.round(sigma[i], 2), num[i])
#                 for i in
#                 range(len(tests))]
legend_items = [r"{}, n={}".format(titles[i], num[i]) for i in range(len(tests))]

table_data = [mu,
              sigma,
              [percentiles[i][0] for i in range(len(mu))],
              [percentiles[i][1] for i in range(len(mu))],
              [percentiles[i][2] for i in range(len(mu))],
              num]
pp.pprint(table_data)

table_data_T = [*zip(*table_data)]
row_labels = titles
col_labels = ["μ", "σ", "25th", "50th", "75th", "n"]
colours = COLOURS[:len(titles)]

the_table = plt.table(cellText=table_data_T,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      rowColours=colours,
                      bbox=[0.3, -0.5, 0.35, 0.3])

# description = "\n".join(
#     ["{}: \n\t$μ={}$, \n\t$σ={}$, \n\t$n={}$".format(
#         titles[i],
#         np.round(mu[i], 2),
#         np.round(sigma[i], 2),
#         num[i]) for i in
#         range(len(tests))]
# )
#
#
# plt.figtext(0.0, -0.5, description)

params = {'legend.fontsize': 6,
          'legend.handlelength': 1}
plt.rcParams.update(params)
plt.legend(legend_items, loc='best').get_frame().set_alpha(0.5)

plt.xlabel('Mark')
plt.ylabel('Frequency')
plt.tight_layout()

if SHOULD_SAVE:
    plt.savefig("_vs_".join([title.replace(" ", "_") for title in titles]), dpi=400, bbox_inches='tight')
else:
    plt.show(dpi=400)
