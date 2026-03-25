from qsrlib_io.world_trace import World_Trace, Object_State
from qsrlib.qsrlib import QSRlib, QSRlib_Request_Message

def build_world_trace(detections_over_time):
    world = World_Trace()

    object_tracks = {}

    # Organize data per object
    for frame in detections_over_time:
        t = frame["timestamp"]
        for obj in frame["objects"]:
            name = obj["id"]

            if name not in object_tracks:
                object_tracks[name] = []

            object_tracks[name].append(
                Object_State(
                    name=name,
                    timestamp=t,
                    x=obj["x"],
                    y=obj["y"]
                )
            )

   
    for obj_states in object_tracks.values():
        world.add_object_state_series(obj_states)

    return world


def compute_qtc(world):
    qsrlib = QSRlib()

    request = QSRlib_Request_Message(
        which_qsr="qtcbs",   
        input_data=world
    )

    response = qsrlib.request_qsrs(request)
    return response


def print_qtc(response):
    for t, qsrs in response.qsrs.trace.items():
        print(f"Time {t}:")
        for pair, relation in qsrs.qsrs.items():
            print(f"  {pair}: {relation.qsr}")


detections = [
    {"timestamp": 0, "objects": [
        {"id": "robot", "x": 0, "y": 0},
        {"id": "person", "x": 5, "y": 0}
    ]},
    {"timestamp": 1, "objects": [
        {"id": "robot", "x": 1, "y": 0},
        {"id": "person", "x": 4, "y": 0}
    ]}
]



world = build_world_trace(detections)
response = compute_qtc(world)
print_qtc(response)