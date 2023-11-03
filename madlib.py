class Madlib:

    def __init__(self, story: str, type_placeholders: list[str]):
        self.incomplete_story = story
        self.completed_story = ""
        self.type_placeholders = type_placeholders

    def get_placeholders(self) -> list[str]:
        return self.type_placeholders

    def fill_story(self, inputs: list) -> None:

        s = self.incomplete_story

        for input in inputs:
            s = s.replace("##", input, 1)

        self.completed_story = s

    def get_incomplete_story(self) -> str:
        return self.incomplete_story

    def get_completed_story(self) -> str:
        return self.completed_story