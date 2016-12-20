#TEST
def demo1():
    background("black")
    setColor("white")

    right(90)
    forward(20)
    while True:
        right(90)
        for l in range(0, 1250, +5):
            forward(l)
            right(170)
            time.sleep(0.01)
        main._Pen.reset() #Not clear
        while not empty(): undo(), time.sleep(0.01)


demo1()


