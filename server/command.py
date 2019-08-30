import time
import random
import string


class Command(object):
    """An object the represents a basic command.
    When checking the results of the command, it must match the output and the time must not have expired
    """

    def __init__(self, data):
        """
        Data can be anything that is unique to the request, this will prevent a collision if
        there are multiple requests at the same time
        """
        self.time = time.time()  # The time that the command was issued
        self.id = hash(data) + hash(self.time)  # The ID of the command
        self.result = "".join(random.choice(string.ascii_lowercase) for i in range(30))

    def __hash__(self):
        return self.id

    def __str__(self):
        return "echo {}\n".format(self.result)

    def check(self, text):
        if time.time() - self.time > 60:
            raise ValueError("The command has expired")
        if text.strip() != self.result.strip():
            raise ValueError("The results do not match")
        return True
