import numpy as np
import time
import requests


class QTC:
    def __init__(self, threshold=0.01):
        self.prev_distance = None
        self.threshold = threshold

    def compute(self, pos_a, pos_b):

        distance = np.linalg.norm(np.array(pos_a) - np.array(pos_b))

        if self.prev_distance is None:
            self.prev_distance = distance
            return "stable"

        delta = distance - self.prev_distance
        self.prev_distance = distance

        if delta < -self.threshold:
            return "approaching"
        elif delta > self.threshold:
            return "moving_away"
        else:
            return "stable"
        

class QSREngine:

    def __init__(self):
        self.qtc = QTC()

    def compute_phase(self, human, obj):

        if human.position is None or obj.position is None:
            return "idle"

        movement = self.qtc.compute(human.position, obj.position)

        if movement == "approaching":
            return "human_approaching_object"
        elif movement == "moving_away":
            return "human_finished"
        elif movement == "stable":
            return "human_interacting"
        else:
            return "idle"
        

class Entity:
    def __init__(self,label):
        self.position  =  None
        self.label = label
        self.prev_postion = None


    def update(self, new_position):
      self.prev_postion = self.position
      self.position = new_position



class BehaviorManager:

    def __init__(self, robot_controller):
        self.robot = robot_controller

    def react(self, phase):

        print("PHASE:", phase)

        if phase == "human_approaching_object":
            self.robot.look_left()

        elif phase == "human_interacting":
            self.robot.look_forward()

        elif phase == "human_finished":
            self.robot.look_right()

        else:
            self.robot.idle()



class RobotController:

    def look_left(self):
        print("Robot looks left")

    def look_right(self):
        print("Robot looks right")

    def look_forward(self):
        print("Robot looks forward")

    def idle(self):
        print("Robot idle")

# Initialize
human = Entity("human")
cup = Entity("cup")

engine = QSREngine()
robot = RobotController()
behavior = BehaviorManager(robot)


# Fake test loop
for step in range(20):

    # Simulated human moving toward cup
    human_position = (-6.5 - step * 0.05, 0, 0)
    cup_position = (0, 0, 0)

    human.update(human_position)
    cup.update(cup_position)

    phase = engine.compute_phase(human, cup)

    behavior.react(phase)



    time.sleep(0.2)




