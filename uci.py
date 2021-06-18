from engine import find_best_move, set_position


START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def main():
    while True:
        command = input()
        if command == "quit":
            return

        if command == "uci":
            print("id name Vivchess")
            print("id author Vivek Vinod")
            print("uciok")

        elif command == "isready":
            print("readyok")

        elif command.startswith("position"):
            if "fen" in command:
                fen = " ".join(command.split()[2:8])
            else:
                fen = START_POSITION
            if "moves" in command:
                moves = command.split("moves")[1].split()
            else:
                moves = []
            set_position(fen, moves)

        elif command.startswith("go"):
            move = find_best_move()
            print("bestmove", move)
        

if __name__ == "__main__":
    main()
