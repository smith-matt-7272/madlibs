import PySimpleGUI as sg
import textwrap
from madlib import Madlib


class MadlibGUI():

    def __init__(self):
        self.title = 'MadLibs'
        self.B1 = '-B1-'
        self.B2 = '-B2-'
        self.Q = '-Q-'
        self.I = '-I-'
        self.game_closed_by_user = "Game closed by user."

    def player_selection(self) -> bool | None:

        layout = [
            [sg.Text("Do you wish to play? Or let the computer randomly select inputs?", key=self.Q)],
            [sg.Button("I'll play!", key=self.B1), sg.Button("Let the computer play!", key=self.B2)]
        ]

        window = sg.Window(self.title, layout)
        event, values = window.read()
        player_selected = None

        if event == sg.WIN_CLOSED:
            print(self.game_closed_by_user)
        elif event == self.B1:
            player_selected = True
        elif event == self.B2:
            player_selected = False

        window.close()

        return player_selected

    def madlib_selection_mode(self) -> bool | None:

        layout = [
            [sg.Text("Do you wish to select the Madlib? Or let the computer randomly select one?", key=self.Q)],
            [sg.Button("I'll select!", key=self.B1), sg.Button("Let the computer choose.", key=self.B2)]
        ]

        window = sg.Window(self.title, layout)
        event, values = window.read()
        player_selection_mode = None

        if event == sg.WIN_CLOSED:
            print(self.game_closed_by_user)
        elif event == self.B1:
            player_selection_mode = True
        elif event == self.B2:
            player_selection_mode = False

        window.close()

        return player_selection_mode

    def madlib_selection(self, num_madlibs) -> int:

        layout = [
            [sg.Text(f"Choose a number between 1 and {num_madlibs}", key=self.Q)],
            [sg.Input(key=self.I)],
            [sg.Button("Ok", key=self.B1, bind_return_key=True)]
        ]
        selection = -1
        window = sg.Window(self.title, layout)
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                print(self.game_closed_by_user)
                break
            elif event == self.B1:
                input_val = values[self.I]
                if input_val.isdigit() and (1 <= int(input_val) <= num_madlibs):
                    selection = int(input_val)
                    break
                else:
                    window[self.Q].update(f"\"{input_val}\" is not a valid choice.\nPlease enter a number between 1 and {num_madlibs}")

        window.close()
        return selection

    def request_placeholder_inputs(self, ml: Madlib) -> list:
        layout = [
            [sg.Text(f"Please enter a {ml.type_placeholders[0]}",key=self.Q)],
            [sg.Input(key=self.I)],
            [sg.Button("Submit",key=self.B1, bind_return_key=True)]
        ]

        window = sg.Window(self.title, layout)
        index = 0

        input_list = []

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                print(self.game_closed_by_user)
                break
            elif event == self.B1:
                if not values[self.I]:
                    continue
                else:
                    index = index + 1
                    input_list.append(values[self.I].upper())
                    if index < len(ml.type_placeholders):
                        window[self.Q].update(f"Please enter a {ml.type_placeholders[index]}.")
                        window[self.I].update("")
                    else:
                        break

        window.close()
        return input_list

    def display_completed_story(self, completed_story: str) -> None:
        layout = [
            [sg.Text(textwrap.fill(completed_story, 100), key=self.Q)],
            [sg.Button("Play again!", key=self.B1), sg.Button("Exit", key=self.B2)]
        ]
        play_again = 0
        window = sg.Window(self.title, layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, self.B2):
                break
            elif event == self.B1:
                play_again = 1
                break

        window.close()
        return play_again
