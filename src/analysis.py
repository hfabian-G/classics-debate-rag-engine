from debate_scorer import find_most_recent_file
import json
from datetime import datetime

def analyze_meta_results(file_name):
    with open(file_name,'r') as file:
        data = json.load(file)

        question_count = len(data)

        abstract = data.popitem()[1]

        for question in data:
            for mode in data[question]:
                if 'standard' == mode:
                    for value in data[question][mode]:
                        abstract[mode][value] += data[question][mode][value]
                elif 'poisoned' == mode:
                    for value in data[question][mode]:
                        abstract[mode][value] += data[question][mode][value]


        for mode in abstract:
            for value in abstract[mode]:
                abstract[mode][value] = abstract[mode][value]/question_count

        timestamp = datetime.now().isoformat()

        with open(f"logs/meta/abstract/meta_{timestamp}.log",'w') as file:
            json.dump(abstract, file, indent = 2)


if __name__ == '__main__':
    file_name = 'logs/meta/nonabstract/meta_2026-04-29T15:14:54.315919.log'
    analyze_meta_results(file_name=file_name)