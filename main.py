#
# import numpy as np
# from cv2 import aruco
# import matplotlib.pyplot as plt
# import matplotlib as mpl
#
# aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
#
# fig = plt.figure()
# nx = 5
# ny = 4
# for i in range(1, nx * ny + 1):
#     ax = fig.add_subplot(ny, nx, i)
#     img = aruco.drawMarker(aruco_dict, i, 700)
#     ax.set_title(i, size=5)
#     plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
#     ax.axis("off")
#
# plt.savefig("/Users/boydkane/Desktop/markers.pdf")
# plt.show()
import pprint

with open("_data/mam1000w.txt") as textfile:
    mam = set([line.strip().lower().split(":")[1] for line in textfile.readlines() if len(line.split(":")) > 1])
with open("_data/csc1016s.txt") as textfile:
    csc = set([line.split(":")[1].strip().lower() for line in textfile.readlines()])
with open("_data/sll1074s.txt") as textfile:
    sll = set([line.split(":")[1].strip().lower() for line in textfile.readlines()])
with open("_data/sta1006s.txt") as textfile:
    sta = set([line.split(":")[1].strip().lower() for line in textfile.readlines()])

intersect = sta.intersection(csc)
intersect = sorted(list(intersect))
# names = [item.split(", ")[1] + " " + item.split(", ")[0] for item in intersect]
print(len(intersect))
pprint.pprint([name.lower() for name in intersect])
