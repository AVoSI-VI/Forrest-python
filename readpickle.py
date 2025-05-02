import os
import pickle

if os.path.isfile("./.ugit/pickle/ugit.pkl"):
    with open('./.ugit/pickle/ugit.pkl', 'rb') as f:
        dirdir = pickle.load(f)

for k in dirdir.items():
    print(k)