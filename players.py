#!/usr/bin/env python3

#required for random_player
import random

#required for simple_nn
try:
	import autograd.numpy as np
	from autograd import grad
except:
	pass

class random_benchmark:
	def play(self,hand,state):
		return random.choice(hand)
	def reset(self):
		pass


class simple_nn:
	def __init__(self,no_players=None,no_cards=None):
		
		if no_players == None:
			self.no_players = 4
		else:
			self.no_players = no_players

		if no_cards == None:
			self.no_cards = 36
		else:
			self.no_cards = no_cards

		self.cards_per_players = self.no_cards // self.no_players
		self.dim_in = (self.cards_per_players+self.no_players)*(self.no_cards+1)
		self.dim_out = self.cards_per_players

		self.network_size = [self.dim_in,10,10,self.dim_out]

		self.weights = []
		self.biases = []

		for layer_index in range(1,len(self.network_size)):
			self.weights.append(np.random.randn(self.network_size[layer_index],
												self.network_size[layer_index-1]))
			self.biases.append(np.random.randn(self.network_size[layer_index]))

	def activation(self,x):
		return np.maximum(x,0)

	def infere(self,vector):

		for layer_index in range(len(self.weights)):
			vector = self.activation(np.matmul(self.weights[layer_index],vector)
									 +self.biases[layer_index])
		exp_norm = np.sum(np.exp(vector))
		return np.exp(vector)/exp_norm

	def one_hot(self,raw_lables):
		oh_lables = np.zeros((raw_lables.size,self.no_cards+1))
		oh_lables[np.arange(raw_lables.size),raw_lables+1] = 1.0
		return oh_lables.flatten()

	def play(self,hand,state):

		int_hand = [card.id for card in hand]
		int_state = [card.id for card in state]

		in_vector = np.zeros(self.dim_in)
		in_vector[:len(hand)*(self.no_cards+1)] = self.one_hot(np.array(int_hand))
		in_vector[-len(state)*(self.no_cards+1):] = self.one_hot(np.array(int_state))

		call = np.argmax(self.infere(in_vector.T))

		if call < len(hand):
			return hand[call]
		else:
			return random.choice(hand)

	def reset(self):
		pass



