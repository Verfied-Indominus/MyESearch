import openai
#API KEY
API_KEY="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"
#SET API KEY

openai.api_key = API_KEY

#OTHER CONFIG STUFF
TEMPERATURE=0.5
MAX_TOKENS=1000
MODEL="text-davinci-003"


def prompt(sentence):
    response = openai.Completion.create(
    max_tokens=MAX_TOKENS,
    model=MODEL,
    temperature=TEMPERATURE,
    prompt=sentence,
    )
    return response