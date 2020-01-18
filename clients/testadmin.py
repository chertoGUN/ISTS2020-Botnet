from admin import BotnetAdmin

def main():
    cli = BotnetAdmin(server="http://0.0.0.0:5000", token="adminadmin")
    print(cli.getscore())
    print(cli.gethosts())

main()