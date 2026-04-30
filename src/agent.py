from argue import argue
import yaml

class agent:
    
    def __init__(self, question, position, prompt):
        self.question = question
        self.position = position
        self.current_response = ''

        self.prompt = prompt
        self.prompt = self.prompt.replace('***QUESTION***', question)
        self.prompt = self.prompt.replace('***POSITION***', position)
        
        self.is_poisoner = False

    def set_chunks(self, chunks: list[dict]):
        self.chunks = chunks
        self.str_chunks = str([str(chunk) for chunk in self.chunks])

        split_prompt = self.prompt.split('***CHUNKS***')
        split_prompt[1] = self.str_chunks
        self.prompt = '***CHUNKS***'.join(split_prompt)

    def argue(self):
        self.past_response = self.current_response
        self.current_response = argue(self.prompt)
        return self.current_response

    def set_opponents_previous_argument(self, opponent_previous_argument):
        split_prompt = []
        if not '***OPPONENT PREVIOUS ARGUMENT***' in self.prompt:
            self.prompt += '***OPPONENT PREVIOUS ARGUMENT***'
            self.prompt += r"This is your opponent's previous response to the question. Respond directly to them"
            self.prompt += '***OPPONENT PREVIOUS ARGUMENT***'

        split_prompt = self.prompt.split('***OPPONENT PREVIOUS ARGUMENT***')
        split_prompt[1] = opponent_previous_argument
        self.prompt = '***OPPONENT PREVIOUS ARGUMENT***'.join(str(item) for item in split_prompt)

    def set_poisoner(self):
        if not self.is_poisoner:
            with open('prompt_pieces.yml','r') as file:
                config = yaml.safe_load(file)
                self.prompt += config['poison_prompt_yes_undermine']
            self.is_poisoner = True



