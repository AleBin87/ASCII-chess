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

    def __init__(self, color: str, position: str, board: Chessboard):
        if color.lower() not in ["black", "white"]:
            raise ValueError("Invalid color")
        if sq_pattern.search(position) == None:
            raise ValueError("Invalid position")
        self.color = color
        self.position = position
        self.on_the_board = 1


class Pawn(Piece):
    valore = 1
    en_passant = 0

    def __init__(self, color, position, board):
        super().__init__(color, position, board)

    def move(self, start_pos, final_pos, board) -> int:
        start_col, start_row = start_pos[0], start_pos[1]
        final_col, final_row = final_pos[0], final_pos[1]
        if self.color == "white":
            mov = 1
            starting_row = "2"
        else:
            mov = -1
            starting_row = "7"

        if (  # normal move, 1 row forward
            start_col == final_col
            and (int(start_row) + mov == int(final_row))
            and board.squares[final_pos] == " "
        ):
            return 1
        elif (  # 2 rows forward if in starting position
            start_col == final_col
            and start_row == starting_row
            and (int(start_row) + (mov * 2) == int(final_row))
            and board.squares[start_col + str(int(start_row) + mov)] == " "
            and board.squares[final_pos] == " "
        ):
            return 2
        elif (  # diagonal capture
            int(start_row) + mov == int(final_row)
            and (
                (ord(final_col) == ord(start_col) + 1)
                or (ord(final_col) == ord(start_col) - 1)
            )
            and board.squares[final_pos] != " "
        ):
            return 1
        elif (  # en passant
            int(start_row) + mov == int(final_row)
            and (
                (ord(final_col) == ord(start_col) + 1)
                or (ord(final_col) == ord(start_col) - 1)
            )
            and board.squares[final_pos] == " "
            and isinstance(board.squares[final_pos[0] + start_pos[1]], Pawn)
            and board.squares[final_pos[0] + start_pos[1]].en_passant == 1
            and board.squares[start_pos].en_passant == 1
        ):
            return 3
        else:
            return 0

    def promote(self, position, board) -> Piece:
        while True:
            promote = (
                input("Promote to (N=knight, B=bishop, R=rook, Q=queen): ")
                .lower()
                .strip()
            )
            if promote in ["n", "b", "r", "q"]:
                match promote:
                    case "n":
                        if position[1] == "8":
                            return Knight("white", position, board)
                        else:
                            return Knight("black", position, board)
                    case "b":
                        if position[1] == "8":
                            return Bishop("white", position, board)
                        else:
                            return Bishop("black", position, board)
                    case "r":
                        if position[1] == "8":
                            return Rook("white", position, board)
                        else:
                            return Rook("black", position, board)
                    case "q":
                        if position[1] == "8":
                            return Queen("white", position, board)
                        else:
                            return Queen("black", position, board)

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
            return 1
        else:
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
            return 0
        while i <= 9:
            if i == 9:
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
                        return 0
                else:
                    if (
                        board.squares[final_pos] != " "
                        and board.squares[final_pos].color == "black"
                    ):
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
                            return 0
                    i -= 1
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
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                return 0
            return 1
        elif start_pos[1] == final_pos[1] and start_pos != final_pos:
            for x in range(
                min(ord(start_pos[0]), ord(final_pos[0])) + 1,
                max(ord(start_pos[0]), ord(final_pos[0])),
            ):
                if board.squares[chr(x) + start_pos[1]] != " ":
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                return 0
            return 1
        else:
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
            return 0
        if start_pos[0] == final_pos[0]:
            for x in range(
                min(int(start_pos[1]), int(final_pos[1])) + 1,
                max(int(start_pos[1]), int(final_pos[1])),
            ):
                if board.squares[start_pos[0] + str(x)] != " ":
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                return 0
            return 1
        elif start_pos[1] == final_pos[1]:
            for x in range(
                min(ord(start_pos[0]), ord(final_pos[0])) + 1,
                max(ord(start_pos[0]), ord(final_pos[0])),
            ):
                if board.squares[chr(x) + start_pos[1]] != " ":
                    return 0
            if (
                self.color == "white"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "white"
            ):
                return 0
            elif (
                self.color == "black"
                and board.squares[final_pos] != " "
                and board.squares[final_pos].color == "black"
            ):
                return 0
            return 1
        else:
            i = 1
            while i <= 9:
                if i == 9:
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
                            return 0
                    else:
                        if (
                            board.squares[final_pos] != " "
                            and board.squares[final_pos].color == "black"
                        ):
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
                                return 0
                        i -= 1
                    return 1
                i += 1
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
            and board.squares["g1"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["h1"], Rook)
            and board.squares["h1"].can_castle == 1
            and board.check == False
            and not is_attacked(True, "f1", board)
            and not is_attacked(True, "g1", board)
        ):
            return 4
        elif (
            start_pos == "e1"
            and final_pos == "c1"
            and board.squares["b1"] == " "
            and board.squares["c1"] == " "
            and board.squares["d1"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["a1"], Rook)
            and board.squares["a1"].can_castle == 1
            and board.check == False
            and not is_attacked(True, "c1", board)
            and not is_attacked(True, "d1", board)
        ):
            return 5
        elif (
            start_pos == "e8"
            and final_pos == "g8"
            and board.squares["f8"] == " "
            and board.squares["g8"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["h8"], Rook)
            and board.squares["h8"].can_castle == 1
            and board.check == False
            and not is_attacked(False, "f8", board)
            and not is_attacked(False, "g8", board)
        ):
            return 4
        elif (
            start_pos == "e8"
            and final_pos == "c8"
            and board.squares["b8"] == " "
            and board.squares["c8"] == " "
            and board.squares["d8"] == " "
            and self.can_castle == 1
            and isinstance(board.squares["a8"], Rook)
            and board.squares["a8"].can_castle == 1
            and board.check == False
            and not is_attacked(False, "c8", board)
            and not is_attacked(False, "d8", board)
        ):
            return 5
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
                    return 0
            else:
                if (
                    board.squares[final_pos] != " "
                    and board.squares[final_pos].color == "black"
                ):
                    return 0
            return 1
        else:
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
        # if isinstance(piece, King):
        #    if piece.color == "white":
        #        wking = piece
        #    else:
        #        bking = piece
    white_turn = True
    en_passant_count = 0
    turn = 0

    with open("chess_sim_PGN.txt", "w", encoding="utf-8") as pgn:
        pgn.write("Created with chess_sim V1.0\n\n")

    while True:
        if white_turn == True:
            turn += 1

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

        if game.squares[move_from].move(move_from, move_to, game):
            if not is_legal(move_from, move_to, game):
                print("Illegal move")
                continue

        match game.squares[move_from].move(move_from, move_to, game):
            case 0:
                print("Invalid move")
                continue
            case 2:  # enable en passant
                with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                    if white_turn == True:
                        pgn.write(f"{turn}.{move_to}")
                    else:
                        pgn.write(f" {move_to} ")
                print(f"{game.squares[move_from]} {move_to}")
                game.squares[move_from].en_passant = 1
                if sq_pattern.search(
                    chr(ord(move_to[0]) - 1) + move_to[1]
                ) != None and isinstance(
                    game.squares[chr(ord(move_to[0]) - 1) + move_to[1]], Pawn
                ):
                    game.squares[chr(ord(move_to[0]) - 1) + move_to[1]].en_passant = 1
                    game.en_passant = True
                if sq_pattern.search(
                    chr(ord(move_to[0]) + 1) + move_to[1]
                ) != None and isinstance(
                    game.squares[chr(ord(move_to[0]) + 1) + move_to[1]], Pawn
                ):
                    game.squares[chr(ord(move_to[0]) + 1) + move_to[1]].en_passant = 1
                    game.en_passant = True
            case 3:  # en passant
                with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                    if white_turn == True:
                        pgn.write(f"{turn}.{move_from[0]}x{move_to}")
                    else:
                        pgn.write(f" {move_from[0]}x{move_to} ")
                print(f"{game.squares[move_from]} {move_to}")
                game.squares[move_to[0] + move_from[1]].on_the_board = 0
                game.squares[move_to[0] + move_from[1]] = " "
            case 4:  # castling short
                with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                    if white_turn == True:
                        pgn.write(f"{turn}.O-O")
                    else:
                        pgn.write(f" O-O ")
                print("O-O")
                if move_from == "e1":
                    if isinstance(game.squares["h1"], Piece):
                        game.squares["h1"].position = "f1"
                    game.squares["f1"] = game.squares["h1"]
                    game.squares["h1"] = " "
                else:
                    if isinstance(game.squares["h8"], Piece):
                        game.squares["h8"].position = "f8"
                    game.squares["f8"] = game.squares["h8"]
                    game.squares["h8"] = " "
            case 5:  # castling long
                with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                    if white_turn == True:
                        pgn.write(f"{turn}.O-O-O")
                    else:
                        pgn.write(f" O-O-O ")
                print("O-O-O")
                if move_from == "e1":
                    if isinstance(game.squares["a1"], Piece):
                        game.squares["a1"].position = "d1"
                    game.squares["d1"] = game.squares["a1"]
                    game.squares["a1"] = " "
                else:
                    if isinstance(game.squares["a8"], Piece):
                        game.squares["a8"].position = "d8"
                    game.squares["d8"] = game.squares["a8"]
                    game.squares["a8"] = " "
            case 1:
                with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                    if white_turn == True:
                        if isinstance(game.squares[move_from], Pawn):
                            if game.squares[move_to] != " ":
                                pgn.write(f"{turn}.{move_from[0]}x{move_to}")
                            else:
                                pgn.write(f"{turn}.{move_to}")
                        else:
                            if game.squares[move_to] != " ":
                                pgn.write(f"{turn}.{game.squares[move_from]}x{move_to}")
                            else:
                                pgn.write(f"{turn}.{game.squares[move_from]}{move_to}")
                    else:
                        if isinstance(game.squares[move_from], Pawn):
                            if game.squares[move_to] != " ":
                                pgn.write(f" {move_from[0]}x{move_to} ")
                            else:
                                pgn.write(f" {move_to} ")
                        else:
                            if game.squares[move_to] != " ":
                                pgn.write(f" {game.squares[move_from]}x{move_to} ")
                            else:
                                pgn.write(f" {game.squares[move_from]}{move_to} ")
                print(f"{game.squares[move_from]} {move_to}")

        if game.squares[move_to] != " ":
            game.squares[move_to].on_the_board = 0  # Eliminate the piece that was taken
        if isinstance(game.squares[move_from], King) or isinstance(
            game.squares[move_from], Rook
        ):
            game.squares[move_from].can_castle = 0
        game.squares[move_from].position = move_to
        game.squares[move_to] = game.squares[move_from]
        game.squares[move_from] = " "

        if isinstance(game.squares[move_to], Pawn) and (
            move_to[1] == "1" or move_to[1] == "8"
        ):  # promotion of pawns that reach the last rank
            game.squares[move_to].on_the_board = 0
            game.squares[move_to] = game.squares[move_to].promote(move_to, game)
            pieces.append(game.squares[move_to])
            if white_turn == True:
                if isinstance(game.squares[move_to], Queen):
                    with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                        pgn.write("=Q")
                elif isinstance(game.squares[move_to], Rook):
                    with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                        pgn.write("=R")
                elif isinstance(game.squares[move_to], Knight):
                    with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                        pgn.write("=N")
                elif isinstance(game.squares[move_to], Bishop):
                    with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                        pgn.write("=B")
            else:
                if isinstance(game.squares[move_to], Queen):
                    with open("chess_sim_PGN.txt", "r", encoding="utf-8") as file:
                        reader = file.read()
                    reader = reader[:-1] + "=Q "
                    with open("chess_sim_PGN.txt", "w", encoding="utf-8") as pgn:
                        pgn.write(reader)
                elif isinstance(game.squares[move_to], Rook):
                    with open("chess_sim_PGN.txt", "r", encoding="utf-8") as file:
                        reader = file.read()
                    reader = reader[:-1] + "=R "
                    with open("chess_sim_PGN.txt", "w", encoding="utf-8") as pgn:
                        pgn.write(reader)
                elif isinstance(game.squares[move_to], Knight):
                    with open("chess_sim_PGN.txt", "r", encoding="utf-8") as file:
                        reader = file.read()
                    reader = reader[:-1] + "=N "
                    with open("chess_sim_PGN.txt", "w", encoding="utf-8") as pgn:
                        pgn.write(reader)
                elif isinstance(game.squares[move_to], Bishop):
                    with open("chess_sim_PGN.txt", "r", encoding="utf-8") as file:
                        reader = file.read()
                    reader = reader[:-1] + "=B "
                    with open("chess_sim_PGN.txt", "w", encoding="utf-8") as pgn:
                        pgn.write(reader)

        game.check = is_check(white_turn, game)
        if game.check == True:
            with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                if white_turn == True:
                    pgn.write("+")
                else:
                    pgn.write("+ ")
            print("Check!")

        if is_stalemate(white_turn, game):
            with open("chess_sim_PGN.txt", "a", encoding="utf-8") as pgn:
                pgn.write(" 1/2 - 1/2")
            print("Stalemate")
            break

        if white_turn == True:
            if is_checkmate(white_turn, game):
                with open("chess_sim_PGN.txt", "r", encoding="utf-8") as file:
                    reader = file.read()
                reader = reader[:-1] + "# 1-0"
                with open("chess_sim_PGN.txt", "w", encoding="utf-8") as pgn:
                    pgn.write(reader)
                print("White wins!")
                print(game)
                break
            white_turn = False
        else:
            if is_checkmate(white_turn, game):
                with open("chess_sim_PGN.txt", "r", encoding="utf-8") as file:
                    reader = file.read()
                reader = reader[:-3] + "# 0-1"
                with open("chess_sim_PGN.txt", "w", encoding="utf-8") as pgn:
                    pgn.write(reader)
                print("Black wins!")
                print(game)
                break
            white_turn = True

        if (
            game.en_passant == True and en_passant_count == 1
        ):  # resets en_passant on the board and on Pawns
            game.en_passant = False
            en_passant_count = 0
            for piece in pieces:
                if isinstance(piece, Pawn) and piece.en_passant == 1:
                    piece.en_passant = 0
        if game.en_passant == True and en_passant_count == 0:
            en_passant_count = 1


