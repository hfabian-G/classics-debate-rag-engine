from retrieve import retrieve
from agent import agent
import json
from datetime import datetime
import yaml

def coordinate_side_by_side_debate(question:str,prompt:str):

    coordinate_debate(question, prompt)
    coordinate_debate(question, prompt, poisoned=True)

def coordinate_debate(question:str, prompt: str, poisoned: bool = False, undermine_self: bool = False):

    CHUNK_COUNT = 6
    ROUNDS = 4

    agent_a = agent(question, 'YES', prompt)
    agent_b = agent(question, 'NO', prompt)

    if poisoned:
        agent_a.set_poisoner()

    chunks = retrieve(question, CHUNK_COUNT)
    chunks_for_a = chunks
    chunks_for_b = chunks

    agent_a.set_chunks(chunks_for_a)
    agent_b.set_chunks(chunks_for_b)

    argument_log = {}

    for i in range(ROUNDS):
        agent_a_response = agent_a.argue()
        agent_b_response = agent_b.argue()

        argument_log[f'round {str(i)}'] = {
            'question':agent_a.question,
            'agent_a_prompt':agent_a.prompt,
            'agent_a_position': agent_a.position,
            'agent_b_prompt':agent_b.prompt,
            'agent_b_position': agent_b.position,
            'agent_a_response':agent_a_response, 
            'agent_b_response': agent_b_response,
            'agent_a_chunks':chunks_for_a,
            'agent_b_chunks':chunks_for_b
        }

        agent_a.set_opponents_previous_argument(agent_b_response)
        agent_b.set_opponents_previous_argument(agent_a_response)

        assert agent_a_response is not None
        assert agent_b_response is not None

        if i < ROUNDS - 1:
            chunks_for_a = retrieve(agent_b_response, CHUNK_COUNT)
            chunks_for_b = retrieve(agent_a_response, CHUNK_COUNT)
            agent_a.set_chunks(chunks_for_a)
            agent_b.set_chunks(chunks_for_b)

    timestamp = datetime.now().isoformat()
    file_path = ''

    if poisoned:
        file_path = f'logs/poisoned/argument_{timestamp}.log'
    else:
        file_path = f'logs/standard/argument_{timestamp}.log'

    with open(file_path, 'w') as file:
        json.dump(argument_log, file, indent = 2)

if __name__ == '__main__':

    question = 'Is Achilles culpable for the death of Patroclus?'

    prompt = ''
    
    with open('prompt_pieces.yml','r') as file:
        config = yaml.safe_load(file)
        prompt = config['prompt']

    coordinate_debate(question, prompt)

    coordinate_debate(question, prompt, poisoned=True)
