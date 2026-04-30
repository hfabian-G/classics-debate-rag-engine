import json
from datetime import datetime
from argue import score
import glob
import os
import yaml

def score_debate(file_name, log_sub_folder = ''):

    prompt = ''
    with open('prompt_pieces.yml','r') as file:
        config = yaml.safe_load(file)
        prompt = config['debate_score_prompt']

    output = {}

    with open(file_name, 'r') as file:
        data = json.load(file)
        
        for round in data:
            for agent in ('agent_a','agent_b'):
                argument_data = {}
                argument_data['question'] = data[round]['question']
                argument_data['position'] = data[round][f'{agent}_position']
                argument_data['response'] = data[round][f'{agent}_response']
                argument_data['documents'] = data[round][f'{agent}_chunks']

                individual_prompt = prompt + f"'Question being debated': '{argument_data['question']}', 'agents position': '{argument_data['position']}', 'agent response': '{argument_data['response']}', 'documents': '{argument_data['documents']}'"

                response = score(individual_prompt)
                json_response = json.loads(response)

                if round not in output:
                    output[round] = {}

                output[round][agent] = json_response['scores']

        for round in output:
            for agent in output[round]:
                total_score = 0
                for score_category in output[round][agent]:
                    if score_category != 'citation_quantity':
                        total_score += int(output[round][agent][score_category])
                output[round][agent]['total_score'] = total_score

    output['chunk_uniqueness'] = count_chunk_uniqueness(file_name)

    timestamp = datetime.now().isoformat()
    file_path = f'logs/{log_sub_folder}/scores/scored_argument_{timestamp}.log'

    with open(file_path, 'w') as file:
        json.dump(output, file, indent = 2)

def find_most_recent_file(directory):
    list_of_files = glob.glob(f"{directory}/*")
    latest_file = max(list_of_files, key = os.path.getmtime)
    return latest_file

def count_chunk_uniqueness(file_name):
    with open(file_name,'r') as file:
        
        data = json.load(file)

        unique_chunks = set()
        total_chunks_count = 0

        for round in data:
            agent_a_chunks = list(data[round]['agent_a_chunks'])
            agent_b_chunks = list(data[round]['agent_b_chunks'])
            unified_chunks = agent_a_chunks + agent_b_chunks
            total_chunks_count += len(unified_chunks)
            for chunk in unified_chunks:
                unique_chunks.add(chunk['text'])

        return len(unique_chunks)/total_chunks_count

if __name__ == '__main__':
    standard_file = find_most_recent_file('logs/standard')
    poisoned_file = find_most_recent_file('logs/poisoned')

    score_debate(standard_file,'standard')
    score_debate(poisoned_file,'poisoned')