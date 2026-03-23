
import numpy as np
import time
from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose


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

    def __init__(self, label):
        self.label = label
        self.position = None
        self.prev_position = None

    def update(self, new_position):
        self.prev_position = self.position
        self.position = new_position



class RobotController:

    def __init__(self, mini):
        self.mini = mini

    def look_left(self):
        print("Robot looks LEFT")
        self.mini.goto_target(
            head=create_head_pose(yaw=30, degrees=True),
            duration=1.0
        )

    def look_right(self):
        print("Robot looks RIGHT")
        self.mini.goto_target(
            head=create_head_pose(yaw=-30, degrees=True),
            duration=1.0
        )

    def look_forward(self):
        print("Robot looks FORWARD")
        self.mini.goto_target(
            head=create_head_pose(yaw=0, degrees=True),
            duration=1.0
        )

    def idle(self):
        print("Robot IDLE")
        self.look_forward()



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



def get_perception_data(step):
        return {
            "human": (1.5 - step * 0.05, 0, 0),
            "cup": (0, 0, 0)
        }
    


def main():

        human = Entity("human")
        cup = Entity("cup")

        engine = QSREngine()

    # Connect to Reachy
        with ReachyMini() as mini:

            robot = RobotController(mini)
            behavior = BehaviorManager(robot)

            print("Connected to Reachy Mini ✅")

            for step in range(20):

                data = get_perception_data(step)

                if "human" in data and "cup" in data:

                    human.update(data["human"])
                    cup.update(data["cup"])

                    phase = engine.compute_phase(human, cup)

                    behavior.react(phase)

                time.sleep(1.0)