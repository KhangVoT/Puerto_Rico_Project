import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ak135 = pd.read_csv("/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/_v_list/ak135.txt", delim_whitespace=True,
                    header=None, skiprows=1)
depth = ak135.iloc[:, 0]
velP = ak135.iloc[:, 1]

mit = pd.read_csv("/Users/khangvo/PycharmProjects/Puerto_Rico_Project/files/_v_list/ggge1202-sup-0002-ds01.txt",
                  delim_whitespace=True)
depth_new = mit["Depth"].unique()
depth_new = np.insert(depth_new, 0, -100)

vel_new = np.interp(depth_new, depth, velP)
vel_new = vel_new.round(4)

for i in range(len(vel_new)):
    print(vel_new[i])
print(vel_new)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(velP, depth, "g-", vel_new, depth_new, "or", linewidth=1.5)
ax.set_xlabel("vP (km/s)")
# ax.set_xlim(0, max(velP))
ax.xaxis.set_label_position("top")
ax.xaxis.set_ticks_position("top")
ax.set_ylabel("depth (km)")
# ax.set_ylim(min(depth), max(depth))
ax.invert_yaxis()
ax.yaxis.set_label_position("left")
ax.yaxis.set_ticks_position("left")
ax.yaxis.grid(linestyle="-", color="gray")
plt.title("MIT Interpolated")

plt.savefig("/Users/khangvo/Downloads/Velocity_Profile.jpeg", bbox_inches="tight")

plt.show()
