
import numpy as np
import matplotlib.pyplot as plt


class sphere:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z

        self.radius = radius

        self.resolution = 100
        self.points = np.zeros(shape=(self.resolution, 3))


    def get_pos(self):
        return [self.x, self.y, self.z]

    def draw(self):
        for i in range(self.resolution):
            self.points[i, 0] = self.x + self.radius * np.cos(2 * np.pi * i / self.resolution)
            self.points[i, 1] = self.y + self.radius * np.sin(2 * np.pi * i / self.resolution)
            self.points[i, 2] = self.z + self.radius * np.sin(2 * np.pi * i / self.resolution)
        return self.points

    def plot(self, ax, pos: list = (0, 0)):
        ax.scatter(self.points[:, 0], self.points[:, 1], np.zeros(self.points.shape[0]))
        ax.scatter(self.points[:, 0], np.zeros(self.points.shape[0]), self.points[:, 2])
        ax.scatter(np.zeros(self.points.shape[0]), self.points[:, 0] , self.points[:, 2])


        ax.view_init(elev=pos[0], azim=pos[1])


class point:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z

        self.radius = radius

    def get_pos(self):
        return [self.x +self.radius, self.y + self.radius, self.z + self.radius]



# s = sphere(0, 0, 0, 5)
# s.draw()
# s.plot([45,45])

