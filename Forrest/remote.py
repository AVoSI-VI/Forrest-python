import os
import pickle

def set_remote(remote, name):
    if os.path.isfile("./.Forrest/pickle/remote.pkl"):
            with open('./.Forrest/pickle/remote.pkl', 'rb') as f:
                remote_repo_pickle = pickle.load(f)
    else:
         remote_repo_pickle = {}

    remote_repo_pickle[name] = remote

    with open('./.Forrest/pickle/remote.pkl', 'wb') as f:
        pickle.dump(remote_repo_pickle, f)

def list_remotes():
    if os.path.isfile("./.Forrest/pickle/remote.pkl"):
        with open('./.Forrest/pickle/remote.pkl', 'rb') as f:
            remote_repo_pickle = pickle.load(f)
    else:
        remote_repo_pickle = {}
        print("No remote repos set.")
    
    return remote_repo_pickle