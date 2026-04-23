import os
from dotenv import load_dotenv
from google import genai
from retrieve import retrieve

load_dotenv()

def argue(question: str, position: str, retrieved_chunks: list[dict]):
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_model = os.getenv("LLM_MODEL")

    prompt = f"""You are a historian of the Greek Classics engaging in debate about the Iliad with another historian
The debate topic presented to you about the Iliad is: {question}
This is your position: {position}

You will now be provided with several documents from the Iliad in the form of Book Number and Text: 

DOCUMENTS:
{str([str(chunk) for chunk in retrieved_chunks])}

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

    client = genai.Client(api_key = llm_api_key)
    
    result = client.models.generate_content(
        model = llm_model,
        contents = prompt
    )

    return result.text


if __name__ == '__main__':
    
    query = 'Is Agamemnon an effective leader?'
    
    chunks = retrieve(query,3)

    position = 'You believe that Agamemnon is not an effective leader'
    
    response = argue(query, position, chunks)

    print(response)