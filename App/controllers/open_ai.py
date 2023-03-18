import openai
from App.controllers.ciphers import doubleDeCipher
#API KEY
# API_KEY="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"
API_KEY="w7\oXFVg1vptXr^fpjvo58{JgjFNnkp|o:xU{S8JGWY6h^|RLTN"
         
#SET API KEY

#RAIL KEY
R_KEY="MyeSearch2023"

#CAESER KEY
C_KEY=4

openai.api_key = doubleDeCipher(API_KEY, R_KEY, C_KEY)

#OTHER CONFIG STUFF
TEMPERATURE=0.5
MAX_TOKENS=1000
MODEL="text-davinci-003"

def RAIL_KEY():
    return R_KEY

def CAESAR_KEY():
    return C_KEY


def prompt(sentence):
    response = openai.Completion.create(
    max_tokens=MAX_TOKENS,
    model=MODEL,
    temperature=TEMPERATURE,
    prompt=sentence,
    )
    return response