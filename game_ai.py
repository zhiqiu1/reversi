from copy import deepcopy

import game_mechanics


class AI:
    def __init__(self, game: game_mechanics.Reversi, search_depth: int):
        self._SEARCH_DEPTH = search_depth
        self.MOVE = self._minimax_with_alpha_beta(game, 0, float('-inf'), float('inf'))

    def _minimax_with_alpha_beta(self, game, curr_depth: int, alpha: float, beta: float) -> float:
        if curr_depth == self._SEARCH_DEPTH or game.game_is_over:
            # Using ratio as value is because the tree might be incomplete. 0.01 is used when the divisor is 0.
            if curr_depth % 2 == 0:
                return game.disk_count[game.curr_turn] / (
                    game.disk_count[game.next_turn] if game.disk_count[game.next_turn] != 0 else 0.01)
            return game.disk_count[game.next_turn] / (
                game.disk_count[game.curr_turn] if game.disk_count[game.curr_turn] != 0 else 0.01)
        score = float('-inf') if curr_depth % 2 == 0 else float('inf')
        if curr_depth == 0:
            for i in range(game.N_OF_ROW):
                for j in range(game.N_OF_COL):
                    if game.is_valid_move((i, j)):
                        copy = deepcopy(game)
                        copy.place((i, j), 0 == self._SEARCH_DEPTH - 1)
                        minimax_value = self._minimax_with_alpha_beta(copy, 1, alpha, beta)
                        if minimax_value > score:
                            score = minimax_value
                            alpha = score
                            res = (i, j)
            return res
        for i in range(game.N_OF_ROW):
            for j in range(game.N_OF_COL):
                if game.is_valid_move((i, j)):
                    copy = deepcopy(game)
                    copy.place((i, j), curr_depth == self._SEARCH_DEPTH - 1)
                    minimax_value = self._minimax_with_alpha_beta(copy, curr_depth + 1, alpha, beta)
                    # Maximiser
                    if curr_depth % 2 == 0:
                        score = max(score, minimax_value)
                        alpha = max(score, alpha)
                        if score >= beta:
                            return score
                    # Minimiser
                    else:
                        score = min(score, minimax_value)
                        beta = min(score, beta)
                        if score <= alpha:
                            return score
        return score
