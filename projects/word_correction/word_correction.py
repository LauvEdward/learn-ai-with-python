import streamlit as st

def load_vocabulary():
    file_path = './data/vocab.txt'
    try:
        with open(file_path, 'r') as f:
            lines = f . readlines ()
            vocabulary  = sorted(set([line.strip().lower() for line in lines]))
        return vocabulary
    except FileNotFoundError:
        st.error("Vocabulary file not found.")
    return

def levenshtein_distance(s1, s2):
    distance = []
    for i in range(len(s1) + 1):
        distance.append([0] * (len(s2) + 1))

    for i in range(len(s1) + 1):
        distance[i][0] = i
    for j in range(len(s2) + 1):
        distance[0][j] = j
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1

            deletion = distance[i-1][j] + 1
            insertion = distance[i][j-1] + 1
            substitution = distance[i-1][j-1] + cost

            distance[i][j] = min(deletion, insertion, substitution)
    return distance[len(s1)][len(s2)]

def main():
    vocabulary = load_vocabulary()
    if vocabulary is None:
        return
    st.title("Word Correction App")
    st.write("This app corrects misspelled words using a simple dictionary-based approach.")
    user_input = st.text_input("Enter a word to check:")
    if st.button("Compute: "):
        # Input from user
        leven_distances = dict()
        for word in vocabulary:
            leven_distances[word] = levenshtein_distance(user_input, word)
        sorted_leven_distances = dict(sorted(leven_distances.items(), key=lambda item: item[1]))
        st.write('Correct word: ', list(sorted_leven_distances.keys())[0])
        col1 , col2 = st.columns(2)
        col1.write('Vocabulary: ')
        col1.write(vocabulary)

        col2.write('Distances: ')
        col2.write(sorted_leven_distances)



if __name__ == "__main__":
    main()