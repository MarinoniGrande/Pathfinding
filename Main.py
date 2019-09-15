# A* = a_star
# Guloso = best_first
# Custo Uniforme = dijkstra
# Largura = breadth_first

import pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.finder import visitados
from pathfinding.finder.a_star import AStarFinder  # A*
from pathfinding.finder.best_first import BestFirst  # Guloso
from pathfinding.finder.dijkstra import DijkstraFinder  # Custo Uniforme
from pathfinding.finder.breadth_first import BreadthFirstFinder  # Largura
import pygame
from Algorithms.Menu import main_menu
from Algorithms.Informacoes import informacoes
from Algorithms.Botao import button
import Algorithms.Botao as Botao
from Algorithms.Informacoes import WINDOW_SIZE
import numpy as np
import time


# Initialize pygame
pygame.init()

font = "Minecraft.ttf"
fonte = pygame.font.SysFont('Minecraft.ttf', int(WINDOW_SIZE / 30) - 1)
# Set the HEIGHT and WIDTH of the screen
screen = pygame.display.set_mode([WINDOW_SIZE, WINDOW_SIZE + 120])

# Set title of screen
pygame.display.set_caption("Métodos de busca")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates (60 FPS)
clock = pygame.time.Clock()
metodo, QUANTIDADE, formato_matriz = main_menu(screen)
print("Método a ser utilizado: " + metodo + ". Matriz: " + str(QUANTIDADE) + "x" + str(
    QUANTIDADE) + ". Formato: " + formato_matriz + ".")

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.


grid = []

#  INFO DOS BOTOES
WIDTH, HEIGHT, MARGIN = informacoes(QUANTIDADE)

if formato_matriz == "vazio":
    for row in range(QUANTIDADE):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(QUANTIDADE):
            grid[row].append(1)  # Append a cell

    # Constrói display (Fundo preto com os botões em branco)
    screen.fill(Botao.black)
    color = Botao.white
    for row in range(QUANTIDADE):
        for column in range(QUANTIDADE):
            button(Botao.white, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT,
                   "").draw(screen)

elif formato_matriz == "cheio":
    for row in range(QUANTIDADE):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(QUANTIDADE):
            grid[row].append(0)  # Append a cell

    # Constrói display (Fundo preto com os botões em branco)
    screen.fill(Botao.black)
    color = Botao.dark_gray
    for row in range(QUANTIDADE):
        for column in range(QUANTIDADE):
            button(Botao.dark_gray, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT,
                   "").draw(screen)

else:
    grid_random = np.random.randint(2, size=(QUANTIDADE, QUANTIDADE))
    for row in range(QUANTIDADE):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(QUANTIDADE):
            grid[row].append(0)  # Append a cell

    for row in range(QUANTIDADE):
        for column in range(QUANTIDADE):
            grid[row][column] = grid_random[row][column]
    # Constrói display (Fundo preto com os botões em branco)
    screen.fill(Botao.black)
    color = Botao.white
    for row in range(QUANTIDADE):
        for column in range(QUANTIDADE):
            if grid[row][column] == 1:
                button(Botao.white, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT,
                       "").draw(screen)
            else:
                button(Botao.dark_gray, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                       HEIGHT,
                       "").draw(screen)
