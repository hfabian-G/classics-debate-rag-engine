import yaml

with open('prompt_pieces.yml','r') as file:
    config = yaml.safe_load(file)

    for question in config['questions']:
        print(question)

    print(config['prompt'])