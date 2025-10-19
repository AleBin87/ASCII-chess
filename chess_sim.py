import re
from collections import defaultdict
import os
import sys
import copy


sq_pattern = re.compile(r"^[a-h][1-8]$", re.IGNORECASE)


class Chessboard:
    en_passant = False
    check = False

    def __init__(self):
        squares = defaultdict()
        rows = ["1", "2", "3", "4", "5", "6", "7", "8"]
        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for c in columns:
            for r in rows:
                squares[c + r] = " "
        self.squares = squares

    def __str__(self) -> str:
        return f"""
    a   b   c   d   e   f   g   h
   -------------------------------
8 | {self.squares["a8"]} | {self.squares["b8"]} | {self.squares["c8"]} | {self.squares["d8"]} | {self.squares["e8"]} | {self.squares["f8"]} | {self.squares["g8"]} | {self.squares["h8"]} | 8
  |--- --- --- --- --- --- --- ---| 
7 | {self.squares["a7"]} | {self.squares["b7"]} | {self.squares["c7"]} | {self.squares["d7"]} | {self.squares["e7"]} | {self.squares["f7"]} | {self.squares["g7"]} | {self.squares["h7"]} | 7
  |--- --- --- --- --- --- --- ---|
6 | {self.squares["a6"]} | {self.squares["b6"]} | {self.squares["c6"]} | {self.squares["d6"]} | {self.squares["e6"]} | {self.squares["f6"]} | {self.squares["g6"]} | {self.squares["h6"]} | 6
  |--- --- --- --- --- --- --- ---|
5 | {self.squares["a5"]} | {self.squares["b5"]} | {self.squares["c5"]} | {self.squares["d5"]} | {self.squares["e5"]} | {self.squares["f5"]} | {self.squares["g5"]} | {self.squares["h5"]} | 5
  |--- --- --- --- --- --- --- ---|
4 | {self.squares["a4"]} | {self.squares["b4"]} | {self.squares["c4"]} | {self.squares["d4"]} | {self.squares["e4"]} | {self.squares["f4"]} | {self.squares["g4"]} | {self.squares["h4"]} | 4
  |--- --- --- --- --- --- --- ---|
3 | {self.squares["a3"]} | {self.squares["b3"]} | {self.squares["c3"]} | {self.squares["d3"]} | {self.squares["e3"]} | {self.squares["f3"]} | {self.squares["g3"]} | {self.squares["h3"]} | 3
  |--- --- --- --- --- --- --- ---|
2 | {self.squares["a2"]} | {self.squares["b2"]} | {self.squares["c2"]} | {self.squares["d2"]} | {self.squares["e2"]} | {self.squares["f2"]} | {self.squares["g2"]} | {self.squares["h2"]} | 2
  |--- --- --- --- --- --- --- ---|
1 | {self.squares["a1"]} | {self.squares["b1"]} | {self.squares["c1"]} | {self.squares["d1"]} | {self.squares["e1"]} | {self.squares["f1"]} | {self.squares["g1"]} | {self.squares["h1"]} | 1
   -------------------------------
    a   b   c   d   e   f   g   h              
              """


class Piece:
    on_the_board = 1

    def __init__(self, color: str, position: str, board: Chessboard):
        if color.lower() not in ["black", "white"]:
            raise ValueError("Invalid color")
        if sq_pattern.search(position) == None:
            raise ValueError("Invalid position")
        self.color = color
        self.position = position


