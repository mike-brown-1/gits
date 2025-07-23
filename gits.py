import sys
import os
import pygit2
from dataclasses import dataclass
import typer
from typing_extensions import Annotated

VERSION = '0.2.0'

@dataclass
class RepoClass:
    root_dir: str
    is_dirty: bool
    untracked: int
    staged_new: int
    staged_deleted: int
    modified: int
    deleted: int
    conflicted: int
    unchanged: int


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

def processDir(rootDir: str) -> list[RepoClass]:
   """Attempt to search rootDir directory hierarchy for Git repositories
returning any found as a list of RepoClass object."""

   repos = []
   for dirpath, dirnames, filenames in os.walk(rootDir):
      repo_path = pygit2.discover_repository(dirpath)
      if repo_path is not None:

         repo = pygit2.Repository(repo_path)
         dirty_items = repo.status().items()
         is_dirty = True if dirty_items else False
         r = RepoClass(dirpath, is_dirty, 0, 0, 0, 0, 0, 0, 0)
        #  print(f"Repository: {dirpath} is dirty: {is_dirty}")
         for entry, status in repo.status().items():
            # TODO Add more flags
            if status & pygit2.GIT_STATUS_WT_MODIFIED:
                r.modified += 1
            if status & pygit2.GIT_STATUS_WT_NEW:
                r.untracked += 1

         repos.append(r)

         # Prevent re-walking into subdirectories of a found repo
         # This is important because discover_repository might find the same repo
         # if we continued walking into its subdirectories.
         del dirnames[:] 
   return repos

def main(root_dir: Annotated[str, typer.Argument(help="Directory path to search")],
         show_dirty: Annotated[bool, typer.Option("--dirty", "-d", help="Show only dirty repositories")] = False
         ):
    
    print(f"gits v {VERSION}: Searching: {root_dir}, dirty: {show_dirty}\n")

    repos = processDir(root_dir)
    # print(f'Found {len(repos)} repositories.')
    for r in repos:
        if (show_dirty and r.is_dirty) or not show_dirty:
            repo_name = r.root_dir[len(root_dir) + 1:] if r.root_dir.startswith(root_dir) else r.root_dir
            print(f"Dir: {repo_name}, is dirty: {r.is_dirty}, untracked: {r.untracked}, modified: {r.modified}")


if __name__ == "__main__":
    typer.run(main)
