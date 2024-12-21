import pygame
import random
import copy
import os

# Colors for the tiles
COLORS = {
    0: (238, 228, 218), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
    256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46)
}

class Game2048:
    def __init__(self, difficulty="Medium"):
        pygame.init()

        # Difficulty settings
        self.difficulty = difficulty
        self.set_grid_size_and_tile()

        self.margin = 10
        self.width = self.height = self.grid_size * self.tile_size + (self.grid_size + 1) * self.margin
        self.screen = pygame.display.set_mode((self.width, self.height + 100))
        pygame.display.set_caption(f"2048 Game - {self.difficulty} Mode")
        
        self.font = pygame.font.Font(None, 40)
        self.score_font = pygame.font.Font(None, 60)
        self.undo_font = pygame.font.Font(None, 30)
        self.game_over_font = pygame.font.Font(None, 80)

        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.previous_board = None
        self.score = 0
        self.is_game_over = False

        self.reset_game()

        self.load_leaderboard()

    def set_grid_size_and_tile(self):
        if self.difficulty == "Easy":
            self.grid_size = 3
            self.tile_size = 100
        elif self.difficulty == "Hard":
            self.grid_size = 5
            self.tile_size = 80
        else:  # Default "Medium"
            self.grid_size = 4
            self.tile_size = 100

    def reset_game(self):
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.add_random_tile()
        self.add_random_tile()
        self.score = 0
        self.is_game_over = False

    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def draw_board(self):
        self.screen.fill((250, 248, 239))  # Light beige background
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                rect = pygame.Rect(
                    self.margin + j * (self.tile_size + self.margin),
                    self.margin + i * (self.tile_size + self.margin),
                    self.tile_size,
                    self.tile_size
                )
                
                if value == 0:
                    tile_color = (238, 228, 218)  # Beige color for empty squares
                else:
                    tile_color = COLORS[value]
                
                pygame.draw.rect(self.screen, tile_color, rect)
                
                # Draw border
                border_color = (187, 173, 160)
                border_width = 4
                pygame.draw.rect(self.screen, border_color, rect, border_width)
                
                if value != 0:
                    text = self.font.render(str(value), True, (119, 110, 101))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

        # Draw score
        score_text = self.score_font.render(f"Score: {self.score}", True, (128, 0, 128))
        self.screen.blit(score_text, (20, self.height + 20))

        # Draw undo button
        undo_rect = pygame.Rect(self.width - 120, self.height + 20, 100, 50)
        pygame.draw.rect(self.screen, (119, 110, 101), undo_rect)
        undo_text = self.undo_font.render("Undo", True, (255, 255, 255))
        undo_text_rect = undo_text.get_rect(center=undo_rect.center)
        self.screen.blit(undo_text, undo_text_rect)

        # Game over text
        if self.is_game_over:
            game_over_text = self.game_over_font.render("Game Over!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, game_over_rect)

            # Show leaderboard
            self.show_leaderboard()

        pygame.display.flip()

    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    def merge_row(self, row):
        row = [num for num in row if num != 0]
        merged_row = []
        i = 0
        while i < len(row):
            if i + 1 < len(row) and row[i] == row[i + 1]:
                merged_row.append(row[i] * 2)
                self.score += row[i] * 2
                i += 2
            else:
                merged_row.append(row[i])
                i += 1
        return merged_row + [0] * (self.grid_size - len(merged_row))

    def move_left(self):
        for i in range(self.grid_size):
            self.board[i] = self.merge_row(self.board[i])

    def move_right(self):
        for i in range(self.grid_size):
            self.board[i] = self.merge_row(self.board[i][::-1])[::-1]

    def move_up(self):
        self.board = self.transpose(self.board)
        self.move_left()
        self.board = self.transpose(self.board)

    def move_down(self):
        self.board = self.transpose(self.board)
        self.move_right()
        self.board = self.transpose(self.board)

    def can_move(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return True
                if j + 1 < self.grid_size and self.board[i][j] == self.board[i][j + 1]:
                    return True
                if i + 1 < self.grid_size and self.board[i][j] == self.board[i + 1][j]:
                    return True
        return False

    def undo(self):
        if self.previous_board:
            self.board = self.previous_board
            self.previous_board = None

    def handle_click(self, pos):
        undo_rect = pygame.Rect(self.width - 120, self.height + 20, 100, 50)
        if undo_rect.collidepoint(pos):
            self.undo()

    def handle_keypress(self, key):
        if not self.is_game_over:
            self.previous_board = copy.deepcopy(self.board)
            if key == pygame.K_UP:
                self.move_up()
            elif key == pygame.K_DOWN:
                self.move_down()
            elif key == pygame.K_LEFT:
                self.move_left()
            elif key == pygame.K_RIGHT:
                self.move_right()
            elif key == pygame.K_F1:  # Change difficulty to Easy
                self.difficulty = "Easy"
                self.set_grid_size_and_tile()
                self.reset_game()
                pygame.display.set_caption(f"2048 Game - {self.difficulty} Mode")
            elif key == pygame.K_F2:  # Change difficulty to Medium
                self.difficulty = "Medium"
                self.set_grid_size_and_tile()
                self.reset_game()
                pygame.display.set_caption(f"2048 Game - {self.difficulty} Mode")
            elif key == pygame.K_F3:  # Change difficulty to Hard
                self.difficulty = "Hard"
                self.set_grid_size_and_tile()
                self.reset_game()
                pygame.display.set_caption(f"2048 Game - {self.difficulty} Mode")

            if self.board != self.previous_board:
                self.add_random_tile()

            if not self.can_move():
                self.is_game_over = True
                self.update_leaderboard()

    def load_leaderboard(self):
        """Load leaderboard from file"""
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r") as file:
                self.leaderboard = [int(line.strip()) for line in file.readlines()]
        else:
            self.leaderboard = []

    def save_leaderboard(self):
        """Save leaderboard to file"""
        with open("leaderboard.txt", "w") as file:
            for score in self.leaderboard:
                file.write(f"{score}\n")

    def update_leaderboard(self):
        """Update leaderboard if the score is high enough"""
        self.leaderboard.append(self.score)
        self.leaderboard.sort(reverse=True)
        self.leaderboard = self.leaderboard[:5]  # Keep top 5 scores
        self.save_leaderboard()

    def show_leaderboard(self):
        """Display the leaderboard"""
        y_offset = self.height // 2 + 100
        leaderboard_text = self.game_over_font.render("Leaderboard", True, (0, 0, 255))
        self.screen.blit(leaderboard_text, (self.width // 2 - leaderboard_text.get_width() // 2, y_offset))

        for idx, score in enumerate(self.leaderboard):
            score_text = self.game_over_font.render(f"{idx + 1}. {score}", True, (0, 0, 0))
            self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, y_offset + (idx + 1) * 50))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keypress(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.draw_board()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    # Default difficulty is Medium
    Game2048(difficulty="Medium").run()
