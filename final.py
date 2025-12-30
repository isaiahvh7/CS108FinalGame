"""
CS 108 Final Project
By Isaiah VanHorn
"""

import pygame, gif_pygame, sys
from random import randint

class worldObject:
    """
    Creates a object to be placed in the game world.
    
    Init Paramaters:
        x: int for the x pos of the upper left corner of the object
        y: int for the y pos of the upper left corner of the object
        width: int for the width of the object
        height: int for the height of the object
        image_path: str for the path to the image
        animated: boolean for whether the image is a gif or not
        real: boolean for whether the object can be interacted with
    
    Functions:
        return_rect: Returns a pygame.Rect object of the worldObject
    """
    loaded_img = ""
    def __init__(self, x, y, width, height, image_path, animated, real = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image_path
        self.gif = animated
        self.real = real
    
    def return_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class worldFinish:
    """
    Creates a object to be placed in the game world. Triggering one of these objects ends a level.
    
    Init Paramaters:
        x: int for the x pos of the upper left corner of the object
        y: int for the y pos of the upper left corner of the object
        width: int for the width of the object
        height: int for the height of the object
        image_path: str for the path to the image
        animated: boolean for whether the image is a gif or not
        real: boolean for whether the object can be interacted with
    
    Functions:
        return_rect: Returns a pygame.Rect object of the worldObject
    """
    gif_image = ""
    def __init__(self, x, y, width, height, image_path, real = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = image_path
        self.real = real
        
    def return_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
class worldNpc:
    """
    Creates a npc to be placed in the world
    
    Init Paramaters:
        x: int for the x pos of the upper left corner of the object
        y: int for the y pos of the upper left corner of the object
        width: int for the width of the object
        height: int for the height of the object
        image_path: str for the path to the image
        attack_paths: str for paths to all image files for attacks
        health: int for the npc's health
        damage: int for the npc's damage
        speed: int for the npc's speed
        actual_hitbox: Tuple for the object's actual hitbox
        actual_attack_hitboxes: List of tuples for the object's attack htiboxes
    
    Functions:
        return_rect: Returns a pygame.Rect object of the worldObject
        return_atk_hitbox: Returns a pygame.Rect object for the npc's attack hitbox
        face_player: Makes the npc face the player
        move: Makes the npc move
        attack: Makes the npc attack
    """
    gif_image = ""
    gif_atks = []
    real = False
    facing = 'Right'
    attacking = False
    attack_frame = 0
    dmg = False
    atk_count = 0
    flipped = False
    def __init__(self, x, y, width, height, image_path, attack_paths, health, damage, speed, actual_hitbox, actual_attack_hitboxes):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = image_path
        self.atk_imgs = attack_paths
        self.hp = health
        self.dmg = damage
        self.speed = speed
        self.ah = actual_hitbox
        self.atkhitboxes = actual_attack_hitboxes
        
    def return_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def return_atk_hitbox(self):
        hitbox = self.atkhitboxes[self.attack_frame*2]
        if self.facing == "Left":
            hitbox = self.atkhitboxes[self.attack_frame*2+1]
            return pygame.Rect(self.x + hitbox[0], self.y + hitbox[1], hitbox[2], hitbox[3])
        return pygame.Rect(self.x + hitbox[0], self.y + hitbox[1], hitbox[2], hitbox[3])
        
    def face_player(self, player_x):
        if player_x < self.x+self.ah[0]:
            if self.facing != 'Left':
                self.facing = 'Left'
                gif_pygame.transform.flip(self.gif_img, True, False)
        elif player_x > self.x+self.ah[0]:
            if self.facing == 'Left':
                self.facing = 'Right'
                gif_pygame.transform.flip(self.gif_img, True, False)
            
    def move(self):
        if self.facing == 'Right':
            self.x += self.speed
        else:
            self.x -= self.speed
   
    def attack(self, player_x):
        self.dmg = False
        self.atk_count = len(self.gif_atks[self.attack_frame].get_durations())*6
        self.attacking = True
        if self.facing == 'Left' and not self.flipped:
            self.flipped = True
            for atk in self.gif_atks:
                gif_pygame.transform.flip(atk, True, False)
        elif self.facing == 'Right' and self.flipped:
            self.flipped = False
            for atk in self.gif_atks:
                gif_pygame.transform.flip(atk, True, False)
        self.attack_frame +=1
        if self.attack_frame >= len(self.gif_atks):
            self.attack_frame = 0
        
def rect_overlap(rect1, rect2):
    """
    Using the upper left and lower right corners of two rectangles,
    determine if they overlap
    
    Args:
        rect1: worldObject for the first rectangle
        rect2: worldObject for the second rectangle
    
    Returns:
        Boolean: True if the rectangles overlap, otherwise returns False.
        
    Raises:
        None
    """
    if (rect1.x > rect2.x+rect2.width or rect2.x > rect1.x+rect1.width):
        return False

    if (rect1.y > rect2.y+rect2.height or rect2.y > rect1.y+rect1.height):
        return False
    return True

def handle_collisions(obj, player_rect, object_list, velocity, jumpforce, gravity, grounded):
    """
    Handles all collisions
    
    Args:
        player_rect: worldObject for the player
        obj_list: list of game objects
        velocity: int for player's velocity
        jumpforce: int for the player's jump force
        gravity: int for the player's gravity
        grounded: boolean for whether the player is on the ground
        crouching: boolean for if the player is crouching
        
    Returns:
        List: a int for what wall the player is touching and a boolean for whether the player is on the ground
        
    Raises:
        None
    """
    # Brute forces which direction will stop the player from colliding
    wall_side_touch = -1
    touching_roof = False
    if rect_overlap(player_rect,obj) is True: 
        for object in object_list:
            object.x+=velocity
        wall_side_touch = 1
        if rect_overlap(player_rect,obj) is True: 
            for object in object_list:
                object.x-= velocity*2
            wall_side_touch = 0    
            if rect_overlap(player_rect,obj) is True:
                    for object in object_list:
                        object.x+=velocity
                        if not grounded:
                            object.y-=jumpforce
                    touching_roof = True
                    wall_side_touch = -1
                    if rect_overlap(player_rect,obj) is True: 
                        touching_roof = False
                        for object in object_list:
                            if not grounded:
                                object.y+= jumpforce
                            object.y+= gravity
                        # Calculates difference from scaling gravity.
                        dif = (obj.y - (player_rect.y+player_rect.height)) 
                        for object in object_list:
                            object.y-= dif
                        return [wall_side_touch, True, touching_roof]
    return [wall_side_touch, False, touching_roof]
                            
def keypress():
    """
    Returns what keys are being pressed
    
    Args:
        None
        
    Returns:
        key_list: A list of every key being pressed
        
    Raises:
        None
    """
    keys = pygame.key.get_pressed()
    key_list = []
    if keys[pygame.K_a]:
        key_list.append('a')
    if keys[pygame.K_d]:
        key_list.append('d')
    if keys[pygame.K_w]:
        key_list.append('w')
    if keys[pygame.K_s]:
        key_list.append('s')
    if keys[pygame.K_SPACE]:
        key_list.append('space')
    if keys[pygame.K_LSHIFT]:
        key_list.append('shift')
    if keys[pygame.K_RSHIFT]:
        key_list.append('shift')
    return key_list

def render_objects(win, obj_list, player_obj, bg):
    """
    Renders all objects except the player
    
    Args:
        win: a pygame window object
        obj_list: a list of rectangles to render 
        player_obj: a worldObject for the player
        bg: str for background
        
    Returns:
        None
        
    Raises:
        None
    """
    # Clear Screen
    win.fill('lightblue')
    rd = 0
    # Background
    win.blit(pygame.transform.scale(bg, (1280, 720)), (0, 0))
    # Render Objects
    # Only visable objects are rendered
    for object in obj_list:
        if isinstance(object, worldObject):
            if pygame.Rect.colliderect(object.return_rect(), win.get_rect()):
                image = pygame.transform.scale(object.loaded_img, (object.width, object.height))
                win.blit(image, (object.x, object.y))
        elif isinstance(object, worldNpc):
            if pygame.Rect.colliderect(object.return_rect(), win.get_rect()):
                if not object.attacking:
                    win.blit(object.gif_img.blit_ready().convert_alpha(), (object.x, object.y))
                if object.attacking:
                    win.blit(object.gif_atks[object.attack_frame].blit_ready().convert_alpha(), (object.x, object.y))
        elif isinstance(object, worldFinish):
            if pygame.Rect.colliderect(object.return_rect(), win.get_rect()):
                win.blit(object.gif_img.blit_ready().convert_alpha(), (object.x, object.y))
                   
def render_player(win, player_obj, pimg, facing, x_width_scale, y_height_scale):
    """
    Renders the player
    
    Args:
        win: a pygame window object
        player_obj: a worldObject for the player
        pimg: str for the player gif
        facing: str for the direction the player is facing
        x_height_scale: into for the x difference based on image size
        y_height_scale: int for the y difference based on image size
        
    Returns:
        None
        
    Raises:
        None
    """
    win.blit(pimg.blit_ready().convert_alpha(), (player_obj.x-x_width_scale, player_obj.y-y_height_scale))

def main():
    """
    The main function of the game. Running this starts the game.
    
    Args:
        None
    
    Returns:
        None
        
    Raises:
        None
    """
    # Setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED | pygame.FULLSCREEN, vsync = 1) # Make RESIZABLE or FULLSCREEN
    clock = pygame.time.Clock()
    running = True
    
    # Main Menu
    screen.fill('Black')
    pygame.mixer.Channel(1)
    pygame.mixer.music.load("sounds/mainmenu.mp3")
    pygame.mixer.music.play()
    titlescreen = gif_pygame.load("backgrounds/titlescreen.gif")
    startbutton = pygame.image.load("textures/play.png")
    startbutton = pygame.transform.scale(startbutton, (600, 300))
    startrect = pygame.Rect(screen.width/2, screen.height/2+60, 600, 300)
    started = False
    while not started:
        # Check if the player clicks 'play'
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                posx, posy = pygame.mouse.get_pos()
                mouseRect = pygame.Rect(posx, posy, 1, 1)
                if rect_overlap(mouseRect, startrect):
                    started = True
        screen.blit(titlescreen.blit_ready().convert_alpha(), (0, 0))
        screen.blit(startbutton, (screen.width/2, screen.height/2+60))
        pygame.display.flip()
    pygame.mixer.music.pause()
    
    # Game Sounds
    effect_channel = pygame.mixer.Channel(0)
    pygame.mixer.music.load("sounds/level1.mp3")
    pygame.mixer.music.play()
    
    # Objects
    # Objects are defined, then added to lists
    player = worldObject(screen.width/2-40, screen.height/2-60, 80, 120, "player/idle.gif", True)
    pimg = gif_pygame.load(player.image)
    gif_pygame.transform.scale(pimg, (360,240))
    # Level 1 Objects
    ground1 = worldObject(0, 700, 1000, 1000, "textures/stonetexture1.jpg", False)
    ground2 = worldObject(1000, 550, 1000, 1000, "textures/stonetexture1.jpg", False)
    ground3 = worldObject(1300, 350, 200, 100, "textures/stonetexture1.jpg", False)
    ground4 = worldObject(-1000, 350, 1000, 1000, "textures/stonetexture1.jpg", False)
    ground5 = worldObject(2000, 700, 1300, 1300, "textures/stonetexture1.jpg", False)
    ground6 = worldObject(2500, 400, 300, 200, "textures/stonetexture1.jpg", False)
    ground7 = worldObject(3700, 700, 400, 400, "textures/stonetexture1.jpg", False)
    ground8 = worldObject(4400, -100, 500, 500, "textures/stonetexture1.jpg", False)
    ground9 = worldObject(4400, 550, 700, 700, "textures/stonetexture1.jpg", False)
    instruct = worldObject(400, 350, 380, 170, "textures/wasdtomove.png", False, False)
    instruct2 = worldObject(2200, 400, 248, 113, "textures/shift.png", False, False)
    # Level 1 Finish
    level1fin = worldFinish(4900, 415, 150, 150, "textures/flag.gif")
    #Level 2 Objects
    sground0 = worldObject(0, 700, 2000, 1000, "textures/stonetexture2.png", False)
    sground02 = worldObject(3000, -100, 2000, 1000, "textures/stonetexture2.png", False)
    sground1 = worldObject(1000, 550, 300, 150, "textures/stonetexture2.png", False)
    sground2 = worldObject(1600, 350, 300, 150, "textures/stonetexture2.png", False)
    sground3 = worldObject(2200, 300, 300, 150, "textures/stonetexture2.png", False)
    sground4 = worldObject(1000, 150, 300, 150, "textures/stonetexture2.png", False)
    sground5 = worldObject(1700, 0, 300, 150, "textures/stonetexture2.png", False)
    sground6 = worldObject(2200, -150, 300, 150, "textures/stonetexture2.png", False)
    sground7 = worldObject(2200, 1100, 300, 150, "textures/stonetexture2.png", False)
    sground8 = worldObject(2500, 1300, 300, 150, "textures/stonetexture2.png", False)
    sground9 = worldObject(2900, 1500, 300, 150, "textures/stonetexture2.png", False)
    sground10 = worldObject(3100, 1800, 500, 250, "textures/stonetexture2.png", False)
    sinstruct = worldObject(400, 550, 192.5, 35.5, "textures/spaceattack.png", False, False)
    # Level 2 Npcs
    sbird1 = worldNpc(1000, 500, 200, 200, "npctextures/bird.gif", ["npctextures/bird.gif"], 60, 5, 5, (50, 50, 100, 100), [(0, 0, 150, 150),(0, 0, 150, 150)])
    sbird2 = worldNpc(1300, 100, 200, 200, "npctextures/bird.gif", ["npctextures/bird.gif"], 60, 5, 5, (50, 50, 100, 100), [(0, 0, 150, 150),(0, 0, 150, 150)])
    sbird3 = worldNpc(3600, -400, 200, 200, "npctextures/bird.gif", ["npctextures/bird.gif"], 80, 5, 6, (50, 50, 100, 100), [(0, 0, 150, 150),(0, 0, 150, 150)])
    sbird4 = worldNpc(3800, -300, 200, 200, "npctextures/bird.gif", ["npctextures/bird.gif"], 80, 5, 3, (50, 50, 100, 100), [(0, 0, 150, 150),(0, 0, 150, 150)])
    sbird5 = worldNpc(-100, -300, 200, 200, "npctextures/bird.gif", ["npctextures/bird.gif"], 80, 5, 7, (50, 50, 100, 100), [(0, 0, 150, 150),(0, 0, 150, 150)])
    sbird6 = worldNpc(4000, -400, 200, 200, "npctextures/bird.gif", ["npctextures/bird.gif"], 80, 5, 4, (50, 50, 100, 100), [(0, 0, 150, 150),(0, 0, 150, 150)])
    # Level 2 Finish
    level2fin = worldFinish(5000, -100, 400, 400, "textures/portal.gif")
    level2fin2 = worldFinish(3600, 1800, 400, 400, "textures/portal.gif")
    # Level 3 Objects
    tground1 = worldObject(0, 700, 3000, 1000, "textures/bigrock.png", False)
    # Level 3 Npcs
    boss = worldNpc(1600, 300 , 600, 600, "npctextures/bossidle.gif", ["npctextures/bossattack1.gif"], 450, 10, 3, (190, 170, 200, 350), [(250, 200, 300, 300), (0, 200, 300, 300)])
    # Object Lists
    objects = [ground1, ground2, ground3, ground4, ground5, ground6, ground7, ground8, ground9, instruct, instruct2, level1fin]
    objectsL2 = [sground0, sground02, sground1, sground2, sground3, sground4, sground5, sground6, sground7, sground8, sground9, sground10, sinstruct, level2fin, level2fin2, sbird1, sbird2, sbird3, sbird4, sbird5, sbird6]
    objectsL3 = [tground1, boss]
    
    # Load images
    background = pygame.image.load("backgrounds/l1background2.png").convert()
    for obj in objects:
        if isinstance(obj, worldObject):
            obj.loaded_img = pygame.image.load(obj.image).convert_alpha()
        else:
            obj.gif_img = gif_pygame.load(obj.img)
            gif_pygame.transform.scale(obj.gif_img, (obj.width, obj.height))

    # Variables
    win = False
    force_crouch = False
    velocity = 0
    gravity = 0
    jump_speed = 20
    grounded = False
    jumping = False
    kp = keypress()
    facing = "Right"
    last_facing = ""
    state = "Fall"
    last_state = ""
    attack_count = 0
    attack_anim = 0
    roll_count = 0
    crouching = False
    y_height_scale = 120
    dmg = False
    hp = 100
    hit_damage = 20
    
    # The main game loop
    while running:
        # Poll for events
        # Pygame.QUIT event means the user clicked X to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Reset player state
        state = "player/idle.gif"
        
        # Check if player has fallen off the map
        if objects[0].y < -3000 and objects == objectsL2:
            running = False
        elif objects[0].y < -1000:
            running = False
        
        # Handle crouching
        if 's' in kp and grounded and not crouching and roll_count == 0 or force_crouch and not crouching and roll_count == 0:
            crouching = True
            state = "player/crouch.gif"
            y_height_scale = 160
            player.height = 80
            player.y = screen.height/2-20
        if crouching and not roll_count > 0 or force_crouch and not roll_count > 0:
            state = "player/crouch.gif"
        if not 's' in kp and grounded and crouching and not force_crouch and roll_count == 0:
            crouching = False
            y_height_scale = 120
            player.height = 120
            player.y = screen.height/2-60
            
        # Handle Movement
        # Player moves slower if crouching
        if crouching is False and roll_count == 0 and state != 'Attack':
            if 'a' in kp and 'd' in kp:
                if velocity > 0:
                    velocity -= 3
                if velocity < 0:
                    velocity += 3
                if velocity <= 2 and velocity >= -2:
                    velocity = 0
            elif 'a' in kp:
                facing = "Left"
                state = "player/run.gif"
                if velocity < 12:
                    velocity += 1.5
            elif 'd' in kp:
                facing = "Right"
                state = "player/run.gif"
                if velocity > -12:
                    velocity -= 1.5
            else:
                if velocity > 0:
                    velocity -= 3
                if velocity < 0:
                    velocity += 3
                if velocity <= 2 and velocity >= -2:
                    velocity = 0
        elif crouching is True and roll_count == 0 and state != 'Attack':
            if 'a' in kp and 'd' in kp:
                if velocity > 0:
                    velocity -= 3
                if velocity < 0:
                    velocity += 3
                if velocity <= 2 and velocity >= -2:
                    velocity = 0
            elif 'a' in kp:
                facing = "Left"
                state = "player/crouchwalk.gif"
                if velocity < 6:
                    velocity += 0.5
                if velocity > 6:
                    velocity -= 0.5
            elif 'd' in kp:
                facing = "Right"
                state = "player/crouchwalk.gif"
                if velocity > -6:
                    velocity -= 0.5
                if velocity < -6:
                    velocity += 0.5
            else:
                if velocity > 0:
                    velocity -= 3
                if velocity < 0:
                    velocity += 3
                if velocity <= 2 and velocity >= -2:
                    velocity = 0
        elif roll_count > 0:
            if facing == 'Right':
                velocity = -13
                if 'a' in kp:
                    velocity = -9
            if facing == 'Left':
                velocity = 13
                if 'd' in kp:
                    velocity = 9
        if attack_count > 0:
            if facing == 'Right':
                velocity = -3
            if facing == 'Left':
                velocity = 3
        for object in objects:
            object.x += velocity
        
        
        # Handle Gravity and Jumping
        if 'w' in kp and grounded and roll_count == 0:
            jumping = True
            grounded = False
            for object in objects:
                object.y += 1
            jump_speed = 20
        elif jumping and not grounded:
            if jump_speed > 0:
                jump_speed -= 1
                state = "player/jump.gif"
            else:
                jumping = False
            for object in objects:
                object.y += jump_speed
        elif not grounded:
            if force_crouch is False:
                state = "player/fall.gif"
            if gravity < 20:
                gravity += 1
            for object in objects:
                object.y -= gravity
        
        # Handle Rolling
        if 'shift' in kp and state != 'Attack':
            if roll_count == 0:
                # Dash animation, play dash sound, change player hitbox
                state = "Roll"
                dash = pygame.mixer.Sound("sounds/dash.wav")
                effect_channel.play(dash)
                roll_count = 1
                if facing == "Right":
                    player.image = "player/roll.gif"
                    pimg = gif_pygame.load(player.image)
                if facing == "Left":
                    player.image = "player/roll.gif"
                    pimg = gif_pygame.load(player.image)
                    gif_pygame.transform.flip(pimg, True, False)
                gif_pygame.transform.scale(pimg, (360,240))
                y_height_scale = 150
                player.height = 90
                player.y = screen.height/2-30
        if roll_count > 0:
            crouching = True
            state = "Roll"
            roll_count += 1
            if not grounded and jumping and roll_count < 15:
                for obj in objects:
                    obj.y += 2
        if roll_count > 40:
            roll_count = 0
            if not force_crouch:
                crouching = False
                y_height_scale = 120
                player.height = 120
                player.y = screen.height/2-60
        
        # Handle Attacks
        if 'space' in kp and roll_count == 0:
            if attack_count == 0:
                # Play slash sound and attack animation
                dmg = False
                if attack_anim > 1:
                    attack_anim = 0
                effect_channel.stop()
                slash = pygame.mixer.Sound("sounds/slash2.wav")
                effect_channel.play(slash)
                state = "Attack"
                attack_count = 1
                if facing == "Right":
                    sword_hitbox = pygame.Rect(player.x+player.width, player.y, 100, 130)
                    if crouching:
                        sword_hitbox = pygame.Rect(player.x-40, player.y, 200, 70)
                        player.image = "player/crouchattack.gif"
                    elif attack_anim == 0:
                        player.image = "player/attacknomove.gif"
                    else:
                         player.image = "player/attack2nomove.gif"
                    pimg = gif_pygame.load(player.image)
                if facing == "Left":
                    sword_hitbox = pygame.Rect(player.x-100, player.y, 100, 130)
                    if crouching:
                        sword_hitbox = pygame.Rect(player.x-80, player.y, 200, 70)
                        player.image = "player/crouchattack.gif"
                    elif attack_anim == 0:
                        player.image = "player/attacknomove.gif"
                    else:
                         player.image = "player/attack2nomove.gif"
                    pimg = gif_pygame.load(player.image)
                    gif_pygame.transform.flip(pimg, True, False)
                gif_pygame.transform.scale(pimg, (360,240))
                attack_anim += 1
        if attack_count > 0:
            state = "Attack"
            attack_count += 1
        if attack_count > 20:
            sword_hitbox = pygame.Rect(0, 0, 0, 0)
            state = "player/idle.gif"
            attack_count = 0
        
        # Handle npc movements
        # Chance to face player, chance to attack
        for npc in objects:
            if isinstance(npc, worldNpc):
                if randint(0, 60) == 19: 
                    npc.face_player(player.x)
                npc.move()
                if randint(0, 70) == 43:
                    npc.attack(player.x)
                if npc.attacking:
                    npc.atk_count -= 1
                if npc.atk_count == 0:
                    npc.attacking = False
                
        
        # Handle Collisions
        kp = keypress()
        grounded = False
        touching_wall = False
        force_crouch = False
        for obj in objects:
            # Iterate through every object
            # If the object is real, check if it collides with anything
            if obj.real is True:
                # Check whether the player should be forced to crouch
                if player.y-39 < obj.y+obj.height and player.y-39 > obj.y and player.x+player.width > obj.x and player.x < obj.x + obj.width and grounded and crouching:
                    force_crouch = True
                collisions = handle_collisions(obj, player, objects, velocity, jump_speed, gravity, grounded)
                # If touching floor, player is grounded
                if collisions[1]:
                    grounded = True
                    gravity = 0
                # If touching ceiling, stop jumping
                if collisions[2] and not grounded:
                    jumpforce = 0
                    jumping = False
                if isinstance(obj, worldFinish):
                    # Switches to next level if touching finish
                    if collisions[0] != -1 or collisions[1] or collisions[2]:
                        if obj == level2fin:
                            hit_damage = 30
                        if objects == objectsL2:
                            pygame.mixer.music.load("sounds/level3.mp3")
                            pygame.mixer.music.play()
                            objects = objectsL3
                            background = pygame.image.load("backgrounds/bossarena2.gif").convert()
                        else:
                            pygame.mixer.music.load("sounds/level2.mp3")
                            pygame.mixer.music.play()
                            objects = objectsL2
                            background = pygame.image.load("backgrounds/l2background.png").convert()
                        for obj in objects:
                            if isinstance(obj, worldNpc):
                                obj.gif_atks = []
                                obj.gif_img = gif_pygame.load(obj.img)
                                gif_pygame.transform.scale(obj.gif_img, (obj.width, obj.height))
                                index = 0
                                for gif in obj.atk_imgs:
                                    obj.gif_atks.append(gif_pygame.load(gif))
                                    gif_pygame.transform.scale(obj.gif_atks[index], (obj.width, obj.height))
                                    index += 1
                            elif isinstance(obj, worldObject):
                                obj.loaded_img = pygame.image.load(obj.image).convert()
                            else:
                                obj.gif_img = gif_pygame.load(obj.img)
                                gif_pygame.transform.scale(obj.gif_img, (obj.width, obj.height))
            if isinstance(obj, worldNpc):
                if state == 'Attack' and dmg is False:
                    # If hitting an npc, deal damage
                    if rect_overlap(sword_hitbox, pygame.Rect(obj.x+obj.ah[0], obj.y+obj.ah[1], obj.ah[2], obj.ah[3])):
                        flesh = pygame.mixer.Sound("sounds/hitflesh.wav")
                        effect_channel.play(flesh)
                        if facing == 'Right' and player.x < obj.x + obj.width/2:
                            dmg = True
                            obj.hp -= hit_damage
                        elif facing == 'Left' and player.x > obj.x + obj.width/2:
                            dmg = True
                            obj.hp -= hit_damage
                        if obj.hp <= 0:
                            if obj == boss:
                                win = True
                                running = False
                            objects.remove(obj)
                            
                # If an npc hits you, you take damage
                if rect_overlap(obj.return_atk_hitbox(), player) and object.attacking:
                    if obj.dmg == False and roll_count == 0:
                        obj.dmg = True
                        hp -= 10
                    if hp <= 0:
                        running = False
                        
        # Player animation handling
        # If attacking, disable moving
        # If rolling, stop jumping and crouching
        # If crouching, stop jump[ing
        if state == 'Attack':
            if 'w' in kp:
                kp.remove('w')
            if 'a' in kp:
                kp.remove('a')
            if 'd' in kp:
                kp.remove('d')
            if 's' in kp:
                kp.remove('s')
            if 'shift' in kp:
                kp.remove('shift')
        if state == 'Roll':
            if 'space' in kp:
                kp.remove('space')
            if 's' in kp:
                kp.remove('s')
        if crouching:
            if 'w' in kp:
                kp.remove('w')
            
        # If changing direction or state, change player gif
        if state != last_state and state != 'Attack' and state != 'Roll' or facing != last_facing and state != 'Attack' and state != 'Roll':
            player.image = state
            pimg = gif_pygame.load(player.image)
            x_width_scale = 120
            if facing == "Left":
                gif_pygame.transform.flip(pimg, True, False)
                x_width_scale = 160
            gif_pygame.transform.scale(pimg, (360,240))
        last_state = state
        last_facing = facing
        
        # Render
        render_objects(screen, objects, player, background)
        render_player(screen, player, pimg, facing, x_width_scale, y_height_scale)
        pygame.draw.rect(screen, "black", (30, 10, 200, 30))
        pygame.draw.rect(screen, "red", (30, 10, hp*2, 30))
        pygame.display.flip()
        # Limit fps to 120
        clock.tick(120)
    
    # If game over, render gameover screen or win screen
    if not win:
        gg = pygame.image.load("backgrounds/gameover.png").convert()
        gg = pygame.transform.scale(gg, (screen.width, screen.height))
        screen.blit(gg, (0, 0))
    if win:
        pygame.mixer.music.load("sounds/win.mp3")
        pygame.mixer.music.play()
        gg = pygame.image.load("backgrounds/win.png").convert()
        gg = pygame.transform.scale(gg, (screen.width, screen.height))
        screen.blit(gg, (0, 0))
    run2 = True
    # Loop to check whether the player presses 'play' or 'quit'
    while run2:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if not win:
                    posx, posy = pygame.mouse.get_pos()
                    if posx > screen.width/2 and posy > screen.height/3:
                        pygame.quit()
                        exit()
                    if posx < screen.width/2 and posy > screen.height/3:
                        run2 = False
                if win:
                    pygame.quit()
                    exit()
        pygame.display.flip()
    
# Main
while True:
    main()