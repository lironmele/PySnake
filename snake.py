import os
import random

class Piece:
    def __init__(self, location):
        self.location = location
    def update_location(self, new_location):
        old_location = self.location
        self.location = new_location
        return old_location

class Head(Piece):
    def __init__(self, location):
        super().__init__(location)
        self.direction = [1, 0]
        self.location = location
        self.body = []
    def add_body_piece(self):
        if self.body:
            last_location = self.body[-1].location
        else:
            last_location = self.location
        self.body.append(Piece(last_location))
    def move(self):
        old_location = self.location[:]
        for p in self.body:
            old_location = p.update_location(old_location)[:]
        self.location = [sum(i) for i in zip(self.location, self.direction)]
    def update_direction(self, new_direction):
        direction_sum = [sum(i) for i in zip(self.direction, new_direction)]
        if direction_sum == [0,0]:
            # means that we try to go in the opposite direction
            return
        if new_direction in [[1,0], [0,1], [-1,0], [0,-1]]:
            self.direction = new_direction 
    def get_locations(self):
        locations = [self.location]
        for p in self.body:
            locations.append(p.location)
        return locations
    def head_to_body_collision(self):
        locations = self.get_locations()
        head_location = locations.pop(0)
        return head_location in locations and len(locations) > 1
        
class Cherry(Piece):
    def __init__(self, dimensions, locations):
        x = random.randrange(0, dimensions[0])
        y = random.randrange(0, dimensions[1])
        while [x, y] in locations:
            x = random.randrange(0, dimensions[0])
            y = random.randrange(0, dimensions[1])
        super().__init__([x, y])

class Board:
    def __init__(self, dimensions, count=1):
        self.dimensions = tuple(dimensions)
        self.snake = Head([dimensions[0]//2, dimensions[1]//2])
        self.spawn_cherry()
        self.game_ended = False
        self.board_string = ""
        for p in range(count-1):
            self.snake.add_body_piece()
    def __str__(self):
        board_string = ""
        locations = self.snake.get_locations()
        for y in range(self.dimensions[1]):
            for x in range(self.dimensions[0]):
                if [x, y] == locations[0]:
                    board_string += "+"
                elif [x, y] in locations:
                    board_string += "-"
                elif [x, y] == self.cherry.location:
                    board_string += "o"
                else:
                    board_string += " "
            board_string += "\n"
        return board_string
    def spawn_cherry(self):
        self.cherry = Cherry(self.dimensions, self.snake.get_locations())
    def snake_outside_border(self):
        x, y = self.snake.location
        if x < 0 or y < 0 or x >= self.dimensions[0] or y >= self.dimensions[1]:
            return True
        return False
    def update(self, user_input=""):
        if self.game_ended:
            return
        directions = {"w":[0,-1], "a":[-1,0], "s":[0,1], "d":[1,0]}
        if user_input in directions.keys(): 
            self.snake.update_direction(directions[user_input])
        self.snake.move()
        if self.snake.location == self.cherry.location:
            self.snake.add_body_piece()
            self.spawn_cherry()
        if self.snake_outside_border() or self.snake.head_to_body_collision():
            self.game_ended = True

if __name__ == "__main__":
    board = Board([15, 15], count=3)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(board)
        board.update(user_input=input())

