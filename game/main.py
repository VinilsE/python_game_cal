import pygame

image_path = '/data/data/com.bseu.myapp/files/app/'

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((600, 333)) # flags=pygame.NOFRAME
pygame.display.set_caption('Игра про письки')
icon = pygame.image.load(image_path + 'картиночки/image.jpg').convert_alpha()
pygame.display.set_icon(icon)

background = pygame.image.load(image_path + 'картиночки/background.png').convert_alpha()
walk_left = [
    pygame.image.load(image_path + 'картиночки/player_left/image11.png').convert_alpha(),
    pygame.image.load(image_path + 'картиночки/player_left/image12.png').convert_alpha(),
    pygame.image.load(image_path + 'картиночки/player_left/image15.png').convert_alpha(),
    pygame.image.load(image_path + 'картиночки/player_left/image16.png').convert_alpha(),
]
walk_right = [
    pygame.image.load(image_path + 'картиночки/player_right/image19.png').convert_alpha(),
    pygame.image.load(image_path + 'картиночки/player_right/image20.png').convert_alpha(),
    pygame.image.load(image_path + 'картиночки/player_right/image23.png').convert_alpha(),
    pygame.image.load(image_path + 'картиночки/player_right/image24.png').convert_alpha(),
]



cal = pygame.image.load(image_path + 'картиночки/какламыс (2).png')
cal_list_in_game = []

player_anim_count = 0
background_x = 0

player_speed = 5
player_x = 150
player_y = 225

is_jump = False
jump_count = 8

background_sound = pygame.mixer.Sound(image_path + 'музыка/Journey Across the Blue.ogg')
background_sound.play()

cal_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cal_timer, 2600)


dead = pygame.image.load(image_path + 'картиночки/afgan.png').convert_alpha()
label = pygame.font.Font(image_path + 'шрифты/SaarSPDemo.otf', 30)
label_restart = label.render('избежать фиаско заново', False, (150, 3, 3))
label_restart_rect = label_restart.get_rect(topleft=(180, 45))

penises_left = 5
penis = pygame.image.load(image_path + 'картиночки/penis.png').convert_alpha()
penises = []

gameplay = True

running = True
while running:

    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 600,0))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if cal_list_in_game:
            for i, el in enumerate(cal_list_in_game):
                screen.blit(cal, el)
                el.x -= 7

                if el.x < -7:
                    cal_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8


        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        background_x -= 3
        if background_x == -600:
            background_x = 0

        if penises:
            for (i, el) in enumerate(penises):
                screen.blit(penis, (el.x, el.y))
                el.x += 4

                if el.x > 610:
                    penises.pop(i)

                if cal_list_in_game:
                    for (index, cal_el) in enumerate(cal_list_in_game):
                        if el.colliderect(cal_el):
                            cal_list_in_game.pop(index)
                            penises.pop(i)

    else:
        screen.blit(dead, (0, 0))
        screen.blit(label_restart, label_restart_rect)

        mouse = pygame.mouse.get_pos()
        if label_restart_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            cal_list_in_game.clear()
            penises.clear()
            penises_left = 5


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == cal_timer:
            cal_list_in_game.append(cal.get_rect(topleft=(610,230)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_f and penises_left > 0:
            penises.append(penis.get_rect(topleft=(player_x + 20, player_y + 18)))
            penises_left -= 1


    clock.tick(15)