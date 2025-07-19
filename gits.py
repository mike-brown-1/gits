import sys
import os
import pygit2
## from pygit2 import Repository, GitError, discover_repository, GIT_STATUS_WT_NEW, GIT_STATUS_INDEX_NEW

def get_readable_status(statusFlags):
    status_map = {
        pygit2.GIT_STATUS_CURRENT: "Unchanged",
        pygit2.GIT_STATUS_INDEX_NEW: "Staged (new file)",
        pygit2.GIT_STATUS_INDEX_MODIFIED: "Staged (modified)",
        pygit2.GIT_STATUS_INDEX_DELETED: "Staged (deleted)",
        pygit2.GIT_STATUS_WT_MODIFIED: "Modified (unstaged)",
        pygit2.GIT_STATUS_WT_DELETED: "Deleted (unstaged)",
        pygit2.GIT_STATUS_WT_NEW: "Untracked",
        pygit2.GIT_STATUS_IGNORED: "Ignored",
        pygit2.GIT_STATUS_CONFLICTED: "Conflicted"
    }

    statuses = []
    # Each status is a bitmask — multiple flags can be set
    for bitmask, label in status_map.items():
        if statusFlags & bitmask:
              statuses.append(label)

    readable = ", ".join(statuses) if statuses else "Unknown"

    return readable

def processDir(rootDir):
   for dirpath, dirnames, filenames in os.walk(rootDir):
      repo_path = pygit2.discover_repository(dirpath)
      if repo_path is not None:

         repo = pygit2.Repository(repo_path)
         dirty_items = repo.status().items()
         is_clean = True if not dirty_items else False
         print(f"Repository: {dirpath} is clean: {is_clean}")
         for entry, status in repo.status().items():
            print(f"\tFile: {entry}, status: {get_readable_status(status)}")

         # Prevent re-walking into subdirectories of a found repo
         # This is important because discover_repository might find the same repo
         # if we continued walking into its subdirectories.
         del dirnames[:] 

if len(sys.argv) <= 1:
   print("You must provide a directory to search")
else:
   processDir(sys.argv[1])
