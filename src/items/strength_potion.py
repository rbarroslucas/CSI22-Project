from items.item import Item

class StrengthPotion(Item):
    def __init__(self, damageImprovement, duration):
        super().__init__(1, "Healing Potion")
        self.damageImprovement = damageImprovement
        self.duration = duration