from ui import user_input, print_board


EMPTY = 0 # empty square

W_P = 1  # white pawn
W_N = 2  # white knight
W_B = 3  # white bishop
W_R = 4  # white rook
W_Q = 5  # white queen
W_K = 6  # white king

B_P = 7  # black pawn
B_N = 8  # black knight
B_B = 9  # black bishop
B_R = 10 # black rook
B_Q = 11 # black queen
B_K = 12 # black king

# castling moves
W_KING_SIDE  = (95, 97, "")
W_QUEEN_SIDE = (95, 93, "")
B_KING_SIDE  = (25, 27, "")
B_QUEEN_SIDE = (25, 23, "")

def main():
    board = create_board()
    white = True # current player, if False, player will be black
    ep_sq = None # possible en passant capture square

    # castling rights [white kingside, queenside, black kingside, queenside]
    castling = [True, True, True, True]
    half_moves = 0 # fifty-move rule counter

    # for detecting threefold repetition. Postion is defined by en_passant
    # capture possibility, side to move, castling rights and piece placement
    positions = {} # count of each position
    position = ""

    while True:
        print_board(board)

        pseudo_moves = gen_moves(board, white, castling, ep_sq)

        # select legal moves from pseudo_moves
        moves = []
        king = W_K if white else B_K
        for move in pseudo_moves:
            copy_board = board[:] # for unmaking the move later
            make_move(board, move, white, False)

            # find king index
            for i in range(len(board)):
                if board[i] == king:
                    king_i = i

            if not is_in_check(board, white, king_i): # legal move
                moves.append(move)

                # for detecting threefold repetition
                if is_en_passant(board, move, ep_sq):
                    position += "e"

            board = copy_board # unmake the move

        # for detecting threefold repetition
        position += "w" if white else "b"
        if castling[0]:
            position += "K"
        if castling[1]:
            position += "Q"
        if castling[2]:
            position += "k"
        if castling[3]:
            position += "q"
        for square in board:
            if square != -1:
                position += str(square)

        if half_moves == 0:
            positions = {}

        # increment or initialize the count of position
        positions[position] = positions.get(position, 0) + 1

        position = ""

        if not moves: # Game over
            king = W_K if white else B_K

            # find king index
            for i in range(len(board)):
                if board[i] == king:
                    king_i = i

            if is_in_check(board, white, king_i):
                print("Black" if white else "White", "wins the game!")
                return
            print("Draw - stalemate")
            return

        for value in positions.values():
            if value >= 3: # threefold repetition
                print("Draw - threefold repetition")
                return

        if half_moves >= 100: # fifty-move rule
            print("Draw - fifty-move rule")
            return

        print("White: " if white else "Black: ", end="")
        move = user_input()

        while move not in moves:
            print_board(board)
            print("Please enter a legal move")
            print("White: " if white else "Black: ", end="")
            move = user_input()

        from_sq = move[0]
        to_sq = move[1]

        # fifty-move rule counter
        if board[from_sq] in [W_P, B_P] \
            or (board[to_sq] != EMPTY and board[from_sq] != board[to_sq]):
            # current move is pawn move or capture
            half_moves = 0
        else:
            half_moves += 1

        make_move(board, move, white, ep_sq)

        # set possible en passant capture square for the next move
        if board[to_sq] in [W_P, B_P] and abs(to_sq - from_sq) == 20:
            ep_sq = to_sq + 10 if white else to_sq - 10
        else:
            ep_sq = None

        # set castling rights
        if board[to_sq] in [W_K, B_K]: # king has moved
            if white:
                castling[0] = False
                castling[1] = False
            else:
                castling[2] = False
                castling[3] = False
        
        # if a rook is not in initial postion castling right is lost
        if board[98] != W_R:
            castling[0] = False
        if board[91] != W_R:
            castling[1] = False
        if board[28] != B_R:
            castling[2] = False
        if board[21] != B_R:
            castling[3] = False

        white = not white # change player


def create_board():
    # out of the board square  = -1
    board = [
        -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1, -1,
        -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1, -1,
        -1,   B_R,   B_N,   B_B,   B_Q,   B_K,   B_B,   B_N,   B_R, -1,
        -1,   B_P,   B_P,   B_P,   B_P,   B_P,   B_P,   B_P,   B_P, -1,
        -1, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, -1,
        -1, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, -1,
        -1, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, -1,
        -1, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, -1,
        -1,   W_P,   W_P,   W_P,   W_P,   W_P,   W_P,   W_P,   W_P, -1,
        -1,   W_R,   W_N,   W_B,   W_Q,   W_K,   W_B,   W_N,   W_R, -1,
        -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1, -1,
        -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1, -1,
    ]

    return board


