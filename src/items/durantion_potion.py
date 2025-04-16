from items.potion import Potion

class DurationPotion(Potion):
    def __init__(self, name, buff, buff_duration, image):
        super().__init__(name, buff, image)
        self.buff_duration = buff_duration