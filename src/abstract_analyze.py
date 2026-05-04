from debate_scorer import find_most_recent_file
from debate_scorer import find_most_recent_files
import json
from datetime import datetime

def analyze_abstract(quantity_abstracts):
    
    most_recent_files = find_most_recent_files('logs/meta/abstract', quantity_abstracts)

    outputs = {}
    outputs['a_impact'] = 0
    outputs['b_impact'] = 0
    outputs['chunk_uniqueness_impact'] = 0

    for ind_file in most_recent_files:
        with open(ind_file, 'r') as file:
            abstractinput = json.load(file)
            outputs['a_impact'] -= abstractinput['standard']['a_average']
            outputs['b_impact'] -= abstractinput['standard']['b_average']
            outputs['chunk_uniqueness_impact'] -= abstractinput['standard']['chunk_uniqueness']
            outputs['a_impact'] += abstractinput['poisoned']['a_average']
            outputs['b_impact'] += abstractinput['poisoned']['b_average']
            outputs['chunk_uniqueness_impact'] += abstractinput['poisoned']['chunk_uniqueness']
        
    outputs['a_impact'] /= len(most_recent_files)
    outputs['b_impact'] /= len(most_recent_files)
    outputs['chunk_uniqueness_impact'] /= len(most_recent_files)

    timestamp = datetime.now().isoformat()
    with open(f'logs/meta/abstract_analysis/analysis_{timestamp}.log','w') as output_file:
        json.dump(outputs, output_file, indent = 2)

if __name__ == '__main__':
    analyze_abstract(5)