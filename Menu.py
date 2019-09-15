import pygame
from Algorithms.Informacoes import informacoes
from Algorithms.Botao import button
import Algorithms.Botao as Botao
from Algorithms.Informacoes import WINDOW_SIZE

WIDTH_BUTTON = WINDOW_SIZE/6
HEIGHT_BUTTON = WINDOW_SIZE/12

button_space = WINDOW_SIZE/4
button_margin = (button_space - WIDTH_BUTTON)/2

dijkstra = button(Botao.yellow, button_margin, 2*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'Custo Uniforme')
a_star = button(Botao.red, button_space + button_margin, 2*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'A*')
guloso = button(Botao.purple, 2*button_space + button_margin, 2*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'Guloso')
largura = button(Botao.blue, 3*button_space + button_margin, 2*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'Largura')


dez = button(Botao.red, button_margin, HEIGHT_BUTTON + 4*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, '10x10')
vinte = button(Botao.red, button_space + button_margin, HEIGHT_BUTTON + 4*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, '20x20')
cinquenta = button(Botao.red, 2*button_space + button_margin, HEIGHT_BUTTON + 4*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, '50x50')
cem = button(Botao.red, 3*button_space + button_margin, HEIGHT_BUTTON + 4*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, '100x100')

matriz_aleatoria = button(Botao.red, WINDOW_SIZE/2 + WIDTH_BUTTON, 2*HEIGHT_BUTTON + 6*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'Aleatória')
matriz_vazia = button(Botao.red, WINDOW_SIZE/2 - WIDTH_BUTTON/2, 2*HEIGHT_BUTTON + 6*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'Vazia')
matriz_cheia = button(Botao.red, WINDOW_SIZE/2 - 2*WIDTH_BUTTON, 2*HEIGHT_BUTTON + 6*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'Cheia')


selecionar = button(Botao.white, WINDOW_SIZE/2 - WIDTH_BUTTON/2, 3*HEIGHT_BUTTON + 8*button_margin, WIDTH_BUTTON, HEIGHT_BUTTON, 'Selecionar')


def draw_buttons(screen):
    dijkstra.draw(screen, Botao.dark_gray)
    a_star.draw(screen, Botao.dark_gray)
    guloso.draw(screen, Botao.dark_gray)
    largura.draw(screen, Botao.dark_gray)
    dez.draw(screen, Botao.dark_gray)
    vinte.draw(screen, Botao.dark_gray)
    cinquenta.draw(screen, Botao.dark_gray)
    cem.draw(screen, Botao.dark_gray)
    matriz_cheia.draw(screen, Botao.dark_gray)
    matriz_aleatoria.draw(screen, Botao.dark_gray)
    matriz_vazia.draw(screen, Botao.dark_gray)
    selecionar.draw(screen, Botao.dark_gray)

