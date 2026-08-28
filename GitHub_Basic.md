# Main branch Workflow

The local working copy of this repository is located at:

```bash
/media/yehlab/C/Xiang/ModelBridge
```

To upload changes to GitHub:

```bash
git status
git add .
git commit -m "Describe what changed"
git push
```

## Meaning

- `git status` — check what changed
- `git add .` — stage all changed and new files
    * Here `.` means everything
    * Nothing is uploaded into GitHub yet, just selecting what you want to upload
- `git commit -m "..."` — save a local snapshot with message `"..."`
- `git push` — upload the commit to GitHub

Remote repository:

```text
YehGroup/ModelBridge
```

> Git does not track empty folders.

Before using `git add .`, check `git status` to avoid accidentally uploading large simulation outputs, logs, `.npy`, `.npz`, `.h5`, or temporary files.


# Contribute safely

## First time only: clone the repository

If you have never downloaded the repository before:

```bash
git clone https://github.com/YehGroup/ModelBridge.git
cd ModelBridge
```

## Start a new pieces of work
First make sure local `main` is up to date:
```bash
git checout main
git pull
```
Before editing any files, create your own branch
```bash
git checkout -b yourbranch
```
Edit ahead. Then:
```bash
git add .
git commit -m "Describe what changed"
git push -u origin yourbranch
```

## Continue on the same branch
```bash
git checkout yourbranch
```
Edit ahead. Then:
```bash
git add .
git commit -m "Describe what changed"
git push
```

## After your branch is merged
Return to `main` and download the merged version:
```bash
git checkout main
git pull
```
Delete your old local branch
```bash
git branch -d yourbranch
```

# Version Control
GitHub essentially keep every single modification that were made using `add-commit-push` sequence. 
## View Previous version
```bash
git log --oneline
```
will return something like
```bash
8b42f12  commit message 1
412e51a  commit message 2
ab23158  commit message 3
```
to inspect one old commit
```bash
git show 412e51a
```

## Tag an important version
When current `main` deserves a named version:
```bash
git checkout main
git pull
git tag -a v0.1.0 -m "Special Message"
git push origin v0.1.0
```
So later you can retrieve exactly that version
```bash
git checkout v0.1.0
```
To see only versions
```bash
git tag
```

## Branch history
On the GitHub website, the merge button has three options
* Create a merge commit — preserves the branch/commit structure.
* Squash and merge — combines all commits from that branch into one commit.
* Rebase and merge — keeps individual commits but rewrites them onto `main` as a straight line.
We should probably always do only `Create a merge commit`. So 
```bash
git log --oneline --graph --all
```
can view both the `main` and other branches' history. 


# Other Files

## `.gitignore`
This is a file that tells Git: "do not track these files." This is so that very large data files will not be uploaded into Github. Only scripts will be included. 
