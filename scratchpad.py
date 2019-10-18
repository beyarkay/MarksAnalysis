import os
import glob
import matplotlib.pyplot as plt

import numpy as np


def draw_graph():
    x1 = np.linspace(0.0, 5.0)
    x2 = np.linspace(0.0, 2.0)
    y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
    y2 = np.cos(2 * np.pi * x2)

    # Create two subplots sharing y axis
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

    # ax1.plot(x1, y1, 'ko-')
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    mu, sigma = 100, 15
    x = mu + sigma * np.random.randn(10000)

    # the histogram of the data
    n, bins, patches = ax1.hist(x, 50, density=True, facecolor='g', alpha=0.75)

    ax1.set(title='A tale of 2 subplots', ylabel='Damped oscillation')

    ax2.plot(x2, y2, 'r.-')
    ax2.set(xlabel='time (s)', ylabel='Undamped')

    plt.show()


def parse_csv():
    READ_PATH = "_data/tabula-CSC1016S_Marksheet_2019.csv"
    WRITE_PATH = "_data/csc1016s_averages.txt"

    with open(READ_PATH, "r") as readfile, open(WRITE_PATH, "x") as writefile:
        writefile.write("CSC Averages\n"
                        "PeopleSoft Number,Practical Assignment Average,Quiz Average,Practical Test Average,Practical Average\n"
                        ",100,100,100,100\n")
        _ = readfile.readline()  # The first line is a header line
        for line in readfile:
            writefile.write("{},{},{},{},{}\n".format(
                line.split(",")[0].strip(),
                line.split(",")[10].strip(),
                line.split(",")[18].strip(),
                line.split(",")[21].strip(),
                line.split(",")[22].strip()
            ))


def reformat_sta1006S_DP_list():
    READFILE = "_data/sta_dp.txt"
    ASSIGNMENT = "_data/sta_assignment_average.txt"
    TEST1 = "_data/sta_test_1_dp_list.txt"
    TEST2 = "_data/sta_test_2_dp_list.txt"
    CLASS_MARK = "_data/sta_class_mark.txt"

    if os.path.exists(ASSIGNMENT):
        os.remove(ASSIGNMENT)
    if os.path.exists(TEST1):
        os.remove(TEST1)
    if os.path.exists(TEST2):
        os.remove(TEST2)
    if os.path.exists(CLASS_MARK):
        os.remove(CLASS_MARK)

    with open(READFILE, "r") as readfile, \
            open(ASSIGNMENT, "x") as assign_file, \
            open(TEST1, "x") as test1file, \
            open(TEST2, "x") as test2file, \
            open(CLASS_MARK, "x") as classmarkfile:
        assign_file.write("100, STA Assignment Average\n")
        test1file.write("100, STA Test 1\n")
        test2file.write("100, STA Test 2\n")
        classmarkfile.write("100, STA Class Mark\n")

        for line in readfile:
            writeline = ",,".join([
                line.split(",")[0],
                line.split(",")[1]
            ])
            assign_file.write(writeline + "\n")

            writeline = ",,".join([
                line.split(",")[0],
                line.split(",")[4]
            ])
            test1file.write(writeline + "\n")

            writeline = ",,".join([
                line.split(",")[0],
                line.split(",")[5]
            ])
            test2file.write(writeline + "\n")

            writeline = ",,".join([
                line.split(",")[0],
                line.split(",")[6]
            ])
            classmarkfile.write(writeline.strip() + "\n")


if __name__ == '__main__':
    draw_graph()
