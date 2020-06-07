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
        transition : transition matrix of the Markov chain.
    '''

    def __init__(self, example_text, memory=1):
        ''' Initialise object
        '''
        self.example_text = example_text.split()
        self.memory = memory # Memory property not yet properly implemented

        self.list_states() # Create a list of states that occur in example text
        self.calc_transition_matrix() # Create the transition matrix of the Markov chain

    def list_states(self):
        ''' Creates an alphabetically ordered list of all states(=words)
        occuring in the example text.
        '''
        states = [""] # The empty string represents the beginning of a sentence.
        state_to_index = {}

        for state in self.example_text:
            states = insert(states, state) # Adds the state to the list alphabetically

        # Create the state_to_index dictionary
        # We use this dictionary to easily find corresponding indices to states
        for i, state in enumerate(states):
            state_to_index[state] = i

        self.states = states
        self.state_to_index = state_to_index

    def calc_transition_matrix(self):
        ''' Calculate the transition matrix of the Markov Chain.
        '''
        freq_matrix = [[0 for state in self.states] for state in self.states]

        last_state_index = 0
        for state in self.example_text:
            state_index = self.state_to_index[state]
            freq_matrix[last_state_index][state_index] += 1

            # In case state is the last word in a sentence, we let its next
            # state be the empty state.
            if state[-1] == "." or state[-1] == "!" or state[-1] == "?":
                freq_matrix[state_index][0] += 1
                last_state_index = 0
            else:
                last_state_index = state_index

        # Create transition matrix from the frequency table
        transition = [[0 for state in self.states] for state in self.states]
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


    def generate_text(self, n=1):
        ''' Generates text.
            n is the number of sentences that should be generated.
        '''
        last_state = self.next_state(0)
        chain = [last_state]

        while n > 0:
            last_state = self.next_state(last_state)
            chain.append(last_state)

            if last_state == 0:
                n -= 1


        text = ""
        for node in chain:
            if node != 0:
                text += self.states[node] + " "

        return text[:-1]


text = open("Trump_Speech.txt").read()
trumpchain = MarkovChain(text)

print(trumpchain.generate_text(4))
