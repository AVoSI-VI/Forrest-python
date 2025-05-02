import difflib
import os
import pickle

from . import data

def diff_file(path):
    try:
        with open('./.Forrest/pickle/Forrest.pkl', 'rb') as f:
            dirdir = pickle.load(f)
    except:
        print("./.Forrest/pickle/Forrest.pkl does not exit")
    
    if len(dirdir[path]) >= 2:
        head = open(f'./.Forrest/objects/{dirdir[path][-1]}', 'rb')
        previous_head = open(f'./.Forrest/objects/{dirdir[path][-2]}', 'rb')
        objhead = head.read()
        objprevhead = previous_head.read()
        _,_, content = objhead.partition(b'\x00')
        _,_, pcontent = objprevhead.partition(b'\x00')
        c = content.decode()
        pc = pcontent.decode()
        difference = difflib.unified_diff(pc.splitlines(), c.splitlines(), lineterm='')
        for line in difference:
            print('\n'.join(difference))
    else:
        print("Nothing to diff")

def diff_commits():
    pass