

class Errors():
    
    def Json_Error(self):
        
        from kivymd.uix.dialog import MDDialog
        from datab.database import database
        lang = database().get_langauge()['Errors.Json_Error']

        self.dialog = MDDialog(
            title=lang['title'].encode('latin1').decode('utf-8'),
            text=lang['text'].encode('latin1').decode('utf-8'),
            buttons=[

            ]
        )
    
    def critical_error(self, e='[No error info aviable]'):
        import os, win32gui, win32con
        win32gui.MessageBox(os.environ.get('Main_Window_hWnd'), 'An error occurred while executing: {}'.format(e), 'Critical Error', win32con.IDI_ERROR)
        win32gui.MessageBeep(win32con.IDI_ERROR)

class Advises():

    def close_adv(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
        from datab.database import database
        btext = database().get_langauge()['advises_shower.close_adv.button']
        try:
            hint_title = database().get_langauge()['advises_shower.close_adv']['title'].encode('latin1').decode('utf-8')
        except UnicodeError:
            hint_title = database().get_langauge()['advises_shower.close_adv']['title']
                
        try:
            hint_text = database().get_langauge()['advises_shower.close_adv']['text'].encode('latin1').decode('utf-8')
        except UnicodeError:
            hint_text = database().get_langauge()['advises_shower.close_adv']['text']

        self.dialog = MDDialog(
                        title= hint_title,
                        text= hint_text,
                        buttons= [
                            MDFlatButton(
                                text=btext[0],
                                on_release=self.dialog.dismiss()),
                            MDFillRoundFlatButton(
                                text=btext[1],
                                on_release=self.dialog.dismiss())],
                        )

    def Deactivate_Adv(self, sw):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
        from datab.database import database
        import os, win32gui, win32con

        if database().get_settings()['deact_adv'] == True:
            return database().manage_aut(sw.id, 'active', True if sw.active else False)

        if not sw.active:
            try:
                hint_title = database().get_langauge()['advises_shower.deactivate_adv']['title'].encode('latin1').decode('utf-8')
            except UnicodeError:
                hint_title = database().get_langauge()['advises_shower.deactivate_adv']['title']
                
            try:
                hint_text = database().get_langauge()['advises_shower.deactivate_adv']['text'].encode('latin1').decode('utf-8')
            except UnicodeError:
                hint_text = database().get_langauge()['advises_shower.deactivate_adv']['text']

            if not os.path.isfile(os.path.join(os.getcwd(), 'tmp', '.switch_acting')):
                if not os.path.isfile('tmp\\.startup'):
                    dlg = win32gui.MessageBox(os.environ.get('Main_Window_hWnd'), hint_text, hint_title, win32con.MB_OKCANCEL)
                    if dlg == win32con.IDOK:
                        database().manage_aut(sw.id, 'active', True if sw.active else False)
                    elif dlg == win32con.IDCANCEL:
                        sw.active = True
                import random
                s = [i for i in range(5)]
                if random.choice(s) == 4:
                    dlg = win32gui.MessageBox(os.environ.get('Main_Window_hWnd'), 
                        'If you turn off this advise, Automator will not send you any dialog at the deactivation of an Automation.',
                        'Do you want to turn it off?',
                        win32con.MB_OKCANCEL)
                    if dlg == win32con.IDOK:
                        database().set('deact_adv', True)
                    else:
                        pass
        else:
            return

class DependencesFail(BaseException):
    pass

#exception that stop the application
class StopApplication(BaseException):
    pass


