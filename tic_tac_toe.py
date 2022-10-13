from tkinter import Tk
from tkinter import messagebox, BOTH
from tkinter.ttk import Button, Frame, Label
from interface import Battlefield as _Battlefield
from interface import Cage as _Cage
from interface import Data as _Data
from interface import Game as _Game


class Game(_Game):
    def __init__(self, size_field: int):
        root = Tk()

        data = Data()
        Board(root, data, size_field)

        root.mainloop()


class Data(_Data):
    def __init__(self):
        self.__x_wins = 0
        self.__zero_wins = 0
        self.__draws = 0
        self.__text = ''

        data = Label(text=self.score)
        data.pack()
        self.data = data

    @property
    def score(self):
        self.__text = f'X wins: {self.__x_wins}\tO wins: {self.__zero_wins}\t Draws: {self.__draws}'.expandtabs(20)
        return self.__text

    @score.setter
    def score(self, value):
        self.__text = value

    def increase_x_wins(self):
        self.__x_wins += 1

    def increase_zero_wins(self):
        self.__zero_wins += 1

    def increase_draws(self):
        self.__draws += 1


class Board(_Battlefield):
    def __init__(self, root: Tk, data_board: Data, dimension: int):
        self.__check_dimension(dimension)
        self.switch = True
        self.frame = Frame(root)
        self.frame.pack()
        self.__data_board = data_board

        self.cells = []
        for row in range(dimension):
            cells_row = []
            for column in range(dimension):
                cell = Cell(self, column, row)
                cells_row.append(cell)
            self.cells.append(cells_row)
        Button(text='NEW GAME', command=self.__new_game).pack(fill=BOTH)

    def __new_game(self):
        self.switch = True
        for row in self.cells:
            for cell in row:
                cell.text = ''
                cell.cell['state'] = 'normal'

    def __disable_cells(self):
        for row in self.cells:
            for cell in row:
                cell.cell['state'] = 'disable'

    def check(self):
        win = self.__check_diagonals() or self.__check_rows() or self.__check_columns()
        if win and self.switch:
            messagebox.showinfo('Winner', 'O - won')
            self.__disable_cells()
            self.__data_board.increase_zero_wins()
        elif win and not self.switch:
            messagebox.showinfo('Winner', 'X - won')
            self.__disable_cells()
            self.__data_board.increase_x_wins()
        elif self.__check_draw():
            messagebox.showinfo('Winner', 'Draw')
            self.__disable_cells()
            self.__data_board.increase_draws()
        self.__data_board.data['text'] = self.__data_board.score

    def __check_draw(self):
        all_cells = [cell.text for row in self.cells for cell in row if cell.text]
        return len(all_cells) == len(self.cells) ** 2

    def __check_rows(self) -> bool:
        for row in self.cells:
            text_row = [cell.text for cell in row]
            if text_row[0] and len(set(text_row)) == 1:
                return True

    def __check_columns(self) -> bool:
        for column in zip(*self.cells):
            text_column = [cell.text for cell in column]
            if text_column[0] and len(set(text_column)) == 1:
                return True

    def __check_diagonals(self) -> bool:
        main_diagonal = [cell.text for i, row in enumerate(self.cells) for j, cell in enumerate(row) if i == j]
        second_diagonal = [cell.text for i, row in enumerate(self.cells) for j, cell in enumerate(row) if
                           i == len(row) - j - 1]
        check_main_diagonal = main_diagonal[0] and len(set(main_diagonal)) == 1
        check_second_diagonal = second_diagonal[0] and len(set(second_diagonal)) == 1
        return check_second_diagonal or check_main_diagonal

    @staticmethod
    def __check_dimension(dimension) -> bool:
        if not isinstance(dimension, int):
            raise TypeError(f'Dimension should be integer. Got: {type(dimension)}')
        elif dimension < 3:
            raise ValueError(f'Dimension should be more or equal to 3. Got: {dimension}')
        return True


class Cell(_Cage):
    def __init__(self, board: Board, column: int, row: int, text: str = ''):
        self.__check_number(column)
        self.__check_number(row)
        self.__check_text(text)

        cell = Button(board.frame, text=text, command=lambda b=board: self.__change_text(b))
        cell.grid(ipadx=80, ipady=65, column=column, row=row)
        self.cell = cell

    @property
    def text(self):
        return self.cell['text']

    @text.setter
    def text(self, value: str):
        self.cell['text'] = value

    def __change_text(self, board: Board):
        if board.switch and not self.text:
            self.text = 'X'
            board.switch = not board.switch
        elif not board.switch and not self.text:
            self.text = 'O'
            board.switch = not board.switch
        board.check()

    @staticmethod
    def __check_number(number) -> bool:
        if not isinstance(number, int):
            raise TypeError(f'Column and Row should be integers. Got {type(number)}')
        elif number < 0:
            raise ValueError(f'Column and Row values should be more than zero. Got {number}')
        return True

    @staticmethod
    def __check_text(text) -> bool:
        if not isinstance(text, str):
            raise TypeError(f'Text should be string. Got {type(text)}')
        elif text not in ('O', 'X', ''):
            raise ValueError(f'Text should be "O" or "X" or "". Got: {text}')
        return True


if __name__ == '__main__':
    Game(4)
