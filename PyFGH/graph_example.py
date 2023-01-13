import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

x = np.array([5, 4, 1, 4, 5])
plt.xlabel("X-axis")
y = np.sort(x)
plt.ylabel("Y-axis")

plt.title("Example graph")
plt.plot(x, y, color="red")

# out put on the screen
#plt.show()
# will save the image as a jpg
plt.savefig("Graph1.jpg")

#img = plt.Image.open('Graph1.jpg')
#img.show('Graph1.jpg',img)
# us tkinter to save