class Pawn(Piece):
    valore = 1
    en_passant = 0

    def __init__(self, color, position, board):
        super().__init__(color, position, board)

    def move(self, start_pos, final_pos, board) -> int:
        if start_pos == final_pos:
            # print("Invalid move")
            return 0
        if (
            self.color == "white"
            and start_pos[1] == "2"
            and start_pos[0] == final_pos[0]
            and (int(final_pos[1]) - int(start_pos[1])) <= 2
            and board.squares[final_pos] == " "
        ):
            if (int(final_pos[1]) - int(start_pos[1])) == 2:
                if board.squares[final_pos[0] + str(int(final_pos[1]) - 1)] == " ":
                    # self.position = final_pos
                    # print(f"Pawn to {final_pos}")
                    if (
                        sq_pattern.search(chr(ord(final_pos[0]) - 1) + final_pos[1])
                        != None
                        and board.squares[chr(ord(final_pos[0]) - 1) + final_pos[1]]
                        != " "
                        and isinstance(
                            board.squares[chr(ord(final_pos[0]) - 1) + final_pos[1]],
                            Pawn,
                        )
                    ):
                        board.squares[
                            chr(ord(final_pos[0]) - 1) + final_pos[1]
                        ].en_passant = 1
                        self.en_passant = 1
                    if (
                        sq_pattern.search(chr(ord(final_pos[0]) + 1) + final_pos[1])
                        != None
                        and board.squares[chr(ord(final_pos[0]) + 1) + final_pos[1]]
                        != " "
                        and isinstance(
                            board.squares[chr(ord(final_pos[0]) + 1) + final_pos[1]],
                            Pawn,
                        )
                    ):
                        board.squares[
                            chr(ord(final_pos[0]) + 1) + final_pos[1]
                        ].en_passant = 1
                        self.en_passant = 1
                    return 1
                else:
                    # print("Invalid move")
                    return 0
            else:
                # print(f"Pawn to {final_pos}")
                return 1
        elif (
            self.color == "black"
            and start_pos[1] == "7"
            and start_pos[0] == final_pos[0]
            and (int(start_pos[1]) - int(final_pos[1])) <= 2
            and board.squares[final_pos] == " "
        ):
            if (int(start_pos[1]) - int(final_pos[1])) == 2:
                if board.squares[final_pos[0] + str(int(final_pos[1]) + 1)] == " ":
                    # self.position = final_pos
                    # print(f"Pawn to {final_pos}")
                    if (
                        sq_pattern.search(chr(ord(final_pos[0]) - 1) + final_pos[1])
                        != None
                        and board.squares[chr(ord(final_pos[0]) - 1) + final_pos[1]]
                        != " "
                        and isinstance(
                            board.squares[chr(ord(final_pos[0]) - 1) + final_pos[1]],
                            Pawn,
                        )
                    ):
                        board.squares[
                            chr(ord(final_pos[0]) - 1) + final_pos[1]
                        ].en_passant = 1
                        self.en_passant = 1
                    if (
                        sq_pattern.search(chr(ord(final_pos[0]) + 1) + final_pos[1])
                        != None
                        and board.squares[chr(ord(final_pos[0]) + 1) + final_pos[1]]
                        != " "
                        and isinstance(
                            board.squares[chr(ord(final_pos[0]) + 1) + final_pos[1]],
                            Pawn,
                        )
                    ):
                        board.squares[
                            chr(ord(final_pos[0]) + 1) + final_pos[1]
                        ].en_passant = 1
                        self.en_passant = 1
                    return 1
                else:
                    # print("Invalid move")
                    return 0
            else:
                # print(f"Pawn to {final_pos}")
                return 1
        elif (
            self.color == "white"
            and (int(final_pos[1]) - int(start_pos[1])) == 1
            and (ord(start_pos[0]) - ord(final_pos[0])) == 1
            and board.squares[final_pos] != " "
        ):
            # self.position = final_pos
            # print(f"Pawn to {final_pos}")
            return 1
        elif (
            self.color == "white"
            and (int(final_pos[1]) - int(start_pos[1])) == 1
            and (ord(final_pos[0]) - ord(start_pos[0])) == 1
            and board.squares[final_pos] != " "
        ):
            # self.position = final_pos
            # print(f"Pawn to {final_pos}")
            return 1
        elif (
            self.color == "black"
            and (int(start_pos[1]) - int(final_pos[1])) == 1
            and (ord(start_pos[0]) - ord(final_pos[0])) == 1
            and board.squares[final_pos] != " "
        ):
            # self.position = final_pos
            # print(f"Pawn to {final_pos}")
            return 1
        elif (
            self.color == "black"
            and (int(start_pos[1]) - int(final_pos[1])) == 1
            and (ord(final_pos[0]) - ord(start_pos[0])) == 1
            and board.squares[final_pos] != " "
        ):
            # self.position = final_pos
            # print(f"Pawn to {final_pos}")
            return 1
        elif (
            self.color == "white"
            and (start_pos[0] == final_pos[0])
            and (int(final_pos[1]) - int(start_pos[1]) == 1)
            and board.squares[final_pos] == " "
        ):
            # self.position = final_pos
            # print(f"Pawn to {final_pos}")
            return 1
        elif (
            self.color == "black"
            and (start_pos[0] == final_pos[0])
            and (int(start_pos[1]) - int(final_pos[1]) == 1)
            and board.squares[final_pos] == " "
        ):
            # self.position = final_pos
            # print(f"Pawn to {final_pos}")
            return 1
        elif self.en_passant == 1:
            if (
                self.color == "white"
                and int(start_pos[1]) == int(final_pos[1]) - 1
                and ord(start_pos[0]) == (ord(final_pos[0]) - 1)
                and isinstance(board.squares[final_pos[0] + start_pos[1]], Pawn)
                and board.squares[final_pos[0] + start_pos[1]].en_passant == 1
            ):
                # self.position = final_pos
                # print(f"Pawn to {final_pos}")
                board.squares[final_pos[0] + start_pos[1]].on_the_board = 0
                board.squares[final_pos[0] + start_pos[1]] = " "
                return 1
            elif (
                self.color == "white"
                and int(start_pos[1]) == int(final_pos[1]) - 1
                and ord(start_pos[0]) == (ord(final_pos[0]) + 1)
                and isinstance(board.squares[final_pos[0] + start_pos[1]], Pawn)
                and board.squares[final_pos[0] + start_pos[1]].en_passant == 1
            ):
                # self.position = final_pos
                # print(f"Pawn to {final_pos}")
                board.squares[final_pos[0] + start_pos[1]].on_the_board = 0
                board.squares[final_pos[0] + start_pos[1]] = " "
                return 1
            elif (
                self.color == "black"
                and int(start_pos[1]) == int(final_pos[1]) + 1
                and ord(start_pos[0]) == (ord(final_pos[0]) - 1)
                and isinstance(board.squares[final_pos[0] + start_pos[1]], Pawn)
                and board.squares[final_pos[0] + start_pos[1]].en_passant == 1
            ):
                # self.position = final_pos
                # print(f"Pawn to {final_pos}")
                board.squares[final_pos[0] + start_pos[1]].on_the_board = 0
                board.squares[final_pos[0] + start_pos[1]] = " "
                return 1
            elif (
                self.color == "black"
                and int(start_pos[1]) == int(final_pos[1]) + 1
                and ord(start_pos[0]) == (ord(final_pos[0]) + 1)
                and isinstance(board.squares[final_pos[0] + start_pos[1]], Pawn)
                and board.squares[final_pos[0] + start_pos[1]].en_passant == 1
            ):
                # self.position = final_pos
                # print(f"Pawn to {final_pos}")
                board.squares[final_pos[0] + start_pos[1]].on_the_board = 0
                board.squares[final_pos[0] + start_pos[1]] = " "
                return 1
            else:
                return 0
        else:
            # print("Invalid move")
            return 0

    def promote(self): ...

    def __str__(self) -> str:
        if self.color == "white":
            return "\u2659"
        else:
            return "\u265f"


