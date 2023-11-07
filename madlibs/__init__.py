from madlib_logic import MadlibLogic


def main():
    play_game = 1
    while play_game == 1:
        play_game = MadlibLogic().play_game()
    exit()


if __name__ == '__main__':
    main()
