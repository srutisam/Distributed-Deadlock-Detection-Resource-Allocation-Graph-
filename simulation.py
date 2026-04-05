import simpy
import random

class DistributedSystem:
    def __init__(self, env, num_sites, processes_per_site):
        self.env = env
        self.num_sites = num_sites
        self.processes_per_site = processes_per_site
        self.wait_for_graph = {f"P{i}": [] for i in range(num_sites * processes_per_site)}

    def request_resource(self, process, resource_owner):
        print(f"{process} requests resource from {resource_owner} at time {self.env.now}")
        self.wait_for_graph[process].append(resource_owner)

    def release_resource(self, process, resource_owner):
        if resource_owner in self.wait_for_graph[process]:
            self.wait_for_graph[process].remove(resource_owner)

    def process(self, name):
        while True:
            yield self.env.timeout(random.randint(1, 5))

            target = random.choice(list(self.wait_for_graph.keys()))
            if target != name:
                self.request_resource(name, target)

            yield self.env.timeout(random.randint(2, 6))
            self.release_resource(name, target)