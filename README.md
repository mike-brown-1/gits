# gits

gits is a utility to check the status of all [Git](https://en.wikipedia.org/wiki/Git) repositories found within a directory tree.

The goal is to provide a utility that anyone can use to check the current status of all Git repositories.  For example, you may want to summary of which local repositories have untracked files.

# For Developers

gits is written in [Python](https://en.wikipedia.org/wiki/Python_(programming_language)).  The initial version was created with version 3.12.3.

Libraries required for this application can be installed with by running `pip install -r requirements.txt`.  If new libraries are added, update requirements.txt by running: `pip freeze > requirements.txt`.

The primary library used is [pygit2](https://github.com/libgit2/pygit2), which has good [documentation](https://www.pygit2.org/).  This library does not use the `git` command, which means it is a faster option.  If you are using this on Windows or macOS, you will need to install libgit2 yourself.

