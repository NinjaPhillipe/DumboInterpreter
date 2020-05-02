from lark import Lark
from lark import Transformer
import logging
logging.basicConfig(level=logging.DEBUG)

# print(dumbo_grammar)

# lol on sait pas si il faut un espace apres for

dic= {}

def getStringInterior(tree,tmp = []):
    tmp.append(tree.children[0].children[0].value)
    if(len(tree.children)==2):
        getStringInterior(tree.children[1],tmp)
    return tmp

def getVar(tree):
    # print("______GET VAR  "+str(tree))
    if(tree.data == "string_expression"):
        if(tree.children[0].data == "string"):
            return tree.children[0].children[0]
        elif(tree.children[0].data == "variable"):
            return getValue(tree.children[0].children[0])
        elif(tree.children[0].data == "string_expression"):
            if(len(tree.children)== 2):
                return getVar(tree.children[0])+getVar(tree.children[1])
            return getVar(tree.children[0])
    elif(tree.data == "integer"):

        print("INTEGER NOT YET IMPLEMENTED")
        print(tree.children)
        return (tree.children[0])
        
        
        
    elif(tree.data == "string_list"):
        return getStringInterior(tree.children[0])
    return "ERROR"

# def getValue(tree):
#     return dic[tree.children[0]]
def getValue(variable):
    return dic[variable]

def executeFor(tree,file):
    if(tree.children[0].data == "variable" ):   
        # tokken where it symbol is stocked  
        tokkenIT = tree.children[0].children[0]
        
        # save value of tokkenIT if exist
        tmp = None
        if(dic.__contains__(tokkenIT)):
            tmp = dic.pop(tokkenIT)

        if(tree.children[1].data == "variable" ):
            ot = getValue(tree.children[1].children[0])
        elif (tree.children[1].data == "string_list" ):
            print("STRING LIST FOR NOT YET IMPLEMENTED")
        
        for it in ot:
            dic[tokkenIT] = it
            if(tree.children[2].data == "expression_list" ):
                explore(tree.children[2],file )
        
        # recover value
        if(tmp != None):
            dic[tokkenIT] = tmp
        else:
            dic.pop(tokkenIT)

def explore(racine,file_out):
    print(racine.data)
    # traite le cas de base
    if racine.data == "programme":
        if(type(racine.children)==list):
            for el in racine.children:
                explore(el,file_out)
    elif racine.data == "txt":
        if(file_out != None):
            file_out.write(racine.children[0])
    
    elif racine.data == "dumbo_bloc":
        if(type(racine.children)==list):
            for el in racine.children:
                explore(el,file_out)

    elif racine.data == "expression_list":
        if(type(racine.children)==list):
            for el in racine.children:
                explore(el,file_out)

    elif racine.data == "expression":
        if(racine.children[0].data == "print"):
            if file_out is not None:
                file_out.write(getVar(racine.children[0].children[0]) )
                
        elif(racine.children[0].data == "if"):
            return 0
        elif(racine.children[0].data == "for"):
            executeFor(racine.children[0],file_out)
        elif(racine.children[0].data == "variable"):
            dic[racine.children[0].children[0]] = getVar(racine.children[1])

    elif racine.data == "variable":
        print("VARIABLE")
        print(racine.children[0])
        print(racine.children)
        print("")


if(__name__=="__main__"):

    with open( "dumboGrammar.lark", "r") as grammar:
        parserDumbo =  Lark(grammar.read(),start="programme")


    with open( "data1.dumbo", "r" ) as texte:
        tree_data = parserDumbo.parse(texte.read())
        # print(data.pretty())


    with open( "template.dumbo", "r" ) as texte:
        tree_template = parserDumbo.parse(texte.read())
        # print(template.pretty())


    # print(tree_data)
    # print(tree_data.data)
    # print(tree_data.children)
    # print(tree_data.children[0])
    # print(tree_data.children[0].data.children)

    # print(tree_template)

    #objet tree


    #load data
    explore(tree_data,None)
    #execute template
    with open( "output.html", "w" ) as output:
        explore(tree_template,output)


    print("nom = "+str(dic["nom"]))
    print("prenom = "+str(dic["prenom"]))
    print("cours = "+str(dic["cours"]))
    print("lol = "+str(dic["lol"]))

    # Tree(op, [Tree(plus, [])])

