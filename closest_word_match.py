import gensim.downloader as api
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle

# Load pre-trained Word2Vec model
model = api.load('word2vec-google-news-300')

# Load the list of words from the pickle file
with open('bag_of_words.pkl', 'rb') as f:
    word_list = pickle.load(f)

# Filter out words not in the model vocabulary
valid_words = [word for word in word_list if word in model]

# If no valid words are found, raise an error
if not valid_words:
    raise ValueError("None of the words in the list are in the model vocabulary.")

# Vectors for the words in the list
word_vectors = np.array([model[word] for word in valid_words])

def get_closest_word(target_word):
    """
    Find the closest word to the target_word from the list of valid_words
    using cosine similarity.
    """
    # Ensure the target word exists in the model vocabulary
    if target_word not in model:
        raise ValueError(f"'{target_word}' is not in the model vocabulary.")
    
    # Vector for the target word
    target_vector = model[target_word].reshape(1, -1)
    
    # Compute cosine similarities between the target word vector and the list of word vectors
    similarities = cosine_similarity(target_vector, word_vectors)
    
    # Get the index of the closest word (highest cosine similarity)
    closest_index = np.argmax(similarities)
    
    # Return the word corresponding to the closest index
    return valid_words[closest_index]

# Example usage
target_word = "apple"
closest_word = get_closest_word(target_word)
print(f"The closest word to '{target_word}' is '{closest_word}'.")
