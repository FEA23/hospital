
class Commands:
    GET_STATUS = ('узнать статус пациента', 'get status')
    STATUS_UP = ('повысить статус пациента', 'status up')
    STATUS_DOWN = ('понизить статус пациента', 'status down')
    DISCHARGE = ('выписать пациента', 'discharge')
    CALCULATE_STATISTICS = ('рассчитать статистику', 'calculate statistic')
    STOP = ('стоп', 'stop')



    def __init__(self, command: str):
        self.command = command
        self.commands = (
            self.GET_STATUS,
            self.STATUS_UP,
            self.STATUS_DOWN,
            self.DISCHARGE,
            self.CALCULATE_STATISTICS,
            self.STOP
        )

    def correct(self):
        for command_tuple in self.commands:
            if self.command.strip() in command_tuple:
                return True

        return False


    def is_get_status(self):
        return self.command.strip() in self.GET_STATUS


    def is_up_status(self):
        return self.command.strip() in self.STATUS_UP

    def is_down_status(self):
        return self.command.strip() in self.STATUS_DOWN

    def is_discharge(self):
        return self.command.strip() in self.DISCHARGE

    def is_statistic(self):
        return self.command.strip() in self.CALCULATE_STATISTICS

    def is_stop(self):
        return self.command.strip() in self.STOP