class Knight(Piece):
    valore = 3

    def __init__(self, color, position, board):
        super().__init__(color, position, board)

    def move(self, start_pos, final_pos, board) -> int:
        if start_pos == final_pos:
            # print("Invalid move")
            return 0
        if (
            (
                (ord(final_pos[0]) == ord(start_pos[0]) + 2)
                and (int(final_pos[1]) == int(start_pos[1]) + 1)
            )
            or (
                (ord(final_pos[0]) == ord(start_pos[0]) + 1)
                and (int(final_pos[1]) == int(start_pos[1]) + 2)
            )
            or (
                (ord(final_pos[0]) == ord(start_pos[0]) - 1)
                and (int(final_pos[1]) == int(start_pos[1]) - 2)
            )
            or (
                (ord(final_pos[0]) == ord(start_pos[0]) - 2)
                and (int(final_pos[1]) == int(start_pos[1]) - 1)
            )
            or (
                (ord(final_pos[0]) == ord(start_pos[0]) - 1)
                and (int(final_pos[1]) == int(start_pos[1]) + 2)
            )
            or (
                (ord(final_pos[0]) == ord(start_pos[0]) - 2)
                and (int(final_pos[1]) == int(start_pos[1]) + 1)
            )
            or (
                (ord(final_pos[0]) == ord(start_pos[0]) + 1)
                and (int(final_pos[1]) == int(start_pos[1]) - 2)
            )
            or (
                (ord(final_pos[0]) == ord(start_pos[0]) + 2)
                and (int(final_pos[1]) == int(start_pos[1]) - 1)
            )
        ):
            # self.position = final_pos
            # print(f"Knight to {final_pos}")
            return 1
        else:
            # print("Invalid move")
            return 0

    def __str__(self) -> str:
        if self.color == "white":
            return "\u2658"
        else:
            return "\u265e"


