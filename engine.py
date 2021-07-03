import random
from chess import B_K, B_P, B_R, W_K, W_P, W_R, \
    gen_moves, is_in_check, make_move
from ui import INDICES, NOTATION

# fen => internal piece representation
PIECES = {
    "P": 1,
    "N": 2,
    "B": 3,
    "R": 4,
    "Q": 5,
    "K": 6,
    "p": 7,
    "n": 8,
    "b": 9,
    "r": 10,
    "q": 11,
    "k": 12
}

board, white, castling, ep_sq = None, None, None, None


def set_position(fen, moves):
    global board
    global white
    global castling
    global ep_sq
    board, white, castling, ep_sq = parse_fen(fen)

    # make the given moves on the board
    for move_string in moves:
        from_sq = INDICES[move_string[:2]]
        to_sq = INDICES[move_string[2:4]]
        promotion = move_string[4:]

        move = (from_sq, to_sq, promotion)

        make_move(board, move, white, ep_sq)

        # set possible en passant capture square for the next move
        if board[to_sq] in [W_P, B_P] and abs(to_sq - from_sq) == 20:
            ep_sq = to_sq + 10 if white else to_sq - 10
        else:
            ep_sq = None

        # set castling rights
        if board[to_sq] in [W_K, B_K]:  # king has moved
            if white:
                castling[0] = False
                castling[1] = False
            else:
                castling[2] = False
                castling[3] = False

        # if a rook is not in initial position castling right is lost
        if board[98] != W_R:
            castling[0] = False
        if board[91] != W_R:
            castling[1] = False
        if board[28] != B_R:
            castling[2] = False
        if board[21] != B_R:
            castling[3] = False

        white = not white  # change player


def find_best_move():
    moves = gen_legal_moves()
    best_move = random.choice(moves)
    return NOTATION[best_move[0]] + NOTATION[best_move[1]] + best_move[2]


def gen_legal_moves():
    global board
    global white
    global castling
    global ep_sq
    pseudo_moves = gen_moves(board, white, castling, ep_sq)

    # select legal moves from pseudo_moves
    moves = []
    king = W_K if white else B_K
    for move in pseudo_moves:
        copy_board = board[:]  # for unmaking the move later
        make_move(board, move, white, False)

        # find king index
        for i in range(len(board)):
            if board[i] == king:
                king_i = i

        if not is_in_check(board, white, king_i):  # legal move
            moves.append(move)

        board = copy_board  # unmake the move

    return moves


def parse_fen(fen):
    fields = fen.split()

    board = create_board(fields[0])

    white = True if fields[1] == "w" else False

    castling = [False, False, False, False]
    for i in fields[2]:
        if i == "K":
            castling[0] = True
        if i == "Q":
            castling[1] = True
        if i == "k":
            castling[2] = True
        if i == "q":
            castling[3] = True

    ep_sq = None if fields[3] == "-" else INDICES[fields[3]]

    return board, white, castling, ep_sq


def create_board(position):
    board = [-1] * 21
    for piece in position:
        if piece == "/":
            board.extend([-1, -1])
        elif piece.isalpha():
            board.append(PIECES[piece])
        else:
            board.extend([0] * int(piece))
    board.extend([-1] * 21)

    return board
