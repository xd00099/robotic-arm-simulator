import tkinter as tk
from src.robot import Robot
from src.canvas_helper import *
from src.display import Display

if __name__=="__main__":
    
    root = tk.Tk()
    root.title("Robotic Arm Simulator")

    # initialize screens and robots
    display = Display(root, width=640, height=350, bg="white")
    robot = Robot(display)
    display.add_robot(robot)
    robot.render()
    display.add_sliders()
    display.canvas.bind("<Button-1>", display.on_click)
    display.add_table()

    
    root.mainloop()