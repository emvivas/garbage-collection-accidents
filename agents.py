import mesa
from random_walk import RandomWalker

class GarbageCollectionCar(RandomWalker):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        garbage = [obj for obj in this_cell if isinstance(obj, Garbage)]
        garbage_collector = [obj for obj in this_cell if isinstance(obj, GarbageCollector)]
        garbage_collection_car = [obj for obj in this_cell if isinstance(obj, GarbageCollectionCar)]
        if len(garbage) > 0:
            garbage_to_collect = self.random.choice(garbage)
            self.model.grid.remove_agent(garbage_to_collect)
            self.model.schedule.remove(garbage_to_collect)
        for death in garbage_collector:
            new_death = Death(self.model.next_id(), death.pos, self.model)
            self.model.grid.place_agent(new_death, death.pos)
            self.model.schedule.add(new_death)
            self.model.grid.remove_agent(death)
            self.model.schedule.remove(death)
        if len(garbage_collection_car) > 1:
            for crash in garbage_collection_car:
                new_crash = Crash(self.model.next_id(), crash.pos, self.model)
                self.model.grid.place_agent(new_crash, crash.pos)
                self.model.schedule.add(new_crash)
    
    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        roads = []
        next_move = None
        while len(roads)==0:
            next_move = self.random.choice(next_moves)
            this_cell = self.model.grid.get_cell_list_contents([next_move])
            roads = [obj for obj in this_cell if isinstance(obj, Road)]
            crashes = [obj for obj in this_cell if isinstance(obj, Crash)]
            if len(crashes)>0:
                continue
        self.model.grid.move_agent(self, next_move)

class GarbageCollector(RandomWalker):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()

class Garbage(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class Pavement(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class Road(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class Crash(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

class Death(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
