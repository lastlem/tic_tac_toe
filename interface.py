from abc import abstractmethod, ABC


class Game(ABC):
    def __init__(self):
        """
        Main class which connects everything
        """


class Data(ABC):
    @abstractmethod
    def __init__(self):
        """
        Creates a board with data about games
        """

    @property
    @abstractmethod
    def score(self) -> dict:
        """
        Text with data about x wins, zero wins and draws
        Example:

        :return: dict["x wins": int, "zero wins": int, "draws": int]
        """
        raise NotImplementedError()

    @abstractmethod
    def increase_x_wins(self) -> None:
        """
        Increase x wins counter for one

        :return: None
        """

    @abstractmethod
    def increase_zero_wins(self) -> None:
        """
        Add one to zero_wins

        :return: None
        """

    @abstractmethod
    def increase_draws(self) -> None:
        """
        Add one to draws

        :return: None
        """


class Battlefield(ABC):
    @abstractmethod
    def __init__(self, size_field: int):
        """
        Creates board with cells with given dimension

        :param size_field: number of cells in column
        """

    @abstractmethod
    def check(self):
        """
        Checks if anyone has won and shows message if yes

        """


class Cage(ABC):
    @abstractmethod
    def __init__(self, column: int, row: int, text: str = ''):
        """
        Creates cell in the given place

        :param column: int
        :param row: int
        """

    @property
    @abstractmethod
    def text(self) -> str:
        """
        Text on the cage

        :return: str
        """
        raise NotImplementedError()

    @text.setter
    @abstractmethod
    def text(self, value: str) -> None:
        """
        Set text on the cage

        :param value: "" or "O" or "X"
        :return: None
        """
        raise NotImplementedError()
