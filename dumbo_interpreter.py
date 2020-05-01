from lark import Lark
from lark import Transformer
import logging
logging.basicConfig(level=logging.DEBUG)

# print(dumbo_grammar)

# lol on sait pas si il faut un espace apres for

with open( "dumboGrammar.lark", "r") as grammar:
    parserDumbo =  Lark(grammar.read(),start="programme")


with open( "data1.dumbo", "r" ) as texte:
    data = parserDumbo.parse(texte.read())
    # print(data.pretty())


with open( "template3.dumbo", "r" ) as texte:
    template = parserDumbo.parse(texte.read())
    # print(template.pretty())

class MyTransformer(Transformer):
    def list(self, items):
        return list(items)
    def pair(self, key_value):
        k, v = key_value
        return k, v
    def dict(self, items):
        return dict(items)
    def op(self,items):
        return 0


tree_data = MyTransformer().transform(data)
tree_template = MyTransformer().transform(template)

# print(tree_data)
# print(tree_data.data)
# print(tree_data.children)
# print(tree_data.children[0])
# print(tree_data.children[0].data.children)

#objet tree


def getStringInterior(tree,tmp = []):
    print("GET STRING INTERIOR ------------")
    print(tree.data)
    print(tree.children[0].children[0])
    tmp.append(tree.children[0].children[0].value)
    print(type(tree.children[0].children[0]))
    if(len(tree.children)==2):
        getStringInterior(tree.children[1],tmp)
    return tmp

def getVar(tree):
    print("______GET VAR  "+str(tree))
    if(tree.data == "string_expression"):
        print(tree.children)
        if(tree.children[0].data == "string"):
            return tree.children[0].children[0]
    elif(tree.data == "Integer"):
        print(tree.children)
        
    elif(tree.data == "string_list"):
        return getStringInterior(tree.children[0])
    return "ERROR"

dic= {}
def explore(racine):
    print(racine.data)
    # traite le cas de base
    if racine.data == "programme":
        if(type(racine.children)==list):
            for el in racine.children:
                explore(el)

    
    elif racine.data == "dumbo_bloc":
        if(type(racine.children)==list):
            for el in racine.children:
                explore(el)

    elif racine.data == "expression_list":
        if(type(racine.children)==list):
            for el in racine.children:
                explore(el)

    elif racine.data == "expression":
        if(type(racine.children)==list):
            for el in racine.children:
                explore(el)

        if(racine.children[0].data == "if"):
            return 0
        if(racine.children[0].data == "for"):
            return 0
        if(racine.children[0].data == "variable"):
            dic[racine.children[0].children[0]] = getVar(racine.children[1])

    elif racine.data == "variable":
        print("VARIABLE")
        print(racine.children[0])
        print(racine.children)
        print("")
            




explore(tree_data)

print("nom = "+str(dic["nom"]))
print("prenom = "+str(dic["prenom"]))
print("cours = "+str(dic["cours"]))

# Tree(op, [Tree(plus, [])])





# with open( "output.html", "w" ) as texte:
#     print("ok")
#     texte.write("caca")

#  DANS LA GRAMMAIRE IL MANQUE / ET * 
# 
# 
# INSTR