while True:
    inp = input('Color >')
    color = eval(inp)
    print(tuple(map(lambda x: round(x/255, 2), color))+(1,))