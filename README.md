# glrp - git log raw parser

A parser for parsing the output of git log, specifically with the `--format=raw` option.
This is the intended git command to use:

```bash
git log -p --format=raw --show-signature --stat
```

Simply pipe the output:

```bash
git log -p --format=raw --show-signature --stat | glrp --stdin --pretty
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
git log -p --format=raw --show-signature --stat | glrp --stdin
```

Or perhaps a bit more realistic:

```bash
git clone https://github.com/cfengine/core
(cd core && git log -p --format=raw --show-signature --stat HEAD~500..HEAD 2>/dev/null) | glrp --stdin
```

(Clone CFEngine core, start subshell which enters the subdirectory and runs git log for the past 500 commits).

### Specifying input

To avoid ambiguity, you need to specify where input is coming from.
If you are in the correct repo, and want it to run `git log` automatically, simply specify `.` as the path:

```bash
glrp .
```

The `glrp` tool will run the git log command (`git log -p --format=raw --show-signature --stat`) inside that folder.

Specifying the path to another folder is also possible:

```bash
glrp path/to/some/dir/
```

`glrp` can also read from the standard input pipe:

```bash
glrp --stdin
```

(If you run this command alone, nothing will happen - it is waiting for input).

The `--stdin` flag can be used to read output from another program, like `git log`:

```bash
git log -p --format=raw --show-signature --stat | glrp --stdin
```

Or from a file:

```bash
git log -p --format=raw --show-signature --stat > git-log.txt
cat git-log.txt | glrp --stdin
```

### Specifying output

You can use shell redirection to print to file instead of standard output:

```bash
glrp . > output.jsonl
```

There are also other flags which affect the output, such as `--summarize`, `--output-dir`, `--summarize`, etc.

### Summarize

You can create a JSON summary of commits using the `--summarize` flag:

```bash
glrp . --summarize
```

This will give you stats about each author, including number of commits, associated fingerprints, and email addresses, number of signed commits, etc:

```json
{
  "counts": {
    "commits": 46,
    "signed": 46,
    "unsigned": 0,
    "trusted": 0,
    "untrusted": 46
  },
  "emails": {
    "john.doe@example.com": {
      "counts": {
        "commits": 43,
        "signed": 43,
        "unsigned": 0,
        "trusted": 0,
        "untrusted": 43
      },
      "names": ["John Doe"],
      "ids": ["John Doe <john.doe@example.com>"],
      "fingerprints": ["ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCD"]
    },
[...]
```

### Compare

You can also generate 2 summaries for comparison.
This is useful for example for comparing the last 30 days, with all the history before that;

```bash
glrp . --compare 30d
```

Specific dates are also supported:

```bash
glrp . --compare 2025-07-01
```

Even commit ranges:

```bash
glrp . --compare main,feature...main
```

(This assumes that feature is based on main).

In all cases, `--compare` saves 2 files, `.before.json` and `.after.json`.

Example: If you find a new name / email in `.after.json`, which is not in `.before.json`, you know you have a new contributor.

### Combine

You can combine summary files using the `--combine` flag:

```bash
glrp --combine .before.json,.after.json > combined.json
```

This is useful for example after generating summaries for different repos.
You can use it to create a global summary of all commits in all repos of an organization.

### Trusted GPG fingerprints

The summarize functionality can be used to classify different kinds of signed commits.
Use the `--trusted` flag to give a path to a folder containing trusted gpg key fingerprints.

```
glrp --summarize . --trusted ~/.password-store/.pub-keys/
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
