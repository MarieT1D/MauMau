import numpy as np
import random
from maumau import *
from tkinter import *

class Chobra(Player):
    def __init__(self,name,gamma):
        Player.__init__(self,name)
        self.score = 0
        self.gamma = gamma

    def handout(self,karten):
        self.karten = karten
    def nehme(self,karte):
        self.karten.append(karte)
    def non_lin(self,z):
        return np.tanh(z)
    def load_weights(self,tree):

        self.score = 0

        np.random.seed(tree[0])
        self.home_counsel               = np.random.random((10,10))
        self.home_counsel_bias          = np.random.random(10)
        self.forgein_counsel            = np.random.random((10,no_players))
        self.forgein_counsel_bias       = np.random.random(10)

        for i in tree[1:]:
            np.random.seed(i)
            self.home_counsel           += np.random.random((10,10))*self.gamma
            self.home_counsel_bias      += np.random.random(10)*self.gamma
            self.forgein_counsel        += np.random.random((10,no_players))*self.gamma
            self.forgein_counsel_bias   += np.random.random(10)*self.gamma


    def lege(self,gelegt):
        
        j = 0
        avail = np.zeros(10)
        for i in self.karten[:10]:
            if i.zeichen == gelegt[-1].zeichen or i.farbe == gelegt[-1].farbe:
                avail[j] = i.id
                j += 1

        if np.sum(avail) == 0:
            return 0

        table = np.zeros(no_players)
        for i in range(len(gelegt)):
            table[i] = gelegt[i].id

        tip1 = np.matmul(self.home_counsel,avail)+self.home_counsel_bias
        tip2 = np.matmul(self.forgein_counsel,table)+self.forgein_counsel_bias

        tip1 = self.non_lin(tip1)
        tip2 = self.non_lin(tip2)

        tip = 0.5*(tip1+tip2)

        answerid  = np.argmax(tip)

        if answerid >= np.nonzero(avail)[0].shape[0]:
            answerid = 0

        for i in self.karten:
            if i.id == avail[answerid]:
                try:
                    self.karten.remove(i)
                    return i
                except:
                    print([j for j in avail])
                    print(i)
                    return None

    def result(self,s):
        self.score += s



class window():

    def __init__(self,pop_size,cutoff):

        self.height = 200
        self.width  = 1500

        self.master = Tk()
        self.canvas = Canvas(self.master,height = self.height,width = self.width)
        self.canvas.pack()

        self.x_dis = 15
        self.pop_size = pop_size
        self.cutoff  = cutoff
        self.y_dis = self.height//self.pop_size


    def update(self,population):
        self.canvas.delete(ALL)

        for i in range(len(population)-1,-1,-1):

            if i < self.cutoff:
                color = '#FF0000'
            else:
                color = '#000000'

            if len(population[i])>1:


                coords = []
                for j in range(len(population[i])):
                    coords.append(j*self.x_dis)
                    coords.append(population[i][j]*self.y_dis)

                self.canvas.create_line(coords,width = 2,fill = color)
            else:
                self.canvas.create_oval(0,population[i][0]*self.y_dis-1,
                                        2,population[i][0]*self.y_dis+1,
                                        fill = color)


        self.canvas.update()


    def freeze(self):
        self.master.mainloop()





#Pretending to do Evolution
def second(elem):
    return elem[1]


pop_size = 200
no_rounds = 500
no_generations = 200
cutoff = 30

controll = window(pop_size,cutoff)


population = [[i] for i in range(pop_size)]
Adam = Playerbot('Adam')
Eva =  Playerbot('Eva')

Proto_Chobra1 = Chobra('Chobra1',0.05)
Proto_Chobra2 = Chobra('Chobra2',0.05)

for generation in range(no_generations):
    random.shuffle(population)

    result = [[i,0] for i in range(pop_size)]


    for p_index in range(0,pop_size,2):

        Proto_Chobra1.load_weights(population[p_index])
        Proto_Chobra2.load_weights(population[p_index+1])
        Adam.reset()
        Eva.reset()

        players = [Proto_Chobra1,Proto_Chobra2,Adam,Eva]

        arena = Game(players)
        for _ in range(no_rounds):
            arena.reset()
            arena.play()


        result[p_index][1]   += Proto_Chobra1.score
        result[p_index+1][1] += Proto_Chobra2.score

        immediate_outcome = np.array([i.score for i in players])
        # print(np.round((immediate_outcome*100.0)/(no_rounds),3))


    #surviving the fittest
    result = sorted(result,key=second,reverse = True)

    population_ = population[:]
    for i in range(cutoff):
        population[i] = population_[result[i][0]]
    population_ = []
    for i in range(cutoff,pop_size):
        population[i] = population[i%cutoff]+[i]


    print('--------------------- Finished '+str(generation)+'th Generation ----------------------')

    for i in range(cutoff):
        print(str(i)+': '+str(population[i][-20:])+'\t '+str(np.round((result[i][1]*100.0)/no_rounds))+'%')

    controll.update(population)
