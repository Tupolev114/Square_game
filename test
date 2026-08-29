import pygame
import random
pygame.init()
mode = ""
WIDTH, HEIGHT = 800, 400
# create a grid somehow
cell_x = 0
cell_y = 0
grid = []
while cell_x <= 780:
    while cell_y <= 380:
        new_cell = {
          "x": cell_x,
          "y": cell_y,
          "occupied": False
        }
        grid.append(new_cell)
        cell_y += 20
    cell_y = 0 
    cell_x += 20
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Fight Game")
numObstacles = random.randint(10,15)
obstacles = []
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
WEAPONS ={
    "block":{
    "type":"melee",
    "damage":10,
    "range":80},
    "gun":{
    "type":"shooting",
    "damage":5
    }}
DIRECITONS = {
    "right": (50, 15),
    "down": (15, 50),
    "left": (-20, 15),
    "up": (15, -20)
}
VECTORS = {
  "right": (1,0),

 
    "down": (0,1),
    
    "left": (-1,0),
  
    "up": (0,-1),
   
   
   

    "left": (-1,0),
    "down": (0,1),


}

projectiles = []
class Player:
    def __init__ (    
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
        self.weapon_type  = "block"
        self.has_hit = False
        self.dash_direction = dash_direction
        self.ammo = ammo
        self.attack_timer = attack_timer
        self.is_ai = False
        self.heal_cooldown = heal_cooldown
        self.path = path
    
        
    def Dont_go_offscreen_plz(self):
        if self.x < 0 or self.x > 780 or self.y < 0 or self.y > 380:
            if self.x < 0:
                    self.x = 0
                
            elif self.x > 780:
                    self.x = 780
            if self.y > 380:
                    self.y = 380
            elif self.y <0:
                    self.y = 0
         
      

        
    def Dont_go_offscreen_plz(self):
        if self.x < 30 or self.x > 730 or self.y < 30 or self.y > 350:
            if self.x < 30:
                    self.x = 30
                
            elif self.x > 730:
                    self.x = 730
            if self.y > 350:
                    self.y = 350
            elif self.y <30:
                    self.y = 30

            
    def attack(self):
    
     if not self.attacking and self.health and not self.returning> 0:
        self.attack_timer = 20
        if self.weapon_type == "block":
            self.attacking = True
           
        elif self.weapon_type == "gun" and self.ammo > 0:
            self.ammo -=1
            kx,ky=DIRECITONS[self.direction]
            vx,vy = VECTORS[self.direction]
            weapon_x = self.x + kx 
            weapon_y = self.y+ky 
            if self.weapon_type == "gun":
              
                new_bullet= {
                "x": weapon_x,
                "y":weapon_y,
                "x_direction":vx,
                "y_direction":vy,
                "owner":self
            }
            
            projectiles.append(new_bullet)
         
            

    def movement(self, Xvelocity, Yvelocity):
      
       
        if self.health > 0:

            self.x += Xvelocity
            self.y += Yvelocity
        player_rect = pygame.Rect(self.x,self.y,50,50)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle["x"],obstacle["y"],20,20)
            if player_rect.colliderect(obstacle_rect):
             
                self.x -=Xvelocity
                self.y -=Yvelocity
      
 
    
            
    def draw_bullet(self):
       
   
        for projectile in projectiles:
    
            bullet = pygame.Rect(projectile["x"],projectile["y"],10,10)
        
            pygame.draw.rect(win,(0,255,0),bullet)
            
    def draw(self, win):
        if self.health > 0:

            player1 = pygame.transform.scale((pygame.image.load('/home/charles/square_game/Skware.png')),(50,50))

       

            
            win.blit(player1,(self.x,self.y))

            HealthBar_rect = pygame.Rect(self.x, self.y + 70, 100, 10)
            Damage_rect = pygame.Rect(self.x, self.y + 70, 100 - self.health, 10)
            kx,ky=DIRECITONS[self.direction]
            vx,vy = VECTORS[self.direction]
            weapon_x = self.x + kx + (vx*self.attack_length)
            weapon_y = self.y+ky + (vy*self.attack_length)
            if self.weapon_type == "block":
                    Weapon_rect = pygame.Rect(
                    weapon_x,weapon_y, 20, 20
                )
                    
            elif self.weapon_type == "gun":
                if self.direction == "right" or self.direction == "left":
                    Weapon_rect = pygame.Rect(weapon_x-(vx*self.attack_length),weapon_y-(vy*self.attack_length),30,10)
                    self.draw_bullet()
                elif self.direction == "up" or self.direction == "down":
                    Weapon_rect = pygame.Rect(weapon_x-(vx*self.attack_length),weapon_y-(vy*self.attack_length),10,30)
            pygame.draw.rect(win, self.color, Weapon_rect)
            
            pygame.draw.rect(win, (0, 255, 0), HealthBar_rect)
            pygame.draw.rect(win, (255, 0, 0), Damage_rect)

    def take_damage(self, amount):
        
        if self.health <= 0:
            print("you has died")
        else:
            self.health -= amount

    def heal(self, amount):
        if self.health < 100 and self.heal_cooldown ==0:
            self.health += amount
    def update_heal(self):
         if self.heal_cooldown > 0:
              self.heal_cooldown -= 1
           
   
