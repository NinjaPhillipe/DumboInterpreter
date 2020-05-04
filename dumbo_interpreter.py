from lark import Lark
from lark import Transformer
import sys

# Variable global
dic= {}

def getStringInterior(tree,tmp):
    """
        Return a string that represents the string interior
        
        Recursive algorithm
    """
    tmp.append(tree.children[0].children[0].value)
    if(len(tree.children)==2):
        getStringInterior(tree.children[1],tmp)
    return tmp

def getVar(tree):
    """
        Use the getValue,getString and evalInteger to get the value assigned to the variable 
        Recursive function that go further in the tree everytime it's called
    """
    if(tree.data == "string_expression"):
        if(tree.children[0].data == "string"):
            return tree.children[0].children[0]
        elif(tree.children[0].data == "variable"):
            return getValue(tree.children[0].children[0])
        elif(tree.children[0].data == "string_expression"):
            # if the child is a string expression apply getVar again on the child
            if(len(tree.children)== 2):
                return getVar(tree.children[0])+getVar(tree.children[1])
            return getVar(tree.children[0])
    elif(tree.data == "integer"):
        return evalInteger(tree)        
        
    elif(tree.data == "string_list"):
        return getStringInterior(tree.children[0],[])
    return "ERROR"

def getValue(variable):
    """
        Return the value of a key if the key exist.
    """
    if(dic.__contains__(variable)):
        return dic[variable]
    else:
        print("Variable : "+str(variable) + " ERROR KEY NOT IN DIC")

def executeFor(tree,file):
    """
    Function called when there's a 'for' encounter in the tree
    A tmp variable is created so the 'true' value of the variable
    in the list is not modified
    """
    if(tree.data == "for" ):   
        # tokken where it symbol is stocked  
        tokkenIT = tree.children[0].children[0]
        
        # save value of tokkenIT if exist
        tmp = None
        if(dic.__contains__(tokkenIT)):
            tmp = dic.pop(tokkenIT)

        # get the value on which the iteration is executed
        if(tree.children[1].data == "variable" ):
            ot = getValue(tree.children[1].children[0])
        elif (tree.children[1].data == "string_list" ):
            ot = getStringInterior(tree.children[1].children[0],[])
        
        # compute the iteration
        for it in ot:
            dic[tokkenIT] = it
            # sanity check
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
    """
    Fuction used when a definition of integer is encountered in the tree
    in order to compute the value of an integer 
    
    if we are in a leaf of the tree, the function is used to return the value of the leaf
    if we are not in a leaf the function is called on the subtree to calculate the value of the subtree
    """
    # if the subtree is a leaf
    if(tree.children[0].data == "int"):
        return int(tree.children[0].children[0].value)
    
    # set Var 1
    if(tree.children[0].data == "integer"):
        var1 = evalInteger(tree.children[0])
    if(tree.children[0].data == "variable"):
        var1 = getValue(tree.children[0].children[0].value)

    # set Var 2 
    if(tree.children[2].data == "integer"):
        var2 = evalInteger(tree.children[2])
    if(tree.children[2].data == "variable"):
        var2 = getValue(tree.children[2].children[0].value)

    # Operation
    if(tree.children[1].children[0].data == "mult"):
        return var1 * var2
    elif(tree.children[1].children[0].data == "plus"):
        return var1 + var2
    elif(tree.children[1].children[0].data == "div"):
        return var1 / var2
    elif(tree.children[1].children[0].data == "minus"):
        return var1 - var2

    print("ERROR : UNEXPECTED TOKKEN")

def evalBoolean(tree):
    """
        Function that evaluate the boolean.

        If the boolean children is a "or" or "and" tokken 
        recursive call are executed on his two member.
    """
    # check if children the children is a "or" or a "and" tokken
    if (tree.children[0].data == "or"):
        return evalBoolean(tree.children[0].children[0]) or evalBoolean(tree.children[0].children[1])
    if (tree.children[0].data) == "and":
        return evalBoolean(tree.children[0].children[0]) and evalBoolean(tree.children[0].children[1])
    
    # set var1
    if(tree.children[0].data == "integer"):
        var1 = evalInteger(tree.children[0])
    elif(tree.children[0].data == "variable"):
        var1 = getValue(tree.children[0].children[0].value)

    # set var2
    if(tree.children[2].data == "integer"):
        var2 = evalInteger(tree.children[2])
    elif(tree.children[2].data == "variable"):
        var2 = getValue(tree.children[2].children[0].value)

    if(tree.children[1].children[0].data == "greater"):
        return var1 > var2
    if(tree.children[1].children[0].data == "less"):
        return var1 < var2
    if(tree.children[1].children[0].data == "equals"):
        return var1 == var2
    if(tree.children[1].children[0].data == "nequal"):
        return var1 != var2

    print("ERROR : UNEXPECTED TOKKEN")
    return False

def executeIf(tree,file):
    """
        Compute expression list if the evalution is true
    """
    if(evalBoolean(tree.children[0])):
        explore(tree.children[1],file)


def explore(racine,file_out):
    """
        Explore recursively the tree to compute his tokken. 
    """
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
                file_out.write(str(getVar(racine.children[0].children[0])) )
                
        elif(racine.children[0].data == "if"):
            executeIf(racine.children[0],file_out)
        elif(racine.children[0].data == "for"):
            executeFor(racine.children[0],file_out)
        elif(racine.children[0].data == "variable"):
            dic[racine.children[0].children[0]] = getVar(racine.children[1])

if(__name__=="__main__"):
    if(len(sys.argv) == 4 ):
        with open( "dumboGrammar.lark", "r") as grammar:
            parserDumbo =  Lark(grammar.read(),start="programme")
        
        with open( sys.argv[1], "r" ) as texte:
            tree_data = parserDumbo.parse(texte.read())

        with open( sys.argv[2], "r" ) as texte:
            tree_template = parserDumbo.parse(texte.read())

        # load data from data file
        explore(tree_data,None)

        #execute template
        with open( sys.argv[3], "w" ) as output:
            explore(tree_template,output)
    else:
        print("Incorrect argument format")