import random as rnd


def insert(lst, inserted):
    ''' Adds word in lst in case that it does not exist in lst yet,
        and such that the alphabetical order is respected. '''

    for index, item in enumerate(lst):
        if item == inserted:
            return lst
        elif item > inserted:
            return lst[:index] + [inserted] + lst[index:]

    return lst + [inserted]


class MarkovChain:
    ''' Represents a Markov chain that simulates text.
        This is done by giving the object an example text from which it
        deduces the conditional probability densities.

        example_text : list that contains the example text from which the
                        conditional probabilities are extracted.
        memory : positive integer that represents the number of words we have
                to look back to determine the next word in the chain.
        states : list of all possible states. These are alphabetically ordered
                and unique.
        state_to_index : dictionary from which we can easily find the index
                        of a certain state.
        words : list of all unique words in de sample text.
        word_to_index : dictionary which contains all indices of the list words
        transition : transition matrix of the Markov chain.
    '''


    def __init__(self, example_text, memory=1):
        ''' Initialise object
        '''
        self.example_text = example_text.split()
        self.memory = memory

        self.list_states() # Create a list of states that occur in example text
        self.calc_transition_matrix() # Create the transition matrix of the Markov chain


    def list_states(self):
        ''' Creates an alphabetically ordered list of all states
        occuring in the example text.
        '''
        states = [] # The empty string represents the beginning of a sentence.
        initial_states = [] # States that begin a sentence
        words = []
        word_to_index = {}
        state_to_index = {}

        #
        # Part where we list all unique words
        #
        for word in self.example_text:
            words = insert(words, word)

        for i, word in enumerate(words):
            word_to_index[word] = i

        #
        # Part where we list all possible states
        #
        for i in range(len(self.example_text) - self.memory):
            state = " ".join(self.example_text[i:i+self.memory])

            if i == 0 or self.example_text[i-1][-1] == "." or \
                self.example_text[i-1][-1] == "!" or self.example_text[i-1][-1] == "?":
                initial_states = insert(initial_states, state)

            # Add states to list in alphabetical order
            states = insert(states, state)

        # Create the state_to_index dictionary
        # We use this dictionary to easily find corresponding indices to states
        for i, state in enumerate(states):
            state_to_index[state] = i

        self.words = words
        self.word_to_index = word_to_index
        self.states = states
        self.state_to_index = state_to_index
        self.initial_states = initial_states


    def calc_transition_matrix(self):
        ''' Calculate the transition matrix of the Markov Chain. '''
        freq_matrix = [[0 for word in self.words] for state in self.states]

        #
        # Calculate frequency matrix
        #
        for i in range(len(self.example_text) - self.memory):
            # Get next state
            state = " ".join(self.example_text[i:i+self.memory])
            state_index = self.state_to_index[state]

            word = self.example_text[i + self.memory]
            word_index = self.word_to_index[word]

            # Increment frequency that word occurs after state
            freq_matrix[state_index][word_index] += 1


        #
        # Create transition matrix from the frequency table
        #
        transition = [[0 for word in self.words] for state in self.states]
        for row_i, row in enumerate(freq_matrix):
            S = sum(row)

            for col_i, col in enumerate(row):
                # Probability is equal to amount of occurrences divided by
                # total number of words.
                transition[row_i][col_i] = col / S

        self.transition = transition


    def next_state(self, i):
        ''' Randomly generate new state dependent on the last state i.
        '''
        distribution = self.transition[i] # Distribution vector
        r = rnd.random() # A random number in [0,1]

        for j in range(0, len(distribution) - 1):
            r -= distribution[j]
            if r <= 0:
                return j

        return len(distribution) - 1


    def initial_state(self):
        ''' Picks a random initial state.
        '''
        n = len(self.initial_states)
        i = int(rnd.random() * n)

        return self.state_to_index[self.initial_states[i]]


    def generate_text(self, n=1):
        ''' Generates text.
            n is the number of sentences that should be generated.
        '''
        last_state = self.initial_state() # Randomly generate first state
        chain = self.states[last_state].split()

        while n > 0:
            new_word = self.words[self.next_state(last_state)]
            chain.append(new_word)

            last_state = self.state_to_index[" ".join(chain[-self.memory:])]

            if new_word[-1] == "." or new_word[-1] == "!" or new_word[-1] == "?":
                n -= 1

        return " ".join(chain)


if __name__ == "__main__":
    text = open("Trump_Speech.txt").read()
    chain = MarkovChain(text, 1)

    print(chain.generate_text(3))
