## CommitPackFT Filtering  Approach

### Research paper findings


-  "We apply quality filters, filter for commercially friendly licenses, and discard
commits that affect more than a single file to ensure commit messages are very specific and to avoid
additional complexity from dealing with multiple files."    This filter allowed authors to scrape 4 terabytes of data from github.

- we apply several strict filters to

### 1) Filters applied to the github archive: resulting in 4 terabytes of data

Description Details
- License:       Only keep samples licensed as MIT, Artistic-2.0, ISC, CC0-1.0, EPL-1.0, MPL2.0, Apache-2.0, BSD-3-Clause, AGPL-3.0, LGPL-2.1, BSD-2-Clause or without license.
- Length:        Only keep code where the commit message has at least 5 and at most 10,000
characters
- Noise:  Remove code where the lowercased commit message is any of ’add files via
upload’, "can’t you see i’m updating the time?", ’commit’, ’create readme.md’,
’dummy’, ’first commit’, ’heartbeat update’, ’initial commit’, ’mirroring from
micro.blog.’, ’no message’, ’pi push’, ’readme’, ’update’, ’updates’, ’update
_config.yaml’, ’update index.html’, ’update readme.md’, ’update readme’, ’updated readme’, ’update log’, ’update data.js’, ’update data.json’, ’update data.js’,
’pi push’ or starts with ’merge’
- Single file:   Remove samples that contain changes across multiple files
Opt-out Remove samples from repositories owned by users that opted out of The
Stack (Kocetkov et al., 2022)

Table 5: COMMITPACK filters.   References: 



### 2) Filters applied to commitpack to  obtain commitpackft

-   Length      :  Remove samples where the before code has more than 50,000 characters
-   Length      :  Remove samples where the after code has 0 characters
-   Difference  :  Remove samples where the before and after code are the same (e.g.
-   Difference  :  Remove samples where the before and after code are the same (e.g. file name
changes)
-   Difference  :  Remove samples that contain a hashtag (to avoid references to issues)
-   Extension   :  Remove samples where the filename of the code after has an atypical extension
for the programming language (e.g. only keep ’.py’ for Python)
Filename    : Remove samples where the filename is contained in the commit message (as we
do not use the filename in finetuning)
-   Length      : Only keep samples where the commit message has more than 10 and less than
1000 characters
-   Words       : Only keep samples where the commit message can be split into more than 4 and
less than 1000 space-separated words
-   Clean       : Remove any appearances of ’[skip ci]’, ’[ci skip]’, sequences at the beginning
or end that are in brackets, sequences at the beginning that end with ’:’ and strip
whitespace at the beginning or end
-   Capitalized : Only keep samples where the message starts with an uppercase letter
-   Tokens Only keep samples where the concatenation of the code before, a special token
and the code after has at least 50 tokens and at most 768 tokens according to
the StarCoder tokenizer
-   Instructions : Only keep samples where the lowercased commit message starts with any of
the words in Table 7
-   Noise        : Remove samples where the lowercased commit message contains any of ’auto
commit’, ’update contributing’, ’<?xml’, ’merge branch’, ’merge pull request’,
’signed-off-by’, "fix that bug where things didn’t work but now they should",
"put the thingie in the thingie", "add a beter commit message", "code review",
"//codereview", "work in progress", "wip", "https://", "http://", "| leetcode",
"cdpcp", " i ", "i’ve" , "i’m" or both "thanks to" and "for"
-   Regex        : Remove samples where the lowercased commit message has a match for
any of the regular expressions (?:v)?\d+\.\d+\.\d+(?=$|\S),
^[a-f0-9]+(?:-[a-f0-9]+)*$, ([a-f0-9]{40}),
issue\s*\d+, bug\s*\d+ or feature\s*\d+
- Downsample With 90% probability remove samples where the commit message starts with
"Bump", "Set version" or "Update version"

Table 6: COMMITPACKFT filters applied to COMMITPACK. With the commit message we refer
to the commit message subject only, not the body.
