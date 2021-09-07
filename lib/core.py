# CORE file contains main shell mechanisms
from importlib import import_module as _import
from time import sleep

from lib.utils import *
from lib.vfs import init


class shell():
    def __init__(self):
        init()

    def __repr__(self):
        return '<Shell Instance>'

    def get_input(self):
        if prop.get('prompt') != NULL:
            if prop.get('prompt') == '-def':
                sh = '@Squirrix/' + get_path() + '> '
            else:
                sh = prop.get('prompt') + ' '
        else:
            sh = '@Squirrix:' + get_path() + '> '
        inp = input(sh)
        return inp

    def execute(self, inp):
        inp = inp.split()
        # print(inp)
        inp = make_s(replace_vars(inp))
        inp = inp.split()
        # print(inp)
        # Get hidden commands as well
        f_list = get_func_list(True)

        try:
            f = inp[0]
            inp.pop(0)
        except IndexError:
            return
        if f in f_list:
            mod = 'bin.' + f
            m = _import(mod)
            try:
                m.main(inp)
            except TypeError:
                try:
                    m.main()
                except TypeError:
                    err(1)
            except AttributeError:
                err(1, f)
        elif f not in f_list:
            analyze(f)

    def start(self):
        print(""" .d8888b.                    d8b                 d8b          
d88P  Y88b                   Y8P                 Y8P          
Y88b.                                                         
 "Y888b.    .d88888 888  888 888 888d888 888d888 888 888  888 
    "Y88b. d88" 888 888  888 888 888P"   888P"   888 `Y8bd8P' 
      "888 888  888 888  888 888 888     888     888   X88K   
Y88b  d88P Y88b 888 Y88b 888 888 888     888     888 .d8""8b. 
 "Y8888P"   "Y88888  "Y88888 888 888     888     888 888  888 
                888                                           
                888                                           
                888                                           """)
        # write config file
        write_config()
        sleep(1)
        print('Running...\n')
        sleep(0.5)
        print('Issue "help" to get started or type "lcom" to list every command...\n')
        while True:
            inp = self.get_input()
            self.execute(inp)
