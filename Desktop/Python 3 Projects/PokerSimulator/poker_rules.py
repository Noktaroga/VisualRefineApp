# poker_rules.py
from pypokerengine.api.game import setup_config, start_poker
from player_strategies import FishPlayer

def run_simulation():
    config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)
    config.register_player(name="Player1", algorithm=RandomPlayer("Player1"))
    config.register_player(name="Player2", algorithm=RandomPlayer("Player2"))
    game_result = start_poker(config)
    return game_result

if __name__ == "__main__":
    game_result = run_simulation()
    print(game_result)
