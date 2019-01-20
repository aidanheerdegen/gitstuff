import os, shlex, subprocess

def get_commit_id(filepath):
    """Return git commit hash for filepath."""
    cmd = shlex.split("git log -n 1 --pretty=format:%H -- ")
    cmd.append(filepath)
    try:
        with open(os.devnull, 'w') as devnull:
            commit_id = subprocess.check_output(cmd, stderr=devnull)

        return commit_id.decode('ascii').strip()

    except subprocess.CalledProcessError:
        return None


def get_git_revision_hash(short=False):
    """Return git commit hash for repository."""

    # XXX: Unused block?
    cmd = ['git', 'rev-parse', 'HEAD']
    if short:
        cmd.insert(-1, '--short')

    try:
        with open(os.devnull, 'w') as devnull:
            revision_hash = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'],
                stderr=devnull
            ).decode('ascii')
        return revision_hash.strip()

    except subprocess.CalledProcessError:
        return None


def is_ancestor(id1, id2):
    """Return True if git commit id1 is a ancestor of git commit id2."""
    try:
        with open(os.devnull, 'w') as devnull:
            cmd = shlex.split('git rev-list {commit_id}'.format(id2))
            revs = subprocess.check_output(cmd, stderr=devnull)
    except subprocess.CalledProcessError:
        return None
    else:
        return id1 in revs
