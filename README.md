![Boardwalk over black water: one pitcher close and large at the walk edge, more pitchers standing in the water, sundew rosettes flat on the margins, canopy light in coins, no lettering anywhere](intro-banner.png)

Herbarium label plate: the title below is set in Besley in loam on cream, ruled like a specimen label, with a tiny pitcher glyph as the section marker throughout, kept at punctuation size.

# codeintel-Secrets-Scanner

![One hooded pitcher plant above dark water, rust tube, gold hood rim, the dark line held inside the mouth, the name lettered below in the herbarium hand](logo.png)

![Boardwalk crossing a bog at canopy light, pitchers on both sides, sundews on the margins, and one weathered sign on the rail carrying the name codeintel-secrets-scanner](banner.png)

![The bog in three depths: canopy light strengthening and weakening in coins, sundew beads taking a cream highlight one by one, a tendril lengthening slowly along the rail, and the dark line inside the pitcher mouth holding steady](scene.svg)

A command-line tool that scans code repositories for accidentally committed secrets (API keys, passwords, etc.) using regular expressions. There is no entropy analysis and no detect-secrets library in the code. In console output and in the `-o` output file the matched secret span, and any value after an `=` or `:` sign on the same line, is replaced with `***`; the rest of the line, the file, the pattern name, and the line number are still reported. - Focused on Tools for static code analysis, vulnerability scanning, and code quality assurance


![Major separator: the full tree ring set on a sawn boardwalk post top](sep-heavy.svg)

## Install
`git clone https://github.com/ShadowStrikeHQ/codeintel-secrets-scanner`

> **Folder inset, flagged in place.** The install line above names ShadowStrikeHQ in place of ShadowGuard-AI. It is preserved exactly as printed and flagged here, never silently fixed.


![Minor separator: a short centred arc of the same post top rings](sep-light.svg)

## Usage
`./codeintel-secrets-scanner [params]`

> **Folder inset: The README Names No Repository Path.** The usage line above is a placeholder. It names no repository path, although the parser requires a positional repository path and ends with exit 1 and a logged error when that path is not a valid directory.


![Major separator: the full tree ring set on a sawn boardwalk post top](sep-heavy.svg)

## Parameters
> **Folder inset: Forty Characters Is a Shape and Not a Verdict.** The AWS_SECRET_ACCESS_KEY pattern is any run of forty characters from its stated alphabet, a shape which will also match hashes and long identifiers that are not secrets at all, so every hit under that name must be judged by hand. Only the first match of each pattern on a line is recorded.

- `-h`: Show help message and exit
- `-p`: No description provided

> **Folder inset: Two Labels Left Blank in the README.** The patterns flag and the exclude flag are left undescribed in the README. From the code: the patterns flag takes names drawn from the four default patterns, or a custom regular expression itself for any other name, compiled once before the scan begins; the exclude flag takes file patterns matched as globs against the full path and against the bare file name. The blanks stand as printed; the code accounts sit beside them, not over them.
- `-e`: No description provided
- `-v`: Enable verbose output.
- `-r`: Scan directories recursively
- `-o`: Output file to save results.


![Minor separator: a short centred arc of the same post top rings](sep-light.svg)

## License
Copyright (c) ShadowStrikeHQ

> **Folder inset, flagged in place.** The closing line above reads Copyright (c) ShadowStrikeHQ, the same wrong house name as the clone line. It is preserved exactly as printed, and no licence name is added, because the README gives none.
