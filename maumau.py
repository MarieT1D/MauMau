"""
Kartendarstellung

        Eichel  Grass   Herz    Schelle
7       10      20      30      40
8       11      21      31      41
9       12      22      32      42
10      13      23      33      43
unter   14      24      34      44
ober    15      25      35      45
koenig  16      26      36      46
sau     17      27      37      47

"""
import random
#Mgliche Farben/Werte
farbe=("Eichel", "Gras", "Herz", "Schelle")
wert=("7","8","9","10","Unter","Ober","Koenig","Sau")

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
    

class Karte():
    def __init__(self,id):
        
        self.id = id
        self.farbe   = get_farbe(id)
        self.zeichen = get_zeichen(id) 
        if self.zeichen== "7":
                self.wert= "zwei_ziehen"
        elif self.zeichen=="8":
                self.wert= "aussetzen"
        self.name    = str(self.farbe)+'_'+str(self.zeichen)
        self.loc     = 'None'
    
class Game():
        players=4
        def __init__(self, players=None):
                assert players < 6
                self.kartensatz=[Karte(i) for i in karten_ids]
                random.shuffle(self.kartensatz)
                self.players=4

                if players == None:
                    self.players = 4
                else:
                    self.players = players
                             
class Player():
    x=iter(list(range(Game.players)))
    def __init__(self, name,game):
                self.name=name
                self.id= next(self.x)
                self.handout=game.kartensatz[(self.id*5):(self.id+1)*5]
    def get_kartenname(self):
        a=[self.handout[i].name for i in range(len(self.handout))]
        return a

    def get_kartenid(self):
        a=[self.handout[i].id for i in range(len(self.handout))]
        return a

class Playerbot(Player):
    def __init__(self,name,game):
        Player.__init__(self,name,game)

tgame = Game(4)
p1=Player("Marie",tgame)

print(p1.get_kartenname(),p1.get_kartenid())


