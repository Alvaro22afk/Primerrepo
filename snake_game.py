import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# --- Configuración de la Pantalla ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Juego de la Serpiente (Snake) por Gemini')

# --- Colores (formato RGB) ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# --- Configuración del Juego ---
TAMANO_BLOQUE = 20
VELOCIDAD_JUEGO = 15

# --- Fuentes de Texto ---
fuente_puntuacion = pygame.font.SysFont("consolas", 35)
fuente_game_over = pygame.font.SysFont("impact", 50)


def mostrar_puntuacion(puntuacion):
    """Muestra la puntuación en la pantalla."""
    valor = fuente_puntuacion.render("Puntuación: " + str(puntuacion), True, BLANCO)
    pantalla.blit(valor, [10, 10])


def dibujar_serpiente(lista_serpiente):
    """Dibuja todos los segmentos de la serpiente."""
    for bloque in lista_serpiente:
        pygame.draw.rect(pantalla, VERDE, [bloque[0], bloque[1], TAMANO_BLOQUE, TAMANO_BLOQUE])


def juego():
    """Función principal que contiene la lógica del juego."""
    game_over = False
    game_close = False

    # Posición inicial de la serpiente
    x_serpiente = ANCHO_PANTALLA / 2
    y_serpiente = ALTO_PANTALLA / 2

    # Cambio de posición (velocidad inicial)
    x_cambio = 0
    y_cambio = 0

    # Lista que almacena los bloques de la serpiente
    lista_serpiente = []
    longitud_serpiente = 1

    # Posición aleatoria de la comida
    comida_x = round(random.randrange(0, ANCHO_PANTALLA - TAMANO_BLOQUE) / TAMANO_BLOQUE) * TAMANO_BLOQUE
    comida_y = round(random.randrange(0, ALTO_PANTALLA - TAMANO_BLOQUE) / TAMANO_BLOQUE) * TAMANO_BLOQUE

    reloj = pygame.time.Clock()

    # --- Bucle Principal del Juego ---
    while not game_over:

        # --- Pantalla de "Game Over" ---
        while game_close:
            pantalla.fill(NEGRO)
            mensaje_perdiste = fuente_game_over.render("¡PERDISTE!", True, ROJO)
            mensaje_instrucciones = fuente_puntuacion.render("Presiona 'C' para continuar o 'Q' para salir", True, BLANCO)
            
            pantalla.blit(mensaje_perdiste, [ANCHO_PANTALLA / 2 - 120, ALTO_PANTALLA / 3])
            pantalla.blit(mensaje_instrucciones, [ANCHO_PANTALLA / 2 - 300, ALTO_PANTALLA / 2])
            
            mostrar_puntuacion(longitud_serpiente - 1)
            pygame.display.update()

            # Opciones al perder
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        juego() # Reinicia el juego

        # --- Manejo de Eventos (Teclado) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_cambio == 0:
                    x_cambio = -TAMANO_BLOQUE
                    y_cambio = 0
                elif event.key == pygame.K_RIGHT and x_cambio == 0:
                    x_cambio = TAMANO_BLOQUE
                    y_cambio = 0
                elif event.key == pygame.K_UP and y_cambio == 0:
                    y_cambio = -TAMANO_BLOQUE
                    x_cambio = 0
                elif event.key == pygame.K_DOWN and y_cambio == 0:
                    y_cambio = TAMANO_BLOQUE
                    x_cambio = 0
        
        # --- Lógica de Colisiones con los Bordes ---
        if x_serpiente >= ANCHO_PANTALLA or x_serpiente < 0 or y_serpiente >= ALTO_PANTALLA or y_serpiente < 0:
            game_close = True

        # Actualizar la posición de la serpiente
        x_serpiente += x_cambio
        y_serpiente += y_cambio

        # --- Actualización y Dibujo en Pantalla ---
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, ROJO, [comida_x, comida_y, TAMANO_BLOQUE, TAMANO_BLOQUE])
        
        cabeza_serpiente = []
        cabeza_serpiente.append(x_serpiente)
        cabeza_serpiente.append(y_serpiente)
        lista_serpiente.append(cabeza_serpiente)
        
        # Mantiene la longitud de la serpiente
        if len(lista_serpiente) > longitud_serpiente:
            del lista_serpiente[0]

        # --- Lógica de Colisión con su propio cuerpo ---
        for bloque in lista_serpiente[:-1]:
            if bloque == cabeza_serpiente:
                game_close = True

        dibujar_serpiente(lista_serpiente)
        mostrar_puntuacion(longitud_serpiente - 1)

        pygame.display.update()

        # --- Lógica de Comer la Comida ---
        if x_serpiente == comida_x and y_serpiente == comida_y:
            comida_x = round(random.randrange(0, ANCHO_PANTALLA - TAMANO_BLOQUE) / TAMANO_BLOQUE) * TAMANO_BLOQUE
            comida_y = round(random.randrange(0, ALTO_PANTALLA - TAMANO_BLOQUE) / TAMANO_BLOQUE) * TAMANO_BLOQUE
            longitud_serpiente += 1

        # Controla la velocidad del juego
        reloj.tick(VELOCIDAD_JUEGO)

    # Salir de Pygame y del programa
    pygame.quit()
    sys.exit()

# Iniciar el juego
juego()