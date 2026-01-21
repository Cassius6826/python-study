class Clock:
    id = None
    price = None

    def ring(self):
        import winsound
        winsound.Beep(2500, 3000)
        print("铃声响起")

clock_1 = Clock()
clock_1.id = 1
clock_1.price = 100
print(clock_1.id)
print(clock_1.price)
clock_1.ring()