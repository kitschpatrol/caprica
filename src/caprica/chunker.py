"""
Log Chunker

Combines consecutive lines from the same author within the same conversation
into single chunks, making responses more natural.
"""

import sys
from pathlib import Path


def chunk_log(input_path):
    """
    Chunk together lines of conversation from the same author.

    Consecutive messages from the same person in the same conversation
    are combined with "..." separators.

    Args:
        input_path: Path to the cleaned log file

    Yields:
        Chunked lines in the format: "id,time,author,combined_words"
    """
    input_path = Path(input_path)

    with open(input_path, encoding="utf-8", errors="replace") as f:
        log = f.readlines()

    last_author = ""
    last_id = None
    current_line = None

    for row in log:
        row = row.strip()
        parts = row.split(",", 3)

        if len(parts) < 4:
            continue

        id_ = parts[0]
        time_ = parts[1]
        author = parts[2]
        words = parts[3]

        if author == last_author and id_ == last_id and current_line is not None:
            # Same author and conversation, append to current chunk
            current_line["words"] += f" ... {words}"
        else:
            # New author or conversation, yield previous and start new
            if current_line is not None:
                yield f"{current_line['id']},{current_line['time']},{current_line['author']},{current_line['words']}"

            current_line = {
                "id": id_,
                "time": time_,
                "author": author,
                "words": words,
            }

        last_author = author
        last_id = id_

    # Yield the last line
    if current_line is not None:
        yield f"{current_line['id']},{current_line['time']},{current_line['author']},{current_line['words']}"


def main():
    """CLI entry point for the log chunker."""
    import argparse

    parser = argparse.ArgumentParser(description="Chunk consecutive messages from the same author")
    parser.add_argument(
        "input",
        help="Path to the cleaned log file",
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
        for line in chunk_log(args.input):
            print(line, file=output)
    finally:
        if args.output:
            output.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