def gen_moves(board, white, castling, ep_sq):
    moves = []
    pieces = [W_P, W_N, W_B, W_R, W_Q, W_K] if white else \
        [B_P, B_N, B_B, B_R, B_Q, B_K]

    opposite_pieces = [B_P, B_N, B_B, B_R, B_Q, B_K] if white else \
        [W_P, W_N, W_B, W_R, W_Q, W_K]

    offsets_list = [
        None,
        None,
        [12, 21, 19, 8, -12, -21, -19, -8], # knight
        [11, 9, -11, -9], # bishop
        [10, -1, -10, 1], # rook
        [10, -1, -10, 1, 11, 9, -11, -9], # queen
        [10, -1, -10, 1, 11, 9, -11, -9] # king
    ]

    # loop over all indices in the board
    for i in range(len(board)):
        piece = board[i]
        if piece in [-1, EMPTY] or piece in opposite_pieces:
            continue

        if piece in [W_P, B_P]: # found a pawn
            moves.extend(gen_pawn_moves(board, white, i, ep_sq))

        else: # found a pice other than pawn
            offsets = offsets_list[piece] if white else offsets_list[piece - 6]

            from_sq = i
            for offset in offsets:
                temp_sq = from_sq
                while True:
                    to_sq = temp_sq + offset
                    if board[to_sq] == -1: # to_sq is off the board
                        break
                    elif board[to_sq] in pieces: # to_sq is same color piece
                        break
                    elif board[to_sq] in opposite_pieces:
                        moves.append((from_sq, to_sq, ""))
                        break
                    moves.append((from_sq, to_sq, ""))

                    # knight and king can only move one square in a direction
                    if piece in [W_N, W_K, B_N, B_K]:
                        break

                    temp_sq = to_sq

            # for castling
            if piece in [W_K, B_K]:
                moves.extend(gen_castling_moves(board, white, castling))

    return moves


def gen_pawn_moves(board, white, i, ep_sq):
    moves = []
    promotion = ""
    last_rank = [21, 22, 23, 24, 25, 26, 27, 28] if white else \
        [91, 92, 93, 94, 95, 96, 97, 98]
    second_rank = [81, 82, 83, 84, 85, 86, 87, 88] if white else \
        [31, 32, 33, 34, 35, 36, 37, 38]
    opposite_pieces = [B_P, B_N, B_B, B_R, B_Q, B_K] if white else \
        [W_P, W_N, W_B, W_R, W_Q, W_K]
    normal_offsets = [-10, -20] if white else [10, 20]
    capture_offsets = [-9, -11] if white else [9, 11]

    from_sq = i

    to_sq = from_sq + normal_offsets[0] # single square move
    if board[to_sq] == EMPTY:
        if to_sq in last_rank:
            for promotion in "nbrq":
                moves.append((from_sq, to_sq, promotion))
            promotion = ""
        else:
            moves.append((from_sq, to_sq, promotion))

    if from_sq in second_rank: # double square move
        to_sq = from_sq + normal_offsets[1]
        if board[to_sq] == EMPTY:
            moves.append((from_sq, to_sq, promotion))

    for offset in capture_offsets:
        to_sq = from_sq + offset
        if board[to_sq] in opposite_pieces: # capture
            if to_sq in last_rank:
                for promotion in "nbrq":
                    moves.append((from_sq, to_sq, promotion))
                promotion = ""
            else:
                moves.append((from_sq, to_sq, promotion))

        if ep_sq: # current move may be en passant capture
            if to_sq == ep_sq:
                moves.append((from_sq, to_sq, promotion))

    return moves


def gen_castling_moves(board, white, castling):
    moves = []
    if white:
        if castling[0] and (board[96] == EMPTY and board[97] == EMPTY):
            if not(is_in_check(board,white,95) or is_in_check(board,white,96)):
                moves.append(W_KING_SIDE)
        if castling[1] and (board[94] == EMPTY and board[93] == EMPTY and \
            board[92] == EMPTY):
            if not(is_in_check(board,white,95) or is_in_check(board,white,94)):
                moves.append(W_QUEEN_SIDE)
    else:
        if castling[2] and (board[26] == EMPTY and board[27] == EMPTY):
            if not(is_in_check(board,white,25) or is_in_check(board,white,26)):
                moves.append(B_KING_SIDE)
        if castling[3] and (board[24] == EMPTY and board[23] == EMPTY and \
            board[22] == EMPTY):
            if not(is_in_check(board,white,25) or is_in_check(board,white,24)):
                moves.append(B_QUEEN_SIDE)

    return moves


