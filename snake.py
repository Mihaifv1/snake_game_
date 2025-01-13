import time
from turtle import Turtle, Screen
import random

class Snake:
    def __init__(self):
        self.snake = []
        self.score = 0
        self.color = "white"
        self.fruit_spawnpoint = Turtle()
        self.fruit_spawnpoint.hideturtle()
        self.is_fruit_active = False
        self.scoreboard = Turtle()
        self.scoreboard.penup()

    def set_color(self, color):
        self.color = color
        for segment in self.snake:
            segment.color(color)

    def add_lenght(self):
        new_turtle = Turtle(shape="square")
        new_turtle.color("white")
        new_turtle.speed(7)
        new_turtle.color(self.color)
        new_turtle.penup()
        if not self.snake:
            self.snake.append(new_turtle)
        elif self.snake[-1].heading() == 90 or self.snake[-1].heading() == 270:
            new_turtle.teleport(self.snake[-1].xcor(), self.snake[-1].ycor() - 20)
            self.snake.append(new_turtle)
        else:
            new_turtle.teleport(self.snake[-1].xcor() - 20, self.snake[-1].ycor())
            self.snake.append(new_turtle)

    def move_snake(self):
        for i in range(1, len(self.snake)):
            curr_snake = len(self.snake) - i
            self.snake[curr_snake].setheading(self.snake[curr_snake - 1].heading())
            self.snake[curr_snake].teleport(
                self.snake[curr_snake - 1].xcor(),
                self.snake[curr_snake - 1].ycor()
            )
            time.sleep(0.15 / len(self.snake))
        if self.snake:
            self.snake[0].fd(20)

    def turn_left(self):
        if self.snake:
            self.snake[0].setheading((self.snake[0].heading() + 90) % 360)

    def turn_right(self):
        if self.snake:
            if self.snake[0].heading() - 90 < 0:
                self.snake[0].setheading((360 + (self.snake[0].heading() - 90)) % 360)
            else:
                self.snake[0].setheading((self.snake[0].heading() - 90) % 360)

    def earn_point(self):
        if abs(self.snake[0].xcor() - self.fruit_spawnpoint.xcor()) < 15 and \
           abs(self.snake[0].ycor() - self.fruit_spawnpoint.ycor()) < 15:
            self.score += 1
            self.is_fruit_active = False
            self.fruit_spawnpoint.undo()
            self.add_lenght()

    def spawn_fruit(self):
        if not self.is_fruit_active:
            random_x = random.randint(-250, 250)
            random_y = random.randint(-250, 250)
            self.fruit_spawnpoint.teleport(random_x, random_y)
            self.fruit_spawnpoint.dot(10, "blue")
            self.is_fruit_active = True

    def update_score(self):
        self.scoreboard.clear()
        self.scoreboard.hideturtle()
        self.scoreboard.color("white")
        self.scoreboard.goto(0, 250)
        self.scoreboard.write(
            f"Score : {self.score}",
            move=False,
            align="center",
            font=("Arial", 24, "normal")
        )

    def game_over(self):
        if self.snake:
            head = self.snake[0]
            if head.xcor() > 300 or head.xcor() < -300 or head.ycor() > 300 or head.ycor() < -300:
                return 1
            for i in range(2, len(self.snake)):
                if self.snake[0].distance(self.snake[i]) < 5:
                    return 1
        return 0