# Bullets should be independent entities after being shot
    def update_shoot(self, enemy):

       
        
         enemy_rect = pygame.Rect(enemy.x,enemy.y,50,50)
        
                       
            
         for projectile in projectiles:
                projectile["x"] += projectile["x_direction"]*3
                projectile["y"] += projectile["y_direction"]*3
                bullet_rect = pygame.Rect(projectile["x"],projectile["y"],10,10)
                if bullet_rect.colliderect(enemy_rect) and projectile["owner"] == self:
                  
                  enemy.take_damage(5)
                  projectiles.remove(projectile)
                if projectile["x"]>WIDTH or projectile["x"]<0 or projectile["y"]>= HEIGHT or projectile["y"]<=0:
                    projectiles.remove(projectile)
                
            
            
            
            
                
                
           
                    

    def update_attack(self, enemy):
        self.attack_timer -=1
        amount = WEAPONS[self.weapon_type]["damage"]
        kx,ky=DIRECITONS[self.direction]
        vx,vy = VECTORS[self.direction]
        weapon_x = self.x + kx + (vx*self.attack_length)
        weapon_y = self.y+ky + (vy*self.attack_length)
        weapon_rect = pygame.Rect(weapon_x,weapon_y,20,20)
        
        if self.attacking and WEAPONS[self.weapon_type]["type"] =="melee":
            self.attack_length += 7
            # MELEE ATTACK RATE: 7
            
            if self.attack_length >= self.Maxlength:
                self.attacking = False
                self.returning = True
            
                
            enemy_rect = pygame.Rect(enemy.x, enemy.y, 50, 50)

            if weapon_rect.colliderect(enemy_rect) and self.has_hit == False:
              
                self.has_hit = True
                enemy.x += vx*50
                enemy.y += vy*50
                enemy_rect = pygame.Rect(enemy.x, enemy.y, 50, 50)
                for obstacle in obstacles:

                     obstacle_rect = pygame.Rect(obstacle["x"],obstacle["y"],20,20)
                     if enemy_rect.colliderect(obstacle_rect):
                        print("c")
                        enemy.x -= vx*20
                        enemy.y -= vy*20

                     obstacle_rect = pygame.Rect(obstacle["x"],obstacle["y"],50,50)
                     if enemy_rect.colliderect(obstacle_rect):
                        print("c")
                        enemy.x -= vx*50
                        enemy.y -= vy*50

                       
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
        
       
        vx,vy = VECTORS[self.direction]
        dash_distance = 100
        if self.dash_timer > 0:
            self.dash_timer -= 1
        else:
            self.dash = False
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
        if self.dash == True:
            if self.dash_direction != self.direction:
                self.dash = False
            self.movement(dash_distance*vx,dash_distance*vy)


def draw_menu():
        
        title = font.render("Welcome to square fighter game,press e to play a bot or p to play a player",True,(255,0,0))
        win.blit(title,(200,100))
def die():
   
    if P.health<=0:
         death_text = font.render((str(P2.name) + " has won"),True,(255,0,0))
    elif P2.health <=0:
        death_text = font.render((str(P.name) + " has won"),True,(255,0,0))
    win.blit(death_text,(200,100))



game_state = "menu"
def P2_inputs():
     if keys[pygame.K_LEFT]:
        P2.movement(-20, 0)
        P2.direction = "left"
     if keys[pygame.K_RIGHT]:
        P2.movement(20, 0)

P = Player(
    "Player_Name", 100, 0, 0, "red", False, 20, 5, 80, False, "right", False, 0, 0,"block",False,"right",100,60,False,300,False
)

