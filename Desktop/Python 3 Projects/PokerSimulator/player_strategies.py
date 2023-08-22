from pypokerengine.players import BasePokerPlayer
from poker_rules import run_simulation  # Importa run_simulation desde poker_rules

class FishPlayer(BasePokerPlayer):
    def __init__(self):
        super().__init__()

    def declare_action(self, valid_actions, hole_card, round_state):
        optimal_actions = run_simulation()
        round_number = round_state['round_count']

        if self.uuid in optimal_actions[round_number]:
            optimal_action = optimal_actions[round_number][self.uuid]
            for action_info in valid_actions:
                if action_info['action'] == optimal_action:
                    return action_info['action'], action_info['amount']
        
        return valid_actions[1]['action'], valid_actions[1]['amount']

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        round_number = round_state['round_count']
        player_name = self.uuid
        action = self.play_histories[round_number]['action']
        optimal_action = run_simulation()[round_number][self.uuid]
        
        if action == optimal_action:
            result = 'Correct'
        else:
            result = 'Incorrect'
        
        print(f'Round {round_number}, Player: {player_name}')
        print(f'Taken Action: {action}, Optimal Action: {optimal_action}')
        print(f'Result: {result}')
        print('=' * 40)