def start_game(game):
    pieces = []
    for square in game.squares:
        if square[1] == "2":
            pieces.append(Pawn("white", square, game))
        elif square[1] == "7":
            pieces.append(Pawn("black", square, game))
        elif square[1] in ("1", "8"):
            if square[0] in ("a", "h"):
                (
                    pieces.append(Rook("white", square, game))
                    if square[1] == "1"
                    else pieces.append(Rook("black", square, game))
                )
            elif square[0] in ("b", "g"):
                (
                    pieces.append(Knight("white", square, game))
                    if square[1] == "1"
                    else pieces.append(Knight("black", square, game))
                )
            elif square[0] in ("c", "f"):
                (
                    pieces.append(Bishop("white", square, game))
                    if square[1] == "1"
                    else pieces.append(Bishop("black", square, game))
                )
            elif square[0] == "d":
                (
                    pieces.append(Queen("white", square, game))
                    if square[1] == "1"
                    else pieces.append(Queen("black", square, game))
                )
            elif square[0] == "e":
                (
                    pieces.append(King("white", square, game))
                    if square[1] == "1"
                    else pieces.append(King("black", square, game))
                )
    return pieces


def is_legal(move_from: str, move_to: str, board: Chessboard) -> bool:
    game_legal = copy.deepcopy(board)
    pieces_legal = []

    for square in game_legal.squares.keys():
        if game_legal.squares[square] != " ":
            pieces_legal.append(game_legal.squares[square])
        if isinstance(game_legal.squares[square], King):
            if game_legal.squares[square].color == "white":
                wking_legal = game_legal.squares[square].position
            else:
                bking_legal = game_legal.squares[square].position

    if game_legal.squares[move_from].color == "white" and game_legal.squares[
        move_from
    ].move(move_from, move_to, board):
        if game_legal.squares[move_to] != " ":
            game_legal.squares[move_to].on_the_board = 0
        if isinstance(game_legal.squares[move_from], King):
            wking_legal = move_to
        game_legal.squares[move_from].position = move_to
        game_legal.squares[move_to] = game_legal.squares[move_from]
        game_legal.squares[move_from] = " "
        for piece in pieces_legal:
            if piece.color == "black" and piece.on_the_board == 1:
                if piece.move(piece.position, wking_legal, game_legal):
                    return False
    elif game_legal.squares[move_from].color == "black" and game_legal.squares[
        move_from
    ].move(move_from, move_to, board):
        if game_legal.squares[move_to] != " ":
            game_legal.squares[move_to].on_the_board = 0
        if isinstance(game_legal.squares[move_from], King):
            bking_legal = move_to
        game_legal.squares[move_from].position = move_to
        game_legal.squares[move_to] = game_legal.squares[move_from]
        game_legal.squares[move_from] = " "
        for piece in pieces_legal:
            if piece.color == "white" and piece.on_the_board == 1:
                if piece.move(piece.position, bking_legal, game_legal):
                    return False

    return True


