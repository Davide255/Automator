from core.execute import Execute
from datab.database import database
import time

class start:

    def __init__(self, **kwargs):
        from kivy import Logger
        
        if kwargs.get('coll_down_time'):
            self.coll_down = float(kwargs.get('coll_down_time'))
        else:
            self.coll_down = 5

        self.done = []
        self.all = {}

        self.data = database().get_data()

        n = 0
        for i in self.data:

            if i['active']:

                self.action = i['actions']
                self.automation = self.action['automation']
                self.action_to_do = self.action['action_to_do']
                self.all[n] = (self.automation, self.action_to_do)

            n += 1

        while True:
            for i in list(self.all.keys()):
                if not i in self.done:
                    try:
                        if Execute().Execute(*self.all[i]):
                            self.done.append(i)
                        Logger.debug('Core: ' + str(self.done))
                    except KeyError as e:
                        Logger.debug('KeyError:', e, 'is not recognized as valid action')
                    except Exception as e:
                        Logger.debug(e)
                else:
                    pass

            time.sleep(self.coll_down)
            