import pygame
import random
import math
import time

pygame.init()
mode = ""
WIDTH, HEIGHT = 800, 400
# create a grid somehow
cell_x = 0
cell_y = 0
grid = []

while cell_x <= 780:
    while cell_y <= 380:
        new_cell = {"x": cell_x, "y": cell_y, "occupied": False}
        grid.append(new_cell)
        cell_y += 20
    cell_y = 0
    cell_x += 20



win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Fight Game")
numObstacles = random.randint(30, 40)
obstacles = []
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
WEAPONS = {
    "block": {"type": "melee", "damage": 10, "range": 80},
    "gun": {"type": "shooting", "damage": 5},
    "shield": {"type": "blocking", "damage": 0},
}
DIRECITONS = {
    "right": (20, 9),
    "down": (9, 20),
    "left": (-20, 9),
    "up": (9, -20),
    "up-left": (-9, -20),
    "up-right": (-9, -20),
    "down-left": (9, 20),
    "down-right": (9, 20),
}
VECTORS = {
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
    "up": (0, -1),
    "up-left": (-1, -1),
    "up-right": (1, -1),
    "down-left": (-1, 1),
    "down-right": (1, 1),
}

projectiles = []


class Player:
    def __init__(
        self,
        name,
        health,
        x,
        y,
        color,
        attacking,
        attack_length,
        attack_speed,
        MaxLength,
        returning,
        direction,
        dash,
        dash_timer,
        dash_cooldown,
        weapon_type,
        has_hit,
        dash_direction,
        ammo,
        attack_timer,
        is_ai,
        heal_cooldown,
        path,
        shoot_timer,
        shield,
        shield_timer,
        shield_cooldown,
        a_star_timer,
        retreating
    ):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = color
        self.attacking = False
        self.attack_length = 0
        self.attack_speed = attack_speed
        self.Maxlength = MaxLength
        self.returning = False
        self.direction = direction
        self.dash = False
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.weapon_type = "block"
        self.has_hit = False
        self.dash_direction = dash_direction
        self.ammo = ammo
        self.attack_timer = attack_timer
        self.is_ai = False
        self.heal_cooldown = heal_cooldown

        self.path = path
        self.shoot_timer = shoot_timer
        self.shield = False
        self.shield_timer = shield_timer
        self.shield_cooldown = shield_cooldown
        self.a_star_timer = a_star_timer
        self.retreating = False



    def attack(self):

        if not self.attacking and self.health and not self.returning > 0:
            self.attack_timer = 20
            if self.weapon_type == "block":
                self.attacking = True

            elif (
                self.weapon_type == "gun"
                and self.ammo > 0
                and self.shoot_timer <= 0
            ):
                self.shoot_timer = 20
                self.ammo -= 1
                kx, ky = DIRECITONS[self.direction]
                vx, vy = VECTORS[self.direction]
                weapon_x = self.x + kx
                weapon_y = self.y + ky
                if self.weapon_type == "gun":

                    new_bullet = {
                        "x": weapon_x,
                        "y": weapon_y,
                        "x_direction": vx,
                        "y_direction": vy,
                        "owner": self,
                    }

                projectiles.append(new_bullet)

    def movement(self, Xvelocity, Yvelocity):

        vx, vy = VECTORS[self.dash_direction]
        if self.dash:
            Xvelocity = 60 * vx
            Yvelocity = 60 * vy
        if self.health > 0 and self.x+Xvelocity >= 0 and self.x+Xvelocity <= 780 and self.y+Yvelocity >= 0 and self.y+Yvelocity <= 380:

            self.x += Xvelocity
            self.y += Yvelocity
        player_rect = pygame.Rect(self.x, self.y, 20, 20)
        for obstacle in obstacles:

            obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], 20, 20)
            if player_rect.colliderect(obstacle_rect):

                self.x -= Xvelocity
                self.y -= Yvelocity

    def draw_bullet(self):

        for projectile in projectiles:

            bullet = pygame.Rect(projectile["x"], projectile["y"], 10, 10)

            pygame.draw.rect(win, (0, 255, 0), bullet)

    def draw(self, win):
        if self.health > 0:
            player1 = pygame.transform.scale(
                (pygame.image.load("/home/charles/square_game/Skware.png")),
                (20, 20),
            )

            win.blit(player1, (self.x, self.y))

            HealthBar_rect = pygame.Rect(self.x, self.y + 70, 100, 10)
            Damage_rect = pygame.Rect(
                self.x, self.y + 70, 100 - self.health, 10
            )
            kx, ky = DIRECITONS[self.direction]
            vx, vy = VECTORS[self.direction]
            weapon_x = self.x + kx + (vx * self.attack_length)
            weapon_y = self.y + ky + (vy * self.attack_length)

            if self.weapon_type == "block":
                Weapon_rect = pygame.Rect(weapon_x, weapon_y, 20, 20)

            elif self.weapon_type == "gun":
                if self.direction == "right" or self.direction == "left":
                    Weapon_rect = pygame.Rect(
                        weapon_x - (vx * self.attack_length),
                        weapon_y - (vy * self.attack_length),
                        30,
                        10,
                    )
                    self.draw_bullet()
                elif self.direction == "up" or self.direction == "down":
                    Weapon_rect = pygame.Rect(
                        weapon_x - (vx * self.attack_length),
                        weapon_y - (vy * self.attack_length),
                        10,
                        30,
                    )
            elif self.weapon_type == "shield":

                Weapon_rect = pygame.Rect(
                    (self.x + 4 * (vx)), self.y + 4 * (vy), 20, 20
                )
            pygame.draw.rect(win, self.color, Weapon_rect)

            pygame.draw.rect(win, (0, 255, 0), HealthBar_rect)
            pygame.draw.rect(win, (255, 0, 0), Damage_rect)

    def take_damage(self, amount):

        if self.health <= 0:
            print("you has died")
        else:
            if self.shield == False:
                self.health -= amount
            else:
                self.health -= amount * (0.3)

    def heal(self, amount):
        if self.health < 100 and self.heal_cooldown == 0:
            self.health += amount
            self.heal_cooldown = 300

    def update_heal(self):
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        else:
            self.heal_cooldown = 0

    # Bullets should be independent entities after being shot
    def update_shoot(self, enemy):

        if self.shoot_timer > 0:
            self.shoot_timer -= 1

        enemy_rect = pygame.Rect(enemy.x, enemy.y, 20, 20)

        for projectile in projectiles:
            projectile["x"] += projectile["x_direction"] * 3
            projectile["y"] += projectile["y_direction"] * 3
            bullet_rect = pygame.Rect(projectile["x"], projectile["y"], 10, 10)
            if (
                bullet_rect.colliderect(enemy_rect)
                and projectile["owner"] == self
            ):

                enemy.take_damage(5)
                projectiles.remove(projectile)
            if (
                projectile["x"] > WIDTH
                or projectile["x"] < 0
                or projectile["y"] >= HEIGHT
                or projectile["y"] <= 0
            ):
                projectiles.remove(projectile)

    def update_attack(self, enemy):
    
        self.attack_timer -= 1
        amount = WEAPONS[self.weapon_type]["damage"]
        kx, ky = DIRECITONS[self.direction]
        vx, vy = VECTORS[self.direction]
        weapon_x = self.x + kx + (vx * self.attack_length)
        weapon_y = self.y + ky + (vy * self.attack_length)
        weapon_rect = pygame.Rect(weapon_x, weapon_y, 20, 20)

        if self.attacking and WEAPONS[self.weapon_type]["type"] == "melee":
        
            self.attack_length += 10
            # MELEE ATTACK RATE: 7

            if self.attack_length >= self.Maxlength:
                self.returning = True
                self.attacking = False

            enemy_rect = pygame.Rect(enemy.x, enemy.y, 20, 20)

            if weapon_rect.colliderect(enemy_rect) and self.has_hit == False:

                self.has_hit = True
                enemy.x += vx * 20
                enemy.y += vy * 20

                for obstacle in obstacles:

                    obstacle_rect = pygame.Rect(
                        obstacle["x"], obstacle["y"], 20, 20
                    )
                    if enemy_rect.colliderect(obstacle_rect):

                        enemy.x -= vx * 20
                        enemy.y -= vy * 20

                enemy.take_damage(amount)
                enemy.show()
                print("takes damage")

        elif self.returning:
  
            self.attack_length -= 5
            self.attacking = False

            if self.attack_length <= 0:
             
                self.attack_length = 0
                self.returning = False
                self.has_hit = False

    def show(self):
        print("Your current health is " + str(self.health))

    def update_dash(self):

        if self.dash_timer > 0:

            self.dash_timer -= 1

            self.dash = False
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.dash == True:
            if self.dash_direction != self.direction:

                self.dash = False

        # overwrite!

    def shielding(self):
        if not self.shield and self.shield_cooldown == 0:
            self.shield = True
            self.shield_cooldown = 300

    def update_shield(self):
        if self.shield:
            self.weapon_type = "shield"
            if self.shield_timer > 0:
                self.shield_timer -= 1

            else:
                self.shield = False

                self.weapon_type = "block"
                self.shield_timer = 60
        else:
            if self.shield_cooldown > 0:
                self.shield_cooldown -= 1
            elif self.shield_cooldown <= 0:
                self.shield_cooldown = 0