def is_in_check(board, white, i):
    pieces = [W_P, W_N, W_B, W_R, W_Q, W_K] if white else \
        [B_P, B_N, B_B, B_R, B_Q, B_K]

    opposite_pieces = [B_P, B_N, B_B, B_R, B_Q, B_K] if white else \
        [W_P, W_N, W_B, W_R, W_Q, W_K]

    # check if a pawn could capture the king
    opposite_pawn = B_P if white else W_P
    capture_offsets = [-9, -11] if white else [9, 11]
    from_sq = i
    for offset in capture_offsets:
        to_sq = from_sq + offset
        if board[to_sq] == opposite_pawn: # to_sq is opposite pawn
            return True

    # check if a king could capture the king
    opposite_king = B_K if white else W_K
    offsets = [10, -1, -10, 1, 11, 9, -11, -9]
    from_sq = i
    for offset in offsets:
        to_sq = from_sq + offset
        if board[to_sq] == opposite_king: # to_sq is opposite king
            return True

    # check if a knight could capture the king
    opposite_knight = B_N if white else W_N
    offsets = [12, 21, 19, 8, -12, -21, -19, -8]
    from_sq = i
    for offset in offsets:
        to_sq = from_sq + offset
        if board[to_sq] == opposite_knight: # to_sq is opposite knight
            return True

    # check if a rook or queen could capture the king
    opposite_qr = [B_R, B_Q] if white else [W_R, W_Q]
    offsets = [10, -1, -10, 1]
    from_sq = i
    for offset in offsets:
        temp_sq = from_sq
        while True:
            to_sq = temp_sq + offset
            if board[to_sq] == -1: # to_sq is off the board
                break
            elif board[to_sq] in pieces: # to_sq is same color piece
                break
            elif board[to_sq] in opposite_pieces:
                if board[to_sq] in opposite_qr: # to_sq: opposite queen or rook
                    return True
                break
            temp_sq = to_sq

    # check if a bishop or queen could capture the king
    opposite_qb = [B_B, B_Q] if white else [W_B, W_Q]
    offsets = [11, 9, -11, -9]
    from_sq = i
    for offset in offsets:
        temp_sq = from_sq
        while True:
            to_sq = temp_sq + offset
            if board[to_sq] == -1: # to_sq is off the board
                break
            elif board[to_sq] in pieces: # to_sq is same color piece
                break
            elif board[to_sq] in opposite_pieces:
                if board[to_sq] in opposite_qb: #to_sq:opposite queen or bishop
                    return True
                break
            temp_sq = to_sq


def is_en_passant(board, move, ep_sq):
    to_sq = move[1]
    return board[to_sq] in [W_P, B_P] and to_sq == ep_sq


def make_move(board, move, white, ep_sq):
    from_sq = move[0]
    to_sq = move[1]
    promotion = move[2]

    board[to_sq] = board[from_sq]
    board[from_sq] = EMPTY

    # pawn promotion
    if promotion:
        if promotion == "n":
            board[to_sq] = W_N if white else B_N
        elif promotion == "b":
            board[to_sq] = W_B if white else B_B
        elif promotion == "r":
            board[to_sq] = W_R if white else B_R
        elif promotion == "q":
            board[to_sq] = W_Q if white else B_Q

    # en passant capture
    elif is_en_passant(board, move, ep_sq):
        # remove the en passant captured pawn
        remove_sq = to_sq + 10 if white else to_sq - 10
        board[remove_sq] = EMPTY

    # castling
    elif board[to_sq] in [W_K, B_K] and abs(to_sq - from_sq) == 2:
        # move the rook to the castled position
        if to_sq == 97: # white kingside
            board[96] = W_R
            board[98] = EMPTY
        elif to_sq == 93: # white queenside
            board[94] = W_R
            board[91] = EMPTY
        elif to_sq == 27: # black kingside
            board[26] = B_R
            board[28] = EMPTY
        elif to_sq == 23: # black queenside
            board[24] = B_R
            board[21] = EMPTY

   
if __name__ == "__main__":
    main()
