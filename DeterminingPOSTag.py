from tokenSearcher import token_matcher
from posCounter import *
from scipy.stats import entropy


def compareTwoambigousTag(Edict1,Edict2):
    unambigousPos = []

    if  (Edict1["entropy"] < Edict2["entropy"]) :
        unambigousPoslist = Edict2['CombinedPos']
        for item in range(len(unambigousPoslist)):
            temp = unambigousPoslist[item].split('#')[0]
            unambigousPos.append(temp)

        return unambigousPos
    elif(Edict1["entropy"] > Edict2["entropy"]):
        unambigousPoslist = Edict1['CombinedPos']
        for item in range(len(unambigousPoslist)):
            
            temp = unambigousPoslist[item].split('#')[1]
            unambigousPos.append(temp)


        return unambigousPos
    elif(Edict1["entropy"] == Edict2["entropy"]):
        Ep1 = []
        Ep2 = []
        Ep3 = []
        tmp1 = Edict2["CombinedPos"]

        tmp2 = Edict1["CombinedPos"]
        for item in range(len(tmp1)):
            Ep2.append(tmp1[item].split('#')[0])
          
        for item in range(len(tmp2)):
            Ep1.append(tmp2[item].split('#')[1])
            
        match = token_matcher(Ep1,Ep2)
        
        if(match == []):
            Ep3 = Ep2 + Ep1
            return Ep3
        else:
            xl = Edict1["entropy"]
            return match

def calculatingEntropy(list1):
    MostpossiblePOS = []
    Probability = 0
    for i in range(len(list1)):
        first = list1[i].split('#')[0]
        second = list1[i].split('#')[1]
        FC = countPOSInLine("pos_sentance.txt",first)
        SC = countPOSInLine("pos_sentance.txt",second)
        Numerator = countPOSInLine2("pos_sentance.txt",list1[i])
        Pr = (Numerator / FC) * (Numerator / SC)
        #print(Pr)
        if Pr > Probability:
            Probability = Pr
            MostpossiblePOS = []
            MostpossiblePOS.append(list1[i])
        elif Pr == Probability:
            MostpossiblePOS.append(list1[i])
            
   
    rdict = {}
    z = 1 - Probability
    rdict['CombinedPos'] = MostpossiblePOS
    rdict['entropy'] = entropy([Probability,z],base = 2)
 
    return(rdict)

