'''
Makes syntactic trees out of a given sentence
Supports:
noun phrases
verb phrases
nbar
resursive nbar

Does not support:
prepositions
prep phrases
complementizers
c-phrases
recursive noun phrases
recursive verb phrases
adverbs
multiple-word "words" (mai tai, Will Styler)
gerund phrases

Other Constraints:
parts of speech must be hard-coded
only works on simple sentences (S -> NP VP)
only works on grammatically correct sentences
'''
class SyntacticTree:
    verbs = ["is"]
    nouns = ["dog", "running"]
    determiners = ["the"]
    prepositions = []
    adjectives = ["fierce"]
    # TODO: figure out how to populate these based on the sentence automatically
    
    def __init__(self, sentence):
        self.sentence = sentence.split(" ")
        self.constituencies = []
        self.root = self.parse_sentence(self.sentence)
        return
    
    def get_tree(self):
        return self.get_tree_helper(self.root, 0)
    
    def get_tree_helper(self, root, level):
        if root == None:
            return ''
        str = "-" * level
        str += root.__str__() + "\n"
        str += self.get_tree_helper(root.left, level + 1)
        str += self.get_tree_helper(root.right, level + 1)
        return str
    
    def arr_to_str(self, arr):
        str = arr[0]
        for i in range(1, len(arr)):
            str += " " + arr[i]
        return str
    
    def parse_sentence(self, sentence):
        sentence_str = self.arr_to_str(sentence)
        print(sentence)
        self.constituencies.append(sentence_str)
        first_verb = 0
        for i in range(len(sentence)):
            if sentence[i] in SyntacticTree.verbs:
                first_verb = i
                break
        np = sentence[:first_verb]
        vp = sentence[first_verb:]
        sentence_node = SyntaxNode(type = "S", 
                                   value = sentence_str, 
                                   left = self.make_np_node(np), 
                                   right = self.make_vp_node(vp))
        return sentence_node
    
    def make_np_node(self, np):
        if (len(np) == 0):
            return None
        np_str = self.arr_to_str(np)
        print(np_str)
        self.constituencies.append(np_str)
        # case: NP -> DET N'
        np_node = SyntaxNode(type = "NP", value = np_str)
        if np[0] in SyntacticTree.determiners:
            det = np[0]
            nbar = np[1:]
            print(nbar)
            np_node.left = SyntaxNode(type = "DET", value = det)
        # case: NP -> N'
        else:
            nbar = np
        np_node.right = self.make_nbar_node(nbar)
        return np_node
    
    def make_vp_node(self, vp):
        if (len(vp) == 0):
            return None
        vp_str = self.arr_to_str(vp)
        self.constituencies.append(vp_str)
        vp_node = SyntaxNode(type = "VP", value = vp_str)
        # case: VP -> V NP, VP -> V
        verb = vp[0]
        np = vp[1:]
        vp_node.left = SyntaxNode(type = "V", value = verb)
        vp_node.right = self.make_np_node(np)
        return vp_node
    
    def make_nbar_node(self, nbar):
        nbar_str = self.arr_to_str(nbar)
        print(nbar_str)
        nbar_node = SyntaxNode(type = "N'", value = nbar_str)
        # case: N' -> N
        if len(nbar) == 1:
            nbar_node.right = SyntaxNode(type = "N", value = nbar_str)
            return nbar_node
        # case: N' -> ADJ N'
        adj =  nbar[0]
        nbar2 = nbar[1:]
        nbar_node.left = SyntaxNode(type = "ADJ", value = adj)
        nbar_node.right = self.make_nbar_node(nbar2)
        return nbar_node
    
    # TODO: make prepositions work (good luck)
    # don't forget to update noun and verb phrase makers
    def make_pp_node(self, pp):
        return None
    
    def make_cp_node(self, cp):
        return None
        
    
            
class SyntaxNode:
        def __init__(self, value = None, type = None, left = None, right = None):
            self.value = value
            self.type = type
            self.left = left
            self.right = right
        
        def __str__(self):
            return self.type + " | \"" + self.value + "\""
tester = SyntacticTree(input())
print(tester.constituencies)
print("check:", end = " ")
print(tester.root.right)
print(tester.get_tree())