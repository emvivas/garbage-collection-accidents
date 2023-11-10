import mesa

from agents import GarbageCollectionCar, GarbageCollector, Garbage, Pavement, Road, Crash, Death
from model import GarbageCollection


def garbage_collection_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is GarbageCollectionCar:
        portrayal["Shape"] = "resources/garbage-collection-car.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is GarbageCollector:
        portrayal["Shape"] = "resources/garbage-collector.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
    
    elif type(agent) is Pavement:
        portrayal["Color"] = ["#F3D500"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1
    
    elif type(agent) is Road:
        portrayal["Color"] = ["#CFCFCF"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1


    elif type(agent) is Garbage:
        portrayal["Shape"] = "resources/garbage.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
    
    elif type(agent) is Crash:
        portrayal["Shape"] = "resources/crash.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
    
    elif type(agent) is Death:
        portrayal["Shape"] = "resources/rip.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(garbage_collection_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Crash", "Color": "#FFCE30"},
        {"Label": "Death", "Color": "#E83845"},
        {"Label": "GarbageCollectionCar", "Color": "#E389B9"},
        {"Label": "GarbageCollector", "Color": "#746AB0"},
        {"Label": "Garbage", "Color": "#288BA8"},
    ]
)

model_params = {
}

server = mesa.visualization.ModularServer(
    GarbageCollection, [canvas_element, chart_element], "Garbage Collection", model_params
)
server.port = 8524
