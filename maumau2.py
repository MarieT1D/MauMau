#!/usr/bin/env python3
import random

colors = ['eichel', 'grass',
		  'herz', 'schelle']
numbers = ['7','8','9','10',
		  'Unter','Ober','König','Ass']

def argmax(list):
	max = list[0]
	arg = 0
	for i in range(len(list)):
		if list[i] > max:
			max = list[i]
			arg = i
	return arg


class Card:
	def __init__(self, id):

		self.id = id
		self.color_id = id//len(numbers)
		self.number_id = id%len(numbers)

		self.color = colors[self.color_id]
		self.number = numbers[self.number_id]

		self.loc = 'pile'

	def __lt__(self,other):
		return self.number_id < other.number_id

	def get_info(self):
		print('color: '+self.color)
		print('number: '+self.number)
		print('loc: '+self.loc)

	def set_loc(self,new_loc):
		self.loc = new_loc

class Game:
	def __init__(self,players,talkative = None):

		self.card_register = [Card(i) for i in range(len(colors)*len(numbers))]
		self.no_players = len(players)
		self.players = players
		
		if talkative is not None:
			self.talkative = talkative
		else:
			self.talkative = False

	def handout(self):

		random.shuffle(self.card_register)

		for i in self.card_register:
			i.loc = 'pile'

		for i in range(self.no_players):
			self.players[i].reset()
			for card in range(i,len(self.card_register),
							  self.no_players):
				self.card_register[card].loc = i

	def round(self):
		
		cards_on_the_table = []

		for player in range(self.no_players):
			played_card = self.players[player].play(self.player_cards[player],cards_on_the_table)
			played_card.loc = 'played'
			self.played_cards.append(played_card)
			self.player_cards[player].remove(played_card)
			cards_on_the_table.append(played_card)

			if self.talkative:
				print('player'+str(player)+' played '+played_card.color+' '+played_card.number)

		return argmax(cards_on_the_table)

	def play(self):
		score_board = [0]*self.no_players

		self.player_cards = [[] for i in range(self.no_players)]
		for card in self.card_register:
			self.player_cards[card.loc].append(card)

		self.played_cards = []


		for round_number in range(len(self.card_register)//self.no_players):

			result = self.round()
			score_board[result] += 1

			if self.talkative:
				print('Player'+str(result)+' won the Round!')

		return score_board

