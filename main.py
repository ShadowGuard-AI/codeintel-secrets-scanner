import argparse
import logging
import os
import fnmatch
import re
import sys
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default regular expressions for common secrets
DEFAULT_PATTERNS = {
    "API_KEY": r"[A-Za-z0-9]{32,45}",  # Example API key pattern
    "PASSWORD": r"password|pwd|secret",  # Example password pattern
    "AWS_ACCESS_KEY_ID": r"AKIA[0-9A-Z]{16}",
    "AWS_SECRET_ACCESS_KEY": r"[a-zA-Z0-9/+]{40}"
}


def setup_argparse():
    """
    Sets up the argparse for the command-line interface.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(description="Scans code repositories for accidentally committed secrets.")
    parser.add_argument("repository_path", help="Path to the code repository to scan.")
    parser.add_argument("-p", "--patterns", nargs='+', default=list(DEFAULT_PATTERNS.keys()),
                        help="List of patterns to search for. Use keys from DEFAULT_PATTERNS or provide custom patterns.")
    parser.add_argument("-e", "--exclude", nargs='+', default=[],
                        help="List of file patterns to exclude from scanning (e.g., *.txt, *.log).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Scan directories recursively")
    parser.add_argument("-o", "--output", help="Output file to save results.")

    return parser


def is_file_excluded(file_path: str, exclude_patterns: List[str]) -> bool:
    """
    Checks if a file should be excluded based on the provided patterns.

    Args:
        file_path (str): The path to the file.
        exclude_patterns (List[str]): A list of patterns to exclude.

    Returns:
        bool: True if the file should be excluded, False otherwise.
    """
    for pattern in exclude_patterns:
        # The help text promises glob patterns such as *.txt. Feeding
        # those to re.search raised "nothing to repeat" and killed the
        # scan, so exclusions are matched as globs, against the full
        # path and against the bare file name.
        if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
            return True
    return False


def mask_line(line: str, match) -> str:
    """Return the line with secret material replaced by a fixed mask.

    The matched span is masked first. Some patterns match only a
    keyword (the PASSWORD pattern matches the word password), so a
    value sitting after an = or : sign on the same line is masked as
    well; printing the whole line used to put that value in the
    console output and in the -o file in clear.
    """
    masked = line[:match.start()] + "***" + line[match.end():]
    masked = re.sub(r"([=:]\s*[\"']?)[^\s\"',;]+", r"\1***", masked)
    return masked


def scan_file(file_path: str, patterns: dict) -> List[Tuple[str, str, int]]:
    """
    Scans a single file for secrets based on the provided patterns.

    Args:
        file_path (str): The path to the file to scan.
        patterns (dict): A dictionary of patterns to search for.  Key is pattern name, Value is regex.

    Returns:
        List[Tuple[str, str, int]]: A list of tuples containing the pattern name, matched line, and line number.
    """
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                for pattern_name, pattern_regex in patterns.items():
                    match = re.search(pattern_regex, line)
                    if match:
                        results.append((pattern_name, mask_line(line, match).strip(), i + 1))  # Line number starts from 1
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
    return results


def scan_repository(repository_path: str, patterns: dict, exclude_patterns: List[str], recursive: bool = False) -> List[Tuple[str, str, str, int]]:
    """
    Scans a repository for secrets.

    Args:
        repository_path (str): The path to the repository.
        patterns (dict): A dictionary of patterns to search for.
        exclude_patterns (List[str]): A list of patterns to exclude.
        recursive (bool): Whether to scan directories recursively. Defaults to False.

    Returns:
        List[Tuple[str, str, str, int]]: A list of tuples containing the file path, pattern name, matched line, and line number.
    """
    results = []
    if recursive:
        for root, _, files in os.walk(repository_path):
            for file in files:
                file_path = os.path.join(root, file)
                if not is_file_excluded(file_path, exclude_patterns):
                    file_results = scan_file(file_path, patterns)
                    for pattern_name, line, line_number in file_results:
                        results.append((file_path, pattern_name, line, line_number))
    else:
        for file in os.listdir(repository_path):
             file_path = os.path.join(repository_path, file)
             if os.path.isfile(file_path) and not is_file_excluded(file_path, exclude_patterns):
                 file_results = scan_file(file_path, patterns)
                 for pattern_name, line, line_number in file_results:
                     results.append((file_path, pattern_name, line, line_number))

    return results


def main():
    """
    Main function to execute the secret scanner.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if not os.path.isdir(args.repository_path):
        logging.error(f"Repository path '{args.repository_path}' is not a valid directory.")
        sys.exit(1)

    # Create a dictionary of patterns to use
    patterns_to_use = {}
    for pattern_name in args.patterns:
        if pattern_name in DEFAULT_PATTERNS:
            patterns_to_use[pattern_name] = DEFAULT_PATTERNS[pattern_name]
        else:
            # Unknown names are custom regexes, as the help text says.
            # Compile once here: an invalid pattern used to surface
            # once per file as a misleading "Error reading file" and
            # the scan still exited 0 with no results at all.
            try:
                re.compile(pattern_name)
            except re.error as e:
                logging.error(f"Pattern '{pattern_name}' is not a valid regex: {e}")
                sys.exit(1)
            logging.warning(f"Pattern '{pattern_name}' not found in default patterns.  Using as a custom regex.")
            patterns_to_use[pattern_name] = pattern_name

    if args.verbose:
        logging.info(f"Scanning repository: {args.repository_path}")
        logging.info(f"Using patterns: {patterns_to_use.keys()}")
        logging.info(f"Excluding patterns: {args.exclude}")

    results = scan_repository(args.repository_path, patterns_to_use, args.exclude, args.recursive)

    if args.output:
        try:
            with open(args.output, "w") as f:
                for file_path, pattern_name, line, line_number in results:
                    f.write(f"File: {file_path}, Pattern: {pattern_name}, Line: {line}, Line Number: {line_number}\n")
            logging.info(f"Results saved to {args.output}")
        except Exception as e:
            logging.error(f"Error writing to output file {args.output}: {e}")
            sys.exit(1)
    else:
        for file_path, pattern_name, line, line_number in results:
            print(f"File: {file_path}, Pattern: {pattern_name}, Line: {line}, Line Number: {line_number}")

    if not results and args.verbose:
        logging.info("No secrets found.")


if __name__ == "__main__":
    main()