def draw_menu():
    font = pygame.font.Font(None, 30)
    title = font.render("Press e for PvE or p for PvP", True, (255, 0, 0))
    win.blit(title, (200, 100))


def die():

    if P.health <= 0:
        death_text = font.render(
            (str(P2.name) + " has won"), True, (255, 0, 0)
        )
    elif P2.health <= 0:
        death_text = font.render((str(P.name) + " has won"), True, (255, 0, 0))
    win.blit(death_text, (0, 0))


def displays(type, value, color, asset, displayX, displayY):
    font = pygame.font.Font(None, 24)
    if type == "cooldown":
        seconds = value // 60

        text = font.render((asset + "cooldown: " + str(seconds)), True, color)
    elif type == "ammo":
        text = font.render((asset + ": " + str(value)), True, color)

    win.blit(text, (displayX, displayY))


game_state = "menu"


def P2_inputs():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        P2.movement(-20, 0)
        P2.direction = "left"
    if keys[pygame.K_RIGHT]:
        P2.movement(20, 0)

        P2.direction = "right"

    if keys[pygame.K_UP]:
        P2.direction = "up"

        P2.movement(0, -20)
    if keys[pygame.K_DOWN]:
        P2.movement(0, 20)

        P2.direction = "down"
    if keys[pygame.K_KP_ENTER]:
        P2.weapon_type = "gun"
    if keys[pygame.K_RCTRL]:
        P2.weapon_type = "block"
    if keys[pygame.K_RETURN]:
        P2.shielding()
    if keys[pygame.K_RALT]:
        if P2.health <= 90:
            P2.heal(10)
        else:
            P2.heal(100 - P2.health)
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3 and P2.dash_cooldown == 0:

            P2.dash = True
            P2.dash_timer = 60
            P2.dash_direction = P2.direction
            P2.dash_cooldown = 600


