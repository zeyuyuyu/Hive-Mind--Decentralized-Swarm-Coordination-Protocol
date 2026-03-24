import os
import time
import random
import logging

from hive_mind.agent import Agent
from hive_mind.swarm import Swarm
from hive_mind.consensus import ConsensusProtocol

# Initialize logger
logging.basicConfig(level=logging.INFO)

# Create a new swarm
swarm = Swarm()

# Register agents to the swarm
for _ in range(100):
    agent = Agent()
    swarm.register_agent(agent)

# Start the consensus protocol
consensus = ConsensusProtocol(swarm)
consensus.start()

# Main loop
while True:
    # Agents perform tasks and update their state
    for agent in swarm.agents:
        agent.perform_task()
        agent.update_state()

    # Swarm coordinates through the consensus protocol
    consensus.update()

    # Wait for a short period of time
    time.sleep(random.uniform(0.1, 1.0))