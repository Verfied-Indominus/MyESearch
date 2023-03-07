import openai
#API KEY
API_KEY="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"
#SET API KEY

openai.api_key = API_KEY

#OTHER CONFIG STUFF
TEMPERATURE=0
MAX_TOKENS=1000
MODEL="text-davinci-003"


def prompt(sentence):
    response = openai.Completion.create(
    max_tokens=MAX_TOKENS,
    model=MODEL,
    prompt=sentence,
    )
    return response