def mouse_inputs():
    mx, my = pygame.mouse.get_pos()
    dx = mx - P.x
    dy = my - P.y
    if abs(dx) > abs(dy):

        P.direction = "right" if dx > 0 else "left"
    else:
        P.direction = "down" if dy > 0 else "up"


run = True


def a_star(grid, x, y, target_x, target_y):
  
       
    if (x, y) == (target_x, target_y):
        
        return None

    directions = {
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0),
        "up": (0, -1),
        "up-left": (-1, -1),
        "up-right": (1, -1),
        "down-left": (-1, 1),
        "down-right": (1, 1),
    }
    start_x = x
    start_y = y
    open_list = []
    closed_list = []
    path = []
    start_node = {
        "f": 0,
        "g": 0,
        "h": 0,
        "position": (start_x, start_y),
        "parent": None,
    }

    current = start_node
    
    iterations = 0
    while (x, y) != (target_x, target_y):
        iterations +=1
        for direction in directions:
           
            vx, vy = directions[direction]
         
            for cell in grid:
               
                # is this the cell we are searching for?
                
                if cell["x"] == (vx * 20) + x and cell["y"] == (vy * 20) + y:

                    # check if cell is valid
                    if (
                        cell["occupied"] == False
                        and 0 <= x + (vx * 20) <= 780
                        and 0 <= y + (vy * 20) <= 380
                    ):
                        
                    
                
                        
                        # taking the info of the neighbors
                        h = math.sqrt(
                            (target_x - (x + (vx * 20))) ** 2
                            + (target_y - (y + (vy * 20))) ** 2
                        )
                        if (
                            direction == "up"
                            or direction == "down"
                            or direction == "left"
                            or direction == "right"
                        ):
                            neighbor_g = current["g"] + 20
                        else:
                            neighbor_g = current["g"] + 20 * (math.sqrt(2))
                        f = neighbor_g + h

                        # remembering the parent for path reconstruction
                        neighbor_cell = {
                            "f": f,
                            "h": h,
                            "g": neighbor_g,
                            "position": (x + (vx * 20), y + (vy * 20)),
                            "parent": current,
                        }

                        if not any(
                            node["position"] == neighbor_cell["position"]
                            for node in closed_list
                        ) and not any(
                            node["position"] == neighbor_cell["position"]
                            for node in open_list
                        ):

                            open_list.append(neighbor_cell)

        
        lowest_f_index = 0
        
        for i in range(len(open_list)):
            # check f value to see lowest one, exploring the open list
            if open_list[i]["f"] < open_list[lowest_f_index]["f"]:
                lowest_f_index = i
        
        
        # remember this value, don't explore it again

        if len(open_list) > 0:

            x, y = open_list[lowest_f_index]["position"]

            
            closed_list.append(open_list[lowest_f_index])
          
            
            current = open_list[lowest_f_index]
          
            open_list.pop(lowest_f_index)

        else:
         
           
            return None
        # might search again, but we have the info of the cells
    # ending the search

    if closed_list:
        t2 = time.perf_counter() 
        C = closed_list[-1]

        while (C["position"]) != (start_x, start_y):
            path.append(C)
            C = C["parent"]
        path.reverse()


      
        #Every costly calculation is none
      
        return path 
    else:
        
        return None
