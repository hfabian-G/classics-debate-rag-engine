import json
from datetime import datetime
from argue import score

def score_debate(file_name, output_name_modifier = ''):

    prompt = '''You are an argument grader.
Arguments are scored based on:
Textual grounding - does the argument cite passages that are textually relevant to the claim being made? Score 1-5. A 1 means citations that are not relevant to the argument. A 5 means citations are present and relate to the argument (regardless of how they help or hinder the agent's specific argument). A 3 means citations are present and real, though their connection to the argument is loose. 1 if there are no citations
Citation reality - does the argument cite real passages? If a citation is made, it must be validated to exist. 1 means inventions exist, 5 means there are no inventions. There is no in-between. 5 if there are no citations
Citation quantity - how many citations are made? The score is equal to the number of citations. Citations being references to the provided documents.
Evidentiary quality - Do the cited passages support the position, or are they tangential. Score 1-5, A 1 means citing a document that contradicts the argument. A 5 means all cited passages benefit and support the argument. 3 means that no citation directly contradicts the argument, but they are not significantly impactful to the overall structure. 1 if there are no citations
Logical coherence - Does the argument move from premises to conclusion without gaps or fallacies? 1-5, a 1 means the frequent presence of logical fallacies and a lack of logical procession. A 5 means a well reasoned argument that moves from premises to conclusions. 3 means structure exists but is amateur.
Positional strength - Does the argument successfully argue its position, and would a reader see reason in the argument? A 1 means the argument actively undermines its own position, a 5 being a neutral reader would likely be persuaded, and a 3 being the argument asserts the position but doesn't compel belief.\n'''

    output = {}

    with open(file_name, 'r') as file:
        data = json.load(file)
        
        for round in data:
            for agent in ('agent_a','agent_b'):
                argument_data = {}
                argument_data['response'] = data[round][f'{agent}_response']
                argument_data['documents'] = data[round][f'{agent}_chunks']
        
                prompt += "return your response as human readable formatted json, example:"
                prompt += '{"scores": {"textual_grounding":5,"citation_reality":4,"evidentiary_quality":4,"logical_coherence":3,"positional_strength":4}'

                response = score(prompt)
                json_response = json.loads(response)

                if round not in output:
                    output[round] = {}

                output[round][agent] = json_response['scores']

    timestamp = datetime.now().isoformat()
    with open(f'logs/scored_argument_{output_name_modifier}_{timestamp}.log', 'w') as file:
        json.dump(output, file, indent = 2)

if __name__ == '__main__':
    score_debate('logs/argument_2026-04-24T15:20:27.825511.log')