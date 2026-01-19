import pygame
import backend as b
import display as d


#----------------------------------------------------------------------------------------------------------------------
                                          #Setup
#----------------------------------------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
width,height = screen.get_size()
folder_directory = "D:\Coding Projects\Fallout - Revisioned\wordbank.txt" # Change to wherever the wordbank is stored


# Colors
faded_green = (0,100,0)
bg_green =  (0,5,0)
words_color = (31,255,64)

# Surfaces
crt_lines_surface = pygame.Surface((width,height), pygame.SRCALPHA)
glow_surface = pygame.Surface((width,height))
glow_surface.fill((0,40,0))

# Fonts
text_font = pygame.font.Font("FSEX300.ttf", int(height*0.04))
char_width, char_height = text_font.size("A")

# Game stats
attempts_remaining = 4
target = "" # The correct word
take_input = True # Only take input if word not found


# Text Generation Variables
symbols = "[]{}()!@#$%^&*_+-=/?"
left_col_words = []
right_col_words = []
L_addresses = []
R_addresses = []
logs = [] # log of clicks made, later improvement: track indices not elements, since eg. ) can be in multiple indices

L_word_rows_indices = {} # dictionary of (row,word) for the left column where there is a word, used to remove duds
R_word_rows_indices = {}


# Left Column: Starting X and Y coords for the first char 
L_col_x_start = width*0.2
L_col_y_start = height* (1/25 + 0.195)

R_col_x_start = width*0.56
R_col_y_start = height* (1/25 + 0.195)


line_spacing = height/25

left_hitbox = pygame.Rect(L_col_x_start, L_col_y_start, char_width * 12, line_spacing * 16)
right_hitbox = pygame.Rect(R_col_x_start, R_col_y_start, char_width * 12, line_spacing * 16)


# Other

open_brackets = ['[', '(', '{' ]
closed_brackets = [']', ')','}']
L_pair_found_indices = []
R_pair_found_indices = []


#----------------------------------------------------------------------------------------------------------------------
                                          #Main
#----------------------------------------------------------------------------------------------------------------------

# Draw the lines before running else they get drawn 60 times a second (performance)
d._add_crt_effect(screen, height, width, crt_lines_surface)

# Generate words
left_col_words = b._random_grid_symbols(symbols)
right_col_words = b._random_grid_symbols(symbols)

left_col_words, right_col_words, target, L_word_rows_indices, R_word_rows_indices = b._word_injection(left_col_words,right_col_words, folder_directory, L_word_rows_indices, R_word_rows_indices)

# Generate addresses
L_addresses, R_addresses = b._hexadecimal_address(L_addresses, R_addresses)