class Bishop(Piece):
    valore = 3

    def __init__(self, color, position, board):
        super().__init__(color, position, board)

    def move(self, start_pos, final_pos, board) -> int:
        i = 1
        if start_pos == final_pos:
            # print("Invalid move")
            return 0
        while i <= 9:
            if i == 9:
                # print("Invalid move")
                return 0
            if (
                ord(start_pos[0]) == ord(final_pos[0]) - i
                or ord(start_pos[0]) == ord(final_pos[0]) + i
            ) and (
                int(start_pos[1]) == int(final_pos[1]) + i
                or int(start_pos[1]) == int(final_pos[1]) - i
            ):
                if self.color == "white":
                    if (
                        board.squares[final_pos] != " "
                        and board.squares[final_pos].color == "white"
                    ):
                        # print("Invalid move")
                        return 0
                else:
                    if (
                        board.squares[final_pos] != " "
                        and board.squares[final_pos].color == "black"
                    ):
                        # print("Invalid move")
                        return 0
                i -= 1
                while i > 0:
                    if (
                        ord(final_pos[0]) > ord(start_pos[0])
                        and final_pos[1] > start_pos[1]
                    ):  # up/right
                        if (
                            board.squares[
                                chr(ord(final_pos[0]) - i) + str(int(final_pos[1]) - i)
                            ]
                            != " "
                        ):
                            # print("Invalid move")
                            return 0
                    elif (
                        ord(final_pos[0]) > ord(start_pos[0])
                        and final_pos[1] < start_pos[1]
                    ):  # down/right
                        if (
                            board.squares[
                                chr(ord(final_pos[0]) - i) + str(int(final_pos[1]) + i)
                            ]
                            != " "
                        ):
                            # print("Invalid move")
                            return 0
                    elif (
                        ord(final_pos[0]) < ord(start_pos[0])
                        and final_pos[1] > start_pos[1]
                    ):  # up/left
                        if (
                            board.squares[
                                chr(ord(final_pos[0]) + i) + str(int(final_pos[1]) - i)
                            ]
                            != " "
                        ):
                            # print("Invalid move")
                            return 0
                    elif (
                        ord(final_pos[0]) < ord(start_pos[0])
                        and final_pos[1] < start_pos[1]
                    ):  # down/left
                        if (
                            board.squares[
                                chr(ord(final_pos[0]) + i) + str(int(final_pos[1]) + i)
                            ]
                            != " "
                        ):
                            # print("Invalid move")
                            return 0
                    i -= 1
                # self.position = final_pos
                # print(f"Bishop to {final_pos}")
                return 1
            i += 1
        return 0

    def __str__(self) -> str:
        if self.color == "white":
            return "\u2657"
        else:
            return "\u265d"


class Rook(Piece):
    valore = 5
    can_castle = 1

    def __init__(self, color, position, board):
        super().__init__(color, position, board)

    def move(self, start_pos, final_pos, board) -> int:
        if start_pos[0] == final_pos[0] and start_pos != final_pos:
            for x in range(
                min(int(start_pos[1]), int(final_pos[1])) + 1,
                max(int(start_pos[1]), int(final_pos[1])),
            ):
                if board.squares[start_pos[0] + str(x)] != " ":
                    # print("Invalid move")
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                # print("Invalid move")
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                # print("Invalid move")
                return 0
            # self.position = final_pos
            # print(f"Rook to {final_pos}")
            return 1
        elif start_pos[1] == final_pos[1] and start_pos != final_pos:
            for x in range(
                min(ord(start_pos[0]), ord(final_pos[0])) + 1,
                max(ord(start_pos[0]), ord(final_pos[0])),
            ):
                if board.squares[chr(x) + start_pos[1]] != " ":
                    # print("Invalid move")
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                # print("Invalid move")
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                # print("Invalid move")
                return 0
            # self.position = final_pos
            # print(f"Rook to {final_pos}")
            return 1
        else:
            # print("Invalid move")
            return 0

    def __str__(self) -> str:
        if self.color == "white":
            return "\u2656"
        else:
            return "\u265c"


