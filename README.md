![Banner](banner.png)

# codeintel-Secrets-Scanner
A command-line tool that scans code repositories for accidentally committed secrets (API keys, passwords, etc.) using regular expressions. There is no entropy analysis and no detect-secrets library in the code. In console output and in the `-o` output file the matched secret span, and any value after an `=` or `:` sign on the same line, is replaced with `***`; the rest of the line, the file, the pattern name, and the line number are still reported. - Focused on Tools for static code analysis, vulnerability scanning, and code quality assurance

## Install
`git clone https://github.com/ShadowStrikeHQ/codeintel-secrets-scanner`

## Usage
`./codeintel-secrets-scanner [params]`

## Parameters
- `-h`: Show help message and exit
- `-p`: No description provided
- `-e`: No description provided
- `-v`: Enable verbose output.
- `-r`: Scan directories recursively
- `-o`: Output file to save results.

## License
Copyright (c) ShadowStrikeHQ