def is_check(turn: bool, board: Chessboard) -> bool:
    if turn == True:  # white turn
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], King)
                and board.squares[square].color == "black"
            ):
                bkp = board.squares[square].position
                break
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], Piece)
                and board.squares[square].color == "white"
                and board.squares[square].on_the_board == 1
            ):
                if board.squares[square].move(
                    board.squares[square].position, bkp, board
                ):
                    return True
    else:  # black turn
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], King)
                and board.squares[square].color == "white"
            ):
                wkp = board.squares[square].position
                break
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], Piece)
                and board.squares[square].color == "black"
                and board.squares[square].on_the_board == 1
            ):
                if board.squares[square].move(
                    board.squares[square].position, wkp, board
                ):
                    return True
    return False


def is_checkmate(turn: bool, board: Chessboard) -> bool:
    if board.check == False:
        return False

    if turn == True:  # white turn
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], Piece)
                and board.squares[square].color == "black"
                and board.squares[square].on_the_board == 1
            ):
                for move_to in board.squares.keys():
                    if board.squares[square].move(
                        board.squares[square].position, move_to, board
                    ) != 0 and is_legal(board.squares[square].position, move_to, board):
                        return False
        return True

    else:  # black turn
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], Piece)
                and board.squares[square].color == "white"
                and board.squares[square].on_the_board == 1
            ):
                for move_to in board.squares.keys():
                    if board.squares[square].move(
                        board.squares[square].position, move_to, board
                    ) != 0 and is_legal(board.squares[square].position, move_to, board):
                        return False
    return True


