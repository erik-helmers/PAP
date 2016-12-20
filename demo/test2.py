def demo2():
    shown = False
    x = 10
    while True:
            
        a = Navigator(pos=(-400, 0), shown=shown)
        b = Navigator(pos=(0, 0), shown=shown)

        b.left(90)

        c = Navigator(pos=(400, 0), shown=shown)
        c.right(180)
        
        d= Navigator(pos=(0, 0), shown=shown)
        d.right(90)

        for i in range(0, 400, x):
            a.link(b)
            c.link(b)
            a.link(d)
            c.link(d)
                
            
            a.forward(x)
            b.forward(x)
            c.forward(x)
            d.forward(x)

            
            time.sleep(0.02)
        a.link(b)
        c.link(b)
        a.link(d)
        c.link(d)

        while not c_empty():
            for loop in range(4):c_undo()
            time.sleep(0.02)
demo2()


