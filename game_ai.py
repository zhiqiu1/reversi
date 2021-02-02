from copy import deepcopy
from typing import Union

import game_mechanics


def minimax_with_alpha_beta(game: game_mechanics.Reversi, curr_depth: int, target_depth: int,
                            alpha: float, beta: float) -> Union[tuple, float]:
    if curr_depth == target_depth or game.game_is_over:
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
                    copy.place((i, j), 0 == target_depth - 1)
                    minimax_value = minimax_with_alpha_beta(copy, 1, target_depth, alpha, beta)
                    if minimax_value > score:
                        score = minimax_value
                        alpha = score
                        res = (i, j)
        return res
    for i in range(game.N_OF_ROW):
        for j in range(game.N_OF_COL):
            if game.is_valid_move((i, j)):
                copy = deepcopy(game)
                copy.place((i, j), curr_depth == target_depth - 1)
                minimax_value = minimax_with_alpha_beta(copy, curr_depth + 1, target_depth, alpha, beta)
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
