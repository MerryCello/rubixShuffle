###############################################################################
# RUBIX SHUFFLE
# Author: Kevin Foniciello
# Description:
#   Provides instructions to randomly shuffle a Rubik's Cube
#   See instructions' guide: https://jperm.net/images/notation.png
###############################################################################
from os import system
from random import Random
from time import sleep
from typing import Any

DEV = 0
PROD = 1
ENV = PROD

TOTAL_MOVES_PRODUCED = 15
if ENV == DEV: TOTAL_MOVES_PRODUCED = 10


#################################################
# DIRECTION
# A direction from up, down, left, right,
# clockwise, or counter clockwise
#################################################
class Direction:
  LEFT = "←"
  RIGHT = "→"
  DOWN = "↓"
  UP = "↑"
  CLOCKWISE = "CW"
  COUNTER_CLOCKWISE = "CCW"

  def __init__(self, direction): self._direction = direction
  def __str__(self) -> str: return self._direction
  
  def __eq__(self, __o: object) -> bool:
    if type(__o) == type(self):
      return __o._direction == self._direction
    else:
      eMessage = "Cannot compare a '{typeA}' to a '{typeDirection}'."
      raise Exception(eMessage.format(typeA=type(__o), typeDirection=type(self)))
  
  # Return the opposite direction
  def opposite(self) -> object:
    if   (self._direction == self.LEFT):              return Direction(self.RIGHT)
    elif (self._direction == self.RIGHT):             return Direction(self.LEFT)
    elif (self._direction == self.DOWN):              return Direction(self.UP)
    elif (self._direction == self.UP):                return Direction(self.DOWN)
    elif (self._direction == self.CLOCKWISE):         return Direction(self.COUNTER_CLOCKWISE)
    elif (self._direction == self.COUNTER_CLOCKWISE): return Direction(self.CLOCKWISE)


#################################################
# MOVE
# A single move
#################################################
class Move:
  def __init__(self, symbol: str, direction: Direction, annotation: str="") -> None:
    self.symbol: str = symbol
    self.direction: Direction = direction
    self.annotation: str = annotation
  
  def __eq__(self, __o: object) -> bool: return not self.__ne__(__o)

  def __ne__(self, __o: object) -> bool:
    if type(__o) == type(self):
      return __o.symbol != self.symbol or __o.direction != self.direction
    else:
      eMessage = "Cannot compare a '{typeA}' to a '{typeMove}'."
      raise Exception(eMessage.format(typeA=type(__o), typeMove=type(self)))
  
  # return reversed moved (marked with an apostrophy, and has the opposite direction)
  def reverseMove(self) -> object:
    if self.symbol[0] == "'":
      return Move(self.symbol.replace("'", ""), self.direction.opposite())
    else:
      return Move("'" + self.symbol, self.direction.opposite())


#################################################
# STACK
# Stack data type implementation
#################################################
class Stack:
  def __init__(self, items:list=[]) -> None: self._stack: list = items
  def push(self, item):       self._stack.append(item)
  def pop(self):              self._stack.pop()
  def top(self) -> Any:       return self._stack[-1]
  def isEmpty(self) -> bool:  return len(self._stack) == 0
  def size(self) -> int:      return len(self._stack)


#################################################
# MOVES
# List of possible moves
#################################################
MOVES = [
  Move(symbol="U" , direction=Direction(Direction.LEFT)              ),
  Move(symbol="D" , direction=Direction(Direction.RIGHT)             ),
  Move(symbol="R" , direction=Direction(Direction.UP)                ),
  Move(symbol="L" , direction=Direction(Direction.DOWN)              ),
  Move(symbol="F" , direction=Direction(Direction.CLOCKWISE)         ),
  Move(symbol="B" , direction=Direction(Direction.COUNTER_CLOCKWISE) ),
  Move(symbol="Uw", direction=Direction(Direction.LEFT)              ),
  Move(symbol="Dw", direction=Direction(Direction.RIGHT)             ),
  Move(symbol="Rw", direction=Direction(Direction.UP)                ),
  Move(symbol="Lw", direction=Direction(Direction.DOWN)              ),
  Move(symbol="Fw", direction=Direction(Direction.CLOCKWISE)         ),
  Move(symbol="Bw", direction=Direction(Direction.COUNTER_CLOCKWISE) ),
  Move(symbol="X" , direction=Direction(Direction.UP)                ),
  Move(symbol="Y" , direction=Direction(Direction.LEFT)              ),
  Move(symbol="Z" , direction=Direction(Direction.CLOCKWISE)         ),
  Move(symbol="M" , direction=Direction(Direction.DOWN)              ),
  Move(symbol="E" , direction=Direction(Direction.RIGHT)             ),
  Move(symbol="S" , direction=Direction(Direction.CLOCKWISE)         ),
]


#################################################
# GENERATE MOVES
#################################################
def generateMoves() -> Stack:
  movesStack = Stack()

  for i in range(TOTAL_MOVES_PRODUCED):
    repeatsCount = 0
    # loop to keep getting another move when the one generated was invalid
    # only runs up to 100 times
    while True:
      repeatsCount+=1
      if repeatsCount == 100: raise Exception("Cannot find suitable next move.")

      # Randomize the move
      newMove: Move = MOVES[Random().randint(0, (len(MOVES)-1))]
      # Randomize the move's direction
      if Random().randint(0, 1): newMove = newMove.reverseMove()
      
      # Validate move
      if movesStack.size() >= 1:
        # Consolidate same consecutive moves
        if movesStack.top() == newMove:
          movesStack.top().annotation = "2x "
        # Can't undo a previous move
        elif movesStack.top() != newMove.reverseMove():
          movesStack.push(newMove)
          break
      # it's the first push, so just add it and move on
      else:
        movesStack.push(newMove)
        break
        
  return movesStack


#################################################
# MAIN
#################################################
def main():
  if ENV == PROD: sleep(1)
  moves = generateMoves()

  n = 1
  while not moves.isEmpty():
    move: Move = moves.top()
    print("\t", str(n) + ".", move.annotation + move.symbol)
    print("\t    " + str(move.direction) + "\n")
    if ENV == PROD: sleep(2)
    moves.pop()
    n+=1
  
  if ENV == PROD: system("pause")

main()
