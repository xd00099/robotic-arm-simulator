from src.canvas_helper import *
import math



class Robot:
    """The Robot class that has three arms.

    The Robot class is responsible for creating and displaying the robotic arm on the canvas. It has 3 attributes: angle1, angle2, angle3
    that represent the angles of the three arms and a canvas object to display the robotic arm. 

    Args:
    display (obj): The display object where the robot is being rendered.
    angle1 (int, optional): Angle for the first arm. Defaults to 90.
    angle2 (int, optional): Angle for the second arm. Defaults to 90.
    angle3 (int, optional): Angle for the third arm. Defaults to 90.

    Attributes:
    angle1 (float): Angle for the first arm in radians.
    angle2 (float): Angle for the second arm in radians.
    angle3 (float): Angle for the third arm in radians.
    display (obj): The display object where the robot is being rendered.
    canvas (tkinter.Canvas): The canvas object that displays the robotic arm.
    """

    def __init__(self, display, angle1=90, angle2=90, angle3=90):
        self.angle1 = math.radians(angle1)
        self.angle2 = math.radians(angle2)
        self.angle3 = math.radians(angle3)
        self.display = display
        self.canvas = display.canvas
        self.x = 420
        self.y = 220
    
    def render(self, color="red"):
        """Renders the robotic arm on the canvas.

        This method is responsible for deleting the existing robotic arm, creating the grid, circle and drawing the robotic arm. 

        Args:
        color (str, optional): Color of the robotic arm. Defaults to "red".
        """
        self.canvas.delete("all")
        draw_grid(self.canvas, "gray")
        draw_circle(self.canvas, "blue")
        draw_arm(self.canvas, self.angle1, self.angle2, self.angle3, color)
    
    def update_arm(self, angle1, angle2, angle3):
        """Updates the angles of the robotic arm.

        This method is responsible for updating the angles of the robotic arm and then calling the render method to display the updated arm. 

        Args:
        angle1 (float): Angle for the first arm in radians.
        angle2 (float): Angle for the second arm in radians.
        angle3 (float): Angle for the third arm in radians.
        """
        self.angle1 = angle1
        self.angle2 = angle2
        self.angle3 = angle3
        self.render()

    def move(self, x, y):
        """
        Move the robotic arm depending on the user's selected mode.
        Mode can be either trajectory based or direct move.
        Parameters
        ----------
        x : int
            The x-coordinate of the target position.
        y : int
            The y-coordinate of the target position.

        """
        if self.display.mode == 0:
            self.direct_move(x,y)
        else:
            self.move_in_trajectory(x,y)


    
    def direct_move(self, x,y):
        """
        Moves the end effector of the robotic arm to the specified position (x, y).

        Parameters
        ----------
        x : int
            The x-coordinate of the target position.
        y : int
            The y-coordinate of the target position.

        Returns
        -------
        None

        Notes
        -----
        This code uses the inverse kinematics of a 3-link robotic arm to determine the angles of the joints,
        given the desired end-effector position in the x,y plane. It first checks if the desired position 
        is within the workspace of the arm, which is within a certain range of the origin, and returns 
        if it's not.
        
        Next, the code splits into two cases based on the x coordinate of the desired position: 
        if x >= 320 or x < 320. For each case, it first checks if the distance from the origin to 
        the desired position is less than 100. If this condition is true, it calculates the position 
        of joint C, the angle between the x-axis and the line connecting the origin and the desired 
        position, and then uses the law of cosines to calculate the angles of each joint.
        If the distance is greater than 100, it calculates the position of joint C differently 
        and again uses the law of cosines to determine the angles of each joint.

        Finally, the code updates the angles of the joints and updates the display of the arm.
        """

        if x < 20 or x > 620 or y > 320 or y < 20:
            return

        if x >= 320:
            # test if the clickpoint to origin is shorter than CD
            if math.sqrt((320-x)**2 + (320-y)**2) < 100:
                angle_AD = math.atan((320-y)/(x-320))
                # calculate C
                Cx = x + 50*math.cos(angle_AD)
                Cy = y - 50*math.sin(angle_AD)
                AC = math.sqrt((Cx-320)**2+(Cy-320)**2)

                angle1 = math.pi - angle_AD + math.acos((150**2+AC**2-100**2)/(2*150*AC))
                if math.degrees(angle1) <= 180:
                    angle2 = -math.pi + math.acos((100**2+150**2-AC**2)/(2*100*150))
                    angle3 = -math.pi + math.acos((100**2+AC**2-150**2)/(2*100*AC))
                else:
                    angle1 = math.pi - angle_AD - math.acos((150**2+AC**2-100**2)/(2*150*AC))
                    angle2 = math.pi - math.acos((100**2+150**2-AC**2)/(2*100*150))
                    angle3 = math.pi - math.acos((100**2+AC**2-150**2)/(2*100*AC))
            else:

                # move the last arm inline with AD
                angle_AD = math.atan((320-y)/(x-320))
                # calculate C
                Cx = x - 50*math.cos(angle_AD)
                Cy = y + 50*math.sin(angle_AD)

                AC = math.sqrt((Cx-320)**2+(Cy-320)**2)

                # apply law of cosine

                # tilt to right if condition allows: angle 1 < 180
                angle1 = math.pi + math.acos((150**2+AC**2-100**2)/(2*150*AC)) - angle_AD
                if math.degrees(angle1) <= 180:
                    angle2 = -math.pi + math.acos((100**2+150**2-AC**2)/(2*100*150))
                    angle3 = math.acos((100**2+AC**2-150**2)/(2*100*AC))
                else:
                    # tilt to left if angle1 > 180
                    angle1 = math.pi - math.acos((150**2+AC**2-100**2)/(2*150*AC)) - angle_AD
                    angle2 = math.pi - math.acos((100**2+150**2-AC**2)/(2*100*150))
                    angle3 = - math.acos((100**2+AC**2-150**2)/(2*100*AC))

        else:
            if math.sqrt((320-x)**2 + (320-y)**2) < 100:
                angle_AD = math.atan((320-y)/(320-x))
                # calculate C
                Cx = x - 50*math.cos(angle_AD)
                Cy = y - 50*math.sin(angle_AD)
                AC = math.sqrt((Cx-320)**2+(Cy-320)**2)

                angle1 = angle_AD + math.acos((150**2+AC**2-100**2)/(2*150*AC))
                angle2 = -math.pi + math.acos((100**2+150**2-AC**2)/(2*100*150))
                angle3 = -math.pi + math.acos((100**2+AC**2-150**2)/(2*100*AC))

            else:

                angle_AD = math.atan((320-y)/(320-x))
                Cx = x + 50*math.cos(angle_AD)
                Cy = y + 50*math.sin(angle_AD)
                AC = math.sqrt((Cx-320)**2+(Cy-320)**2)

                # always tilt to right since it's on left half
                angle2 = math.acos((100**2+150**2-AC**2)/(2*100*150)) - math.pi
                angle3 = math.acos((100**2+AC**2-150**2)/(2*100*AC))
                angle1 = angle_AD + math.acos((150**2+AC**2-100**2)/(2*150*AC))

        # update angles
        self.display.update_sliders(angle1, angle2, angle3)
        self.update_arm(angle1, angle2, angle3)

        # update current position
        self.x = x
        self.y = y


    def move_in_trajectory(self, x, y):
        """Move the object in a smooth trajectory from its current position to (x, y).

        The movement is divided into 21 steps, and the object is moved in each step after 0.25 s.

        Params:
            x (int): The x-coordinate of the target position.
            y (int): The y-coordinate of the target position.
        """

        table = self.display.tree

        
        cur_x = self.x
        cur_y = self.y

        dx = (x - cur_x) / 21
        dy = (y - cur_y) / 21

        def move_step(i):
            nonlocal cur_x, cur_y
            cur_x += dx
            cur_y += dy
            self.direct_move(cur_x, cur_y)
            if i < 21:
                self.canvas.after(250, move_step, i + 1)

        self.canvas.after(250, move_step, 1)

        self.x = x
        self.y = y