from admin import BotnetAdmin

def main():
    cli = BotnetAdmin(server="http://0.0.0.0:5000", token="adminadmin")
    print(cli.getscore())
    print(cli.gethosts())
    print(cli.sethosts(["8.8.8.8","1.1.1.1"]))
    print(cli.getscore())


main()