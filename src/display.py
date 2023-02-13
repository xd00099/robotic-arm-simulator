import tkinter as tk
from tkinter import ttk
from src.canvas_helper import *

class Display:
    def __init__(self, root, width, height, bg):
        self.root = root
        self.canvas = tk.Canvas(root, width=width, height=height, bg=bg)
        self.canvas.pack()
        self.mode = False
        self.switch_button = tk.Button(root, text="Track Trajectory OFF", background="red", command=self.switch_mode)
        self.switch_button.pack()

        draw_grid(self.canvas, "gray")
        draw_circle(self.canvas, "blue")

    def add_robot(self, robot):
        self.robot = robot

    def add_sliders(self):
        self.angle1_slider = tk.Scale(self.root, from_=0, to=180, orient="horizontal", 
            command=lambda x: on_slider_move(self.robot, self.angle1_slider, self.angle2_slider, self.angle3_slider))
        self.angle1_slider.set(90)
        self.angle1_slider.pack()

        self.angle2_slider = tk.Scale(self.root, from_=-180, to=180, orient="horizontal", 
            command=lambda x: on_slider_move(self.robot, self.angle1_slider, self.angle2_slider, self.angle3_slider))
        self.angle2_slider.set(90)
        self.angle2_slider.pack()

        self.angle3_slider = tk.Scale(self.root, from_=-180, to=180, orient="horizontal", 
            command=lambda x: on_slider_move(self.robot, self.angle1_slider, self.angle2_slider, self.angle3_slider))
        self.angle3_slider.set(90)
        self.angle3_slider.pack()
    
    def update_sliders(self, angle1, angle2, angle3):
        self.angle1_slider.set(math.degrees(angle1))
        self.angle2_slider.set(math.degrees(angle2))
        self.angle3_slider.set(math.degrees(angle3))

    def switch_mode(self):
        if not self.mode:
            self.switch_button.config(text="Track Trajectory ON", background="green")
        else:
            self.switch_button.config(text="Track Trajectory OFF", background="red")
        self.mode = not self.mode

    def add_table(self):
        # Create the table
        tree = ttk.Treeview(self.root, columns=("B pos", "A-B ∡", "Δ A-B ∡", "C pos", "B-C ∡", "Δ B-C ∡", "D pos", "C-D ∡", "Δ C-D ∡", "Max Δ ∡"))
        tree.heading("#0", text="Dot #")
        tree.column("#0", width=50, minwidth=50, stretch=tk.NO)
        tree.heading("B pos", text="B pos")
        tree.column("B pos", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("A-B ∡", text="A-B ∡")
        tree.column("A-B ∡", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("Δ A-B ∡", text="Δ A-B ∡")
        tree.column("Δ A-B ∡", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("C pos", text="C pos")
        tree.column("C pos", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("B-C ∡", text="B-C ∡")
        tree.column("B-C ∡", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("Δ B-C ∡", text="Δ B-C ∡")
        tree.column("Δ B-C ∡", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("D pos", text="D pos")
        tree.column("D pos", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("C-D ∡", text="C-D ∡")
        tree.column("C-D ∡", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("Δ C-D ∡", text="Δ C-D ∡")
        tree.column("Δ C-D ∡", width=80, minwidth=80, stretch=tk.NO)
        tree.heading("Max Δ ∡", text="Max Δ ∡")
        tree.column("Max Δ ∡", width=80, minwidth=80, stretch=tk.NO)
        tree.pack(side="left", fill="y")
        self.table = tree

    def on_click(self, event):
        x, y = event.x, event.y

        self.robot.move(x,y)