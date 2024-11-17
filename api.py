from openai import OpenAI

client = OpenAI(
  api_key="rwJgsDpEpOFVhn6SdYm0OuInYRtZmSIB",
  base_url="https://api.lemonfox.ai/v1",
)

# API stuff to generate the poem
def promptLLM(prompt="How many days has a year?", reprompt="", modelName="llama-70b-chat"):
    # models to choose: llama-70b-chat $1.25  ( p. 1mio Tokens)
    # llama-8b-chat                    $0.5 
    # mixtral-chat                   	$0.83    
    completion = client.chat.completions.create(
    messages=[
        { "role": "system", "content": "You are a helpful assistant!" },
        { "role": "user", "content": prompt },
        { "role": "user", "content": reprompt }
    ],
    model=modelName,
    temperature=0.1,
    )
    return completion.choices[0].message.content

# # Tests:
# CITY     = "Munich"
# PROMT_EN = "Create a funny poem with a cross rhyme about the eating and drinking habits in "+CITY
# PROMPT_DE= "Erstelle ein lustiges Gedicht im Kreuzreim über die Essens und Triinkgewohnheiten in "+CITY

# # couplet rhyme = paarreim
# # alternate rhyme / cross rhyme = kreuzreim
# ## Test1: reprompting: -> does not work
# REPORMPT_EN = "This was a couplet rhyme. Please rearrange the words such that the middle words rhyme! Only return the poem!"
# promptLLM(prompt=PROMT_EN, reprompt=REPORMPT_EN)
