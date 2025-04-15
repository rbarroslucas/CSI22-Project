from items.potion import Potion

class HealingPotion(Potion):
    def __init__(self, healEffect):
        super().__init__(1, "Healing Potion")
        self.healEffect = healEffect