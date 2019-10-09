import pprint as pp
import random

import matplotlib.pyplot as plt
import numpy as np

all_files = [
    "_data/csc_test_1.txt",
    "_data/csc_test_2.txt",
    "_data/sta_test_2.txt"]

# QUESTION_MAX = 20
# NUM_QUESTIONS = 5
# with open("_data/sample1.txt", "w+") as textfile:
#     textfile.write(str(QUESTION_MAX * NUM_QUESTIONS) + "\n")
#     for i in range(100):
#         marks = [random.randint(0, QUESTION_MAX) for _ in range(NUM_QUESTIONS)]
#         marks.append(sum(marks))
#         marks.insert(0, "ID"+str(random.random()))
#         textfile.write(",".join([str(mark) for mark in marks]))
#         textfile.write("\n")

files = ["_data/csc_test_1.txt", "_data/csc_test_2.txt", "_data/csc_test_3.txt"]
COLOURS = ['#7734EA', '#00A7EA', '#8AE800', '#71CFBD', '#C7C69C', '#DFDEB3']
# COLOURS = ['#B5A87E', '#B5A87E', '#B5A87E', '#B5A87E', '#B5A87E', '#B5A87E']
NUM_BINS = 20
hundies = []
titles = []
percentages = []
tests = []
mu = []
sigma = []

for i, file in enumerate(files):
    pp.pprint("Opening: " + file)
    with open(file, "r") as textfile:
        first_line = textfile.readline().split(",")
        hundies.append(float(first_line[0]))
        titles.append(first_line[1])
        tests.append([])
        for line in textfile:
            # pp.pprint([question for question in line.strip().lower().split(",")[1:]])
            one_student = [float(question) for question in line.strip().lower().split(",")[1:] if len(question) > 0]
            tests[i].append(one_student)
    # pp.pprint(tests[i])
    percentages.append([np.round(student[-1] / hundies[i] * 100.0, 1) for student in tests[i] if len(student) > 0])
    mu.append(np.mean(percentages[i]))
    sigma.append(np.std(percentages[i]))
pp.pprint(percentages)

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

padding = [0.2, 0.15]
for i, test in enumerate(tests):
    x_pos.append([(mu[i] - sigma[i]) / 100.0, (mu[i] + sigma[i]) / 100.0])
    y_pos.append([0.95 - padding[1] * i, 0.96 - padding[1] * i])
    plt.text(
        mu[i],
        height * y_pos[i][1] * 1.01,
        r"{} $\mu={}$, $\sigma={}$".format(titles[i], np.round(mu[i], 2), np.round(sigma[i], 2)))

    plt.axvline(mu[i], y_pos[i][0], y_pos[i][1], color=COLOURS[i], ls='-')
    plt.axhspan(y_pos[i][0] * height, y_pos[i][1] * height, x_pos[i][0], x_pos[i][1],
                color=COLOURS[i % len(COLOURS)], ls='-', alpha=0.6)

# plt.title(" vs ".join(titles))
plt.title("CSC1016S Test Marks")
plt.grid(axis='y', alpha=0.5)
plt.xlabel('Mark')
plt.ylabel('Frequency')

# plt.show()
plt.savefig(" vs ".join(titles))
