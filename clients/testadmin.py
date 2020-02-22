from admin import BotnetAdmin

def main():
    cli = BotnetAdmin(server="http://0.0.0.0:5000", token="adminadmin")
    print(cli.getscore())
    print(cli.gethosts())
    print(cli.sethosts(
    {
        "127.0.0.1": "linux",
        "8.8.4.4": "windows"
    }))
    print(cli.getscore())


main()