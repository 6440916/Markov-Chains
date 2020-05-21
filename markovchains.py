import numpy as np


def insert(lst, inserted):
    ''' Add word in lst in case that it does not exist in lst yet,
        and such that the alphabetical order is respected. '''

    for index, item in enumerate(lst):
        if item == inserted:
            return lst
        elif item > inserted:
            return lst[:index] + [inserted] + lst[index:]

    return lst + [inserted]


class MarkovTextChain:
    ''' Represents a Markov chain that simulates text.
        This is done by giving the object an example text from which it uses
        the conditional probabilities of a word occuring in a sentence given
        the words that are before it.
    '''

    def __init__(self, example_text, memory):
        ''' Initialise object
        '''
        self.example_text = example_text.split()
        self.memory = memory

        self.list_nodes()
        self.calc_probabilities()

    def list_nodes(self):
        ''' Creates an alphabetically ordered list of all nodes occuring in the
        example text. Nodes are tuples of words with length determined by
        memory.
        '''
        nodes = [""] # The empty string represents the beginning of a sentence.

        for i in range(len(self.example_text) - self.memory):
            node = ""
            for j in range(self.memory):
                node += self.example_text[i + j] + " "
                nodes = insert(nodes, node) # Adds node to nodes alphabetically

        self.nodes = nodes

    def calc_probabilities(self):
        '''
        '''
        next_words = {}

        for node in self.nodes:
            next_words[node] = []

        last_node = ""
        for word in self.example_text:
            next_words[last_node].append(word + " ")
            last_node = last_node[last_node.find(" ") + 1:] + word +  " "

            if word[-1] == "." or word[-1] == "!" or word[-1] == "?":
                next_words[last_node] = [""]
                last_node = ""

        self.next_words = next_words

    def generate_sentence(self):
        ''' Generate a sentence.
        '''
        last_node = np.random.choice(self.next_words[""])
        chain = [last_node]

        while last_node != "":
            last_node = np.random.choice(self.next_words[last_node])
            chain.append(last_node)

        return "".join(chain)


text = open("Trump_Speech.txt").read()
trumpchain = MarkovTextChain(text, 1)

for i in range(20):
    print(trumpchain.generate_sentence())


