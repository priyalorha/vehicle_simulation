import simpy
import random

from Vessel import Vessel
from container_terminal import ContainerTerminal
from variables import NUM_BERTHS, NUM_QUAY_CRANES, NUM_TRUCKS, SIMULATION_TIME, CONTAINERS_PER_VESSEL

def vessel_generator(env, terminal, num_vessels):
    vessel_count = 0
    while vessel_count < num_vessels:
        yield env.timeout(random.expovariate(1 / 5))  # Exponential distribution with mean of 5 hours
        vessel_count += 1
        vessel = Vessel(env, f"Vessel_{vessel_count}", CONTAINERS_PER_VESSEL)
        env.process(terminal.arrive_vessel(vessel))


def simulate(num_vessels, sim_duration):
    env = simpy.Environment()
    terminal = ContainerTerminal(env, num_berths=NUM_BERTHS, num_cranes=NUM_QUAY_CRANES, num_trucks=NUM_TRUCKS)
    env.process(vessel_generator(env, terminal, num_vessels))
    env.run(until=sim_duration)  # Simulate for specified duration


if __name__ == "__main__":
    num_vessels = 10  # Number of vessels to simulate
    sim_duration = SIMULATION_TIME  # Duration of the simulation in hours
    simulate(num_vessels, sim_duration)
