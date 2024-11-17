import nltk
from nltk.corpus import cmudict
DEBUG_MESSAGE = ""

# Download necessary NLTK data
nltk.download('cmudict')
def is_rhyme(word1, word2):
    """Checks if two words rhyme."""
    pronunciation_dict = cmudict.dict()
    pronunciation1 = pronunciation_dict[word1.lower()][0]
    pronunciation2 = pronunciation_dict[word2.lower()][0]

    # Compare the last two phonemes for a simple rhyme check
    return pronunciation1[-2:] == pronunciation2[-2:]

def extract_last_words(poem):
  lines = poem.split('\n')
  last_words = []
  for line in lines:
    words = line.split()
    last_words.append(words[-1])
  return last_words

def check_cross_rhyme(poem):
    global DEBUG_MESSAGE
    try:
        lines = poem.split('\n')
        stanzas = []
        current_stanza = []
        if lines[0] == '':
            lines = lines[1:]
        if lines[-1] != '':
            lines.append('')
        for line in lines:
            if line != '':
                current_stanza.append(line)
            if line == '':
                stanzas.append(current_stanza)
                current_stanza = []
        stanzas = [sublist for sublist in stanzas if sublist]
        for stanza in stanzas:
            print(stanza)
            last_words = extract_last_words('\n'.join(stanza))
            if len(last_words) < 4:
                print(f"Stanza too short for cross rhyme check: {stanza}")
                continue

            if is_rhyme(last_words[0], last_words[2]) and is_rhyme(last_words[1], last_words[3]):
                DEBUG_MESSAGE += "Stanza has a cross rhyme scheme (ABAB):" +last_words[0]+ "<->"+ last_words[2]+";"+ last_words[1]+" <-> "+last_words[3]+"\n"
                print(f"Stanza has a cross rhyme scheme (ABAB): {last_words[0]} <-> {last_words[2]}; {last_words[1]} <-> {last_words[3]} ")
            else:
                print(f"Stanza does not have a cross rhyme scheme:")
                DEBUG_MESSAGE += "Stanza does not have a cross rhyme scheme:"+"\n"
                if not is_rhyme(last_words[0], last_words[2]):
                    print(f" Problem is {last_words[0]} <-> {last_words[2]};")
                    DEBUG_MESSAGE += "Problem is "+last_words[0]+"<->"+last_words[2]+"\n"
                elif not is_rhyme(last_words[1], last_words[3]):
                    print(f" Problem is {last_words[1]} <-> {last_words[3]} ")
                    DEBUG_MESSAGE += "Problem is "+last_words[1]+"<->"+last_words[3]+"\n"
    except Exception as e:
        DEBUG_MESSAGE += "an error occured in cross ryhme check:"+str(e)
    return DEBUG_MESSAGE
    
# ## Test
# POEM = """
# In Berlin's streets, a curious sight
# Fleischküchle and Currywurst in the air
# Beer flows free, day and night
# Pairing well with a Weissbier to share

# Coffee's strong, a morning delight
# Fuel for shopping on the Ku'damm's fare
# Pastries sweet, a tasty bite
#  Berliners love their Kaffee to spare

# """

# check_cross_rhyme(POEM)