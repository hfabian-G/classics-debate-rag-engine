from argue import argue
from retrieve import retrieve
from agent import agent
import json
from datetime import datetime

def coordinate_debate(question:str, prompt: str):

    agent_a = agent(question, 'YES', prompt)
    agent_b = agent(question, 'NO', prompt)

    chunk_count = 6

    chunks = retrieve(question, chunk_count)
    chunks_for_a = chunks
    chunks_for_b = chunks

    agent_a.set_chunks(chunks_for_a)
    agent_b.set_chunks(chunks_for_b)

    argument_log = {}

    max_rounds = 3
    for i in range(max_rounds):
        agent_a_response = agent_a.argue()
        agent_b_response = agent_b.argue()

        argument_log[f'round {str(i)}'] = {
            'agent_a_prompt':agent_a.prompt,
            'agent_b_prompt':agent_b.prompt,
            'agent_a_response':agent_a_response, 
            'agent_b_response': agent_b_response,
            'agent_a_chunks':chunks_for_a,
            'agent_b_chunks':chunks_for_b
            
        }

        agent_a.set_opponents_previous_argument(agent_b_response)
        agent_b.set_opponents_previous_argument(agent_a_response)

        chunks_for_a = retrieve(agent_b_response, chunk_count)
        chunks_for_b = retrieve(agent_a_response, chunk_count)

        if i < max_rounds - 1:
            agent_a.set_chunks(chunks_for_a)
            agent_b.set_chunks(chunks_for_b)

    timestamp = datetime.now().isoformat()
    with open(f'logs/argument_{timestamp}.log', 'w') as file:
        json.dump(argument_log, file, indent = 2)

def coordinate_poisoned_debate(question: str, prompt: str):

    agent_a = agent(question, 'YES', prompt)
    agent_b = agent(question, 'NO', prompt)

    chunk_count = 6

    chunks = retrieve(question, chunk_count)
    chunks_for_a = chunks
    chunks_for_b = chunks

    agent_a.set_chunks(chunks_for_a)
    agent_b.set_chunks(chunks_for_b)

    argument_log = {}

    max_rounds = 3
    for i in range(max_rounds):
        agent_a_response = agent_a.argue()
        agent_b_response = agent_b.argue()

        argument_log[f'round {str(i)}'] = {
            'agent_a_prompt':agent_a.prompt,
            'agent_b_prompt':agent_b.prompt,
            'agent_a_response':agent_a_response, 
            'agent_b_response': agent_b_response,
            'agent_a_chunks':chunks_for_a,
            'agent_b_chunks':chunks_for_b
            
        }

        agent_a.set_opponents_previous_argument(agent_b_response)
        agent_b.set_opponents_previous_argument(agent_a_response)

        chunks_for_a = retrieve(agent_b_response, chunk_count)
        chunks_for_b = retrieve(agent_a_response, chunk_count)

        if i < max_rounds - 1:
            agent_a.set_chunks(chunks_for_a)
            agent_b.set_chunks(chunks_for_b)

    timestamp = datetime.now().isoformat()
    with open(f'logs/poisoned_argument_{timestamp}.log', 'w') as file:
        json.dump(argument_log, file, indent = 2)

if __name__ == '__main__':

    question = 'Is Achilles culpable for the death of Patroclus?'

    prompt = f"""You are a historian of the Greek Classics engaging in debate about the Iliad with another historian

The debate topic presented to you about the Iliad is: ***QUESTION***
This is your position: ***POSITION***

You will now be provided with several documents (chunks) from the Iliad in the form of Book Number and Text: 

***CHUNKS***

***CHUNKS***

You must come up with a convincing argument to support your position using the provided documents. The documents that have been provided are not guaranteed to be useful for your argument. If a document serves no purpose to you, discard it.

Your goal is to make as effective an argument as possible. Arguments are effective when they:
Are persuasive in nature
Avoid logical fallacies
Introduce premises and walk the reader from premise to conclusion, informing all the steps along the way
Try to anticipate the objections of an onlistener

RESPONSE MUST INCLUDE:
Argument(s) that cite those provided documents that have not been discarded. 
At least one citation, but as many as possible

"""
    coordinate_debate(question, prompt)
