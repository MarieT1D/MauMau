"""
Kartendarstellung

        Eichel  Grass   Herz    Schelle
7       10      20      30      40
8       11      21      31      41
9       12      22      32      42
koenig  13      23      33      43
10      14      24      34      44
sau     15      25      35      45
unter   16      26      36      46
ober    17      27      37      47

"""
import random
#Mgliche Farben/Werte
farbe=("Eichel", "Gras", "Herz", "Schelle")
wert=("7","8","9","Koenig","10","Sau","Unter","Ober")

#Darstellung im Bot
pos_kartenwert_id=[i for i in range(8)]
pos_kartenfarbe_id=[(j+1)*10 for j in range(4)]

karten_ids=[(i+j)for j in pos_kartenfarbe_id
        for  i in pos_kartenwert_id]

#Dictionary Karte und Kartenname
pos_kartenzeichen=dict(zip(pos_kartenwert_id,wert))
pos_kartenfarben=dict(zip(pos_kartenfarbe_id,farbe))
pos_kartennamen=dict(zip(karten_ids,[(j+"_"+i)for j in farbe 
                       for  i in wert]))


#stellt die farbe einer Karte fest
#Trumpf 0,Eichel 1,Gras 2,Herz 3,Schelle 4
def get_farbe(karte):
    return pos_kartenfarben[(karte//10)*10]
    
def get_punkte(karte):
    return punkt_wert[karte%10]

def get_zeichen(karte):
    return pos_kartenzeichen[karte%10]
    

class karte():
    def __init__(self, id):
        
        self.id = id
        self.farbe   = get_farbe(id)
        self.zeichen = get_zeichen(id) 
        self.wert    = get_punkte(id)
        self.name    = str(self.farbe)+'_'+str(self.zeichen)
        self.loc     = 'None'
    
    #location encoding:
    #'None' - nicht ausgeteilt
    #str - name des Spielers
    #'Stich' - Im aktuellen Stich
    #'gespielt' - In einem vergangenen Stich
    def move_loc(self,loc):
        self.loc = loc

