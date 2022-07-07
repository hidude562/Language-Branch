import json
import openai
import math

openai.api_key = "YOUR API KEY GOES HERE"

class Tree:
    def __init__(self, token, probability, depth=1):
        self.val = token
        self.depth = depth
        self.probability = probability
        self.nodes = []

    def add_node(self, token, probability):
        self.nodes.append(Tree(token, probability))

    def __repr__(self):
        return f"Tree({self.val}, {self.probability}): {self.nodes}"


a = Tree('The', 100)
# Display the tree

def display_tree(node, level=0):
    print('\t' * level + (node.val + " - " + str(round(node.probability, 2)) + "%"))
    for child in node.nodes:
        display_tree(child, level + 1)


def return_token_and_probability(sentence):
    response = openai.Completion.create(
        model="text-ada-001",
        prompt="<|endoftext|>" + sentence,
        temperature=0,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        logprobs=5
    )
    logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]
    parsed_logprobs = []
    for word in logprobs:
        parsed_logprobs.append((word, (math.e ** logprobs[word]) * 100))

    # Return like the following:
    return parsed_logprobs

def tree_last_layer_add(node, prompt = ''):
    prompt = f"{prompt}{node.val}"
    depth = len(prompt.split())
    if node.nodes == [] and depth == a.depth:
        to_add = return_token_and_probability(prompt)
        highest_probability = max([element[1] for element in to_add]) if to_add else 0
        for tup in to_add:
            if highest_probability < tup[1] * 5: #Change the 5 to lower numbers for less leaves
                node.add_node(tup[0], tup[1])
    else:
        for child in node.nodes:
            tree_last_layer_add(child, prompt)

def tree_generate_n_layers(max_layers):
    for i in range(max_layers):
        tree_last_layer_add(a)
        a.depth+=1
def tree_save_as_json(tree, filename=('sentence_tree' + str(a.depth) + ".json")):
    with open(filename, 'w') as f:
        json.dump(to_dict(tree), f)

def to_dict(tree):
    if tree.nodes:
        return {"val": tree.val, "probability": tree.probability, "nodes": [to_dict(n) for n in tree.nodes]}
    else:
        return {"val": tree.val, "probability": tree.probability}

tree_generate_n_layers(3)
display_tree(a)
tree_save_as_json(a)