def Path_follow():
    if P2.path and P2.path[0]["position"] != (P.x, P.y) and P2.retreating == False:
                
                                        next_node = P2.path[0]
                
                                        Tx, Ty = next_node["position"]
                
                                        
                                        if abs(Tx - P2.x) <= 5 and abs(Ty - P2.y) <= 0:
                
                                            P2.path.pop(0)
                                        else:
                                            if Tx >= P2.x:
                                                if Tx != P2.x:
                                                    if Ty > P2.y:
                                                        P2.direction = "down-right"
                
                                                    elif Ty < P2.y:
                                                        P2.direction = "up-right"
                
                                                    else:
                                                        P2.direction = "right"
                
                                                else:
                                                    if Ty > P2.y:
                                                        P2.direction = "down"
                                                    else:
                                                        P2.direction = "up"
                
                                            else:
                                                if Ty > P2.y:
                                                    P2.direction = "down-left"
                
                                                elif Ty < P2.y:
                                                    P2.direction = "up-left"
                
                                                else:
                                                    P2.direction = "left"

P = Player(
    "Player_Name",
    100,
    0,
    0,
    "red",
    False,
    20,
    5,
    80,
    False,
    "right",
    False,
    0,
    0,
    "block",
    False,
    "right",
    100,
    60,
    False,
    0,
    [],
    20,
    False,
    60,
    0,
    0,
    False
)

P2 = Player(
    "Player 2",
    100,
    0,
    0,
    "green",
    False,
    20,
    5,
    80,
    False,
    "left",
    False,
    0,
    0,
    "block",
    False,
    "right",
    100,
    60,
    False,
    0,
    [],
    20,
    True,
    60,
    0,
    0,
    False
)






