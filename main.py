from graphics import Canvas
import time
import random
import math

#game settings
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 500
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 20
BALL_SIZE = 25
PADDLE_MOVE_SPEED = 12
BALL_SPEED = 3
DELAY = 0.002
LIVES = 3

#fireworks
PARTICLES_PER_FIREWORK = 20
FIREWORK_GROUPS = 6
GRAVITY = 0.12
FRAME_DELAY = 0.02
GLOW_COLORS = [
    "#ff66cc", "#ffcc00", "#00ffff", "#66ff66",
    "#ff6666", "#99ccff", "#ff9933", "#ff00ff",
    "#ccff66", "#33ffff"
]

def draw_neon_grid_background(canvas):
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color="#000011")
    line_color = "#003366"
    for x in range(0, CANVAS_WIDTH, 25):
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, color=line_color)
    for y in range(0, CANVAS_HEIGHT, 25):
        canvas.create_line(0, y, CANVAS_WIDTH, y, color=line_color)

def wait_for_start(canvas):
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color="#0f0f1a")
    draw_neon_grid_background(canvas)
    canvas.create_text(CANVAS_WIDTH/2, 150, text="GRID BREAKER", font="Courier", font_size=64, color="#D9C1FD", anchor='center')
    canvas.create_text(CANVAS_WIDTH/2, 220, text="Press 'A' to Launch", font="Courier", font_size=22, color="#D9C1FD", anchor='center')
    canvas.create_text(CANVAS_WIDTH/2, 450, text="Use 'A' and 'L' to Move Paddle", font="Courier", font_size=18, color="#FBFAFC", anchor='center')
    while True:
        keys = canvas.get_new_key_presses()
        if 'a' in keys or 'A' in keys:
            break
        time.sleep(0.01)

def create_bricks(canvas):
    bricks = []
    for row in range(5):
        for col in range(10):
            x = col * (60 + 10) + 20
            y = 60 + row * (25 + 10)
            brick = canvas.create_rectangle(x-12, y, x + 48, y + 25, "#ffcc66")
            bricks.append(brick)
    return bricks

def launch_firework(canvas, x, y):
    particles = []
    for _ in range(PARTICLES_PER_FIREWORK):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        color = random.choice(GLOW_COLORS)
        size = random.randint(4, 6)
        particle = {
            'id': canvas.create_oval(x, y, x+size, y+size, color=color),
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy,
            'trail': []
        }
        particles.append(particle)

    for _ in range(30):
        for p in particles:
            p['dy'] += GRAVITY
            p['x'] += p['dx']
            p['y'] += p['dy']
            canvas.moveto(p['id'], p['x'], p['y'])

            if len(p['trail']) >= 4:
                canvas.delete(p['trail'].pop(0))
            trail = canvas.create_oval(p['x'], p['y'], p['x']+2, p['y']+2, color="#ffffff")
            p['trail'].append(trail)
        time.sleep(FRAME_DELAY)

    for p in particles:
        canvas.delete(p['id'])
        for t in p['trail']:
            canvas.delete(t)

def firework_preview():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color="black")
    canvas.create_text(CANVAS_WIDTH/2, 250, text="You won!", font="Courier", font_size=20, color="#ffffcc", anchor='center')

    for _ in range(FIREWORK_GROUPS):
        fireworks_in_batch = random.randint(2, 3)
        coords = []
        for _ in range(fireworks_in_batch):
            x = random.randint(80, CANVAS_WIDTH - 80)
            y = random.randint(80, CANVAS_HEIGHT - 150)
            coords.append((x, y))

        for x, y in coords:
            launch_firework(canvas, x, y)
        time.sleep(0.3)


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    wait_for_start(canvas)
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color="#0f0f1a")
    draw_neon_grid_background(canvas)

    paddle = canvas.create_rectangle(290, 450, 290 + PADDLE_WIDTH, 450 + PADDLE_HEIGHT, "#00ffc3")
    ball = canvas.create_oval(340, 300, 340 + BALL_SIZE, 300 + BALL_SIZE, "#ff5e5e")
    bricks = create_bricks(canvas)

    score = 0
    lives = LIVES
    score_text = canvas.create_text(10, 10, text=f"Score: {score}", anchor='nw', font='Courier', font_size=18, color="#ffff66")
    lives_text = canvas.create_text(CANVAS_WIDTH - 100, 10, text=f"Lives: {lives}", anchor='nw', font='Courier', font_size=18, color="#66ccff")

    dx = BALL_SPEED
    dy = -BALL_SPEED

    while True:
        canvas.move(ball, dx, dy)
        x = canvas.get_left_x(ball)
        y = canvas.get_top_y(ball)
        ball_right = x + BALL_SIZE
        ball_bottom = y + BALL_SIZE

        if x <= 0 or ball_right >= CANVAS_WIDTH:
            dx = -dx
        if y <= 0:
            dy = -dy

        keys = canvas.get_new_key_presses()
        if 'a' in keys or 'A' in keys:
            canvas.move(paddle, -PADDLE_MOVE_SPEED, 0)
        if 'l' in keys or 'L' in keys:
            canvas.move(paddle, PADDLE_MOVE_SPEED, 0)

        paddle_x = canvas.get_left_x(paddle)
        paddle_y = canvas.get_top_y(paddle)
        paddle_right = paddle_x + PADDLE_WIDTH
        paddle_bottom = paddle_y + PADDLE_HEIGHT

        if (ball_bottom >= paddle_y and y <= paddle_bottom and
            ball_right >= paddle_x and x <= paddle_right):
            dy = -abs(dy)
            paddle_center = paddle_x + PADDLE_WIDTH / 2
            ball_center = x + BALL_SIZE / 2
            dx = (ball_center - paddle_center) / 10

        hit = None
        for brick in bricks:
            bx = canvas.get_left_x(brick)
            by = canvas.get_top_y(brick)
            brick_right = bx + 60
            brick_bottom = by + 25
            if (ball_right >= bx and x <= brick_right and
                ball_bottom >= by and y <= brick_bottom):
                hit = brick
                break

        if hit:
            canvas.delete(hit)
            bricks.remove(hit)
            dy = -dy
            score += 5
            canvas.delete(score_text)
            score_text = canvas.create_text(10, 10, text=f"Score: {score}", anchor='nw', font='Courier', font_size=18, color="#ffff66")

        if ball_bottom >= CANVAS_HEIGHT:
            lives -= 1
            canvas.delete(lives_text)
            lives_text = canvas.create_text(CANVAS_WIDTH - 100, 10, text=f"Lives: {lives}", anchor='nw', font='Courier', font_size=18, color="#66ccff")
            canvas.delete(ball)
            ball = canvas.create_oval(340, 300, 340 + BALL_SIZE, 300 + BALL_SIZE, "#ff5e5e")
            dx = BALL_SPEED
            dy = -BALL_SPEED
            if lives == 0:
                break

        if not bricks:
            firework_preview()
            return

        time.sleep(DELAY)
    draw_neon_grid_background(canvas)
    canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, text="GAME OVER!", font="Courier", font_size=36, color="#ff3366", anchor='center')

if __name__ == '__main__':
    main()
