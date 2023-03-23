import random


class Dominoes:
    def __init__(self):
        self.stock_pieces = []
        self.pc_pieces = []
        self.player_pieces = []
        self.snake = []
        self.status = None
        self.__game_started = False

    @property
    def snake_start(self):
        return self.snake[0][0]

    @property
    def snake_end(self):
        return self.snake[-1][1]

    @staticmethod
    def max_double(pieces):
        doubles = [piece for piece in pieces if piece[0] == piece[1]]
        if len(doubles) != 0:
            return max(doubles, key=lambda l: sum(l))

    def initialize_pieces(self):
        pieces = [[i, j] for i in range(7) for j in range(7) if i <= j]
        while True:
            random.shuffle(pieces)
            self.stock_pieces = pieces[:14]
            self.pc_pieces = pieces[14:21]
            self.player_pieces = pieces[21:]

            pc_max = self.max_double(self.pc_pieces)
            player_max = self.max_double(self.player_pieces)
            if pc_max and player_max:
                max_double_piece = max(pc_max, player_max, key=lambda x: sum(x))
                if max_double_piece in self.player_pieces:
                    self.status = 'computer'
                    self.player_pieces.remove(max_double_piece)
                else:
                    self.status = 'player'
                    self.pc_pieces.remove(max_double_piece)
                self.snake.append(max_double_piece)
                break

    def show_snake(self):
        snake_len = len(self.snake)
        if snake_len > 6:
            print(*self.snake[:3], '...', *self.snake[-3:], sep='')
        else:
            print(*self.snake, sep='')

    def show_player_pieces(self):
        for i in range(len(self.player_pieces)):
            print(f'{i + 1}:{self.player_pieces[i]}')

    def __check_finished(self):
        if len(self.player_pieces) == 0:
            print('Status: The game is over. You won!')
            self.__game_started = False
        elif len(self.pc_pieces) == 0:
            print('Status: The game is over. The computer won!')
            self.__game_started = False
        elif self.snake[0][0] == self.snake[-1][-1] and \
                sum(map(lambda x: x.count(self.snake[0][0]), self.snake)) == 8:
            print("Status: The game is over. It's a draw!")
            self.__game_started = False

    def player_step(self):
        while True:
            try:
                selection = int(input())
                if abs(selection) > len(self.player_pieces):
                    raise ValueError
                if selection == 0 and len(self.stock_pieces) > 0:
                    self.player_pieces.append(self.stock_pieces.pop())
                    break
                elif selection > 0:
                    selection -= 1
                    piece = self.player_pieces[selection]
                    if self.snake_end not in piece:
                        print('Illegal move. Please try again.')
                        continue
                    if piece[1] == self.snake_end:
                        piece.reverse()
                    self.snake.append(piece)
                    self.player_pieces.remove(piece)
                    break
                elif selection < 0:
                    selection = selection * -1 - 1
                    piece = self.player_pieces[selection]
                    if self.snake_start not in piece:
                        print('Illegal move. Please try again.')
                        continue
                    if piece[0] == self.snake_end:
                        piece.reverse()
                    self.snake.insert(0, piece)
                    self.player_pieces.remove(piece)
                    break
            except ValueError:
                print('Invalid input. Please try again.')

    def pc_step(self):
        available_pieces = self.snake + self.pc_pieces
        counts = {i: sum(map(lambda p: p.count(i), available_pieces)) for i in range(7)}
        score = [(p, counts[p[0]] + counts[p[1]]) for p in self.pc_pieces]
        score.sort(key=lambda x: x[1], reverse=True)

        for piece, _ in score:
            if self.snake_end in piece:
                if piece[1] == self.snake_end:
                    piece.reverse()
                self.snake.append(piece)
                self.pc_pieces.remove(piece)
                break
            elif self.snake_start in piece:
                if piece[0] == self.snake_start:
                    piece.reverse()
                self.snake.insert(0, piece)
                self.pc_pieces.remove(piece)
                break
        else:
            if len(self.stock_pieces) > 0:
                self.pc_pieces.append(self.stock_pieces.pop())

    def next_step(self):
        print(70 * '=')
        print(f'Stock size: {len(self.stock_pieces)}')
        print(f'Computer pieces: {len(self.pc_pieces)}\n')
        self.show_snake()
        print(f'\nYour pieces:')
        self.show_player_pieces()
        print()

        self.__check_finished()
        if not self.__game_started:
            return

        if self.status == 'computer':
            print('Status: Computer is about to make a move. Press Enter to continue...')
            input()
            self.pc_step()
            self.status = 'player'
        elif self.status == 'player':
            print('Status: It\'s your turn to make a move. Enter your command.')
            self.player_step()
            self.status = 'computer'

    def play(self):
        self.__game_started = True
        self.initialize_pieces()
        while self.__game_started:
            self.next_step()


if __name__ == "__main__":
    game = Dominoes()
    game.play()
