from items.item import Item

class Barrel(Item):
    def __init__(self, life):
        super().__init__(1, "Barrel")
        self.life = life

