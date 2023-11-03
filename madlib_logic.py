
from madlib_interface import MadlibGUI
from madlib_data import MadlibData
from madlib import Madlib
import random

class MadlibLogic:
    """The logic and middle layer of the Madlib game.
    Loads the needed data from the MadlibData layer,
    and prompts the MadlibGui layer to display results,
    request inputs, etc.
    """
    def load_placeholder_words(self, ml: Madlib, data: MadlibData) -> dict:
        """Loads possible computer-selected inputs.

        Considers the unique placeholders for the Madlib puzzle,
        and loads the needed word files to populate the selections.
        """
        placeholder_words_dict = {}

        for placeholder in ml.get_placeholders():
            if placeholder not in placeholder_words_dict.keys():
                placeholder_words_dict[placeholder] = data.load_words(f"static/{placeholder.replace(' ','_')}s.txt")

        return placeholder_words_dict

    def get_computer_inputs(self,ml: Madlib, data: MadlibData) -> list:
        """Will provide computer-selected inputs for the Madlib puzzle.

        Loads possible word selections from data layer and randomly selects
        words from dictionary.
        """
        input_list = []
        placeholder_words_dict = self.load_placeholder_words(ml, data)

        for type in ml.type_placeholders:
            num_word_types = len(placeholder_words_dict[type])
            input_list.append(placeholder_words_dict[type][random.randint(0, num_word_types-1)].upper())

        return input_list

    def choose_madlib(self,player_choice,num_madlibs, gui) -> int:
        """Prompts user or system to select from available Madlib puzzles.

        Depending on player_choice, will either prompt user to select, or
        have system randomly select from index of available Madlibs
        """
        if num_madlibs == 1:
            return 1

        if player_choice:
            return gui.madlib_selection(num_madlibs)
        else:
            return random.randint(1, num_madlibs)


    def play_game(self):
        """Core driver of the game

        Handles the core logic of the game, performing the necessary prompts,
        responses, and actions needed to complete a Madlib cycle.
        """
        data = MadlibData()
        gui = MadlibGUI()

        madlibs_list: list[Madlib] = [Madlib(x[0], x[1]) for x in data.load_stories("static/madlibs.txt")]
        if madlibs_list == []:
            print("No madlibs were loaded. Please check for static/madlibs.txt and ensure stories and placeholders are present")
            return 0
        player_is_user: bool = gui.player_selection()
        print(f"User as player: {player_is_user}")
        if player_is_user is None:
            return 0
        player_chooses_madlib: bool = gui.madlib_selection_mode()
        if player_chooses_madlib is None:
            return 0
        print(f"User will select Madlib: {player_chooses_madlib}")

        selected_madlib_num: int = self.choose_madlib(player_chooses_madlib, len(madlibs_list), gui)
        if selected_madlib_num == -1:
            return 0
        print(f"Madlib selected: {selected_madlib_num}")

        madlib: Madlib = madlibs_list[selected_madlib_num-1]
        print(f"Selected story: \n{madlib.get_incomplete_story()}")
        inputs = []

        if player_is_user:
            inputs = gui.request_placeholder_inputs(madlib)
        else:
            inputs = self.get_computer_inputs(madlib, data)

        madlib.fill_story(inputs)
        completed_story = madlib.get_completed_story()
        data.write_story_to_file("./completed_madlibs.txt",completed_story)

        play_again = gui.display_completed_story(completed_story)

        return play_again
