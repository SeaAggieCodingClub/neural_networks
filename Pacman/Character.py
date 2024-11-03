# Parent class over Pacman and Ghosts
class Character:
    images = None
    id = None
    pos = None
    dir = None
    speed = None
    base_speed = None
    
    # Adds a given magnitude to the position of the character depending on the direction
    def move(self, speed):
        match self.dir:
            case 'w':
                self.pos.y -= speed
            case 'a':
                self.pos.x += speed
            case 's':
                self.pos.y += speed
            case 'd':
                self.pos.x -= speed