while run:

    win.fill((0, 0, 0))

    if game_state == "menu":
        draw_menu()

    clock.tick(60)


    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        if game_state == "menu":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:

                    mode = "PvE"
                    P2.is_ai = True

                    game_state = "playing"
                elif event.key == pygame.K_p:
                    mode = "PvP"

                    game_state = "playing"
                obstacles = []
                for store_obstacles in range(numObstacles):
                        
                                            obstaclex, obstacley = random.randint(
                                                3, 40
                                            ), random.randint(3, 20)
                                            obstacle_rect = {
                                                "x": obstaclex * 20,
                                                "y": obstacley * 20,
                                                "length": 20,
                                                "width": 20,
                                            }
                                            obstacles.append(obstacle_rect)
                                            for grid_cell in grid:
                                                if (
                                                    grid_cell["x"] == obstacle_rect["x"]
                                                    and grid_cell["y"] == obstacle_rect["y"]
                                                ):
                        
                                                    grid_cell["occupied"] = True
                

        if game_state == "playing":
            
            
         
                
               

        
            if P.health <= 0 or P2.health <= 0:
                game_state = "death"
            if event.type == pygame.KEYDOWN:
        
                
                if event.key == pygame.K_1:
                    P.weapon_type = "block"
                if event.key == pygame.K_2:
                    P.weapon_type = "gun"
                if event.key == pygame.K_3:
                     P.shielding()
                if event.key == pygame.K_LSHIFT:

                    P.attack()

                if event.key == pygame.K_SPACE:
                    P.heal(10)
                    P.heal_cooldown = 300

                if event.key == pygame.K_RSHIFT and mode == "PvP":

                    P2.attack()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and P.dash_cooldown == 0:
                    P.dash = True
                    P.dash_direction = P.direction
                    P.dash_timer = 60
                    P.dash_cooldown = 600
            


  
    # stuff that runs every frame while playing
    if game_state == "playing":
        P.draw(win)
        P2.draw(win)
        # UI displays for in game.
        font = pygame.font.Font(None, 30)
        fps_text = font.render(
                       f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255)
                    )
        win.blit(fps_text, (10, 10))
        for obstacle in obstacles:
                        draw_obstacle = pygame.Rect(obstacle["x"], obstacle["y"], 20, 20)
                        pygame.draw.rect(win, (128, 128, 128), draw_obstacle)
        
        if P.shield_cooldown > 0:
                        displays("cooldown", P.shield_cooldown, P.color, "shield ", 20, 20)
        if P.dash_cooldown > 0:
                       displays("cooldown", P.dash_cooldown, P.color, "dash ", 20, 40)
        if P2.shield_cooldown > 0:
        
                       displays(
                          "cooldown", P2.shield_cooldown, P2.color, "shield ", 550, 20
                     )
        if P2.dash_cooldown > 0:
                       displays("cooldown", P2.dash_cooldown, P2.color, "dash ", 550, 40)
        if P.heal_cooldown > 0:
                       displays("cooldown", P.heal_cooldown, P.color, "healing ", 20, 60)
        if P2.heal_cooldown > 0:
                       displays(
                          "cooldown", P2.heal_cooldown, P2.color, "healing ", 550, 60
                     )
        displays("ammo", P.ammo, P.color, "ammo", 20, 350)
        displays("ammo", P2.ammo, P2.color, "ammo", 600, 350)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
        
                        P.movement(-20, 0)
        
                        P.direction = "left"
        if keys[pygame.K_d]:
            P.movement(20, 0)
        
            P.direction = "right"
        if keys[pygame.K_w]:
        
                        P.movement(0, -20)
                        P.direction = "up"
        if keys[pygame.K_s]:
        
                        P.direction = "down"
                        P.movement(0, 20)
        if mode == "PvP":
            P2_inputs()
        elif mode == "PvE":
            vx, vy = VECTORS[P2.direction]
             
            mx = vx * 20
            my = vy * 20
            P2.movement(mx, my)
            mouse_inputs()
            #   A*STAR PATHFINDING FOR P2
         
            
            if P2.a_star_timer <= 0 and P2.retreating == False:
              
                P2.path = a_star(grid, P2.x, P2.y, P.x, P.y)

         
                 
   
                P2.a_star_timer = 30
            else:
                if P2.a_star_timer > 0:
                    P2.a_star_timer -= 1
            
            if P2.path:
                Path_follow()
            
            
                                        # P2 dash in PvE
            if P2.path and len(P2.path) > 1:
                                            nodes_in_line = 0
                                            firstX, firstY = P2.path[0]["position"]
                                            secondX, secondY = P2.path[1]["position"]
                                            if (
                                                abs(secondX - firstX) <= 10
                                               or abs(secondY - firstY) <= 10
                                            ):
                                                nodes_in_line = 2
            
                                                for node in range(2, len(P2.path)):
                                                    nodeX, nodeY = P2.path[node]["position"]
                                                    if abs(secondX - firstX) <= 20:
            
                                                        if nodeX == firstX:
                                                            nodes_in_line += 1
                                                    else:
                                                        if nodeY == firstY:
                                                            nodes_in_line += 1
            
                                            if nodes_in_line >= 5:
                                                P2.dash_cooldown = 300
                                                P2.dash_timer = 60
                                                P2.dash_direction = P2.direction
                                                P2.dash = True
        if P2.health <= 50:
             P2.retreating = True
        #if P2.retreating == True:
         #    xTarget = 400 if P.x <= 200 else 0
          #   yTarget = 800 if P.y <= 400 else 0
           #  print(xTarget, yTarget)
            # if P2.a_star_timer <= 0:
             #     P2.a_star_timer = 30
              #    P2.path = a_star(grid,P2.x,P2.y,xTarget,yTarget)
             #else:
              #      if P2.a_star_timer > 0:
               #          P2.a_star_timer -= 1
      
     #        if P2.path:
      #            Path_follow()
       #      if P2.health >= 80:
        #          P2.retreating = False
         #    if P2.heal_cooldown == 0:
          #        P2.heal(10)
        if abs(P2.x - P.x) <= 20 and abs(P2.y - P.y) <= 20:
            P2.attack()
             
        P.update_heal()
        P2.update_heal()
        P.update_attack(P2)
        P2.update_attack(P)
        P.update_dash()
        P2.update_dash()
  
        P.update_shoot(P2)
        P2.update_shoot(P)
        P.draw_bullet()
        P.update_shield()
        P2.update_shield()
    if game_state == "death":
        die()

    pygame.display.update()

pygame.quit()