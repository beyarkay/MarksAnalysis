import pprint as pp

import matplotlib.pyplot as plt
import numpy as np

# files = ["_data/sta_test_1_dp_list.txt",
#          "_data/sta_test_2_dp_list.txt",
#          "_data/sta_assignment_average.txt",
#          "_data/sta_class_mark.txt"]

# files = ["_data/csc_test_1.txt",
#          "_data/csc_test_2.txt",
#          "_data/csc_test_3.txt"]

# files = ["_data/sta_test_1.txt",
#          "_data/sta_test_2.txt"]

# files = ["_data/sta_test_1.txt",
#          "_data/sta_test_1_dp_list.txt"]

# files = ["_data/sta_test_2.txt",
#          "_data/sta_test_2_dp_list.txt"]

# files = "_data/csc1016s_assignments.txt"
# files = "_data/csc1016s_averages.txt"
# files = "_data/csc1016s_practical_tests.txt"
files = "_data/csc1016s_quizes.txt"
COLOURS = ['#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8',
           '#911eb4', '#f032e6', '#a9a9a9', '#800000', '#9A6324', '#808000', '#469990',
           '#000075', '#fabebe', '#ffd8b1', '#fffac8', '#aaffc3', '#e6beff', '#eeeeee',
           '#111111']
SHOULD_SAVE = True

NUM_BINS = 20
hundies = []
titles = []
percentages = []
tests = []
mu = []
sigma = []
num = []
PERCENTILE_VALUES = [25, 50, 75]  # TODO This isn't dynamic, and only works if len(PERCENTILE_VALUES) == 3
percentiles = []
grand_title = ""


def isfloat(string):
    return string.replace('.', '', 1).isdigit()


if type(files) is list:
    for i, file in enumerate(files):
        pp.pprint("Opening: " + file)
        with open(file, "r") as textfile:
            first_line = textfile.readline().split(",")
            # TODO improve this formatting check to be more robust
            if len(first_line[1]) < 200:
                titles.append(first_line[0])
                hundies.append(float(first_line[1].strip()))
            else:
                raise Exception("The first line should contain a title and total, but instead it contains: '{}'".format(
                    ",".join(first_line)))

            tests.append([])
            percentages.append([])
            for line in textfile:
                # one_student = [float(question) for question in line.strip().lower().split(",")[1:] if len(question) > 0]
                if isfloat(line.split(",")[-1].strip()):
                    mark = float(line.split(",")[-1].strip())
                    tests[i].append(mark)
                    percentages[i].append(np.round(mark / hundies[i] * 100.0, 2))
                else:
                    print(f"Couldn't parse this line'{line}', as isfloat('{line.split(',')[-1].strip()}') is false")
    grand_title = "\nvs ".join(titles)
    # percentages.append([np.round(mark / hundies[i] * 100.0, 1) for mark in tests[i] if len(student) > 0])
else:
    with open(files, "r") as textfile:
        grand_title = textfile.readline().strip()
        titles = [title.strip() for title in textfile.readline().split(",")[1:]]
        hundies = [float(hundie.strip()) for hundie in textfile.readline().split(",") if len(hundie) > 0]
        percentages = [[] for _ in hundies]
        for line in textfile:
            marks = [float(line.strip()) for line in line.split(",")[1:]]
            for i, mark in enumerate(marks):
                percentages[i].append(np.round(mark / hundies[i] * 100.0, 2))

for percentage in percentages:
    # Calculate the sample statistics
    mu.append(np.round(np.mean(percentage), 2))
    sigma.append(np.round(np.std(percentage), 2))
    num.append(len(percentage))
    # percentiles.append([np.percentile(percentage, percentile) for percentile in PERCENTILE_VALUES])
    percentiles.append([])
    for j, percentile in enumerate(PERCENTILE_VALUES):
        percentiles[-1].append(np.round(np.percentile(percentage, percentile), 2))

# pp.pprint(percentages)
pp.pprint(mu)
pp.pprint(titles)

# Plot the histograms simultaneously
n, bins, patches = plt.hist(x=percentages,
                            bins=NUM_BINS,
                            color=COLOURS[:len(percentages)],
                            alpha=0.7,
                            rwidth=0.85)
plt.xticks(bins, range(0, 100 + 1, 100 // NUM_BINS))

maxfreq = np.max(n)
height = np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10
plt.ylim(ymax=height)

x_pos = []
y_pos = []
padding = [0, 0.025]
for i, test in enumerate(percentages):
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

plt.title(grand_title, fontsize=10)
plt.grid(axis='y', alpha=0.5)

legend_items = [r"{}, n={}".format(titles[i], num[i]) for i in range(len(percentages))]

table_data = [mu,
              sigma,
              [percentiles[i][0] for i in range(len(mu))],
              [percentiles[i][1] for i in range(len(mu))],
              [percentiles[i][2] for i in range(len(mu))],
              num]
print("TABLE DATA:\n")
pp.pprint(table_data)

table_data_T = [*zip(*table_data)]
row_labels = titles
col_labels = ["μ", "σ", "25th", "50th", "75th", "n"]
colours = COLOURS[:len(titles)]

# TODO the_table doesn't dynamically resize itself when the data shape
the_table = plt.table(cellText=table_data_T,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      rowColours=colours,
                      bbox=[0.3, -0.5, 0.35, 0.3])

params = {'legend.fontsize': 6,
          'legend.handlelength': 1}
plt.rcParams.update(params)
plt.legend(legend_items, loc='best').get_frame().set_alpha(0.5)

plt.xlabel('Mark')
plt.ylabel('Frequency')
plt.tight_layout()

if SHOULD_SAVE:
    graph_title = "graphs/" + grand_title.replace(" ", "_").replace("\n", "_")
    plt.savefig(graph_title, dpi=400, bbox_inches='tight')
else:
    plt.show(dpi=400)
