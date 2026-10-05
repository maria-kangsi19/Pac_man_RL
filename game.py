
import random, sys


SIZE = 10                                 
START_PAC, START_GHOST = (0, 0), (9, 9)
START_PELLETS = ((0, 9), (9, 0), (4, 4), (2, 7), (7, 2), (5, 5))  
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
MAX_STEPS = 120                            

def clamp(p):
    
    return (min(max(p[0], 0), SIZE - 1), min(max(p[1], 0), SIZE - 1))

def new_game():
   
    return (START_PAC, START_GHOST, START_PELLETS)

def step(state, action):
    
    pac, ghost, pellets = state
    pac = clamp((pac[0] + MOVES[action][0], pac[1] + MOVES[action][1]))
    reward = -1                                   

    if pac in pellets:                             
        pellets = tuple(p for p in pellets if p != pac)
        reward += 10
    if pac == ghost:                              
        return (pac, ghost, pellets), reward - 50, True
    if not pellets:                                 
        return (pac, ghost, pellets), reward + 50, True

    ghost = clamp(random.choice([(ghost[0] + dr, ghost[1] + dc) for dr, dc in MOVES]))
    if pac == ghost:                               
        return (pac, ghost, pellets), reward - 50, True
    return (pac, ghost, pellets), reward, False

Q = {}                                            
ALPHA, GAMMA = 0.1, 0.95                            

def q(state):
    if state not in Q:
        Q[state] = [0.0] * 4                       
    return Q[state]

def choose_action(state, epsilon):
    if random.random() < epsilon:                   
        return random.randrange(4)
    values = q(state)                               
    best = max(values)
    return random.choice([a for a in range(4) if values[a] == best])

def learn(state, action, reward, next_state, game_over):
     
    future = 0 if game_over else max(q(next_state))
    target = reward + GAMMA * future
    q(state)[action] += ALPHA * (target - q(state)[action])  

def play_episode(epsilon, training=True):
    state, total = new_game(), 0
    for _ in range(MAX_STEPS):
        action = choose_action(state, epsilon)
        next_state, reward, over = step(state, action)
        if training:
            learn(state, action, reward, next_state, over)
        state, total = next_state, total + reward
        if over: break
    return total, (not state[2]) and state[0] != state[1]     

def train(episodes=60000):
    for ep in range(1, episodes + 1):
        epsilon = max(0.05, 1 - ep / (episodes * 0.7))        
        play_episode(epsilon)
        if ep % 5000 == 0:
            wins = sum(play_episode(0, training=False)[1] for _ in range(200))
            print(f"game {ep:6d} | win rate when playing greedily: {wins/2:.0f}%")


def show():
    import pygame
    pygame.init()
    C = 50                                
    screen = pygame.display.set_mode((SIZE * C, SIZE * C))
    pygame.display.set_caption("Pac-Man Q-learning")
    clock = pygame.time.Clock()
    while True:
        state = new_game()
        for _ in range(MAX_STEPS):
            for e in pygame.event.get():
                if e.type == pygame.QUIT: return
            pac, ghost, pellets = state
            screen.fill((10, 10, 40))
            for p in pellets:
                pygame.draw.circle(screen, (255, 255, 255), (p[1]*C + C//2, p[0]*C + C//2), 5)
            pygame.draw.circle(screen, (255, 220, 0), (pac[1]*C + C//2, pac[0]*C + C//2), C//2 - 4)
            pygame.draw.rect(screen, (255, 60, 60), (ghost[1]*C + 8, ghost[0]*C + 8, C - 16, C - 16), border_radius=10)
            pygame.display.flip(); clock.tick(6)
            state, _, over = step(state, choose_action(state, 0))  
            if over: break
        pygame.time.wait(700)

if __name__ == "__main__":
    train()
    if "--no-gui" not in sys.argv:
        show()