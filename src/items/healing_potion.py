from items.item import Item

class HealingPotion(Item):
    def __init__(self, healEffect):
        super().__init__(1, "Healing Potion")
        self.healEffect = healEffect