def is_stalemate(turn: bool, board: Chessboard) -> bool:
    if board.check == True:
        return False
    if turn == True:  # white turn
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], Piece)
                and board.squares[square].color == "black"
                and board.squares[square].on_the_board == 1
            ):
                for move_to in board.squares.keys():
                    if board.squares[square].move(
                        board.squares[square].position, move_to, board
                    ) != 0 and is_legal(board.squares[square].position, move_to, board):
                        return False
        return True

    else:  # black turn
        for square in board.squares.keys():
            if (
                isinstance(board.squares[square], Piece)
                and board.squares[square].color == "white"
                and board.squares[square].on_the_board == 1
            ):
                for move_to in board.squares.keys():
                    if board.squares[square].move(
                        board.squares[square].position, move_to, board
                    ) != 0 and is_legal(board.squares[square].position, move_to, board):
                        return False
        return True


def is_attacked(turn: bool, square: str, board: Chessboard) -> bool:
    if turn == True:
        for piece in board.squares.keys():
            if (
                isinstance(board.squares[piece], Piece)
                and board.squares[piece].color == "black"
                and board.squares[piece].on_the_board == 1
            ):
                if board.squares[piece].move(
                    board.squares[piece].position, square, board
                ):
                    return True
    else:
        for piece in board.squares.keys():
            if (
                isinstance(board.squares[piece], Piece)
                and board.squares[piece].color == "white"
                and board.squares[piece].on_the_board == 1
            ):
                if board.squares[piece].move(
                    board.squares[piece].position, square, board
                ):
                    return True
    return False


if __name__ == "__main__":
    main()
