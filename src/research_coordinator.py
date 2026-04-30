from debate_coordinator import coordinate_side_by_side_debate
from debate_scorer import score_debate
from debate_scorer import find_most_recent_file
import yaml
import json
from datetime import datetime
from analysis import analyze_meta_results

def coordinate_research():
    
    prompt = ''
    questions = []
    
    with open('prompt_pieces.yml','r') as file:
        config = yaml.safe_load(file)
        prompt = config['prompt']
        questions = config['questions']

    research = {}

    for question in questions:
        coordinate_side_by_side_debate(question=question, prompt=prompt, poison_self_damage=True)

        standard_file = find_most_recent_file('logs/standard')
        poisoned_file = find_most_recent_file('logs/poisoned')

        score_debate(standard_file,'standard')
        score_debate(poisoned_file,'poisoned')
        
        score_file_names = [find_most_recent_file('logs/standard/scores'), find_most_recent_file('logs/poisoned/scores')]
        for score_file_name in score_file_names:
            with open(score_file_name,'r') as file:
                scores = json.load(file)

                a_running_total = 0.0
                b_running_total = 0.0
                for round in scores:
                    for agent in scores[round]:
                        if "agent_a" == agent:
                            a_running_total += scores[round][agent]['total_score']
                        elif "agent_b" == agent:
                            b_running_total += scores[round][agent]['total_score']

                round_count = sum(1 for key in scores if 'round' in key)
                
                a_running_total /= round_count
                b_running_total /= round_count

                poisoned = 'poisoned' in score_file_name

                if question not in research:
                    research[question] = {}

                research[question]['poisoned' if poisoned else 'standard'] = {
                    "a_average": a_running_total,
                    "b_average": b_running_total,
                    "chunk_uniqueness": scores['chunk_uniqueness']
                }

    timestamp = datetime.now().isoformat()
    with open(f"logs/meta/nonabstract/meta_{timestamp}.log",'w') as file:
        json.dump(research, file, indent = 2)

    non_meta_results_file = find_most_recent_file('logs/meta/nonabstract')

    analyze_meta_results(non_meta_results_file)



if __name__ == "__main__":
    coordinate_research()

        


    