class Queen(Piece):
    valore = 9

    def __init__(self, color, position, board):
        super().__init__(color, position, board)

    def move(self, start_pos, final_pos, board) -> int:
        if start_pos == final_pos:
            # print("Invalid move")
            return 0
        if start_pos[0] == final_pos[0]:
            for x in range(
                min(int(start_pos[1]), int(final_pos[1])) + 1,
                max(int(start_pos[1]), int(final_pos[1])),
            ):
                if board.squares[start_pos[0] + str(x)] != " ":
                    # print("Invalid move")
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                # print("Invalid move")
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                # print("Invalid move")
                return 0
            # self.position = final_pos
            # print(f"Queen to {final_pos}")
            return 1
        elif start_pos[1] == final_pos[1]:
            for x in range(
                min(ord(start_pos[0]), ord(final_pos[0])) + 1,
                max(ord(start_pos[0]), ord(final_pos[0])),
            ):
                if board.squares[chr(x) + start_pos[1]] != " ":
                    # print("Invalid move")
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                # print("Invalid move")
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                # print("Invalid move")
                return 0
            # self.position = final_pos
            # print(f"Queen to {final_pos}")
            return 1
        else:
            i = 1
            while i <= 9:
                if i == 9:
                    # print("Invalid move")
                    return 0
                if (
                    ord(start_pos[0]) == ord(final_pos[0]) - i
                    or ord(start_pos[0]) == ord(final_pos[0]) + i
                ) and (
                    int(start_pos[1]) == int(final_pos[1]) + i
                    or int(start_pos[1]) == int(final_pos[1]) - i
                ):
                    if self.color == "white":
                        if (
                            board.squares[final_pos] != " "
                            and board.squares[final_pos].color == "white"
                        ):
                            # print("Invalid move")
                            return 0
                    else:
                        if (
                            board.squares[final_pos] != " "
                            and board.squares[final_pos].color == "black"
                        ):
                            # print("Invalid move")
                            return 0
                    i -= 1
                    while i > 0:
                        if (
                            ord(final_pos[0]) > ord(start_pos[0])
                            and final_pos[1] > start_pos[1]
                        ):  # up/right
                            if (
                                board.squares[
                                    chr(ord(final_pos[0]) - i)
                                    + str(int(final_pos[1]) - i)
                                ]
                                != " "
                            ):
                                # print("Invalid move")
                                return 0
                        elif (
                            ord(final_pos[0]) > ord(start_pos[0])
                            and final_pos[1] < start_pos[1]
                        ):  # down/right
                            if (
                                board.squares[
                                    chr(ord(final_pos[0]) - i)
                                    + str(int(final_pos[1]) + i)
                                ]
                                != " "
                            ):
                                # print("Invalid move")
                                return 0
                        elif (
                            ord(final_pos[0]) < ord(start_pos[0])
                            and final_pos[1] > start_pos[1]
                        ):  # up/left
                            if (
                                board.squares[
                                    chr(ord(final_pos[0]) + i)
                                    + str(int(final_pos[1]) - i)
                                ]
                                != " "
                            ):
                                # print("Invalid move")
                                return 0
                        elif (
                            ord(final_pos[0]) < ord(start_pos[0])
                            and final_pos[1] < start_pos[1]
                        ):  # down/left
                            if (
                                board.squares[
                                    chr(ord(final_pos[0]) + i)
                                    + str(int(final_pos[1]) + i)
                                ]
                                != " "
                            ):
                                # print("Invalid move")
                                return 0
                        i -= 1
                    # self.position = final_pos
                    # print(f"Queen to {final_pos}")
                    return 1
                i += 1
        # print("Invalid move")
        return 0

    def __str__(self) -> str:
        if self.color == "white":
            return "\u2655"
        else:
            return "\u265b"


