from turtle import Screen, Turtle
import time
import os
from snake import Snake

BASE_DIR = os.path.dirname(__file__)
SCORE_FILE = os.path.join(BASE_DIR, "scores.txt")

points = 0
high_score = 0
total_points = 0
snake_color = "white"
fruit_color = "blue"

def load_scores():
    global high_score, total_points
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            try:
                data = file.read().strip().split(",")
                high_score = int(data[0]) if len(data) > 0 else 0
                total_points = int(data[1]) if len(data) > 1 else 0
            except ValueError:
                high_score = 0
                total_points = 0
    else:
        high_score = 0
        total_points = 0

def save_scores():
    with open(SCORE_FILE, "w") as file:
        file.write(f"{high_score},{total_points}")

load_scores()

def start_game():
    global points, high_score, total_points, snake_color, fruit_color

    screen.clear()
    screen.bgcolor("black")
    screen.title("My Snake Game")
    screen.tracer(0, 0)

    snake = Snake()
    snake.set_color(snake_color)
    snake.add_lenght()
    snake.add_lenght()
    snake.add_lenght()
    points = 0

    fruit = Turtle()
    fruit.shape("circle")
    fruit.color(fruit_color)
    fruit.penup()
    fruit.goto(0, 100)

    score_turtle = Turtle()
    score_turtle.hideturtle()
    score_turtle.color("white")
    score_turtle.penup()
    score_turtle.goto(0, 260)
    score_turtle.write(f"Scor: 0  High Score: {high_score}", align="center", font=("Arial", 16, "bold"))

    def update_score():
        score_turtle.clear()
        score_turtle.write(f"Scor: {points}  High Score: {high_score}", align="center", font=("Arial", 16, "bold"))

    screen.listen()

    def spawn_fruit():
        import random
        fruit.goto(random.randint(-280, 280), random.randint(-280, 280))
        fruit.color(fruit_color)

    while True:
        time.sleep(0.12 / len(snake.snake))
        snake.move_snake()
        screen.onkey(fun=snake.turn_left, key="a")
        screen.onkey(fun=snake.turn_right, key="d")

        if snake.snake and snake.snake[0].distance(fruit) < 15:
            points += 1
            total_points += 1
            spawn_fruit()
            snake.add_lenght()
            update_score()

        if snake.game_over():
            break
        screen.update()

    if points > high_score:
        high_score = points

    save_scores()

    screen.clear()
    show_final_screen(points)

def show_final_screen(points):
    global high_score, total_points

    screen.clear()
    screen.bgcolor("black")

    if points > high_score:
        high_score = points
    save_scores()

    title = Turtle()
    title.hideturtle()
    title.color("white")
    title.penup()
    title.goto(0, 100)
    title.write(
        f"Scor final: {points}\nHigh Score: {high_score}\nTotal Puncte: {total_points}",
        align="center",
        font=("Arial", 20, "bold")
    )

    instructions_title = Turtle()
    instructions_title.hideturtle()
    instructions_title.color("white")
    instructions_title.penup()
    instructions_title.goto(0, -50)
    instructions_title.write("Instrucțiuni:", align="center", font=("Arial", 16, "bold"))

    instructions_restart = Turtle()
    instructions_restart.hideturtle()
    instructions_restart.color("white")
    instructions_restart.penup()
    instructions_restart.goto(0, -80)
    instructions_restart.write(
        "Apasa 'r' pentru a reîncepe jocul.",
        align="center",
        font=("Arial", 14, "italic")
    )

    instructions_menu = Turtle()
    instructions_menu.hideturtle()
    instructions_menu.color("white")
    instructions_menu.penup()
    instructions_menu.goto(0, -110)
    instructions_menu.write(
        "Apasa 'b' pentru a reveni la meniu.",
        align="center",
        font=("Arial", 14, "italic")
    )

    screen.listen()
    screen.onkey(show_menu, "b")
    screen.onkey(start_game, "r")

