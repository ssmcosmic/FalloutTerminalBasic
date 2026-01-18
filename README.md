# FalloutTerminalBasic

<img width="498" height="100" alt="ascii-art-text (1)" src="https://github.com/user-attachments/assets/a28377da-1dd8-4888-804f-bab365dbb3cf" />



I found the Fallout game series to be super fun after initially dropping it and restarting years later. In every game, there was always this aspect of terminal hacking that I quite enjoyed, and I wondered whether I could implement a basic version of the terminal. Similar to how I had dropped Fallout 4 the first time I played it, I had also dropped this project, until now.

This project is a work-in-progress, and for now, aims to implement the most basic version of the terminal. I aim to improve and add more features in later versions. There's gonna be a lot of bugs and the program does not really do anything once the target is found yet, but I'll probably add more later on.



<img width="544" height="100" alt="ascii-art-text (2)" src="https://github.com/user-attachments/assets/52e10ab3-6d35-414a-9cda-c94bdf80ab22" />

1) Store the font file (FSEX300.ttf), main.py file and the wordbank.txt in the same folder
2) Change the folder directory inside main.py to the folder in step 1
3) Ensure the versions match those below (the program might still work but is not guaranteed)
4) The program should now run


<img width="517" height="100" alt="ascii-art-text (3)" src="https://github.com/user-attachments/assets/4047f478-757b-489f-ac7c-fe665319ec0b" />

The program basically splits of words generated into two columns (left and right).
Operations on each column are the same; each column is represented as a 2D array (each row is a string so that individiual characters can be accessed).
The program displays according to the resolution of the screen, so that resizing should generally not cause any issues and it helps with pixel calculations

**Here's how the program identifies words and symbol pairs:**

1. Create a rectangle for each column within which mouse inputs are registered
2. Map each pixel within the rectangle to an index corresponding to the 2D array. It sounds complicated but this is achieved with two lines by doing some smart math:

*i = int(25*((mouse_y - y_start)/(height)) - 0.195) <br>
*j = int((mouse_x - x_start) / char_width) <br>
*i,j = row,col

**How is this derived? Within any rectangle, since we are looking at a 2D array, the first character should be at index (0,0) for the relevant column. Consider the pixel positions when the text was rendered in the left column:**

Recall: def renderText(text,font,color,relative_x,relative_y,center = True):

In line 497: <br>
renderText(left_col_words[i], text_font, words_color, 0.2, (i+1)/25 + 0.195, center=False)

The first character is rendered at (X,Y) = (0.2, (0+1)/25 + 0.195) when i = 0

**Consider the mouse x coordinate obtained when we hover over the first character:**

mouse_x = L_col_x_start + (j*char_width)
j = int((mouse_x - L_col_x_start) / char_width)

L_col_x_start = The first X value = 0.2. Every other character is an offset of this value <br>
j = column value
char_width = obtained from the font used <br>
Each next character is a char_width from the previous, so a loop can be used to obtain the next character from the current one


**Now consider the mouse y coordinate obtained when we hover over the first character:**


mouse_y = L_col_y_start + height*(i/25 + 0.195)<br>
i = int(25*((mouse_y - L_col_y_start)/(height)) - 0.195)

L_col_y_start = The first Y value = 1/25 + 0.195. Every other character is an offset of this value <br>
height = the height of the screen. We are using relative pixel values which is why we need to multiply the Y value with height (since that is how the pixel is rendered in this program)

Finally, leaving us with:

row = int(25*((mouse_y - y_start)/(height)) - 0.195)<br>
col = int((mouse_x - x_start) / char_width)

For each column i.e left_col_words and right_col_words.

<img width="458" height="100" alt="ascii-art-text (4)" src="https://github.com/user-attachments/assets/d4a242ba-3e73-4ace-9d3a-fb865a8ef918" />
1. Add audio (background and when hovering / clicking) <br>
2. Add a green box over hovered characters and words <br>
3. Upon finding the correct word, lead to a different screen








<img width="372" height="100" alt="ascii-art-text" src="https://github.com/user-attachments/assets/2c7f1a55-378a-449e-ba5e-d7592cc91aba" />
          
pygame-ce: 2.5.6

python: 3.14.0
