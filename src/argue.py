import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from retrieve import retrieve

load_dotenv()

def argue(debate_prompt:str):
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_model = os.getenv("LLM_MODEL")

    retry_options = types.HttpRetryOptions(
        attempts = 5,
        initial_delay = 1.0,
        max_delay=60.0,
        http_status_codes=[500,502,503,504,429]
    )

    client = genai.Client(
        api_key = llm_api_key,
        http_options = types.HttpOptions(retry_options=retry_options))

    result = client.models.generate_content(
        model = llm_model,
        contents = debate_prompt
    )

    return result.text

def score(score_prompt:str):
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_model = os.getenv("LLM_MODEL")

    retry_options = types.HttpRetryOptions(
        attempts = 5,
        initial_delay = 1.0,
        max_delay=60.0,
        http_status_codes=[500,502,503,504,429]
    )

    client = genai.Client(
        api_key = llm_api_key,
        http_options = types.HttpOptions(retry_options=retry_options))

    result = client.models.generate_content(
        model = llm_model,
        contents = score_prompt
    )

    text = result.text

    first_index = -1
    last_index = -1

    for index, char in enumerate(text):
        if first_index == -1 and char == '{':
            first_index = index
        if char == '}':
            last_index = index

    return_text = text[first_index:last_index + 1]

    if not return_text:
        raise ValueError('Did not response correctly')
    else:
        return return_text