def open_shop():
    global total_points, snake_color, fruit_color

    screen.clear()
    screen.bgcolor("black")

    shop_title = Turtle()
    shop_title.hideturtle()
    shop_title.color("white")
    shop_title.penup()
    shop_title.goto(0, 200)
    shop_title.write(f"Magazinul - Puncte disponibile: {total_points}",
                     align="center", font=("Arial", 20, "bold"))

    instructions = Turtle()
    instructions.hideturtle()
    instructions.color("white")
    instructions.penup()
    instructions.goto(0, 160)
    instructions.write("Apasa pe buton pentru a cumpara o culoare.",
                       align="center", font=("Arial", 14, "italic"))

    instructions_back = Turtle()
    instructions_back.hideturtle()
    instructions_back.color("white")
    instructions_back.penup()
    instructions_back.goto(0, 130)
    instructions_back.write("Apasa 'b' pentru a reveni la meniu.",
                            align="center", font=("Arial", 14, "italic"))

    def buy_snake_color(color):
        global total_points, snake_color
        if total_points >= 10:
            total_points -= 10
            snake_color = color
            save_scores()
            shop_title.clear()
            shop_title.write(f"Magazinul - Puncte disponibile: {total_points}",
                             align="center", font=("Arial", 20, "bold"))
        else:
            error_message("Nu ai suficiente puncte!")

    def buy_fruit_color(color):
        global total_points, fruit_color
        if total_points >= 5:
            total_points -= 5
            fruit_color = color
            save_scores()
            shop_title.clear()
            shop_title.write(f"Magazinul - Puncte disponibile: {total_points}",
                             align="center", font=("Arial", 20, "bold"))
        else:
            error_message("Nu ai suficiente puncte!")

    def display_shop_items():
        snake_colors = ["red", "blue", "green", "yellow"]
        snake_prices = [10, 10, 10, 10]
        for i, (color, price) in enumerate(zip(snake_colors, snake_prices)):
            color_button = Turtle()
            color_button.shape("square")
            color_button.color(color)
            color_button.shapesize(stretch_wid=1.5, stretch_len=5)
            color_button.penup()
            color_button.goto(-200 + (i * 100), 50)
            color_button.onclick(lambda x, y, c=color: buy_snake_color(c))

            price_label = Turtle()
            price_label.hideturtle()
            price_label.color("white")
            price_label.penup()
            price_label.goto(-200 + (i * 100), 80)
            price_label.write(f"{price}p", align="center", font=("Arial", 12, "bold"))

        fruit_colors = ["pink", "orange", "cyan", "purple"]
        fruit_prices = [5, 5, 5, 5]
        for i, (color, price) in enumerate(zip(fruit_colors, fruit_prices)):
            color_button = Turtle()
            color_button.shape("circle")
            color_button.color(color)
            color_button.penup()
            color_button.goto(-200 + (i * 100), -100)
            color_button.onclick(lambda x, y, c=color: buy_fruit_color(c))

            price_label = Turtle()
            price_label.hideturtle()
            price_label.color("white")
            price_label.penup()
            price_label.goto(-200 + (i * 100), -70)
            price_label.write(f"{price}p", align="center", font=("Arial", 12, "bold"))

    def error_message(message):
        error_turtle = Turtle()
        error_turtle.hideturtle()
        error_turtle.color("red")
        error_turtle.penup()
        error_turtle.goto(0, -200)
        error_turtle.write(message, align="center", font=("Arial", 14, "bold"))
        screen.ontimer(lambda: error_turtle.clear(), 2000)

    display_shop_items()

    screen.listen()
    screen.onkey(show_menu, "b")

def exit_game():
    screen.bye()

def show_menu():
    screen.clear()
    screen.bgcolor("black")
    title = Turtle()
    title.hideturtle()
    title.color("white")
    title.penup()
    title.goto(0, 200)
    title.write("Snake Game", align="center", font=("Arial", 30, "bold"))

    play_button = Turtle()
    play_button.shape("square")
    play_button.color("green")
    play_button.shapesize(stretch_wid=1.5, stretch_len=5)
    play_button.penup()
    play_button.goto(0, 50)

    shop_button = Turtle()
    shop_button.shape("square")
    shop_button.color("blue")
    shop_button.shapesize(stretch_wid=1.5, stretch_len=5)
    shop_button.penup()
    shop_button.goto(0, -50)

    exit_button = Turtle()
    exit_button.shape("square")
    exit_button.color("red")
    exit_button.shapesize(stretch_wid=1.5, stretch_len=5)
    exit_button.penup()
    exit_button.goto(0, -150)

    label_turtle = Turtle()
    label_turtle.hideturtle()
    label_turtle.color("white")
    label_turtle.penup()

    label_turtle.goto(0, 70)
    label_turtle.write("Joaca", align="center", font=("Arial", 16, "bold"))

    label_turtle.goto(0, -30)
    label_turtle.write("Magazin", align="center", font=("Arial", 16, "bold"))

    label_turtle.goto(0, -130)
    label_turtle.write("Iesi", align="center", font=("Arial", 16, "bold"))

    def on_click(x, y):
        if -50 <= x <= 50 and 25 <= y <= 75:
            start_game()
        elif -50 <= x <= 50 and -75 <= y <= -25:
            open_shop()
        elif -50 <= x <= 50 and -175 <= y <= -125:
            exit_game()

    screen.onclick(on_click)

screen = Screen()
screen.setup(width=600, height=600)
show_menu()
screen.mainloop()
