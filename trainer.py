#!/usr/bin/env python3

import maumau2
import players


G1 = maumau2.Game([players.random_benchmark(),players.random_benchmark(),
				   players.random_benchmark(),players.simple_nn()],talkative = False)
for _ in range(10):
	G1.handout()
	print(G1.play())

