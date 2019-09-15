WINDOW_SIZE = 600

def informacoes(QUANTIDADE):
    #  Size of squares in screen
    RELACAO = WINDOW_SIZE / QUANTIDADE

    # This sets the WIDTH and HEIGHT of each grid location (90% da relacao)
    WIDTH = RELACAO * 0.9
    HEIGHT = RELACAO * 0.9

    # This sets the margin between each cell (10% da relacao)
    MARGIN = RELACAO * 0.1

    return WIDTH, HEIGHT, MARGIN
