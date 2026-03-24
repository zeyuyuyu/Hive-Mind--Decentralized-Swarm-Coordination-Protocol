import random
import time
import math

class SwarmNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []
        self.state = 'idle'
        self.target_position = None
        self.consensus_timer = 0

    def join_swarm(self, other_nodes):
        self.neighbors = other_nodes
        for node in other_nodes:
            node.neighbors.append(self)

    def update_state(self):
        if self.state == 'idle':
            self.consensus_timer += 1
            if self.consensus_timer > 10:
                self.initiate_consensus()
        elif self.state == 'consensus':
            if self.reached_target():
                self.state = 'idle'
                self.consensus_timer = 0
            else:
                self.move_towards_target()

    def initiate_consensus(self):
        self.state = 'consensus'
        self.target_position = (random.uniform(-10, 10), random.uniform(-10, 10))
        self.broadcast_consensus()

    def broadcast_consensus(self):
        for neighbor in self.neighbors:
            neighbor.receive_consensus(self.target_position)

    def receive_consensus(self, target_position):
        self.target_position = target_position
        self.state = 'consensus'

    def reached_target(self):
        distance = math.sqrt((self.target_position[0] - self.position[0])**2 + (self.target_position[1] - self.position[1])**2)
        return distance < 0.5

    def move_towards_target(self):
        dx = self.target_position[0] - self.position[0]
        dy = self.target_position[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self.position = (self.position[0] + dx/distance, self.position[1] + dy/distance)

    @property
    def position(self):
        return (random.uniform(-10, 10), random.uniform(-10, 10))

def main():
    nodes = [SwarmNode(i) for i in range(50)]
    for node in nodes:
        node.join_swarm([n for n in nodes if n != node])

    while True:
        for node in nodes:
            node.update_state()
        time.sleep(0.1)

if __name__ == '__main__':
    main()