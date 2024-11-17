import nltk
from nltk.corpus import cmudict

# Download necessary NLTK data
nltk.download('cmudict')
def is_rhyme(word1, word2):
    """Checks if two words rhyme."""
    pronunciation_dict = cmudict.dict()
    pronunciation1 = pronunciation_dict[word1.lower()][0]
    pronunciation2 = pronunciation_dict[word2.lower()][0]

    # Compare the last two phonemes for a simple rhyme check
    return pronunciation1[-2:] == pronunciation2[-2:]
print(is_rhyme("cat", "hat"))  # Output: True