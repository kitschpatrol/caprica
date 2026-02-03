"""
AIM Log Parser

Converts AIM chat logs to the Caprica CSV format:
CHATID,DATE,AUTHOR,CHAT

Sessions are demarcated with either:
- Session Start (obrigado:ollHONDAllo): Tue Mar 30 16:22:16 2004
- Start of ollHONDAllo buffer: Sat Sep 29 02:07:00 2001
"""

import re
import sys
import time
from pathlib import Path


def parse_aim_log(input_path, my_username="obrigado"):
    """
    Parse an AIM log file and yield CSV-formatted lines.

    Args:
        input_path: Path to the AIM log file
        my_username: Your username in the logs (others will be anonymized as "other")

    Yields:
        Formatted strings: "chat_id,unix_time,author,text"
    """
    input_path = Path(input_path)

    with open(input_path, encoding="utf-8", errors="replace") as f:
        aim_log = f.readlines()

    chat_id = 0
    unix_time = 0.0

    for line in aim_log:
        line = line.strip()

        # Skip empty lines and meta-cruft
        if len(line) == 0 or re.match(r"^\*", line) or re.match(r"^-", line):
            continue

        # Look for conversation start
        if re.match(r"^Start of", line) or re.match(r"^Session Start", line):
            chat_id += 1
            # Extract the date (comes in as "Sep 29 02:14:02 2001")
            time_string = line[-20:]
            try:
                python_time = time.strptime(time_string, "%b %d %H:%M:%S %Y")
                unix_time = time.mktime(python_time)
            except ValueError:
                # If date parsing fails, keep the previous timestamp
                pass

        # Look for conversation end
        elif re.match(r"^End of", line) or re.match(r"^Session Close", line):
            pass

        # Must be a line of conversation
        else:
            # Split off the author from the text
            expanded_line = line.split(":", 1)

            # Make sure it's a legitimate colon-laden line
            if len(expanded_line) > 1:
                author = expanded_line[0]
                text = expanded_line[1].strip()

                # Anonymize the author if it's not me
                if not re.match(my_username, author, re.IGNORECASE):
                    author = "other"

                yield f"{chat_id},{unix_time},{author.lower()},{text}"


def main():
    """CLI entry point for the AIM parser."""
    import argparse

    parser = argparse.ArgumentParser(description="Convert AIM chat logs to Caprica CSV format")
    parser.add_argument(
        "input",
        help="Path to the AIM log file",
    )
    parser.add_argument(
        "-u",
        "--username",
        default="obrigado",
        help="Your username in the logs (default: obrigado)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file (default: stdout)",
    )
    args = parser.parse_args()

    output = sys.stdout
    if args.output:
        output = open(args.output, "w", encoding="utf-8")

    try:
        for line in parse_aim_log(args.input, args.username):
            print(line, file=output)
    finally:
        if args.output:
            output.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