while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply screen effects and then add text
    screen.fill(bg_green)
    d._terminal_effects(screen, crt_lines_surface, glow_surface)

    

    # Introductory text
    d.renderText("ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL", text_font, words_color, 0.01, 0.05, width, height, screen,center=False)
    d.renderText("ENTER PASSWORD NOW", text_font, words_color, 0.01, 0.085, width, height, screen,center=False)
    d.renderText("{} ATTEMPT(S) LEFT: ".format(attempts_remaining) + "[]"*attempts_remaining, text_font, words_color, 0.01, 0.145, width, height, screen,center=False)

    # Left Column and Addresses
    

    for i in range(16):
        d.renderText(left_col_words[i], text_font, words_color, 0.2, (i+1)/25 + 0.195, width, height, screen,center=False)
        d.renderText(L_addresses[i], text_font, words_color, 0.1, (i+1)/25 + 0.195, width, height, screen,center=False)

    
    # Right Column and Addresses
    for i in range(16):
        d.renderText(right_col_words[i], text_font, words_color, 0.56, (i+1)/25 + 0.195, width, height, screen,center=False)
        d.renderText(R_addresses[i], text_font, words_color, 0.46, (i+1)/25 + 0.195, width, height, screen,center=False)





    # Mouse checking only when hovering around the two columns (use colliders)
    mouse_pos = pygame.mouse.get_pos()

    if(attempts_remaining == 0):
        if "Out of tries!" not in logs:
            logs.append("Out of tries!")
    else:

        if(left_hitbox.collidepoint(mouse_pos)):
            
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]

            X,Y = b._pixel_pos_to_indices(mouse_x,mouse_y, L_col_x_start,L_col_y_start, height, char_width)


            # Display text as it is hovered over
            
            display_text = left_col_words[X][Y]
            display_text = b._find_word(display_text,X,Y,left_col_words)
            pair_found = b._search_pairs(X,Y,left_col_words, open_brackets, closed_brackets)
            
            # If a pair of brackets is found, display the sequence of symbols
        
            if pair_found[0] != -1:
                display_text = pair_found[1]
                
                

            d.renderText('>'+display_text, text_font, words_color, 0.76, (16)/25 + 0.195, width, height, screen,center=False)
            

            # Add to logs and then we display all logs outside of the two checks
            if event.type == pygame.MOUSEBUTTONDOWN and take_input:
                
                            
                if (pair_found[0] != -1) and (X,Y) not in L_pair_found_indices:
                    L_pair_found_indices.append((X,Y))
                    if pair_found[0] == 0:
                        left_col_words, right_col_words = b._remove_dud(left_col_words, right_col_words, L_word_rows_indices, R_word_rows_indices, target)
                        logs.append("Dud removed")
                        logs.append(pair_found[1])
                    elif pair_found[0] == 1:
                        attempts_remaining = b._reset_tries(attempts_remaining)
                        logs.append("Tries reset")
                        logs.append(pair_found[1])


            
                if display_text in logs:
                    pass
                else:
                    if display_text[0].isalpha() == True:
                        logs.append(display_text)
                        attempts_remaining -= 1

                
                # Will change how to deal with storing only once later
                if display_text == target:

                    take_input = False

                    if "Exact match!" not in logs:
                        logs.append("Exact match!")
                    
                    if "Please wait" not in logs:
                        logs.append("Please wait")
                    
                    if "while system!" not in logs:
                        logs.append("while system!")

                    if "is accessed" not in logs:
                        logs.append("is accessed")

        

        if(right_hitbox.collidepoint(mouse_pos)):
            
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]

            X,Y = b._pixel_pos_to_indices(mouse_x,mouse_y, R_col_x_start,R_col_y_start, height, char_width)


            # Display text as it is hovered over
            
            display_text = right_col_words[X][Y]        
            display_text = b._find_word(display_text,X,Y,right_col_words)
            pair_found = b._search_pairs(X,Y,right_col_words, open_brackets, closed_brackets)

            # If a pair of brackets is found, display the sequence of symbols
            if pair_found[0] != -1:
                display_text = pair_found[1]
                

            d.renderText('>'+display_text, text_font, words_color, 0.76, (16)/25 + 0.195, width, height, screen,center=False)

            # Add to logs and then we display all logs outside of the two checks
            if event.type == pygame.MOUSEBUTTONDOWN and take_input:

            
                    
                
                if (pair_found[0] != -1) and (X,Y) not in R_pair_found_indices:
                    R_pair_found_indices.append((X,Y))
                    if pair_found[0] == 0:
                        left_col_words, right_col_words = b._remove_dud(left_col_words, right_col_words, L_word_rows_indices, R_word_rows_indices, target)
                        logs.append("Dud removed")
                    elif pair_found[0] == 1:
                        attempts_remaining =b._reset_tries(attempts_remaining)
                        logs.append("Tries reset")

                

                if display_text in logs:
                    pass
                else:
                    if display_text[0].isalpha() == True:
                        logs.append(display_text)
                        attempts_remaining -= 1
                        
            
                # Will change how to deal with storing only once later
                if display_text == target:
                    
                    take_input = False

                    if "Exact match!" not in logs:
                        logs.append("Exact match!")
                    
                    if "Please wait" not in logs:
                        logs.append("Please wait")
                    
                    if "while system!" not in logs:
                        logs.append("while system!")

                    if "is accessed" not in logs:
                        logs.append("is accessed")

            

                
            

                

    

    # Need to keep log size constant, eliminate the oldest entry when almost full
    for index,entry in enumerate(logs[::-1]):
         d.renderText('>'+entry, text_font, words_color, 0.76, (15-index)/25 + 0.185, width, height, screen,center=False)

    if len(logs) > 15:
        del logs[0]
    
  



    pygame.display.flip()
    clock.tick(60)




pygame.quit()





