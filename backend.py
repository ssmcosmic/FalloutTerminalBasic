import random
#----------------------------------------------------------------------------------------------------------------------
                                          #Backend Methods
#----------------------------------------------------------------------------------------------------------------------

def _random_grid_symbols(symbols):
    """
    Generates 16 strings of length 12, of random symbols
    To be used to inject words for each column, at random    """   

    column = [''.join(random.choices(symbols,k=12)) for i in range(16)]
    return column
  



def _word_injection(left_col_words,right_col_words, folder_directory, L_word_rows_indices, R_word_rows_indices):

    """
    Injects words into a randomly generated block of symbols above and also chooses a random word as target
    """
    already_injected = []
    L_rows_added_to = [] # Avoid injecting word to a row already having a word (left col)
    R_rows_added_to = [] # Avoid injecting word to a row already having a word (right col)
    
    with open(folder_directory) as file:
        words = [words.strip() for words in file]
        
    # Generate a random word for a random line. Ensure atleast 10 words generated

    while len(already_injected) < 10:
        for line in range(16):

            L_generate_word = bool(random.randint(0,1))
            R_generate_word = bool(random.randint(0,1))


            # Word generation for left side
            if L_generate_word and line not in L_rows_added_to:

                L_rows_added_to.append(line)
                L_random_start_index = random.randint(0,11)
            
                L_max_word_size = 11-L_random_start_index
            
                # Filter words that cannot be injected, then randomly choose from them
                L_word_filter = [w for w in words if (len(w) <= L_max_word_size) and (w not in already_injected)]
            
                # Inject into left side
                if L_word_filter:
                    injected_word = random.choice(L_word_filter)
                    already_injected.append(injected_word)               

                
                    substring_to_replace = left_col_words[line][L_random_start_index:L_random_start_index + len(injected_word)]
                    new_string = left_col_words[line].replace(substring_to_replace,injected_word)
                    left_col_words[line] = new_string

                    L_word_rows_indices[line] = injected_word

            

                if R_generate_word and line not in R_rows_added_to:

                    R_rows_added_to.append(line)
            
                    R_random_start_index = random.randint(0,11)
                    R_max_word_size = 11-R_random_start_index

                    # Filter words that cannot be injected, then randomly choose from them
                    R_word_filter = [w for w in words if (len(w) <= R_max_word_size) and (w not in already_injected)]

                    # Inject into right side
                    
                    if R_word_filter:
                        injected_word = random.choice(R_word_filter)
                        already_injected.append(injected_word)               

                    
                        substring_to_replace = right_col_words[line][R_random_start_index:R_random_start_index + len(injected_word)]
                        new_string = right_col_words[line].replace(substring_to_replace,injected_word)
                        right_col_words[line] = new_string

                        R_word_rows_indices[line] = injected_word

      
        target = random.choice(already_injected)

        return (left_col_words,right_col_words,target,L_word_rows_indices, R_word_rows_indices)
       
                

def _hexadecimal_address(L_addresses, R_addresses):
        start_address = random.randint(0x1000,0xF000)

        for i in range(32):

            address_generated = start_address + random.randint(12,48)
            string_val =  f"0x{address_generated:04X}"

            if i < 16:
                L_addresses.append(string_val)
            else:
                R_addresses.append(string_val)

        return (L_addresses, R_addresses)
            

def _pixel_pos_to_indices(mouse_x,mouse_y, x_start,y_start,height, char_width):

    #left column
    
    """
    Stats to consider

    height = 1920
    width = 1080

    first char of first col: 
    L_col_x_start = width*0.2
    L_col_y_start = height* (1/25 + 0.195)
    

    last char of first col (the diagnonal corners): 
    x = width*0.1
    y = height* (17/25 + 0.195)

    width of a char 
    Create a rectangle based on that for mouse detection
    Get coords and translate based on all this information


    Rectangle coordinates:
    top left
    top right
    bottom left
    bottom right:

    translate (x,y) -> (row,col) using start stats

    mouse_x = L_col_x_start + (j*char_width)
    j = int((mouse_x - L_col_x_start) / char_width)
    
    mouse_y = L_col_y_start + height*(i/25 + 0.195)
    mouse_y - L_col_y_start = height*(i/25 + 0.195)

    i = int(25*((mouse_y - L_col_y_start)/(height)) - 0.195)






    My version:
    mouse_x = L_col_x_start + height(j/25 + 0.195)
    j = int((mouse_x - L_col_x_start) / char_width)

    
    
    i = int(25*((mouse_y - L_col_y_start)/(height)) - 0.195)
    j = int((mouse_x - L_col_x_start) / char_width)

    """

    
   

    i = int(25*((mouse_y - y_start)/(height)) - 0.195)
    j = int((mouse_x - x_start) / char_width)
    return (i,j)





