from os import system as sys
from math import sin
from time import sleep
import csv


class AnsiColors:
    end = '\u001b[0m'

    class color:
        white = 255, 255, 255
        black = 0, 0, 0
        red = 255, 0, 0
        blue = 0, 0, 255

    @staticmethod
    def rgb(r: int, g: int, b: int, is_background: bool = True) -> str:
        args = r, g, b
        for arg in args:
            if not 0 <= arg <= 255:
                raise ValueError('AnsiColors.rgb can get only 0..255 values')

        return f'\u001b[{3 + is_background}8;2;{r};{g};{b}m'

    @staticmethod
    def inverted(r: int, g: int, b: int) -> tuple:
        return 255 - r, 255 - g, 255 - b


class Painter:

    @staticmethod
    def bicolor(matrix: list[list[int]], main_color: tuple, addit_color: tuple):
        for row in matrix:
            for cell in row:
                print(AnsiColors.rgb(*(main_color, addit_color)[cell]), end=' ')
            print(AnsiColors.end)

    @staticmethod
    def plot(
            main_color: tuple, addit_color: tuple,
            max_x: int,
            max_y: float,
            step_y: float,
            accuracy: float,
            func: callable,
            title: str = '',
            min_y: float = 0,
            min_x: int = 0,
            step_x: float = 1.0
    ):
        bg_ac = AnsiColors.rgb(*addit_color)
        bg_mc = AnsiColors.rgb(*main_color)
        fg = AnsiColors.rgb(*AnsiColors.inverted(*addit_color), is_background=False)
        cell_width = 3
        add_cells = int(1 / step_x) - 1

        print(f'{AnsiColors.rgb(*addit_color, is_background=False)}'
              f'{AnsiColors.rgb(*AnsiColors.inverted(*addit_color))}'
              f'{title:^{9 + cell_width * (max_x - min_x) * (add_cells + 1) + cell_width * add_cells}}'
              f'{AnsiColors.end}')
        y = max_y + step_y
        while (y := y - step_y) > min_y - step_y / 2:
            print(f'{fg}{bg_ac}{y:>5.2f}', end=' ')
            for x in range(min_x, max_x + 1):
                for step_i in range(add_cells + 1):
                    if abs(func(x + step_x * step_i) - y) < accuracy:
                        print(f'{bg_mc}', end=' '*cell_width)
                    else:
                        print(f'{bg_ac}', end=' '*cell_width)
            print(AnsiColors.end)

        print(f'{fg}{bg_ac}', end='      ')
        for x in range(min_x, max_x + 1):
            print(f'{x:>3}', end='')
            for _ in range(add_cells):
                print('', end=' '*cell_width)
        print(AnsiColors.end)


def get_switz_matrix() -> list[list[int]]:
    def _line(value: int, length: int) -> list[int]:
        return [value] * length

    def _draw_by_commands(matr: list, *cmds):
        for cmd in cmds:
            if cmd == 'A':
                for _ in range(2):
                    matr.append(_line(0, 22))
            elif cmd == 'B':
                for _ in range(2):
                    matr.append(_line(0, 9) + _line(1, 4) + _line(0, 9))
            elif cmd == 'C':
                for _ in range(2):
                    matr.append(_line(0, 4) + _line(1, 14) + _line(0, 4))
            else:
                raise ValueError(f'Unknown command: "{cmd}"')

    matrix = list()
    _draw_by_commands(matrix, *list('ABCBA'))

    return matrix


def get_pattern_matrix(width: int, height: int) -> list[list[int]]:
    line_patterns = [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0] * 2,
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0] * 2,
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0] * 2,
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0] * 2,
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0] * 2,
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] * 2
    ]
    pattern_width = len(line_patterns[0])
    pattern_height = len(line_patterns)
    matrix = list()
    for i in range(height):
        matrix.append(
            (
                    line_patterns[i % pattern_height]
                    * (width // pattern_width + 1)
            )
            [:width]
        )

    return matrix


def function_base_task(x: int) -> float:
    return x / 3


def function_additional_task(x: int) -> float:
    return 2 * sin(x)


def score_book_data():
    def _strip_quotes(string: str) -> str:
        return string.strip('"')

    total_cnt, ok_cnt = 0, 0
    with open('books.csv', 'r', encoding='ansi') as f:
        for vals in csv.reader(f, delimiter=';'):
            if total_cnt == 0:
                total_cnt = 1
                continue

            total_cnt += 1
            # Для возраста 16 лет и остальные (до 10 скачиваний и выше)
            if int(vals[5]) >= 16 and int(vals[8]) >= 10:
                ok_cnt += 1

    return ok_cnt, total_cnt


if __name__ == '__main__':
    print('The Switzerland\'s flag!')
    Painter.bicolor(
        matrix=get_switz_matrix(),
        main_color=AnsiColors.color.red,
        addit_color=AnsiColors.color.white
    )
    input('Press Enter to go next\n>>')
    sys('cls')
    print('48x24 picture is produced by 22x6 pattern')
    Painter.bicolor(
        matrix=get_pattern_matrix(48, 24),
        main_color=AnsiColors.color.black,
        addit_color=AnsiColors.color.white
    )
    input('Press Enter to go next\n>>')
    sys('cls')
    print('Plot is produced by step_y=1, accuracy=0.5')
    Painter.plot(
        main_color=AnsiColors.color.red,
        addit_color=AnsiColors.color.black,
        max_x=25,
        max_y=9,
        step_y=1,
        accuracy=0.5,
        func=function_base_task,
        title='y = x / 3'
    )
    input('Press Enter to go next\n>>')
    sys('cls')
    print('Plot is produced by step_y=0.5, accuracy=0.2')
    Painter.plot(
        main_color=AnsiColors.color.red,
        addit_color=AnsiColors.color.black,
        max_x=25,
        max_y=9,
        step_y=0.5,
        accuracy=0.2,
        func=function_base_task,
        title='y = x / 3'
    )
    input('Press Enter to go next\n>>')
    sys('cls')
    speed = 8
    steps = 60 * speed
    for i in range(steps):
        sys('cls')
        print(f'animation progress: [{i + 1}/{steps}] ({(i + 1) / steps * 100:.2f}%)')
        Painter.plot(
            main_color=AnsiColors.color.red,
            addit_color=AnsiColors.color.black,
            max_x=5 + i,
            min_x=i,
            max_y=1,
            min_y=-1,
            step_y=0.2,
            step_x=0.333,
            accuracy=0.1,
            func=sin,
            title='y = sin(x)'
        )
        sleep(1 / speed)

    input('Press Enter to go next\n>>')
    sys('cls')

    selected_books_cnt, total_books_cnt = score_book_data()
    sel_prt = selected_books_cnt / total_books_cnt
    dgm_width = 60
    print(f'selectors:\n\tage >= 16\n\tdownloads >= 10\n'
          f'result: {sel_prt * 100:.2f}% of books\n'
          f'{AnsiColors.rgb(*AnsiColors.color.red)}{" " * int(dgm_width * sel_prt)}'
          f'{AnsiColors.rgb(*AnsiColors.color.blue)}{" " * int(dgm_width * (1 - sel_prt))}'
          f'{AnsiColors.end}')
    input('Press Enter to exit\n>>')
