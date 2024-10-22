from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt

class SimpleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

class SimpleModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        for i in range(self.num_agents):
            a = SimpleAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            agent_reporters={"Position": lambda a: (a.pos if hasattr(a, 'pos') else None)}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


if __name__ == "__main__":
    model = SimpleModel(10, 10, 10)
    for i in range(100):
        model.step()
    
    data = model.datacollector.get_agent_vars_dataframe()
    positions = data.xs(0, level="AgentID")["Position"]
    x = [pos[0] for pos in positions]
    y = [pos[1] for pos in positions]
    
    plt.scatter(x, y)
    plt.xlabel("X координата")
    plt.ylabel("Y координата")
    plt.title("Позиції агентів після 100 кроків")
    plt.show()