class King(Piece):
    valore = 1000
    can_castle = 1

    def __init__(self, color, position, board):
        super().__init__(color, position, board)

    def move(self, start_pos, final_pos, board) -> int:
        if (
            start_pos == "e1"
            and final_pos == "g1"
            and board.squares["f1"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["h1"], Rook)
            and board.squares["h1"].can_castle == 1
        ):
            # print("King castle")
            # self.position = final_pos
            board.squares["h1"].position = "f1"
            board.squares["f1"] = board.squares["h1"]
            board.squares["h1"] = " "
            return 1
        elif (
            start_pos == "e1"
            and final_pos == "c1"
            and board.squares["d1"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["a1"], Rook)
            and board.squares["a1"].can_castle == 1
        ):
            # print("King castle")
            # self.position = final_pos
            board.squares["a1"].position = "d1"
            board.squares["d1"] = board.squares["a1"]
            board.squares["a1"] = " "
            return 1
        elif (
            start_pos == "e8"
            and final_pos == "g8"
            and board.squares["f8"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["h8"], Rook)
            and board.squares["h8"].can_castle == 1
        ):
            # print("King castle")
            # self.position = final_pos
            board.squares["h8"].position = "f8"
            board.squares["f8"] = board.squares["h8"]
            board.squares["h8"] = " "
            return 1
        elif (
            start_pos == "e8"
            and final_pos == "c8"
            and board.squares["d8"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["a8"], Rook)
            and board.squares["a8"].can_castle == 1
        ):
            # print("King castle")
            # self.position = final_pos
            board.squares["a8"].position = "d8"
            board.squares["d8"] = board.squares["a8"]
            board.squares["a8"] = " "
            return 1
        if (
            (
                ord(final_pos[0]) in range(ord(start_pos[0]) - 1, ord(start_pos[0]) + 2)
            )  # use +2 because range excludes the final number
            and int(final_pos[1]) in range(int(start_pos[1]) - 1, int(start_pos[1]) + 2)
            and start_pos != final_pos
        ):
            if self.color == "white":
                if (
                    board.squares[final_pos] != " "
                    and board.squares[final_pos].color == "white"
                ):
                    # print("Invalid move")
                    return 0
            else:
                if (
                    board.squares[final_pos] != " "
                    and board.squares[final_pos].color == "black"
                ):
                    # print("Invalid move")
                    return 0
            # self.position = final_pos
            # print(f"King to {final_pos}")
            return 1
        else:
            # print("Invalid move")
            return 0

    def __str__(self) -> str:
        if self.color == "white":
            return "\u2654"
        else:
            return "\u265a"