P2 = Player(
    "Player 2", 100, 0, 0, "green", False, 20, 5, 80, False, "left", False, 0, 0,"block",False,"right",100,60,False,300,False
)
game_state = "menu"
def P2_inputs():
     if keys[pygame.K_LEFT]:
        P2.movement(-10, 0)
        P2.direction = "left"
     if keys[pygame.K_RIGHT]:
        P2.movement(10, 0)

        P2.direction = "right"

     if keys[pygame.K_UP]:
        P2.direction = "up"

        P2.movement(0, -20)
     if keys[pygame.K_DOWN]:
        P2.movement(0, 20)

        P2.movement(0, -10)
     if keys[pygame.K_DOWN]:
        P2.movement(0, 10)

        P2.direction = "down"
     if keys[pygame.K_KP0]:
                P2.weapon_type = "gun"
     if keys[pygame.K_KP1]:
                P2.weapon_type = "block"
     if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button ==3 and P2.dash_cooldown == 0:
              
                P2.dash = True
                P2.dash_timer = 60
                P2.dash_direction = P2.direction
                P2.dash_cooldown = 600
def mouse_inputs():
     mx, my = pygame.mouse.get_pos()
     dx = mx-P.x
     dy = my-P.y
     if abs(dx) > abs(dy):
        
          P.direction = "right" if dx > 0 else "left"
     else:
          P.direction = "down" if dy > 0 else "up"
run = True

def a_star(grid,x,y, target_x, target_y):
   
    if(x,y) == (target_x,target_y):
        
         return None
    
    directions = {
               "right": (1,0),
               "down": (0,1),
               "left": (-1,0),
               "up": (0,-1)
          
     }
    start_x = x
    start_y = y
    open_list = []
    closed_list = []
    path = []
    start_node = {
         "f": 0,
         "g":0,
         "h": 0,
         "position":(start_x,start_y),
         "parent": None
    }

    current = start_node
    while (x,y)!= (target_x,target_y):
     
  
        for direction in directions:
            vx,vy = directions[direction]
            for cell in grid: 
                # is this the cell we are searching for?
                if cell["x"] == (vx*20)+x and cell["y"] == (vy*20) + y:
                   
                    #check if cell is valid
                    if cell["occupied"] == False and 0<=x+(vx*20)<=780 and 0<=y+(vy*20)<=380:
                        
                        #taking the info of the neighbors
                        h = abs(target_x-(x+(vx*20))) + abs(target_y-(y+(vy*20)))
                        neighbor_g = current["g"]+20
                        f = neighbor_g+h
                       
                        #remembering the parent for path reconstruction
                        neighbor_cell = {"f": f, "h": h, "g": neighbor_g, "position":(x+(vx*20),y+(vy*20)),"parent":current}
                        
                       
                              
                        if not any(node["position"]==neighbor_cell["position"] for node in closed_list) and not any(node["position"] == neighbor_cell["position"] for node in open_list):
                                
                                 open_list.append(neighbor_cell)
                                
        lowest_f_index = 0
        for i in range(len(open_list)):
            # check f value to see lowest one, exploring the open list
            if open_list[i]["f"] < open_list[lowest_f_index]["f"]:
                lowest_f_index = i
                
        #remember this value, don't explore it again
    
        if len(open_list) > 0:
           
            x,y = open_list[lowest_f_index]["position"]
        
            closed_list.append(open_list[lowest_f_index])
            current = open_list[lowest_f_index]
            open_list.pop(lowest_f_index)
  
        else:
          
             return None
        # might search again, but we have the info of the cells
    # ending the search

    if closed_list:
        C = closed_list[-1]
    
        while (C["position"]) != (start_x,start_y):
            path.append(C)
            C = C["parent"]
        path.reverse()
        return path
    else:
     
         return None
P = Player(
    "Player_Name", 100, 120, 380, "red", False, 20, 5, 80, False, "right", False, 0, 0,"block",False,"right",100,60,False,300,[]
)

