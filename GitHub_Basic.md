# GitHub Workflow

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

For only one file:

```bash
git add path/to/file
git commit -m "Update file"
git push
```

> Git does not track empty folders.

Before using `git add .`, check `git status` to avoid accidentally uploading large simulation outputs, logs, `.npy`, `.npz`, `.h5`, or temporary files.
