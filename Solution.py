from enum import Enum
import random
import copy

"""Types of moves each tick:
jump: Jump in this tick
stay: Don't jump this tick
hang: Jumped within the last [Solution.hangtime] tickes
dead: Dead from this point forward
"""

hangtime = 3 # Number of ticks the agent remains in the air for
jumpChance = .3 # % chance that the agent will jump
mutationChance = .005 # % chance of a mutation occurring for each tick
deleteMoves = 5 # How many moves after a jump to delete

class Solution:
	def __init__(self, parent1=None, parent2=None):
		random.seed()
		self.moves = []
		self.parent1 = parent1
		self.parent2 = parent2

		if parent1 is None or parent2 is None:
			return

		self.mergeParents()

	# Breed parents to make a new solution
	def mergeParents(self):

		shorter = None
		longer = None
		if len(self.parent1.moves) > len(self.parent2.moves):
			shorter = copy.deepcopy(self.parent2.moves)
			longer = copy.deepcopy(self.parent1.moves)
		else:
			shorter = copy.deepcopy(self.parent1.moves)
			longer = copy.deepcopy(self.parent2.moves)

		# augment shorter solution with random move
		for i in range(len(longer)-len(shorter)):
			shorter += [self.pickMove()]

		# for each tick that the longer solution made it to
		for i in range(len(shorter)):
			# replace em with
			if shorter[i] == "hang" or shorter[i] == "dead":
				shorter[i] = self.pickMove()
			if longer[i] == "hang" or longer[i] == "dead":
				longer[i] = self.pickMove()

			# 10% chance of just picking a totally different move (should be moved to up top, but idk what to name it)
			if(random.random() < mutationChance):
				self.moves += [self.pickMove()]
			else:
				# 50-50 chance of which parent it draws from
				if random.randint(0, 1) == 0:
					self.moves += [shorter[i]]
				else:
					self.moves += [longer[i]]
		# fill in moves after jump with hangtime
		for i in range(len(self.moves)-hangtime):
			if self.moves[i] == "jump":
				for j in range(hangtime):
					self.moves[i+j+1] = "hang"

		self.removeDead()

	# Randomly pick a move
	def newMove(self):
		if random.random() <= jumpChance:
			self.moves += ['jump']
			for i in range(hangtime):
				self.moves += ['hang']
		else:
			self.moves += ['stay']

	def pickMove(self):
		if random.random() <= jumpChance:
			return 'jump'
		else:
			return 'stay'

	# Died at some point, delete last couple moves
	def removeDead(self):
		# delete anything where it's hanging in the air
		while self.moves[-1] == 'hang':
			del self.moves[-1]
		#delete last couple moves
		for i in range(deleteMoves):
			if len(self.moves) > 0:
				del self.moves[-1]

	# Recursively print the lineage
	def printLineage(self, level=0):
		if self.parent1 is not None or self.parent2 is not None:
			self.parent1.printLineage(level+1)
			self.parent2.printLineage(level+1)
		print(' ' * (level*2), end='')
		print(self.moves)

	# Heuristic function to compare them
	def score(self):
		return len(self.moves)


if __name__ == "__main__":
	start1 = Solution()
	while len(start1.moves) < 10:
		start1.newMove()
	start2 = Solution()
	while len(start2.moves) < 5:
		start2.newMove()
	kid1 = Solution(start1, start2)
	kid2 = Solution(start1, start2)
	baby = Solution(kid1, kid2)  # Note: baby is very inbred. Proceed with caution
	baby.printLineage()