# -------- Main Program Loop -----------
custo = 0
path = 0
runs = 0
opcao_selecionada = ""
is_comecar = False
start, end = [None, None], [None, None]
margem_botoes = 10
no_inicial = button(Botao.light_blue, margem_botoes, WINDOW_SIZE + 20, 100, 60, "Nó inicial")
no_final = button(Botao.light_blue, 3 * margem_botoes + 100, WINDOW_SIZE + 20, 100, 60, "Nó final")
barreira = button(Botao.light_blue, 5 * margem_botoes + 2 * 100, WINDOW_SIZE + 20, 100, 60, "Barreira")
apagar = button(Botao.light_blue, 7 * margem_botoes + 3 * 100, WINDOW_SIZE + 20, 100, 60, "Apagar")
comecar = button(Botao.red, 9 * margem_botoes + 4 * 100, WINDOW_SIZE + 20, 100, 60, "Começar")
botao_preto = button(Botao.black, 0, WINDOW_SIZE + 20, WINDOW_SIZE, 60, "teste")
finalizado = False
while not done:
    color_of_block = (255, 255, 255, 255)
    no_inicial.draw(screen, Botao.white)
    no_final.draw(screen, Botao.white)
    barreira.draw(screen, Botao.white)
    comecar.draw(screen, Botao.white)
    apagar.draw(screen, Botao.white)
    for event in pygame.event.get():  # User did something

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if no_inicial.isOver(pos):
                no_inicial.color = Botao.green
            else:
                if opcao_selecionada != "start":
                    no_inicial.color = Botao.light_blue

            if no_final.isOver(pos):
                no_final.color = Botao.green
            else:
                if opcao_selecionada != "end":
                    no_final.color = Botao.light_blue

            if barreira.isOver(pos):
                barreira.color = Botao.green
            else:
                if opcao_selecionada != "barreira":
                    barreira.color = Botao.light_blue

            if comecar.isOver(pos):
                comecar.color = Botao.green
            else:
                if opcao_selecionada != "comecar":
                    comecar.color = Botao.red

            if apagar.isOver(pos):
                apagar.color = Botao.green
            else:
                if opcao_selecionada != "apagar":
                    apagar.color = Botao.light_blue

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = int(pos[0] // (WIDTH + MARGIN))
            row = int(pos[1] // (HEIGHT + MARGIN))
            # Set that location to one
            # print("Click ", pos, "Grid coordinates: ", row, column)
            color_of_block = screen.get_at(pos)
            if start == [row, column]:
                start = [None, None]
            if end == [row, column]:
                end = [None, None]

            if no_inicial.isOver(pos):
                no_inicial.color = Botao.green
                opcao_selecionada = "start"
            if no_final.isOver(pos):
                no_final.color = Botao.green
                opcao_selecionada = "end"
            if barreira.isOver(pos):
                barreira.color = Botao.green
                opcao_selecionada = "barreira"
            if apagar.isOver(pos):
                apagar.color = Botao.green
                opcao_selecionada = "apagar"

            if comecar.isOver(pos):
                comecar.color = Botao.green
                opcao_selecionada = "comecar"
                if start != [None, None] and end != [None, None]:
                    texto = fonte.render("", 1, Botao.white)
                    textoRect = texto.get_rect()
                    textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 100)
                    screen.blit(texto, textoRect)
                    is_comecar = True
                else:
                    texto = fonte.render("Você precisa selecionar o nó inicial e o nó final!", 1, Botao.white)
                    textoRect = texto.get_rect()
                    textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 100)
                    screen.blit(texto, textoRect)

            try:

                if opcao_selecionada == "barreira":
                    grid[row][column] = 0
                    button(Botao.dark_gray, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN,
                           WIDTH, HEIGHT, "").draw(screen)
                elif opcao_selecionada == "start":
                    grid[row][column] = 1
                    if start[0] != None and start[1] != None:
                        button(Botao.white, (MARGIN + WIDTH) * start[1] + MARGIN,
                               (MARGIN + HEIGHT) * start[0] + MARGIN,
                               WIDTH, HEIGHT, "").draw(screen)
                    start = [row, column]
                    button(Botao.red, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                           HEIGHT, "").draw(screen)
                elif opcao_selecionada == "end":
                    grid[row][column] = 1
                    if end[0] != None and end[1] != None:
                        button(Botao.white, (MARGIN + WIDTH) * end[1] + MARGIN, (MARGIN + HEIGHT) * end[0] + MARGIN,
                               WIDTH, HEIGHT, "").draw(screen)
                    end = [row, column]
                    button(Botao.green, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                           HEIGHT, "").draw(screen)
                elif opcao_selecionada == "apagar":
                    grid[row][column] = 1
                    button(Botao.white, (MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                           HEIGHT, "").draw(screen)

            except IndexError:
                continue
            # for row in grid:
            #     print(row)
            # print("\n")

            # print("start: " + str(start) + ", end: " + str(end) + "\n")
            if is_comecar and opcao_selecionada == "comecar" and not finalizado:
                grid_procura = Grid(matrix=grid)
                start = grid_procura.node(start[1], start[0])
                end = grid_procura.node(end[1], end[0])
                if metodo == "a_star":
                    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                elif metodo == "guloso":
                    finder = BestFirst(diagonal_movement=DiagonalMovement.always)
                elif metodo == "dijkstra":
                    finder = DijkstraFinder(diagonal_movement=DiagonalMovement.always)
                else:
                    finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.always)
                start_time = time.time()
                path, runs = finder.find_path(start, end, grid_procura)
                end_time = time.time()
                total_time = end_time-start_time
                for no in visitados:
                    if grid[no.x][no.y] != '0' and [no.x, no.y] != [start.x, start.y] and [no.x, no.y] != [end.x, end.y]:
                        button(Botao.light_blue, (MARGIN + WIDTH) * no.x + MARGIN, (MARGIN + HEIGHT) * no.y + MARGIN, WIDTH,
                               HEIGHT, "").draw(screen)
                    if (no.x, no.y) in path:
                        if [no.x, no.y] != [start.x, start.y] and [no.x, no.y] != [end.x, end.y]:
                            button(Botao.blue, (MARGIN + WIDTH) * no.x + MARGIN, (MARGIN + HEIGHT) * no.y + MARGIN,
                                   WIDTH,
                                   HEIGHT, "").draw(screen)
                print("Número de nós visitados: ", len(set(visitados)))
                print(path)
                print("start: (" + str(start.x) + ", " + str(start.y) + "), end: (" + str(end.x) + ", " + str(end.y) + ")\n")
                print('operations:', runs, 'path length:', len(path))
                print('tempo: ' + str(total_time))
                custo = 0
                anterior = None
                for no in path:
                    node = grid_procura.node(no[0], no[1])
                    if anterior != None:
                        if metodo == "largura":
                            custo += finder.calc_cost(anterior, node)
                        else:
                            custo = finder.calc_cost(anterior, node)  # Soma na função, por isso não +=
                        anterior = node
                    else:
                        anterior = node

                print('custo:', custo)
                print(grid_procura.grid_str(path=path, start=start, end=end))
                # for no in visitados:
                #     print(str(no.x) + " " + str(no.y))
                finalizado = True
    if finalizado:
        botao_preto.draw(screen, Botao.black)
        font_fim = pygame.font.SysFont('comicsans', 30)
        texto = font_fim.render("Número de nós visitados: " + str(len(set(visitados))), 1, Botao.white)
        textoRect = texto.get_rect()
        textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 20)
        screen.blit(texto, textoRect)
        texto = font_fim.render("Custo da solução: " + str(round(custo, 2)), 1, Botao.white)
        textoRect = texto.get_rect()
        textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 40)
        screen.blit(texto, textoRect)
        texto = font_fim.render("Tamanho do caminho encontrado: " + str(len(path)), 1, Botao.white)
        textoRect = texto.get_rect()
        textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 60)
        screen.blit(texto, textoRect)
        texto = font_fim.render("Tempo: " + str(total_time), 1, Botao.white)
        textoRect = texto.get_rect()
        textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 80)
        screen.blit(texto, textoRect)
        if metodo == "a_star":
            texto = font_fim.render("A*. Caminho final apresentado no terminal.", 1, Botao.white)
            textoRect = texto.get_rect()
            textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 100)
            screen.blit(texto, textoRect)
        elif metodo == "guloso":
            texto = font_fim.render("Guloso. Caminho final apresentado no terminal.", 1, Botao.white)
            textoRect = texto.get_rect()
            textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 100)
            screen.blit(texto, textoRect)
        elif metodo == "dijkstra":
            texto = font_fim.render("Custo uniforme. Caminho final apresentado no terminal.", 1, Botao.white)
            textoRect = texto.get_rect()
            textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 100)
            screen.blit(texto, textoRect)
        else:
            texto = font_fim.render("Largura. Caminho final apresentado no terminal.", 1, Botao.white)
            textoRect = texto.get_rect()
            textoRect.center = (WINDOW_SIZE / 2, WINDOW_SIZE + 100)
            screen.blit(texto, textoRect)
    # Limit to 60 frames per second
    clock.tick(60)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
