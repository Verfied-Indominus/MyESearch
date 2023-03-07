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