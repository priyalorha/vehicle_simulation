import simpy


class ContainerTerminal:
    def __init__(self, env, num_berths, num_cranes, num_trucks):
        self.env = env
        self.berths = simpy.Resource(env, capacity=num_berths)
        self.cranes = simpy.Resource(env, capacity=num_cranes)
        self.trucks = simpy.Resource(env, capacity=num_trucks)
        self.waiting_queue = []

    def arrive_vessel(self, vessel):
        if len(self.berths.users) < self.berths.capacity:
            print(f"Vessel {vessel.name} arrives at time {self.env.now}")
            with self.berths.request() as berth_req:
                yield berth_req
                print(f"Vessel {vessel.name} berths at time {self.env.now}")
                with self.cranes.request() as crane_req:
                    yield crane_req
                    print(f"Quay crane starts unloading containers from vessel {vessel.name} at time {self.env.now}")
                    yield self.env.process(self.unload_cargo(vessel))
        else:
            print(
                f"Vessel {vessel.name} arrives but all berths are full. Added to waiting queue at time {self.env.now}")
            self.waiting_queue.append(vessel)

    def unload_cargo(self, vessel):
        containers_remaining = vessel.containers
        while containers_remaining > 0:
            # Move container from vessel to truck
            with self.trucks.request() as truck_req:
                yield truck_req
                print(f"Quay crane moves a container from vessel {vessel.name} to a truck at time {self.env.now}")
                yield self.env.timeout(3)  # Time taken by crane to move one container
                print(f"Container moved from vessel {vessel.name} to truck at time {self.env.now}")

            # Drop off container at yard block
            yield self.env.timeout(6)  # Time taken by truck to drop off container at yard block
            print(f"Truck drops off container at yard block at time {self.env.now}")

            containers_remaining -= 1

        print(f"All containers unloaded from vessel {vessel.name} at time {self.env.now}")

        # Check if there are vessels waiting in the queue
        if self.waiting_queue:
            next_vessel = self.waiting_queue.pop(0)
            print(f"Vessel {next_vessel.name} from waiting queue starts berthing at time {self.env.now}")
            yield self.env.process(self.arrive_vessel(next_vessel))
        else:
            print("No vessels in the waiting queue.")