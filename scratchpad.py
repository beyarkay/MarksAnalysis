import os

READFILE = "_data/sta_dp.txt"
ASSIGNMENT = "_data/sta_assignment_average.txt"
TEST1 = "_data/sta_test1.txt"
TEST2 = "_data/sta_test2.txt"
CLASS_MARK = "_data/sta_class_mark.txt"

if os.path.exists(ASSIGNMENT):
    os.remove(ASSIGNMENT)
if os.path.exists(TEST1):
    os.remove(TEST1)
if os.path.exists(TEST2):
    os.remove(TEST2)
if os.path.exists(CLASS_MARK):
    os.remove(CLASS_MARK)

with open(READFILE, "r") as readfile,  \
        open(ASSIGNMENT, "x") as assign_file,  \
        open(TEST1, "x") as test1file,  \
        open(TEST2, "x") as test2file,  \
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
