from lark import Lark
from lark import Transformer
import logging
logging.basicConfig(level=logging.DEBUG)

# print(dumbo_grammar)

# lol on sait pas si il faut un espace apres for

dic= {}

def getStringInterior(tree,tmp):
    print(" add "+tree.children[0].children[0].value)
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

        print(tree.children)
        return (tree.children[0])
        
        
        
    elif(tree.data == "string_list"):
        return getStringInterior(tree.children[0],[])
    return "ERROR"

# def getValue(tree):
#     return dic[tree.children[0]]
def getValue(variable):
    return dic[variable]

def executeFor(tree,file):
    if(tree.data == "for" ):   
        # tokken where it symbol is stocked  
        tokkenIT = tree.children[0].children[0]
        
        # save value of tokkenIT if exist
        tmp = None
        if(dic.__contains__(tokkenIT)):
            tmp = dic.pop(tokkenIT)

        if(tree.children[1].data == "variable" ):
            ot = getValue(tree.children[1].children[0])
        elif (tree.children[1].data == "string_list" ):
            print("pipi -------")
            ot = getStringInterior(tree.children[1].children[0],[])
            print("pipi ------- "+ str(ot))
            # print("STRING LIST FOR NOT YET IMPLEMENTED")
        
        for it in ot:
            dic[tokkenIT] = it
            if(tree.children[2].data == "expression_list" ):
                explore(tree.children[2],file )
        
        # recover value
        if(tmp != None):
            dic[tokkenIT] = tmp
        else:
            dic.pop(tokkenIT)
    else:
        print("Incorrect for ")

def evalInteger(tree):
    if(len(tree.children) == 1):
        return int(tree.children[0].children[0].value)
    
    if(tree.children[0].data == "integer"):
        var1 = evalInteger(tree.children[0])

    if(tree.children[2].data == "integer"):
        var2 = evalInteger(tree.children[2])

    # faire cas variable

    if(tree.children[1].children[0].data == "mult"):
        return var1 * var2
    elif(tree.children[1].children[0].data == "plus"):
        return var1 + var2
    elif(tree.children[1].children[0].data == "div"):
        return var1 / var2
    elif(tree.children[1].children[0].data == "minus"):
        return var1 - var2

    print("INTERDIT")

def evalBoolean(tree):
    if (tree.children[0].data == "or"):
        return evalBoolean(tree.children[0].children[0]) or evalBoolean(tree.children[0].children[1])

    if (tree.children[0].data) == "and":
        return evalBoolean(tree.children[0].children[0]) and evalBoolean(tree.children[0].children[1])
    if(tree.children[0].data == "integer"):
        var1 = evalInteger(tree.children[0])
    elif(tree.children[0].data == "variable"):
        print(getValue(tree.children[0].children[0]))
        var1 = getValue(tree.children[0].children[0].value)


    if(tree.children[2].data == "integer"):
        var2 = evalInteger(tree.children[2])
    elif(tree.children[2].data == "variable"):
        print(getValue(tree.children[2].children[0]))
        var2 = getValue(tree.children[2].children[0].value)

    


    if(tree.children[1].children[0].data == "greater"):

        return var1 > var2
    if(tree.children[1].children[0].data == "less"):
        return var1 < var2
    if(tree.children[1].children[0].data == "equals"):
        return var1 == var2
    if(tree.children[1].children[0].data == "nequal"):
        return var1 != var2

    print("NE DOIT PAS ETRE LA ")
    return False

def executeIf(tree,file):
    if(evalBoolean(tree.children[0])):
        explore(tree.children[1],file)


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
            executeIf(racine.children[0],file_out)
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
    print("mdr = "+str(dic["mdr"]))

    # Tree(op, [Tree(plus, [])])
