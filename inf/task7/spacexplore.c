/**
 * spacexplore.c -- прототип игры управления звездолетом
 * 
 * Copyright (c) 2017, Alexander Borodin <aborod@petrsu.ru>
 *
 * This code is licensed under a MIT-style license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <SDL.h>

#define VXD 5
#define VYD 5


/* Описание экрана игры */
typedef struct _gamescreen {
    /* Поверхность отрисовки */
    SDL_Surface *sprite;
} gamescreen;


/* Описание управляемого пользователем корабля */
typedef struct _spaceship {
    /* Поверхность отрисовки */
    SDL_Surface *sprite;
    /* Координаты корабля */
    int x;
    int y;
    /* Проекции скорости корабля */
    int vx;
    int vy;
} spaceship;


/* Ресурсы и состояние игры  */
typedef struct _game {
    /* Экран игры */
    gamescreen *screen;
    /* Корабль пользователя */
    spaceship *ship;
} game;

/**
 * Инициализирует игру
 * @returns g указатель на структуру состояния игры
 */
game *init();

/**
 * Инициализирует игру
 * @param g указатель на структуру состояния игры
 */
void run(game *g);

/**
 * Отрисовывает объекты в новой позиции
 * @param g указатель на структуру состояния игры
 */
void draw(game *g);


/**
 * Основная программа
 */
int main()
{
    /* Инициализируем игру */
    game *g = init();

    /* Запускаем цикл обработки событий игры */
    run(g);

    return 0;
}


/**
 * Инициализирует игру
 * @returns g указатель на структуру состояния игры
 */
game *init()
{
    /* Создаем структуру представления состояния игры */
    game *g;
    g = (game *) malloc(sizeof(game));
    if (g == NULL) {
        fprintf(stderr, "Not enough memory!");
        exit(EXIT_FAILURE);
    }

    /* Инициализируем библиотеку SDL, используем только видеоподсистему */
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "Couldn't initialize SDL: %s\n", SDL_GetError());
        exit(EXIT_FAILURE);
    }

    /* Регистрируем обработчик завершения программы */
    atexit(SDL_Quit);

    /* Выделяем память для структуры представления экрана */
    g->screen = (gamescreen *) malloc(sizeof(gamescreen));
    if (g->screen == NULL) {
        fprintf(stderr, "Not enough memory!");
        exit(EXIT_FAILURE);
    }    
    
    /* Инициализируем видеорежим */
    g->screen->sprite =
        SDL_SetVideoMode(1024, 768, 0, SDL_HWSURFACE | SDL_DOUBLEBUF);
    if (g->screen->sprite == NULL) {
        fprintf(stderr, "Couldn't set video mode: %s\n", SDL_GetError());
        exit(EXIT_FAILURE);
    }

    /* Выделяем память для структуры представления корабля */
    g->ship = (spaceship *) malloc(sizeof(spaceship));
    if (g->ship == NULL) {
        fprintf(stderr, "Not enough memory!");
        exit(EXIT_FAILURE);
    }

    g->ship->sprite = SDL_LoadBMP("ship.bmp");
    if (g->ship->sprite == NULL) {
        fprintf(stderr, "Couldn't load a bitmap: %s\n", SDL_GetError());
        exit(EXIT_FAILURE);
    }

    /* Устанавливаем заголовок окна */
    SDL_WM_SetCaption("Space explore", NULL);

    return g;
}


/**
 * Инициализирует игру
 * @param g указатель на структуру состояния игры
 */
void run(game * g)
{
    /* Флажок выхода */
    int done = 0;

    /* Продолжаем выполнение, пока не поднят флажок */
    while (!done) {
        /* Структура описания события */
        SDL_Event event;

        /* Извлекаем и обрабатываем все доступные события */
        while (SDL_PollEvent(&event)) {
            switch (event.type) {
            /* Если клавишу нажали */
            case SDL_KEYDOWN:
                switch (event.key.keysym.sym) {
                case SDLK_LEFT:
                    g->ship->vx += -VXD;
                    break;
                case SDLK_RIGHT:
                    g->ship->vx += VXD;
                    break;
                case SDLK_UP:
                    g->ship->vy += -VYD;
                    break;
                case SDLK_DOWN:
                    g->ship->vy += VYD;
                    break;
                case SDLK_ESCAPE:
                    done = 1;
                    break;
                }
                break;
            /* Если клавишу отпустили */
            case SDL_KEYUP:
                switch (event.key.keysym.sym) {
                case SDLK_LEFT:
                    g->ship->vx += VXD;
                    break;
                case SDLK_RIGHT:
                    g->ship->vx += -VXD;
                    break;
                case SDLK_UP:
                    g->ship->vy += VYD;
                    break;
                case SDLK_DOWN:
                    g->ship->vy += -VYD;
                    break;
                default:
                    break;
                }
                break;
            /* Если закрыли окно */
            case SDL_QUIT:
                done = 1;
                break;
            default:
                break;
            }
        }

        g->ship->x += g->ship->vx;
        g->ship->y += g->ship->vy;
        draw(g);
        SDL_Delay(10);
    }
}


/**
 * Отрисовывает объекты в новой позиции
 * @param g указатель на структуру состояния игры
 */
void draw(game * g)
{
    /* Прямоугольники, определяющие зону отображения */
    SDL_Rect src, dest;

    /* Корабль отображаем целиком */
    src.x = 0;
    src.y = 0;
    src.w = g->ship->sprite->w;
    src.h = g->ship->sprite->h;

    /* в новую позицию */
    dest.x = g->ship->x;
    dest.y = g->ship->y;
    dest.w = g->ship->sprite->w;
    dest.h = g->ship->sprite->h;

    /* Выполняем отображение */
    SDL_BlitSurface(g->ship->sprite, &src, g->screen->sprite, &dest);
    
    /* Отрисовываем обновленный экран */
    SDL_Flip(g->screen->sprite);
}
