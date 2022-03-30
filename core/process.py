import subprocess

def getallprocs():
    try:
        cmd_out = execshproc('wmic process get description,processid')
        cmd_out = cmd_out.replace('\r','')
        cmd_out = cmd_out.split('\n')
        return cmd_out
    except FileNotFoundError:
        if input('wmic not in path! Can Automator add to the path variable? (y/n, default y) ') != 'n':
            from datab.env_vars import ADD_WMIC_TO_PATH
            ADD_WMIC_TO_PATH()
            if input('A reboot is required to apply changes. Reboot now? (y/n, default y)') != 'n':
                from core.execute import Attuator
                Attuator.System().shotdown(message='Rebooting',reboot=True)
                exit(0)
            else:
                return []
        else:
            return []

def execshproc(proc, lists=False, sep=' '):
    proc = proc.split(' ')
    cmd_out = subprocess.run(proc, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.decode('utf8')
    if lists == True:
        return cmd_out.split(sep)
    else:
        return cmd_out

def execpowershellprocess(proc):
    return subprocess.Popen(["powershell.exe", str(proc)], stdout=subprocess.PIPE).communicate()[0].decode('UTF-8')

def ExecutionPolicy():
    if execpowershellprocess('ExecutionPolicy') != 'RemoteSigned':
        try:
            from libs.LibWin import get_admin_rights
            get_admin_rights()
        except ImportError:
            import elevate
            elevate.elevate()
        proc = 'Set-ExecutionPolicy RemoteSigned'
        execpowershellprocess(proc)
        return True
    else:
        return True
