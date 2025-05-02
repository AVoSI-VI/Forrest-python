import argparse
import os
import sys
import textwrap

from . import base
from . import clone
from . import data
from . import diffs
from . import remote


def main():
    args = parse_args()
    args.func(args)

def parse_args():
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    init_parser = commands.add_parser('init')
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')

    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('object')

    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser('read-tree')
    read_tree_parser.set_defaults(func=read_tree)

    commit_parser = commands.add_parser('commit')
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('-m', '--message', required=True)

    log_parser = commands.add_parser('log')
    log_parser.set_defaults(func=log)
    log_parser.add_argument('oid', nargs='?')

    checkout_parser = commands.add_parser('checkout')
    checkout_parser.set_defaults(func=checkout)
    checkout_parser.add_argument('oid')

    tag_parser = commands.add_parser('tag')
    tag_parser.set_defaults(func=tag)
    tag_parser.add_argument('name')
    tag_parser.add_argument('oid', nargs='?')

    diff_parser = commands.add_parser('diff')
    diff_parser.set_defaults(func=diff)
    diff_parser.add_argument('file')

    rollbf_parser = commands.add_parser('rollbf')
    rollbf_parser.set_defaults(func=rollbf)
    rollbf_parser.add_argument('file')
    rollbf_parser.add_argument('oid')

    show_oid_history_parser = commands.add_parser('filehist')
    show_oid_history_parser.set_defaults(func=show_oid_history)
    show_oid_history_parser.add_argument('file')

    set_remote_parser = commands.add_parser('set-remote')
    set_remote_parser.set_defaults(func=set_remote)
    set_remote_parser.add_argument('remote')
    set_remote_parser.add_argument('tag')

    list_remotes_parser = commands.add_parser('list-remotes')
    list_remotes_parser.set_defaults(func=list_remotes)

    clone_repo_parser = commands.add_parser('clone')
    clone_repo_parser.set_defaults(func=clone_repo)
    clone_repo_parser.add_argument('tag')

    clone_file_parser = commands.add_parser('clone-file')
    clone_file_parser.set_defaults(func=clone_file)
    clone_file_parser.add_argument('tag')
    clone_file_parser.add_argument('file')

    #TODO set print of commit logs

    return parser.parse_args()

def init(args):
    data.init()
    print(f'Initialized empty Forrest repository in {os.getcwd()}/{data.GIT_DIR}')

def hash_object(args):
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))

def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_commit_objects(args.object, expected=None))
    print('\n')

def write_tree(args):
    print(base.write_tree())

def read_tree(args):
    base.read_tree() #args.tree

def commit(args):
    print(base.commit(args.message))

def log(args):
    oid  = args.oid
    commit = base.get_commit(oid)
    ch = commit.changes[1:-1]
    changes_list = ch.split(", ")
    #changes_list = commit.changes.split(",")
    #changes_list[0] = changes_list[0][1:]
    #changes_list[-1] = changes_list[-1][:-1]

    print(f'commit {oid}\n')
    print("changes:\n")
    for change in changes_list:
        print(change)
    # reader = csv.reader(commit.changes, quotechar='"')
    # for row in reader:
    #     print(row)    
    #print(f'changes:\n {commit.changes}\n')
    print('')
    print("message:\n")
    print(textwrap.indent(commit.message, '   '))
    print('')

def checkout(args):
    base.checkout(args.oid)

def tag(args):
    oid = args.oid or data.get_ref('HEAD')
    base.create_tag(args.name, oid)

def diff(args):
    diffs.diff_file(args.file)

def rollbf(args):
    base.roll_back_file(str(args.file), str(args.oid))

def show_oid_history(args):
    base.show_oid_history(str(args.file))

def set_remote(args):
    remote.set_remote(args.remote, args.tag)

def list_remotes(args):
    for k,v in remote.list_remotes().items():
        print(f'tag: {k}, remote: {v}')

def clone_repo(args):
    clone.clone_repo(args.tag)

def clone_file(args):
    clone.clone_file(args.tag, args.file)