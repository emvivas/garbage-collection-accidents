import mesa
from agents import GarbageCollectionCar, GarbageCollector, Garbage, Pavement, Road, Crash, Death
from scheduler import RandomActivationByTypeFiltered

class GarbageCollection(mesa.Model):

    height = 20
    width = 20
    initial_garbageCollectionCars = 3
    initial_garbageCollectors = 6
    initial_garbage = 20
    verbose = False
    description = ("A model for simulating garbage collection process with accidents.")

    def __init__(
        self,
        width=20,
        height=20,
        initial_garbageCollectionCars = 3, 
        initial_garbageCollectors = 6, 
        initial_garbage = 20, 
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.initial_garbageCollectionCars = initial_garbageCollectionCars 
        self.initial_garbageCollectors = initial_garbageCollectors
        self.initial_garbage = initial_garbage
        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Crash": lambda m: m.schedule.get_type_count(Crash),
                "Death": lambda m: m.schedule.get_type_count(Death),
                "GarbageCollectionCar": lambda m: m.schedule.get_type_count(GarbageCollectionCar),
                "GarbageCollector": lambda m: m.schedule.get_type_count(GarbageCollector),
                "Garbage": lambda m: m.schedule.get_type_count(Garbage),
            }
        )
        # Create garbage collection cars
        for i in range(self.initial_garbageCollectionCars):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            garbageCollectionCar = GarbageCollectionCar(self.next_id(), (x, y), self, True)
            self.grid.place_agent(garbageCollectionCar, (x, y))
            self.schedule.add(garbageCollectionCar)
        # Create garbage collectors
        for i in range(self.initial_garbageCollectors):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            garbageCollector = GarbageCollector(self.next_id(), (x, y), self, True)
            self.grid.place_agent(garbageCollector, (x, y))
            self.schedule.add(garbageCollector)
        # Create paths
        map = ["#######-----##-----#", 
               "#-----#-----##-----#", 
               "#-----------##-----#", 
               "#-----------##-----#", 
               "#-----------##-----#", 
               "#-----------##-----#",
               "#-----#-----##-----#",
               "#######-----##-----#",
               "------------##------",
               "------------##------",
               "------------##------",
               "--------------------",
               "--------------------",
               "#######------------#",
               "#-----#------------#",
               "#-----#------------#",
               "#-----########-----#",
               "#------------------#",
               "#------------------#",
               "#######-----##-----#"]
        for line in range(len(map)):
            for character in range(len(map[line])):
                x = character
                y = line
                way = Pavement(self.next_id(), (x, y), self) if(map[line][character]=="#") else Road(self.next_id(), (x, y), self)
                self.grid.place_agent(way, (x, y))
                self.schedule.add(way)
        # Create garbage
        for i in range(self.initial_garbage):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            garbage = Garbage(self.next_id(), (x, y), self)
            self.grid.place_agent(garbage, (x, y))
            self.schedule.add(garbage)
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(GarbageCollectionCar),
                    self.schedule.get_type_count(GarbageCollector),
                    self.schedule.get_type_count(Pavement),
                    self.schedule.get_type_count(Garbage),
                ]
            )

    def run_model(self, step_count=200):
        if self.verbose:
            print("Initial number garbage collection cars: ", self.schedule.get_type_count(GarbageCollectionCar))
            print("Initial number garbage collectors: ", self.schedule.get_type_count(GarbageCollector))
            print("Initial number garbage: ", self.schedule.get_type_count(Garbage))
        for i in range(step_count):
            self.step()
        if self.verbose:
            print("")
            print("Final number garbage collection cars: ", self.schedule.get_type_count(GarbageCollectionCar))
            print("Final number garbage collectors: ", self.schedule.get_type_count(GarbageCollector))
            print("Final number garbage: ", self.schedule.get_type_count(Garbage))
