import pygame
import random
pygame.init()
mode = ""
WIDTH, HEIGHT = 800, 400
# create a grid somehow
cell_x = 0
cell_y = 0
grid = []
while cell_x <= 750:
     while cell_y <= 350:
        new_cell = {
            "x": cell_x,
            "y": cell_y,
            "occupied": False
        }
        grid.append(new_cell)
        cell_y += 50
     cell_y = 0
     cell_x += 50
print(grid)
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
   "right-down":(1,1),
    "down": (0,1),
    "left-down":(-1,1),
    "left": (-1,0),
    "left-up": (-1,-1),
    "up": (0,-1),
   
    "right-up":(1,-1),
   
   
    

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
        collided,
        move_timer,
        collided_directions,
        collided_timer,
    
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
        self.collided = False
        self.move_timer = move_timer
        self.collided_directions = collided_directions
        self.collided_timer = collided_timer
    
        
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
            self.collided = True
      
            
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
            obstacle_rect = pygame.Rect(obstacle["x"],obstacle["y"],50,50)
            if player_rect.colliderect(obstacle_rect):

                self.collided_directions.append(self.direction)
                self.x -=Xvelocity
                self.y -=Yvelocity
                if self.is_ai == True:
                   self.collided = True
                   if self.direction == "up":
                        self.direction = "left"
                   elif self.direction == "right":
                        self.direction = "up"
                   elif self.direction == "down":
                        self.direction = "right"
                   elif self.direction == "left":
                        self.direction = "down"
 
            
    def draw_bullet(self):
       
   
        for projectile in projectiles:
    
            bullet = pygame.Rect(projectile["x"],projectile["y"],10,10)
        
            pygame.draw.rect(win,(0,255,0),bullet)
            
    def draw(self, win):
        if self.health > 0:
            player1 = pygame.transform.scale((pygame.image.load('Downloads/square.png')),(50,50))
            
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

P = Player(
    "Player_Name", 100, 0, 0, "red", False, 20, 5, 80, False, "right", False, 0, 0,"block",False,"right",100,60,False,300,False,15,[],60
)

P2 = Player(
    "Player 2", 100, 0, 0, "green", False, 20, 5, 80, False, "left", False, 0, 0,"block",False,"right",100,60,False,300,False,15,[],60
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
                        obstaclex,obstacley = random.randint(0,15),random.randint(0,15)
                        obstacle_rect = {"x":obstaclex*50,"y":obstacley*50,"length": 50,"width":50}
                       
                        obstacles.append(obstacle_rect)
                  
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
        

          

                        
                          
                   
          

    if mode == "PvE":
         mouse_inputs()
         if P2.collided_directions == [] and P2.collided_timer > 0:
            if P.x - P2.x > 10 and P2.collided == False:
                P2.direction = "right"
           
                
            elif P2.x - P.x > 10 and P2.collided == False:
                P2.direction = "left"
            
                
            if P.y - P2.y > 10 and P2.collided == False :
                P2.direction = "down"
              
            
            elif P2.y - P.y > 10 and P2.collided == False:
                P2.direction = "up"
         if abs(P.x-P2.x) > 30 or (P.y - P2.y) > 30:
            
            vx, vy = VECTORS[P2.direction]
       
            mx = vx * 10
            my = vy * 10
            P2.movement(mx,my)

         if P2.collided == True and P2.move_timer > 0:
              P2.move_timer -= 1
   
         if P2.move_timer <= 0:
          
           
              
                   P2.move_timer = 60
                
                   P2.collided = False
         if P2.collided_timer > 0 and P2.collided == False:
            P2.collided_timer -= 1
         if P2.collided_timer <= 0:
              P2.collided_timer = 60
              P2.collided_directions = []

         if (abs(P2.x-P.x) < 10 or abs(P2.y-P.y) < 10) and P2.attack_timer <= 0:
            pass
            #P2.attack()

            

         
    
    if game_state == "playing":
        P.draw(win)
        P2.draw(win)
    if game_state == "death":
            die()
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
    
                   
    pygame.display.update()

pygame.quit()
