import pygame
#----------------------------------------------------------------------------------------------------------------------
                                          #Display Methods
#----------------------------------------------------------------------------------------------------------------------

def _add_crt_effect(screen, height, width, crt_lines_surface):
    for y in range(0,height,4):
        pygame.draw.line(crt_lines_surface, (0, 20, 0, 80), (0, y), (width, y))
    
    screen.blit(crt_lines_surface, (0, 0))


def _terminal_effects(screen, crt_lines_surface, glow_surface):    
    # Apply the CRT lines
    screen.blit(crt_lines_surface,(0,0))
    # Add a glow effect
    screen.blit(glow_surface, (0,0), special_flags=pygame.BLEND_RGB_ADD)

def renderText(text,font,color,relative_x,relative_y, width, height, screen, center = True):

    text_surface = font.render(text,True,color)
    
    pos_x = width * relative_x
    pos_y = height * relative_y

    text_rect = text_surface.get_rect()

    if center:
        text_rect.center = (pos_x, pos_y)
    else:
        text_rect.topleft = (pos_x, pos_y)
        
    screen.blit(text_surface, text_rect)

