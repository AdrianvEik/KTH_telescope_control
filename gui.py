#Import the required Libraries
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from sphere import sphere

class Gui(tk.Tk):
    def __init__(self, figsize=(7, 7), dpi=80):
        super().__init__()
        self.title("GUI")
        # self.geometry("800x500")

        self.frame = tk.Frame(self)

        self.resizable(0, 0)

        self.row = 0

        # init figure
        self.fig = plt.figure(figsize=figsize, dpi=dpi)
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Telescope positions
        self.theta = np.radians(90)
        self.phi = np.radians(20)

        self.xpos = np.cos(self.theta) * np.cos(self.phi)
        self.ypos = np.sin(self.theta) * np.cos(self.phi)
        self.zpos = np.sin(self.phi)

        self.ax.plot([-1, 1], [0, 0], [0, 0], color='black')
        self.ax.plot([0, 0], [-1, 1], [0, 0], color='black')
        self.ax.plot([0, 0], [0, 0], [-1, 1], color='black')

        self.telpos = self.ax.plot([self.xpos], [self.ypos], [self.zpos],
                                   marker="o", color="C3", linestyle="", markersize=20,
                                   label="Telescope")

        self.telposlnx = self.ax.plot([0, self.xpos], [0, self.ypos], [0, 0],
                                       color = "C3", linestyle = "-")
        self.telposlnz = self.ax.plot([self.xpos, self.xpos], [self.ypos, self.ypos], [0, self.zpos],
                                      color="C3", linestyle="-")
        self.telposlnxyz = self.ax.plot([0, self.xpos], [0, self.ypos], [0, self.zpos],
                                        color="C3", linestyle="-")

        # Projected positions
        self.thetaproj = 0
        self.phiproj = 0

        self.xproj = np.cos(self.thetaproj)
        self.yproj = np.sin(self.thetaproj)
        self.zproj = np.sin(self.phiproj)

        self.projpos = self.ax.plot([self.xproj], [self.yproj], [self.zproj],
                                    marker="o", color="C4", linestyle="", markersize=20,
                                    label="Projected")

        self.projposlnx = self.ax.plot([0, self.xproj], [0, self.yproj], [0, 0],
                                        color="C4", linestyle="-")

        self.projposlnz = self.ax.plot([self.xproj, self.xproj], [self.yproj, self.yproj], [0, self.zproj],
                                       color="C4", linestyle="-")

        self.projposlnxyz = self.ax.plot([0, self.xproj], [0, self.yproj], [0, self.zproj],
                                        color="C4", linestyle="-")


        self.init_projpos()

        self.create_plot()
        self.show_cords()
        self.enter_cords()

    def init_projpos(self):

        def dummy(*args):
            print(self.focus_get(), self.focus_get().__str__())

        def ptestx(*args):
            thetabias = 0
            x = float(self.xposnrvar.get())

            # hard coded entry variables for now
            # todo: make the entry variables dynamic
            if self.check_point(x, self.yproj, self.zproj) or self.focus_get().__str__() != ".!entry":  # focus var is hard coded
                pass
            else:
                self.yposnrvar.set(np.sqrt(1 - x ** 2))

                if x < 0:
                    thetabias = 180

                try:
                    self.thetanrvar.set(str(thetabias + np.degrees(np.arctan(float(self.yposnrvar.get()) / x))) + "°")
                except ZeroDivisionError:
                    self.thetanrvar.set("90°")


        self.xposnrvar = tk.StringVar()
        self.xposnrvar.trace_add("write", ptestx)

        def ptesty(*args):
            thetabias = 0
            y = float(self.yposnrvar.get())

            if self.check_point(self.xproj, y, self.zproj) or self.focus_get().__str__() != ".!entry2":
                pass
            else:
                self.xposnrvar.set(np.sqrt(1 - y ** 2))

                if y < 0:
                    thetabias = 360

                try:
                    self.thetanrvar.set(str(thetabias + np.degrees(np.arctan(y / float(self.xposnrvar.get())))) + "°")
                except ZeroDivisionError:
                    self.thetanrvar.set("90°")


        self.yposnrvar = tk.StringVar()
        self.yposnrvar.trace_add("write", ptesty)

        def ptestz(*args):
            z = float(self.zposnrvar.get())

            if self.check_point(self.xproj, self.yproj, z) or self.focus_get().__str__() != ".!entry3":
                pass
            else:
                self.phinrvar.set(np.str(np.degrees(np.arcsin(z))) + "°")

                theta, phi = self.getvarangles()
                self.xposnrvar.set(np.cos(theta) * np.cos(phi))
                self.yposnrvar.set(np.sin(theta) * np.cos(phi))


        self.zposnrvar = tk.StringVar()
        self.zposnrvar.trace_add("write", ptestz)

        def ptesttheta(*args):
            try:
                theta, phi = self.getvarangles()
            except:
                return None

            if self.focus_get().__str__() not in [".!entry4", ".!entry5"]:
                pass
            else:
                self.xposnrvar.set(np.cos(theta) * np.cos(phi))
                self.yposnrvar.set(np.sin(theta) * np.cos(phi))
                self.zposnrvar.set(np.sin(phi))

        self.thetanrvar = tk.StringVar()
        self.thetanrvar.trace_add("write", ptesttheta)

        self.phinrvar = tk.StringVar()
        self.phinrvar.trace_add("write", ptesttheta)

    def update_pos(self, theta, phi):
        self.theta = theta
        self.phi = phi

        self.xpos = np.cos(self.theta)
        self.ypos = np.sin(self.theta)
        self.zpos = np.sin(self.phi)

    def update_proj(self, angles):
        theta, phi = angles

        # Update the coordinates
        self.thetaproj = theta
        self.phiproj = phi

        self.xproj = np.cos(self.thetaproj) * np.cos(self.phiproj)
        self.yproj = np.sin(self.thetaproj) * np.cos(self.phiproj)
        self.zproj = np.sin(self.phiproj)

        # Update the plot
        self.projpos[0].set_data(np.asarray([self.xproj]), np.asarray([self.yproj]))
        self.projpos[0].set_3d_properties(np.asarray([self.zproj]))

        self.projposlnx[0].set_data(np.asarray([0, self.xproj]), np.asarray([0, self.yproj]))
        self.projposlnx[0].set_3d_properties([0, 0])

        self.projposlnz[0].set_data(np.asarray([self.xproj, self.xproj]), np.asarray([self.yproj, self.yproj]))
        self.projposlnz[0].set_3d_properties(np.asarray([0, self.zproj]))

        self.projposlnxyz[0].set_data(np.asarray([0, self.xproj]), np.asarray([0, self.yproj]))
        self.projposlnxyz[0].set_3d_properties(np.asarray([0, self.zproj]))

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, rowspan=10, columnspan=1)

        # Move the telescope
        self.move_telescope(angles)


    def loop_cords(self):
        pass

    # occupies (0,0) and shows the position/next coordinates of the telescope
    def create_plot(self):
        s = sphere(0, 0, 0, 1)
        s.draw()
        s.plot(self.ax, [20, -80])

        plt.axis('off')
        plt.tight_layout()

        plt.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, rowspan=10, columnspan=1)

    # occupies (0,1) and shows the current position of the telescope in x, y, z and angles
    def show_cords(self):

        self.row = 0

        header = tk.Label(self, text="Current position", font=("Arial", 15))
        header.grid(column=1, row=self.row, columnspan=2)

        self.row += 1

        xposlbl = tk.Label(self, text="x: ")
        xposlbl.grid(column=1, row=self.row)
        xposnr = tk.Label(self, text=str(self.xpos))
        xposnr.grid(column=2, row=self.row)

        thetalbl = tk.Label(self, text="theta: ")
        thetalbl.grid(column=3, row=self.row)
        thetanr = tk.Label(self, text=str(np.degrees(self.theta)) + "°")
        thetanr.grid(column=4, row=self.row)

        # End of row 0 block
        self.row += 1

        yposlbl = tk.Label(self, text="y: ")
        yposlbl.grid(column=1, row=self.row)
        yposnr = tk.Label(self, text=str(self.ypos))
        yposnr.grid(column=2, row=self.row)

        philbl = tk.Label(self, text="phi: ")
        philbl.grid(column=3, row=self.row)
        phinr = tk.Label(self, text=str(np.degrees(self.phi)) + "°")
        phinr.grid(column=4, row=self.row)

        self.row += 1

        zposlbl = tk.Label(self, text="z: ")
        zposlbl.grid(column=1, row=self.row)
        zposnr = tk.Label(self, text=str(self.zpos))
        zposnr.grid(column=2, row=self.row)

        self.row += 1

    def enter_cords(self):

        self.row = 4

        header = tk.Label(self, text="New position", font=("Arial", 15))
        header.grid(column=1, row=self.row, columnspan=2)

        self.row += 1

        # Entry fields for the coordinates / angles
        xposlbl = tk.Label(self, text="x: ")
        xposlbl.grid(column=1, row=self.row)

        xposnr = tk.Entry(self, textvariable=self.xposnrvar)
        xposnr.insert(0, string=str(self.xproj))
        xposnr.grid(column=2, row=self.row)

        self.row += 1

        # y-coordinate
        yposlbl = tk.Label(self, text="y: ")
        yposlbl.grid(column=1, row=self.row)

        yposnr = tk.Entry(self, textvariable=self.yposnrvar)
        yposnr.insert(0, string=str(self.yproj))
        yposnr.grid(column=2, row=self.row)

        self.row += 1

        # z-coordinate
        zposlbl = tk.Label(self, text="z: ")
        zposlbl.grid(column=1, row=self.row)

        zposnr = tk.Entry(self, textvariable=self.zposnrvar)
        zposnr.insert(0, string=str(self.zproj))
        zposnr.grid(column=2, row=self.row)

        self.row += 1

        # theta angle
        thetalbl = tk.Label(self, text="theta: ")
        thetalbl.grid(column=1, row=self.row)

        thetanr = tk.Entry(self, textvariable=self.thetanrvar)
        thetanr.insert(0, string=str(np.degrees(self.thetaproj)) + " °")
        thetanr.grid(column=2, row=self.row)

        # phi angle
        philbl = tk.Label(self, text="phi: ")
        philbl.grid(column=3, row=self.row)

        phinr = tk.Entry(self, textvariable=self.phinrvar)
        phinr.insert(0, string=str(np.degrees(self.phiproj)) + " °")
        phinr.grid(column=4, row=self.row)

        self.row += 1

        # Button to update the coordinates
        def getcords():
            x, y, z, theta, phi = float(xposnr.get()), float(yposnr.get()), float(zposnr.get()), thetanr.get(), phinr.get()

            if theta[-1] == "°":
                theta = np.radians(float(theta[:-1]))
            elif theta.split(" ")[-1] == "deg":
                theta = np.radians(float(theta[:-3]))
            elif theta.split(" ")[-1] == "rad":
                theta = float(theta[:-3])

            if phi[-1] == "°":
                phi = np.radians(float(phi[:-1]))
            elif phi.split(" ")[-1] == "deg":
                phi = np.radians(float(phi[:-3]))
            elif phi.split(" ")[-1] == "rad":
                phi = float(phi[:-3])

            return theta, phi

        updatebtn = tk.Button(self, text="Update", command=lambda: self.update_proj(getcords()))
        updatebtn.grid(column=1, row=self.row, columnspan=2, sticky='nesw')

        loopbtn = tk.Button(self, text="Loop", command=lambda: self.loop_cords(xposnr.get(), yposnr.get(), zposnr.get(), thetanr.get(), phinr.get()))
        loopbtn.grid(column=3, row=self.row, columnspan=2, sticky='nesw')

        toolbarFrame = tk.Frame(self)
        toolbarFrame.grid(row=self.row, column=0)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)

    def getvarangles(self):

        theta, phi = self.thetanrvar.get(), self.phinrvar.get()

        if theta[-1] == "°":
            theta = np.radians(float(theta[:-1]))
        elif theta.split(" ")[-1] == "deg":
            theta = np.radians(float(theta[:-3]))
        elif theta.split(" ")[-1] == "rad":
            theta = float(theta[:-3])

        if phi[-1] == "°":
            phi = np.radians(float(phi[:-1]))
        elif phi.split(" ")[-1] == "deg":
            phi = np.radians(float(phi[:-3]))
        elif phi.split(" ")[-1] == "rad":
            phi = float(phi[:-3])

        return theta, phi

    def check_point(self, x, y, z) -> bool:
        return 1 - 0.0001 <= np.sqrt(x ** 2 + y ** 2 + z ** 2) <= 1 + 0.0001

    def move_telescope(self, angles: list) -> None:
        theta, phi = angles
        pass



class drag_event:
    def __init__(self, widget):
        self.widget = widget
        self.widget.bind("<ButtonPress-1>", self.on_button_press)
        self.widget.bind("<B1-Motion>", self.on_move_press)
        self.widget.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.widget.focus_set()
        self.x = event.x
        self.y = event.y

    def on_move_press(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.x = event.x
        self.y = event.y
        self.widget.move("current", deltax, deltay)

    def on_button_release(self, event):
        pass

if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()