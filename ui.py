from os import name, system


# for printing the board
SYMBOLS = ".PNBRQKpnbrqk" if name == "nt" else \
    " \u2659\u2658\u2657\u2656\u2655\u2654\u265F\u265E\u265D\u265C\u265B\u265A"

# board index position => chess notation
NOTATION = [
    "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
    "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
    "-1", "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "-1",
    "-1", "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "-1",
    "-1", "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "-1",
    "-1", "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "-1",
    "-1", "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "-1",
    "-1", "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "-1",
    "-1", "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "-1",
    "-1", "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "-1",
    "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
    "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
]

# chess notation => board index position
INDICES = {
    "a8":21, "b8":22, "c8":23, "d8":24, "e8":25, "f8":26, "g8":27, "h8":28,
    "a7":31, "b7":32, "c7":33, "d7":34, "e7":35, "f7":36, "g7":37, "h7":38,
    "a6":41, "b6":42, "c6":43, "d6":44, "e6":45, "f6":46, "g6":47, "h6":48,
    "a5":51, "b5":52, "c5":53, "d5":54, "e5":55, "f5":56, "g5":57, "h5":58,
    "a4":61, "b4":62, "c4":63, "d4":64, "e4":65, "f4":66, "g4":67, "h4":68,
    "a3":71, "b3":72, "c3":73, "d3":74, "e3":75, "f3":76, "g3":77, "h3":78,
    "a2":81, "b2":82, "c2":83, "d2":84, "e2":85, "f2":86, "g2":87, "h2":88,
    "a1":91, "b1":92, "c1":93, "d1":94, "e1":95, "f1":96, "g1":97, "h1":98
}


def user_input():
    move_string = input()
    if move_string == "quit":
        quit()

    from_sq = INDICES.get(move_string[:2])
    to_sq = INDICES.get(move_string[2:4])
    promotion = move_string[4:] # used for pawn promotion

    return (from_sq, to_sq, promotion)


def print_board(board):
    if name == "nt":
        system("cls")
        count = 0 # count the number of squares printed
        for square in board:
            if square != -1: # square is not outside of board
                print(SYMBOLS[square], end=" ")
                count += 1
                if count % 8 == 0:
                    print()
    else:
        print_color_board(board)
    

def print_color_board(board):
    system("clear")
    i = 0 # count the number of squares printed
    row_count = 0
    print(8 - row_count, end=" ")
    for square in board:
        if square != -1: # square is not outside of board
            if row_count % 2 == 0:
                print("\033[107m" if i % 2 == 0 else "\033[106m", end="")
            else:
                print("\033[106m" if i % 2 == 0 else "\033[107m", end="")

            print(SYMBOLS[square], end=" \033[0m")
            i += 1
            if i % 8 == 0:
                print()
                row_count += 1
                if row_count < 8:
                    print(8 - row_count, end=" ")
    print("  a b c d e f g h")


def print_moves(moves):
    for move in moves:
        print(NOTATION[move[0]], NOTATION[move[1]], move[2], sep="", end=" ")
    print()