P2 = Player(
    "Player 2", 100, 0, 0, "green", False, 20, 5, 80, False, "left", False, 0, 0,"block",False,"right",100,60,False,300,[]
)
P2.x = 0
P2.y = 0




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
                        print("section under construction")
                        game_state = "playing"
                    elif event.key == pygame.K_p:
                        mode = "PvP"
                       
                        game_state = "playing"
                    obstacles = []


                    for store_obstacles in range(numObstacles):
                        obstaclex,obstacley = random.randint(3,40),random.randint(3,20)
                        obstacle_rect = {"x":obstaclex*20,"y":obstacley*20,"length": 20,"width":20}
                        obstacles.append(obstacle_rect)
                        for grid_cell in grid:
                                                     if grid_cell["x"] == obstacle_rect["x"] and grid_cell["y"] == obstacle_rect["y"]:
                                                      
                                                          grid_cell["occupied"] = True
                  
                
                  
        elif game_state == "playing":
        
            if mode == "PvP":
                P2_inputs()
                P.draw(win)
                P2.draw(win)
                
                        
            
            if P.health <= 0 or P2.health <= 0:
                game_state = "death"
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LSHIFT:
                
                    P.attack()
                if event.key == pygame.K_r:
                    P.heal(10)
                    P.heal_cooldown = 300
                if event.key == pygame.K_KP4:
                    P2.heal(10)
                if event.key == pygame.K_RSHIFT and mode == "PvP":
                    
                        P2.attack()
            
            
                        
                if event.key == pygame.K_1:
                    P.weapon_type = "block"
                if event.key == pygame.K_2:
                    P.weapon_type = "gun"
                    
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and P.dash_cooldown == 0:
                    P.dash = True
                    P.dash_direction = P.direction
                    P.dash_timer = 60
                    P.dash_cooldown = 600
            
               

    
    keys = pygame.key.get_pressed()
    if game_state == "playing":
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
        

          

                        
                          
                   
          
    if mode == "PvE":
        
            
          
            print("A* start:", P2.x, P2.y)
            print("Grid aligned:", P2.x % 20 == 0 and P2.y % 20 == 0)
            
            P2.path = a_star(grid, P2.x,P2.y,P.x,P.y)
            
        
            if P2.path and P2.path[0]["position"] != (P.x,P.y):
              
               
                next_node = P2.path[0]
             
                Tx,Ty = next_node["position"]
              
          
                
             
                if abs(Tx-P2.x) <= 5 and abs(Ty - P2.y) <=  5:
                     print("pop")
                     P2.path.pop(0)
                else:
                    if Tx != P2.x:
                     if Tx > P2.x: 
                          P2.direction = "right"
                     elif Tx < P2.x:
                          P2.direction = "left"
                    elif P2.y != Ty:
                     if Ty > P2.y:
                          P2.direction = "down"
                     elif Ty < P2.y:
                          P2.direction = "up"
        
             
            vx, vy = VECTORS[P2.direction]
       
            mx = vx * 20
            my = vy * 20
            P2.movement(mx,my)


            if (abs(P2.x-P.x) < 10 or abs(P2.y-P.y) < 10) and P2.attack_timer <= 0:
                    pass
            #P2.attack()

            

          
                    
          
            if P.health <= 0 or P2.health <= 0:
                game_state = "death"
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LSHIFT:
                
                    P.attack()
                if event.key == pygame.K_r:
                    P.heal(10)
                    P.heal_cooldown = 300
                if event.key == pygame.K_KP4:
                    P2.heal(10)
                if event.key == pygame.K_RSHIFT and mode == "PvP":
                    
                        P2.attack()
            
            
                        
                if event.key == pygame.K_1:
                    P.weapon_type = "block"
                if event.key == pygame.K_2:
                    P.weapon_type = "gun"
                    
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1 and P.dash_cooldown == 0:
                    P.dash = True
                    P.dash_direction = P.direction
                    P.dash_timer = 60
                    P.dash_cooldown = 600
            
            

          
    for obstacle in obstacles:
                        draw_obstacle = pygame.Rect(obstacle["x"],obstacle["y"],50,50)
                        pygame.draw.rect(win,(128,128,128),draw_obstacle)
                        P2_rect = pygame.Rect(P2.x,P2.y,50,50)
                   
                        
                          
                   
                        


    P.update_heal()
    P2.update_heal()
    P.update_attack(P2)
    P2.update_attack(P)
    P.update_dash()
    P2.update_dash()
    P.Dont_go_offscreen_plz()
    P2.Dont_go_offscreen_plz()
    P.update_shoot(P2)
    P2.update_shoot(P)
    P.draw_bullet()

            

    
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        P.movement(-10, 0)
        P.direction = "left"

    if keys[pygame.K_d]:
        P.movement(10, 0)
        P.direction = "right"
    if keys[pygame.K_w]:
        P.movement(0, -10)
        P.direction = "up"
    if keys[pygame.K_s]:
        P.direction = "down"
        P.movement(0, 10)
    if mode == "PvP":
        P2_inputs()
    elif mode == "PvE":
         mouse_inputs()
        

         if (abs(P2.x-P.x) < 10 or abs(P2.y-P.y) < 10) and P2.attack_timer <= 0:
            pass
            #P2.attack()

            

         
    
    if game_state == "playing":
        P.draw(win)
        P2.draw(win)
    if game_state == "death":
            die()


    pygame.display.update()

pygame.quit()