def _find_word(character,row,col,word_list):
    """
    If a alphachar is found, look both ways to find the whole word by building it piece by piece

    character -> Any char the mouse hovers over
    X -> The row pos of the char
    Y -> The col pos of the char
    """

    formed_word = ""
   
    if character.isalpha():
        
        # Find start of string and go forward, keeping the boundaries in check

        if(col == 0):
            pass
        else:
            while word_list[row][col-1].isalpha() and col >= 0:
                col -= 1
        
        # Now build forward
        while word_list[row][col+1].isalpha() and col < 12:
                formed_word += word_list[row][col]
                col += 1
        
        formed_word += word_list[row][col]

   
        return formed_word
    else:
        return character
        
        

def _remove_dud(left_col_words, right_col_words, L_word_rows_indices, R_word_rows_indices, target):
    """
    If a pair of brackets is found, this method is triggered
    Remove one incorrect word from either column, replaced with symbols

    column_choice:
        0 -> left column
        1 -> right column

    L_word_rows_indices -> [(row,word)]

    
    Find a 

    Make sure the same pair cannot be selected again

    """
    
    
    rows_tried = []
    sequence = ""

    column_choice = random.randint(0,1) 

    # Left side
    if(column_choice == 0):

        random_row = random.randint(0,15)
        rows_tried.append(random_row)
        
        while random_row not in L_word_rows_indices.keys() and random_row in rows_tried or L_word_rows_indices[random_row] == target:
            random_row = random.randint(0,15)
            
            if random_row in L_word_rows_indices.keys():
                break
            
            rows_tried.append(random_row)
    

        # Replace word with ....

        for c in range(12):
            if left_col_words[random_row][c].isalpha():
                sequence += "."
            else:
                sequence += left_col_words[random_row][c]
        
        left_col_words[random_row] = sequence

    
        
        
    
     # Right side

    rows_tried = []
    if(column_choice == 1):

        random_row = random.randint(0,15)
        rows_tried.append(random_row)
        
        while random_row not in R_word_rows_indices.keys() and random_row in rows_tried or R_word_rows_indices[random_row] == target:
            random_row = random.randint(0,15)
            
            if random_row in R_word_rows_indices.keys():
                break
            
            rows_tried.append(random_row)
    

         # Replace word with ....

        for c in range(12):
            if right_col_words[random_row][c].isalpha():
                sequence += "."
            else:
                sequence += right_col_words[random_row][c]

        right_col_words[random_row] = sequence
        


    return (left_col_words, right_col_words)

        


        


def _reset_tries(attempts_remaining):

    return 4


            
def _search_pairs(row,col,word_list,open_brackets, closed_brackets):
    """
    Search pairs of brackets if hovered char is not an alphachar
    Search carried from 
    Once a pair is found, generate a number between 0,1
    0 -> remove dud
    1 -> reset tries

    Returns a pair of (action,sequence) where action = 0 (remove dud), 1 (reset tries), -1 (no pair found), and sequence = the sequence between the bracket pair
    """
    char = word_list[row][col]
    bracket_index = -1
    sequence =  word_list[row][col]

    if char.isalpha() == False: 
        # Check if open bracket. Store the corresponding index of the closed bracket
        for index,bracket in enumerate(open_brackets):
            if char == bracket:
                bracket_index = index
        
        if bracket_index == -1:
               return (-1,"NO PAIRS")
           
        # Now look through the line until the first closed bracket is found
        for s in range(col + 1,12):
            sequence += word_list[row][s]
            

            if word_list[row][s] == closed_brackets[bracket_index]:

                choice = random.randint(0,1)

                if(choice == 0):
                    return(0,sequence)
                elif(choice == 1):
                    return (1,sequence)

            
    return (-1,"NO PAIRS") 

