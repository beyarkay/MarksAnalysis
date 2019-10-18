import os
import glob

"""
Red
#e6194B
Green
#3cb44b
Yellow
#ffe119
Blue
#4363d8
Orange
#f58231
Purple
#911eb4
Cyan
#42d4f4
Magenta
#f032e6
Lime
#bfef45
Pink
#fabebe
Teal
#469990
Lavender
#e6beff
Brown
#9A6324
Beige
#fffac8
Maroon
#800000
Mint
#aaffc3
Olive
#808000
Apricot
#ffd8b1
Navy
#000075
Grey
#a9a9a9
White
#ffffff
Black
#000000
"""


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
    parse_csv()
