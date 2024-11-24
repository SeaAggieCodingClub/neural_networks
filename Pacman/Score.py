from Position import *
from Sprites import *

class Score:
    pos = None
    image = None
    active_seconds = 0
    
    active_timer = 2
    l = list()
    
    def __init__(self, type, pos, index):
        self.pos = pos
        self.active_seconds = 0
        
        sprites = ScoreSprites()
        self.image = sprites.get_image(type, index)
        
        Score.l.append(self) # Add to list
    
    def update_scores(fps):
        for score in Score.l: # Check for each score object
            score.active_seconds += 1 / fps
            if score.active_seconds > Score.active_timer:
                Score.l.remove(score) # Remove from list
