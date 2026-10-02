# pfa-week04  
# STAY CLEAN


## How to run it
First, open your terminal, open a brand new text file and paste then enter those command lines:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\stay_clean.py
```


## What I made better

It was entierly made for this assignment, also by talking with my agent I added
a dirt meter, collision feedback and a score.



## How it works

'def draw_player' : This function draws the player, and make his look evolve when the dirt meter rises
'def update_poops' : This function is managing the collision between the charater and the dirt falling. 

I did my own function on line 24: 'def ew'  :
def ew():
    return "EW!"

 to make it work, i added on line84: game["message"] = ew()
 It is in the loop of the 'def update_poops' function. 
 Right after the line:   if poop["rect"].colliderect(player): 
 So that when the poop and the player collide, the message will appear.

 The function def ew is making a ew message appear each time that the poop and player collide !

  

## One undo

asked the agent to add a purple sky. I removed it in the script in the terminal because it made the game harder to read.

## Recording

Vimeo :  https://vimeo.com/1232246867?share=copy&fl=sv&fe=ci

