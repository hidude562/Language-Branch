import json

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


a = Tree('The', 1)
# Display the tree

def display_tree(node, level=0):
    print('\t' * level + repr(node.val))
    for child in node.nodes:
        display_tree(child, level + 1)


def return_token_and_probability(sentence):
    # Currently a placeholder

    # Return like the following:
    return [('apple', 0.3), ('banana', 0.4), ('mango', 0.06)]

def tree_last_layer_add(node, prompt = ''):
    prompt = f"{prompt} {node.val}"
    depth = len(prompt.split())
    if node.nodes == [] and depth == a.depth:
        to_add = return_token_and_probability(prompt[1:])
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
def tree_save_as_json(tree, filename='grammar.json'):
    with open(filename, 'w') as f:
        json.dump(to_dict(tree), f)

def to_dict(tree):
    if tree.nodes:
        return {"val": tree.val, "probability": tree.probability, "nodes": [to_dict(n) for n in tree.nodes]}
    else:
        return {"val": tree.val, "probability": tree.probability}

tree_generate_n_layers(2)
display_tree(a)
tree_save_as_json(a)
