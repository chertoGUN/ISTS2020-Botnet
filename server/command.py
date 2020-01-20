import time
import random
import string
import base64
import uuid

def generateCommand(type_, team, ip, user):
    """Return a new command object of the given type"""

    command_types = {
        "linux": LinuxCommand,
        "windows": WindowsCommand
    }
    retval = command_types.get(type_, Command)
    return retval(team, ip, user)

class Command(object):
    """An object the represents a basic command.
    When checking the results of the command, it must match the output and the time must not have expired
    """

    TYPE = "generic/unknown"

    def __init__(self, team, ip, user):
        """
        Generate a command for the team/ip combo
        """
        self.ip = ip
        self.team = team
        self.time = time.time()  # The time that the command was issued
        self.user = user
        self.id = str(uuid.uuid4())

        # This result value is what the output of the command is tested agaist
        self.result = ""
        # The actual command that is to be run
        self.command = ""

    def __hash__(self):
        return self.id

    def __str__(self):
        return self.command.strip()+"\n"

    def json(self):
        return {
            "id": self.id,
            "command": self.command,
            "ip": self.ip,
            "team": self.team,
            "type": self.TYPE,
            "user": self.user
        }

    def check(self, text):
        """Check whether the result is valid is not"""
        if time.time() - self.time > 60:
            raise ValueError("The command has expired")
        if text.strip() != self.result.strip():
            raise ValueError("The results do not match")
        return True


class WindowsCommand(Command):
    """This class represents a Windows command object

    This will randomly choose a command that can be run and return it to the
    bot. This class expacts powershell commands to be run
    """
    TYPE = "windows"

    def __init__(self, team, ip, user):
        # Call the supers init function
        super().__init__(team, ip, user)
        
        # All the different options for the commands
        commands = [
            self._echo,
            self._checkAlpha, self._checkPhantom, self._checkVoodoo,
            self._lsass,
            self._drivers

        ]

        # Choose a random function to run
        com = random.choice(commands)
        # Run the function
        com()

    def _echo(self):
        """This is a simple echo out of a random value"""
        self.result = "".join(random.choice(string.ascii_lowercase) for i in range(30))
        self.command = "echo {}".format(self.result)
    
    def _checkAlpha(self):
            """This makes sure specific users are present"""
            self.result = "Name\n----\nalpha"
            self.command = "Get-LocalUser -Name \"alpha\" | select Name"

    def _checkVoodoo(self):
        """This makes sure specific users are present"""
        self.result = "Name\n----\nvoodoo"
        self.command = "Get-LocalUser -Name \"voodoo\" | select Name"

    def _checkPhantom(self):
        """This makes sure specific users are present"""
        self.result = "Name\n----\nphantom"
        self.command = "Get-LocalUser -Name \"phantom\" | select Name"
    
    def _lsass(self):
        self.result = "ProcessName\n----\nlsass"
        self.command = "get-process lsass |select ProcessName"
    
    def _drivers(self):
        self.result = "True"
        self.command = "Test-Path \'C:\Windows\system32\drivers\'"
 
    # TODO: Add these commands
    # Check system32 files/folders

class LinuxCommand(Command):
    """This class represents a linux command object

    This will randomly choose a command that can be run and return it to the
    bot.
    """
    TYPE = "linux"

    def __init__(self, team, ip, user):
        # Call the supers init function
        super().__init__(team, ip, user)
        
        # All the different options for the commands
        commands = [
            self._echo,
            self._base64,
            #self._printf,
            #self._ipa,
        ]

        # Choose a random function to run
        com = random.choice(commands)
        # Run the function
        com()

    def _echo(self):
        """This is a simple echo out of a random value"""
        self.result = "".join(random.choice(string.ascii_lowercase) for i in range(30))
        self.command = "echo {}".format(self.result)

    def _base64(self):
        """This command sends the base64 string to the bot and expects the decoded reply
        
        e.x.  sh -c "echo aGk= | base64 -d"    ==>    "hi"
        """
        # Generate a random result
        self.result = "".join(random.choice(string.ascii_lowercase) for i in range(30))
        # Base 64 the random result
        base_encoded = base64.standard_b64encode(self.result.encode("utf-8")).decode()
        # Set the command that is to be run
        self.command = 'sh -c "echo {} | base64 -d"'.format(base_encoded)

    def _printf(self):
        """This command runs printf with hex values and expects the output
        
        e.x.  printf "\x68\x69\n"     ==>     "hi"

        TODO: This is broken, but not really requried
        """
        # Generate a random result
        self.result = "".join(random.choice(string.ascii_lowercase) for i in range(30))
        # Create the hex values for the string
        printf = [hex(ord(i)).replace("0x", "\\x") for i in self.result]
        self.command = "printf '{}\\n'".format("".join(printf))
    
    def _ipa(self):
        """Check that they arent lying about the IP address

        Commented out by default because systems might not have ipa
        """
        self.command = "sh -c 'ip a | grep -o {}'".format(self.ip)
        self.result = self.ip
    
    # TODO:  Add more commands
    # Uname
    # Check Users
    # Maybe Root


def main():
    i = 0
    while i < 10:
        com = LinuxCommand("0", "8.8.8.8")
        print("{}. '{}' ==> '{}'   {}".format(i, com, com.result, com.id))
        i += 1

if __name__ == "__main__":
    main()