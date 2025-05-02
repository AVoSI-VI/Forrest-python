import itertools
import operator
import os
import pickle

from collections import namedtuple
from . import data

def write_tree(directory='.'):
    if os.path.isfile("./.Forrest/pickle/Forrest.pkl"):
        with open('./.Forrest/pickle/Forrest.pkl', 'rb') as f:
            dirdir = pickle.load(f)
    else:
        dirdir = {}
    changes = {}
    for dirpath, dirnames, files in os.walk(directory):
        for file in files:
            
            path = dirpath+'/'+file
            if is_ignored(path):
                 continue
            type_ = 'blob'
            with open(path, 'rb') as f:
                oid = data.hash_object(f.read())
            if path not in dirdir:
                dirdir[path] = [oid]
                changes[path] = [oid]
            elif path in dirdir and oid in dirdir[path]:
                continue
            else:
                dirdir[path].append(oid)
                changes[path] = [oid]

    with open('./.Forrest/pickle/Forrest.pkl', 'wb') as f:
        pickle.dump(dirdir, f)
    
    return changes

def _empty_current_directory():
    for root, dirnames, filenames in os.walk('.', topdown=False):
        for filename in filenames:
            path = os.path.relpath(f'{root}/{filename}')
            if is_ignored(path) or not os.path.isfile(path):
                continue
            os.remove(path)
        for dirname in dirnames:
            path = os.path.relpath(f'{root}/{dirname}')
            if is_ignored(path):
                continue
            try:
                os.rmdir(path)
            except(FileNotFoundError, OSError):
                pass


def read_tree():
    if os.path.isfile("./.Forrest/pickle/Forrest.pkl"):
        with open('./.Forrest/pickle/Forrest.pkl', 'rb') as f:
            dirdir = pickle.load(f)
    _empty_current_directory()
    for k, v in dirdir.items():
        os.makedirs(os.path.dirname(k), exist_ok=True)
        with open(k, 'wb') as f:
             f.write(data.get_object(dirdir[k][-1]))

def write_clone_file(file):
    if os.path.isfile("./.Forrest/pickle/Forrest.pkl"):
        with open('./.Forrest/pickle/Forrest.pkl', 'rb') as f:
            dirdir = pickle.load(f)
    else:
        print("problem with directory, Forrest.pkl not found")

    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'wb') as f:
        f.write(data.get_object(dirdir[file][-1]))

def roll_back_file(file, oid):
    if os.path.isfile("./.Forrest/pickle/Forrest.pkl"):
        with open('./.Forrest/pickle/Forrest.pkl', 'rb') as f:
            dirdir = pickle.load(f)
    index_of_oid = dirdir[file].index(oid) 
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'wb') as f:
        f.write(data.get_object(dirdir[file][index_of_oid]))

def show_oid_history(file):
    if os.path.isfile("./.Forrest/pickle/Forrest.pkl"):
        with open('./.Forrest/pickle/Forrest.pkl', 'rb') as f:
            dirdir = pickle.load(f)
    print(dirdir[file])

def commit(message):
    changes = write_tree()
    c = []
    for k, v in changes.items():
        c.append(f'{k}: {v}')
    commit = f'changes: {c}\n'
    #commit = f'changes: {write_tree()}\n'
    commit += '\n'
    commit += f'{message}\n'

    oid = data.write_commit_objects(commit.encode(), 'commit')

    return oid

def checkout(oid):
    commit = get_commit(oid)
    read_tree(commit.tree)
    data.update_ref('HEAD', oid)

def create_tag(name, oid):
    pass

Commit = namedtuple('Commit', ['changes', 'message'])

def get_commit(oid):
    commit = data.get_commit_objects(oid, 'commit').decode()
    lines = iter(commit.splitlines())
    for line in itertools.takewhile(operator.truth, lines):
        key, value = line.split(' ', 1)
        if key == 'changes:':
            changes = value
        else:
            assert False, f'Unknown field {key}'

    message = '\n'.join(lines)
    return Commit(changes=changes, message=message)

def is_ignored(path):
    return '.Forrest' in path.split('/')
