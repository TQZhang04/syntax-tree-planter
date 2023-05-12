'''
Makes syntactic trees out of a given sentence
Supports:
noun phrases
verb phrases
nbar
recursive nbar
recursive NP
recursive VP
prepositions
prep phrases
complementizers
comp phrases

Does not support:
adverbs
multiple-word "words" (mai tai, Will Styler)
gerund phrases

Other Constraints:
parts of speech must be hard-coded
only works on simple sentences (S -> NP VP)
only works on grammatically correct sentences
gets fucked up by ambiguity

Weird sentences:
"the lazy brown fox jumped over the white fence while the dog slept in the garden"
    VP -> VP CP?
'''
class SyntacticTree:
    verbs = ["jumped", "slept"]
    nouns = ["fox", "fence", "dog", "garden"]
    determiners = ["the"]
    prepositions = ["over", "in"]
    adjectives = ["lazy", "brown", "white"]
    complimentizers = ["while"]
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
        self.constituencies.append(sentence_str)
        first_verb = 0
        first_verb = -1
        for verb in SyntacticTree.verbs:
            try:
                first_verb = sentence.index(verb)
                break
            except ValueError:
                continue
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
        self.constituencies.append(np_str)
        np_node = SyntaxNode(type = "NP", value = np_str)
        # check for preposition
        prep_present = False
        for word in np:
            if word in SyntacticTree.prepositions:
                prep_present = True
        # case: NP -> NP PP
        if prep_present:
            prep_index = -1
            for prep in SyntacticTree.prepositions:
                try:
                    prep_index = np.index(prep)
                    break
                except ValueError:
                    continue
            np2 = np[:prep_index]
            pp = np[prep_index:]
            np_node.left = self.make_np_node(np2)
            np_node.right = self.make_pp_node(pp)
        else:
            # case: NP -> DET N'
            if np[0] in SyntacticTree.determiners:
                det = np[0]
                nbar = np[1:]
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
        verb = vp[0]
        vp_node.left = SyntaxNode(type = "V", value = verb)
        # case: VP -> V CP
        if len(vp) == 1:
            return vp_node
        if vp[1] in SyntacticTree.complimentizers:
            cp = vp[1:]
            vp_node.right = self.make_cp_node(cp)
        # commented out because I'm just going to ignore ambiguity until I know what to do with it
        # # check for preposition
        # prep_present = False
        # for word in vp:
        #     if word in SyntacticTree.prepositions:
        #         prep_present = True
        # # preposition cases
        # if prep_present:
        #     prep_index = -1
        #     for prep in SyntacticTree.prepositions:
        #         try:
        #             prep_index = vp.index(prep)
        #             break
        #         except ValueError:
        #             continue
        #     # case: VP -> V PP
        #     if prep_index == 1:
        #         verb = vp[0]
        #         vp_node.left = SyntaxNode(type = "V", value = verb)
        #     # case: VP -> VP PP
        #     else:
        #         vp2 = vp[:prep_index]
        #         vp_node.left = self.make_vp_node(vp2)
        #     pp = vp[prep_index:]
        #     vp_node.right = self.make_pp_node(pp)
        # case: VP -> V PP
        elif vp[1] in SyntacticTree.prepositions:
            pp = vp[1:]
            vp_node.right = self.make_pp_node(pp)
        # case: VP -> V NP, VP -> V
        else:
            verb = vp[0]
            np = vp[1:]
            vp_node.left = SyntaxNode(type = "V", value = verb)
            vp_node.right = self.make_np_node(np)
        return vp_node
    
    def make_nbar_node(self, nbar):
        nbar_str = self.arr_to_str(nbar)
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
        pp_str = self.arr_to_str(pp)
        self.constituencies.append(pp_str)
        pp_node = SyntaxNode(type = "PP", value = pp_str)
        # only one case: PP -> P NP
        prep = pp[0]
        np = pp[1:]
        pp_node.left = SyntaxNode(type = "P", value = prep)
        pp_node.right = self.make_np_node(np)
        return pp_node
    
    def make_cp_node(self, cp):
        cp_str = self.arr_to_str(cp)
        cp_node = SyntaxNode(type = "CP", value = cp_str)
        comp = cp[0]
        s = cp[1:]
        cp_node.left = SyntaxNode(type = "C", value = comp)
        cp_node.right = self.parse_sentence(s)
        return cp_node
        
    
            
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