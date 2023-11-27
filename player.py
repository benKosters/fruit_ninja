
class Player:
    
    
    def __init__(self):
        """constructor for a player object
        """
        self.name = ""
        self.score = 0
        self.lives = 3
        
        
    def set_name(self,name):
        """Sets the name of a player
        """
        self.name = name
    
    def get_name(self):
        """used to return the name of the player
        """
        return self.name
        
    def set_score(self,score):
        """Sets score of player
        """
        self.score = score
        
    def increment_score(self):
        """Increases score of player
        """
        self.score+= 1
        
    def get_score(self):
        """Returns score of player
        """
        return self.score
    
        
    def remove_life(self):
        """Removes a life
        """
        self.lives -= 1
        
    def get_lives(self):
        """Returns player life
        """
        return self.lives
        