def main_menu(screen):
    screen.fill(Botao.white)
    fonte = pygame.font.SysFont('Minecraft.ttf', int(WINDOW_SIZE/30) - 1)

    texto = fonte.render("Métodos de busca:", 1, (0, 0, 0))
    textoRect = texto.get_rect()
    textoRect.center = (WINDOW_SIZE/2, button_margin)
    screen.blit(texto, textoRect)

    texto = fonte.render("Tamanho da matriz:", 1, (0, 0, 0))
    textoRect = texto.get_rect()
    textoRect.center = (WINDOW_SIZE / 2,  HEIGHT_BUTTON + 3*button_margin)
    screen.blit(texto, textoRect)

    texto = fonte.render("Geração da barreira:", 1, (0, 0, 0))
    textoRect = texto.get_rect()
    textoRect.center = (WINDOW_SIZE / 2, 2* HEIGHT_BUTTON + 5 * button_margin)
    screen.blit(texto, textoRect)

    texto = fonte.render("By: Lucas Lavratti & Nícolas Marinoni Grande", 1, (0, 0, 0))
    textoRect = texto.get_rect()
    textoRect.center = (WINDOW_SIZE - 160, WINDOW_SIZE - 15 + 100)
    screen.blit(texto, textoRect)

    menu = True
    clock = pygame.time.Clock()
    metodo = ""
    matrix = 0
    formato_matriz = ""
    selecionado = False

    while menu:
        draw_buttons(screen)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                #   BOTÕES DOS MÉTODOS DE BUSCA
                if dijkstra.isOver(pos):
                    dijkstra.color = Botao.green
                    metodo = "dijkstra"
                if a_star.isOver(pos):
                    a_star.color = Botao.green
                    metodo = "a_star"
                if guloso.isOver(pos):
                    guloso.color = Botao.green
                    metodo = "guloso"
                if largura.isOver(pos):
                    largura.color = Botao.green
                    metodo = "largura"

                #   BOTÕES DA MATRIZ
                if dez.isOver(pos):
                    dez.color = Botao.green
                    matrix = 10
                if vinte.isOver(pos):
                    vinte.color = Botao.green
                    matrix = 20
                if cinquenta.isOver(pos):
                    cinquenta.color = Botao.green
                    matrix = 50
                if cem.isOver(pos):
                    cem.color = Botao.green
                    matrix = 100

                # MATRIZ
                if matriz_cheia.isOver(pos):
                    matriz_cheia.color = Botao.green
                    formato_matriz = "cheio"
                if matriz_vazia.isOver(pos):
                    matriz_vazia.color = Botao.green
                    formato_matriz = "vazio"
                if matriz_aleatoria.isOver(pos):
                    matriz_aleatoria.color = Botao.green
                    formato_matriz = "aleatorio"

                # SELECIONAR
                if selecionar.isOver(pos):
                    if matrix != 0 and metodo != "" and formato_matriz != "":
                        selecionar.color = Botao.green
                        menu = False
                    else:
                        if not selecionado:
                            texto = fonte.render("Você precisa selecionar um método, um formato e um tamanho da matriz!", 1, Botao.red)
                            textoRect = texto.get_rect()
                            textoRect.center = (WINDOW_SIZE / 2, 3 * HEIGHT_BUTTON + 7 * button_margin)
                            screen.blit(texto, textoRect)
                            selecionado = True


            if event.type == pygame.MOUSEMOTION:

                #   BOTÕES DOS MÉTODOS DE BUSCA
                if dijkstra.isOver(pos):
                    dijkstra.color = Botao.green
                else:
                    if metodo != 'dijkstra':
                        dijkstra.color = Botao.red

                if a_star.isOver(pos):
                    a_star.color = Botao.green
                else:
                    if metodo != 'a_star':
                        a_star.color = Botao.red

                if guloso.isOver(pos):
                    guloso.color = Botao.green
                else:
                    if metodo != 'guloso':
                        guloso.color = Botao.red

                if largura.isOver(pos):
                    largura.color = Botao.green
                else:
                    if metodo != 'largura':
                        largura.color = Botao.red

                #   BOTÕES DA MATRIZ
                if dez.isOver(pos):
                    dez.color = Botao.green
                else:
                    if matrix != 10:
                        dez.color = Botao.red

                if vinte.isOver(pos):
                    vinte.color = Botao.green
                else:
                    if matrix != 20:
                        vinte.color = Botao.red

                if cinquenta.isOver(pos):
                    cinquenta.color = Botao.green
                else:
                    if matrix != 50:
                        cinquenta.color = Botao.red

                if cem.isOver(pos):
                    cem.color = Botao.green
                else:
                    if matrix != 100:
                        cem.color = Botao.red

                # FORMATO MATRIZ
                if matriz_cheia.isOver(pos):
                    matriz_cheia.color = Botao.green
                else:
                    if formato_matriz != "cheio":
                        matriz_cheia.color = Botao.red
                if matriz_vazia.isOver(pos):
                    matriz_vazia.color = Botao.green
                else:
                    if formato_matriz != "vazio":
                        matriz_vazia.color = Botao.red
                if matriz_aleatoria.isOver(pos):
                    matriz_aleatoria.color = Botao.green
                else:
                    if formato_matriz != "aleatorio":
                        matriz_aleatoria.color = Botao.red


                #   SELECIONAR
                if selecionar.isOver(pos):
                    selecionar.color = Botao.green
                else:
                    selecionar.color = Botao.white

        pygame.display.update()
        clock.tick(60)

    return metodo, matrix, formato_matriz
