#!/usr/bin/python
import random
from Tkinter import *

KEY_UP = "Up"
KEY_DOWN = "Down"
KEY_LEFT = "Left"
KEY_RIGHT = "Right"

rows, cols = (21, 21)
initialSnake = [(10, 10), (11, 10), (12, 10)]
cellWidth = 20
margin = 5
delay = 500


class Snake:
    def __init__(self):
        self.food = None
        self.body = None
        self.keyPressed = None
        self.isGameOver = False
        self.reset()

    def randomFood(self):
        self.food = (random.randint(0, rows - 1), random.randint(0, cols - 1))

    def head(self):
        return self.body[0]

    def nextStep(self, direction):
        x, y = self.head()

        if direction == KEY_UP:
            x -= 1
        elif direction == KEY_DOWN:
            x += 1
        elif direction == KEY_LEFT:
            y -= 1
        elif direction == KEY_RIGHT:
            y += 1

        return x, y

    def move(self):
        nextStep = self.nextStep(self.keyPressed)
        if nextStep in self.body:
            self.gameOver()
        elif self.hitBorder(nextStep):
            self.gameOver()
        elif self.hitFood(nextStep):
            self.body.insert(0, nextStep)
            self.randomFood()
        else:
            self.body.insert(0, nextStep)
            self.body.pop()

    def hitFood(self, ns):
        return self.food == ns

    def hitBorder(self, ns):
        x, y = ns
        if x < 0 or y < 0 or x >= cols or y >= rows:
            return True
        return False

    def gameOver(self):
        self.isGameOver = True

    def reset(self):
        self.keyPressed = KEY_RIGHT
        self.body = [x for x in initialSnake]
        self.isGameOver = False
        self.randomFood()


class Game:
    def __init__(self, snake):
        self._task = None
        self.root = Tk()
        self.snake = snake
        canvas_width = margin + rows * cellWidth
        canvas_height = margin + cols * cellWidth
        self.canvas = Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack()

    def run(self):
        self.root.bind("<Key>", self.keyPressed)
        self.timerFired()
        self.root.mainloop()

    def restartGame(self):
        self.snake.reset()
        self.root.after_cancel(self._task)
        self.timerFired()

    def timerFired(self):
        self.snake.move()
        if not self.snake.isGameOver:
            # draw snake
            self.redrawAll()
            self._task = self.canvas.after(delay, self.timerFired)
        else:
            # draw game over
            cx = margin + rows * cellWidth / 2
            cy = margin + cols * cellWidth / 2
            self.canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
            self.canvas.create_text(cx, cy + 32,
                text="press 'space' to restart", font=("Helvetica", 22))

    def redrawAll(self):
        self.canvas.delete(ALL)

        # draw border
        self.canvas.create_rectangle(
            margin, margin, margin + cellWidth * cols, margin + cellWidth * rows,
            fill="white", width=2)

        # draw snake
        for cell in self.snake.body:
            self.drawCell(cell, "blue")

        # draw food
        self.drawCell(self.snake.food, "red")

    def drawCell(self, cell, color):
        row, col = cell
        left = margin + col * cellWidth
        right = left + cellWidth
        top = margin + row * cellWidth
        bottom = top + cellWidth
        self.canvas.create_rectangle(left, top, right, bottom, fill=color, width=0)

    def keyPressed(self, event):
        hKeys = [KEY_LEFT, KEY_RIGHT]
        vKeys = [KEY_UP, KEY_DOWN]

        allowedKeys = vKeys if self.snake.keyPressed in hKeys else hKeys

        if event.keysym == "space":
            self.restartGame()
        elif event.keysym in allowedKeys:
            self.snake.keyPressed = event.keysym
            self.root.after_cancel(self._task)
            self.timerFired()


if __name__ == "__main__":
    s = Snake()
    game = Game(s)
    game.run()
