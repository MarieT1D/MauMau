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

no_players = 4
no_cards = 5


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
        def __init__(self,players):
                assert no_players < no_cards*no_players
                self.kartensatz=[Karte(i) for i in karten_ids]
                random.shuffle(self.kartensatz)
               # self.players = no_players
                self.players = players
                self.player_cards = dict(zip([i.id for i in self.players],[]*no_players))
                self.reihenfolge = [i  for i in range(no_players)]


        def reset(self):
            random.shuffle(self.kartensatz)

            for i in self.kartensatz:
                i.loc = 'gespielt'

            for i in range(no_players):
                for j in range(no_cards):
                    self.kartensatz[i*no_cards+j].loc = self.players[i].id
                self.players[i].handout(self.kartensatz[i*no_cards:(i+1)*no_cards])

            self.reihenfolge = [self.reihenfolge[-1]]+self.reihenfolge[:-1]


        def check_karten(self):
            player_ids = [i.id for i in self.players]
            self.player_cards = dict(zip(player_ids,[[]for i in range(len(player_ids))]))
            for i in self.kartensatz:
                if i.loc in player_ids:
                    self.player_cards[i.loc].append(i)


        def play(self):

            es_gibt_einen_gewinner = False
            gelegt = self.kartensatz[no_players*no_cards:]

            counter = 0


            while not(es_gibt_einen_gewinner):


                for i in self.reihenfolge:

                    answer = self.players[i].lege(gelegt[-no_players:])
                    if answer != 0:
                        assert answer.loc == self.players[i].id     #schaut ob er die Karte hat
                        assert answer.farbe == gelegt[-1].farbe or answer.zeichen == gelegt[-1].zeichen
                        answer.loc = 'gespielt'
                        gelegt.append(answer)


                    if answer == 0 and len(gelegt)>no_players:
                        j = random.randint(0,len(gelegt)-no_players)
                        gelegt[j].loc = self.players[i].id
                        self.players[i].nehme(gelegt[j])
                        gelegt.pop(j)
                        answer = self.players[i].lege([gelegt[-1]])
                        if answer !=0:
                            answer.loc = 'gespielt'
                            gelegt.append(answer)



                    self.check_karten()
                    for j in self.players:
                        if len(self.player_cards[j.id]) == 0:
                            es_gibt_einen_gewinner = True
                            winner = j
                            j.result(1)
                          #  print('Grandios, ' +str(j.name)+ ' ist toll')
                            for k in self.players:
                                if k != j:
                                    k.result(0)


        
                    if es_gibt_einen_gewinner:
                        break

                counter += 1

                if counter >= 10000:
                    es_gibt_einen_gewinner = True

            return counter


            """
            TODO:
            besondere Regeln (aussetzen)
            """



                             
class Player():
    x=iter(list(range(no_players)))
    def __init__(self, name):
                self.name=name
                self.id= next(self.x)

    def get_kartenname(self):
        a=[self.karten[i].name for i in range(len(self.karten))]
        return a

    def get_kartenid(self):
        a=[self.karten[i].id for i in range(len(self.karten))]
        return a



class Playerbot(Player):
    def __init__(self,name):
        Player.__init__(self,name)
        self.score = 0
    def handout(self,karten):
        self.karten = karten



    def lege(self,gelegt):


        k=gelegt[-1]
        f = 0
        for i in range(len(self.karten)):                
            if k.farbe==self.karten[i].farbe or k.zeichen == self.karten[i].zeichen:
                f=self.karten[i]
        if f != 0:
            self.karten.remove(f)
        return f

    def nehme(self,a):
        self.karten.append(a)

    def result(self,s):
        self.score += s

    def reset(self):
        self.score = 0