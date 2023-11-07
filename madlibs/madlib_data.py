class MadlibData():
    """Data layer to Madlib game.

    Performes the necessary file reads/writes to play
    the MadLib game.
    """
    def load_stories(self, filename) -> list[(str, list[str])]:
        """Loads Madlib stories given a filename.
        Returns a list of tuples.
        """
        stories = []
        try:
            with open(filename, 'r') as f:
                for text in f:
                    stories.append((text.strip(), f.readline().strip().split(',')))
        except FileNotFoundError:
            print("Stories file not found.")
        return stories

    def load_words(self, filename) -> list[str]:
        """Loads words from a given filename.
        Returns a list of strings.
        """
        words = []
        try:
            with open(filename, 'r') as f:
                words = [x.strip() for x in f.read().splitlines()]
        except FileNotFoundError:
            print(f"Words file {filename} was not found.")
        return words

    def write_story_to_file(self, filename, completed_story):
        """Writes a completed story to a given filename.
        Returns a boolean.
        """
        with open(filename, 'a') as f:
            f.write(completed_story)
            f.write("\n-----------------------------------\n")