def main():
    game = Chessboard()
    pieces = start_game(game)  # Initialize all pieces
    for piece in pieces:  # Put pieces on the chessboard
        game.squares[piece.position] = piece
        if isinstance(piece, King):
            if piece.color == "white":
                wking = piece
            else:
                bking = piece
    white_turn = True

    while True:
        # checking for en_passant on any Pawn
        for piece in pieces:
            if isinstance(piece, Pawn) and piece.en_passant == 1:
                game.en_passant = True
                break

        print(game)
        while True:
            try:
                move_from, move_to = (
                    input(
                        "Insert the coordinates of the piece to move and where to move it, divided by a space: "
                    )
                    .lower()
                    .strip()
                    .split()
                )
                break
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue

        os.system("cls")
        if game.check == True:
            if white_turn == True:
                print("White is in check!")
            else:
                print("Black is in check!")

        if (
            sq_pattern.search(move_from) == None or sq_pattern.search(move_to) == None
        ):  # Check for valid coordinates
            print("Invalid square")
            continue

        if white_turn == True:
            if (
                game.squares[move_from] == " "
                or game.squares[move_from].color == "black"
            ):
                print("White to move")
                continue
        else:
            if (
                game.squares[move_from] == " "
                or game.squares[move_from].color == "white"
            ):
                print("Black to move")
                continue

        # in case of check the only valid moves are the ones that ends the check
        if game.check == True:
            game.check = False
            game_in_check = Chessboard()
            pieces_in_check = copy.deepcopy(pieces)  # duplicate pieces

            for piece in pieces_in_check:  # put new pieces on the new board
                if piece.on_the_board == 1:
                    game_in_check.squares[piece.position] = piece
                    if isinstance(piece, King):
                        if piece.color == "white":
                            wking_in_check = piece
                        else:
                            bking_in_check = piece

            if game_in_check.squares[move_from] != " " and game_in_check.squares[
                move_from
            ].move(
                move_from, move_to, game_in_check
            ):  # try if the move is legal on a copy of the board
                if game_in_check.squares[move_to] != " ":
                    game_in_check.squares[move_to].on_the_board = 0
                game_in_check.squares[move_from].position = move_to
                game_in_check.squares[move_to] = game_in_check.squares[move_from]
                game_in_check.squares[move_from] = " "

                if white_turn == True:
                    for piece in pieces_in_check:
                        if piece.color == "black" and piece.on_the_board == 1:
                            if piece.move(
                                piece.position, wking_in_check.position, game_in_check
                            ):
                                game.check = True
                                break
                else:
                    for piece in pieces_in_check:
                        if piece.color == "white" and piece.on_the_board == 1:
                            if piece.move(
                                piece.position, bking_in_check.position, game_in_check
                            ):
                                game.check = True
                                break
            else:
                game.check = True

        if (
            game.check == True
        ):  # the last move didn't resolve the check so I ask for a new move
            continue

        if not game.squares[move_from].move(move_from, move_to, game):
            print("Invalid move")

        if game.squares[move_from].move(move_from, move_to, game):
            print(f"{game.squares[move_from]} {move_to}")
            if game.squares[move_to] != " ":
                game.squares[move_to].on_the_board = (
                    0  # Eliminate the piece that was taken
                )
            if isinstance(game.squares[move_from], King) or isinstance(
                game.squares[move_from], Rook
            ):
                game.squares[move_from].can_castle = 0
            game.squares[move_from].position = move_to
            game.squares[move_to] = game.squares[move_from]
            game.squares[move_from] = " "

            # Looking for checks
            if white_turn == True:
                if game.squares[move_to].move(move_to, bking.position, game):
                    game.check = True
                    print("Check!")
            else:
                if game.squares[move_to].move(move_to, wking.position, game):
                    game.check = True
                    print("Check!")

            if white_turn == True:
                white_turn = False
            else:
                white_turn = True
            if game.en_passant == True:  # resets en_passant on the board and on Pawns
                game.en_passant = False
                for piece in pieces:
                    if isinstance(piece, Pawn) and piece.en_passant == 1:
                        piece.en_passant = 0


def start_game(game):
    Pa = Pawn("white", "a2", game)
    Pb = Pawn("white", "b2", game)
    Pc = Pawn("white", "c2", game)
    Pd = Pawn("white", "d2", game)
    Pe = Pawn("white", "e2", game)
    Pf = Pawn("white", "f2", game)
    Pg = Pawn("white", "g2", game)
    Ph = Pawn("white", "h2", game)
    pa = Pawn("black", "a7", game)
    pb = Pawn("black", "b7", game)
    pc = Pawn("black", "c7", game)
    pd = Pawn("black", "d7", game)
    pe = Pawn("black", "e7", game)
    pf = Pawn("black", "f7", game)
    pg = Pawn("black", "g7", game)
    ph = Pawn("black", "h7", game)
    Ra = Rook("white", "a1", game)
    Rh = Rook("white", "h1", game)
    Nb = Knight("white", "b1", game)
    Ng = Knight("white", "g1", game)
    Bc = Bishop("white", "c1", game)
    Bf = Bishop("white", "f1", game)
    Qw = Queen("white", "d1", game)
    Kw = King("white", "e1", game)
    ra = Rook("black", "a8", game)
    rh = Rook("black", "h8", game)
    nb = Knight("black", "b8", game)
    ng = Knight("black", "g8", game)
    bc = Bishop("black", "c8", game)
    bf = Bishop("black", "f8", game)
    qb = Queen("black", "d8", game)
    kb = King("black", "e8", game)
    return [
        Pa,
        Pb,
        Pc,
        Pd,
        Pe,
        Pf,
        Pg,
        Ph,
        pa,
        pb,
        pc,
        pd,
        pe,
        pf,
        pg,
        ph,
        Ra,
        Rh,
        Nb,
        Ng,
        Bc,
        Bf,
        Qw,
        Kw,
        ra,
        rh,
        nb,
        ng,
        bc,
        bf,
        qb,
        kb,
    ]


if __name__ == "__main__":
    main()
