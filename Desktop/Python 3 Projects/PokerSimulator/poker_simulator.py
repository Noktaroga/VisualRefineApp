# poker_simulator.py
from pypokerengine.api.game import setup_config, start_poker
from pypokerengine.players import BasePokerPlayer

class FishPlayer(BasePokerPlayer):
    def __init__(self):
        super().__init__()

    def declare_action(self, valid_actions, hole_card, round_state):
        optimal_actions = self.run_simulation()

        round_number = round_state['round_count']

        if self.uuid in optimal_actions[round_number]:
            optimal_action = optimal_actions[round_number][self.uuid]
            for action_info in valid_actions:
                if action_info['action'] == optimal_action:
                    return action_info['action'], action_info['amount']
        
        return valid_actions[1]['action'], valid_actions[1]['amount']

    def run_simulation(self):
        config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=10)
        config.register_player(name="Player1", algorithm=FishPlayer())
        config.register_player(name="Player2", algorithm=FishPlayer())
        game_result = start_poker(config)
        return game_result

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

if __name__ == "__main__":
    fish_player = FishPlayer()
    game_result = fish_player.run_simulation()
    print(game_result)
