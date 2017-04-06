#!/usr/bin/python3

def isLost(s, e):
  """ Test to see if the set a has a triangle """
  for e1 in s:
    for e2 in (s-set([e1])):
      if e == (e1 ^ e2):
        #print("You lose!")
        #print(e, e1, e2)
        return True
  return False
  
def generateSet(n):
  # Generate the elements in the set
  a = set()
  for i in range(n):
    for j in range(i+1, n):
      a.add(frozenset([i, j])) # Frozen set to make immutable
  return a

class TreeNode():
  def __init__(self, s, p1s, p2s, activePlayer):
    self.s = s
    self.p1s = p1s
    self.p2s = p2s
    self.activePlayer = activePlayer

  def simulate(self):
    # Keep track of which are wins/losses/draws
    self.win = set()
    self.loss  = set()
    self.draw = set()

    if self.s == set(): # Empty set
      return 0 # Draw
    for e in self.s:
      #if isLost(self.s, e):
      if self.activePlayer == 1:
        if isLost(self.p1s, e):
          # Bad move - don't pick
          self.loss.add(e)
          continue
      else:
        if isLost(self.p2s, e):
          # Bad move - don't pick
          self.loss.add(e)
          continue
      tempSet = self.s-set([e])
      if self.activePlayer == 1: # I'm player 1
        t = TreeNode(tempSet, self.p1s.union(set([e])), self.p2s, 2)
        result = t.simulate()
        if result == 0: # Draw
          self.draw.add(e)
        elif result == 1: # Player one (me) wins
          self.win.add(e)
        elif result == 2: # Player two (opponent) wins
          self.loss.add(e)
      else: # I'm player 2
        t = TreeNode(tempSet, self.p1s, self.p2s.union(set([e])), 1)
        result = t.simulate()
        if result == 0: # Draw
          self.draw.add(e)
        elif result == 1: # Player one (opponent) wins
          self.loss.add(e)
        elif result == 2: # Player two (me) wins
          self.win.add(e)

    # Check the lists and see if there is a winning strategy
    if len(self.win) > 0:
      return self.activePlayer
    elif len(self.draw) > 0:
      return 0
    else:
      return 1 if self.activePlayer == 2 else 2

  def getWinningPlays(self):
    print(self.win)

  def getLosingPlays(self):
    print(self.loss)

  def getDrawPlays(self):
    print(self.draw)

def makePlay(a, ps, e):
  e = frozenset(e)
  a.remove(e)
  ps.add(e)

def play(e):
  makePlay(play.a, play.ps[play.player], e)
  play.player = (play.player + 1) % 2
  t = TreeNode(play.a, play.ps[0], play.ps[1], play.player+1)
  t.simulate()
  print('It is now player ', play.player+1,  '\'s turn. Strategy is as follows:')
  print('Winning plays')
  t.getWinningPlays()
  print('Draw plays')
  t.getDrawPlays()
  print('Losing plays')
  t.getLosingPlays()

def startGame():
  play.player = 0
  play.a = generateSet(5)
  play.ps = [set(), set()]
  print('New game. It is now player 1\'s turn')
  
play.player = 0
play.a = generateSet(5)
play.ps = [set(), set()]

if __name__ == "__main__":
  n = 6
  a = generateSet(n)
  print(a)

  isLost(a, frozenset([1, 2]))

  player1 = set()
  player2 = set()

  t = TreeNode(a, player1, player2, 1)
  print("The winningest strategy goes to: ", t.simulate())
