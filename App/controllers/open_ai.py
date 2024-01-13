import openai
from openai import OpenAI
from App.controllers.ciphers import doubleDeCipher
#ENCRYPTED API KEY
API_KEY=",Kg$lZ.^EN%KmIJzM%h$zKZ^!\ bq})`imd+zi]1nz^pKknikOc"
         
#SET OpenAI
client = OpenAI()

#RAIL KEY
R_KEY="MyeSearch2024"

#CAESER KEY
C_KEY=24

os.environ['OPENAI_API_KEY'] = doubleDeCipher(API_KEY, R_KEY, C_KEY) 
# openai.api_key = doubleDeCipher(API_KEY, R_KEY, C_KEY)

#OTHER CONFIG STUFF
TEMPERATURE=0.5
MAX_TOKENS=1000
# MODEL="text-davinci-003"
MODEL="gpt-3.5-turbo-instruct"

def RAIL_KEY():
    return R_KEY

def CAESAR_KEY():
    return C_KEY


def prompt(sentence):
    response = client.completions.create( 
    max_tokens=MAX_TOKENS,
    model=MODEL,
    temperature=TEMPERATURE,
    prompt=sentence,
    api_key=doubleDeCipher(API_KEY, R_KEY, C_KEY)
    )
    return response