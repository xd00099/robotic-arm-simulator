import math

# Function to draw grid on canvas
def draw_grid(canvas, color):
    # Loop to create horizontal lines
    for i in range(20, 621, 20):
        canvas.create_line(i, 20, i, 320, fill=color)
    # Loop to create vertical lines
    for j in range(20, 321, 20):
        canvas.create_line(20, j, 620, j, fill=color)

# Function to draw circle on canvas
def draw_circle(canvas, color):
    # Draw the arc with specified start and extent angles
    canvas.create_arc(20, 20, 620, 620, start=0, extent=180, outline=color)

# Function to draw arm on canvas
def draw_arm(canvas, angle1, angle2, angle3, color):
    # Calculate x and y coordinates of each point
    x_b = 320-150 * math.cos(angle1)
    y_b = 320-150 * math.sin(angle1)
    x_c = x_b - 100 * math.cos(angle1 + angle2)
    y_c = y_b - 100 * math.sin(angle1 + angle2)
    x_d = x_c - 50 * math.cos(angle1 + angle2 + angle3)
    y_d = y_c - 50 * math.sin(angle1 + angle2 + angle3)

    # Draw lines connecting the points
    canvas.create_line(320, 320, x_b, y_b, fill=color)
    canvas.create_line(x_b, y_b, x_c, y_c, fill=color)
    canvas.create_line(x_c, y_c, x_d, y_d, fill=color)

# Function to update arm position on canvas
def on_slider_move(robot, angle1_slider, angle2_slider, angle3_slider):
    # Get angles from sliders
    angle1 = angle1_slider.get()
    angle2 = angle2_slider.get()
    angle3 = angle3_slider.get()
    # Update arm with converted angles to radians
    robot.update_arm(math.radians(angle1), math.radians(angle2), math.radians(angle3))
