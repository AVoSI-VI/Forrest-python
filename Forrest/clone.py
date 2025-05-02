import os
import pickle

from shutil import copytree, ignore_patterns, copy2
from . import base
from . import data
from . import remote

def clone_repo(remote_repo_tag):
    remote_repos = remote.list_remotes()
    remote_to_clone = remote_repos[remote_repo_tag]

    directory_for_clone = '.Forrest'

    try:
        copytree(remote_to_clone, directory_for_clone, dirs_exist_ok=True)
    except:
        print("no can do")
    
    base.read_tree()


def clone_file(remote_repo_tag, file):
    remote_repos = remote.list_remotes()
    remote_to_clone = remote_repos[remote_repo_tag]
    directory_for_clone = '.Forrest'

    try:
        copytree(remote_to_clone, directory_for_clone, dirs_exist_ok=True, ignore=ignore_patterns('objects*', 'remote*'))
    except:
         print("no can do")

    if os.path.isfile("./.Forrest/pickle/Forrest.pkl"):
        with open('./.Forrest/pickle/Forrest.pkl', 'rb') as f:
            dirdir = pickle.load(f)

    files_to_copy = dirdir[file]

    for file_name in files_to_copy:
        copy2(f'{remote_to_clone}/objects/{file_name}', './.Forrest/objects/')

    base.write_clone_file(file)

    remote.set_remote("parent", remote_to_clone)

    # os.makedirs(os.path.dirname(directory_for_clone), exist_ok=True)
    # with open(directory_for_clone, 'wb') as f:
    #         f.write(data.get_object(dirdir[file][-1]))
