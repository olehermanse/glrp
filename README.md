# glrp - git log raw parser

A parser for parsing the output of git log, specifically with the `--format=raw` option.
This is the intended git command to use:

```bash
git log -p --format=raw --show-signature --stat
```

Simply pipe the output:

```bash
git log -p --format=raw --show-signature --stat | glrp --pretty
```

The CLI outputs one JSON object per commit.
Each JSON object is on one line, they are separated by newlines.
This format is sometimes referred to as JSONL or JSON lines format.
With `--pretty`, each JSON object is indented to be more readable and printed across multiple lines.
(But then it is no longer JSONL, strictly speaking).

## Why?

The above command provides a lot of useful information about each git commit, which we can analyze, including:

- Commit message
- Diff
- Author name and email
- Committer name and email
- Timestamps
- GPG signature

On its own, `git log` does not output its information in a format which is easy for other programs to use.
So, this tool parses the output and turns it into JSON which is more easy to analyze and check.

## Installation

```bash
pipx install glrp
```

## Usage

Using it is simple.
Run it inside a git repo:

```bash
glrp .
```

Or you can pipe `git log` output to it:

```bash
git log -p --format=raw --show-signature --stat | glrp --output-dir=./out/
```

Or perhaps a bit more realistic:

```bash
git clone https://github.com/cfengine/core
(cd core && git log -p --format=raw --show-signature --stat HEAD~500..HEAD 2>/dev/null) | glrp
```

(Clone CFEngine core, start subshell which enters the subdirectory and runs git log for the past 500 commits).

### Specifying input

By default, `glrp` parses standard input, and outputs to stdout.
To take input from somewhere else, supply a filename:

```bash
glrp some_file.jsonl
```

The file, `some_file.jsonl` is opened and read, its content is used instead of standard input.
You can also specify the path to a folder:

```bash
glrp some_dir/
```

The `glrp` tool will run the git log command (`git log -p --format=raw --show-signature --stat`) inside that folder.
Output from the `git` command will be parsed instead of standard input.

### Specifying output

You can use shell redirection to print to file instead of standard output:

```bash
glrp . > output.txt
```

## Important notes

**Note:** This tool is meant specifically as a parser for the command shown above, not as a generic parser for all the different things `git log` can output.

**Warning:** The output of `--show-signature` varies depending on which keys you have imported / trusted in your installation of GPG.
Make sure you import the correct GPG keys beforehand, and don't expect output to be identical across different machines with different GPG states.

**Warning:** Consider this a best-effort, "lossy" parsing.
Commits may contain non utf-8 characters, to avoid "crashing", we skip these, replacing them with question marks.
Thus, the parsing is lossy, don't expect all the information to be there.
This tool can be used for searching / analyzing commits, but don't use it as some kind of backup tool where you expect to have the ability to "reconstruct" the commits and repo entirely.

## Details

For details on how the parsing works, try running with `--debug` and look at the resulting `./debug/` folder.
Also, see the comments in the source code; [./glrp/internal_parser.py](./glrp/internal_parser.py)
