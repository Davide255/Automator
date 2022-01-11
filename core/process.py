import subprocess

'''def forpriority(priority, dicit):
    for i in dicit:
        for p in priority:
          if p in i:
            print('il programma {p} impedisce lo switch di rete')
            return database.returnv

    database.returnv = True      
    return database.returnv'''

def getallprocs():
    cmd_out = execshproc('wmic process get description')
    cmd_out = cmd_out.replace('\r','')
    cmd_out = cmd_out.split('\n')
    return cmd_out

def execshproc(proc, array=False, sep=' '):
    proc = proc.split(' ')
    cmd_out = subprocess.run(proc, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout.decode('utf8')
    if array == True:
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
