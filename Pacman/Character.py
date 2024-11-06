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
    
    def check_warp_tunnels(self, warp_tunnels):
        pos = self.pos
        if pos.x < warp_tunnels['right']: # If grid indices are out of range to the right
                self.pos.x = warp_tunnels['left'] # Teleport to other side
        elif pos.x > warp_tunnels['left']:  # If grid indices are out of range to the left
            self.pos.x = warp_tunnels['right'] # Teleport to other side`

