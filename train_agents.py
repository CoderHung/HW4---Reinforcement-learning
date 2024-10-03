from agents import ValueIteration, PolicyIteration
import json
from tqdm import tqdm

##################################### Value Iteration #####################################


agent = ValueIteration()
agent.value_iteration()

policy = {}
for x in agent.policy:
    policy[str(x)] = agent.policy[x]

with open("Policies/valueIteration.json", 'w') as json_file:
    json.dump(policy, json_file)

