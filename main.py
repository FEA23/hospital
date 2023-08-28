from application import Application
from hospital import Hospital
from dialogue import Dialogue
from commands import Commands, CommandHandlers
from console import Console

if __name__ == '__main__':
    hospital = Hospital()
    dialogue = Dialogue(console=Console)
    command_handlers = CommandHandlers(hospital=hospital, dialogue=dialogue)

    app = Application(dialogue, command_handlers)
    app.main()
