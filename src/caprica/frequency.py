"""
Frequency Analysis

Analyzes chat logs to find bigram frequencies and collocations,
useful for understanding common word pairings in the logs.
"""

import sys
from pathlib import Path

import nltk
from nltk import FreqDist
from nltk.collocations import BigramCollocationFinder


class Line:
    """Holds chat data."""

    def __init__(self, id_, author, words, index):
        self.id = id_
        self.author = author
        self.words = words
        self.index = index


def parse_log(raw_log):
    """Parse raw log lines into Line objects."""
    parsed = []
    for index, row in enumerate(raw_log):
        row = row.strip()
        parts = row.split(",", 3)

        if len(parts) >= 4:
            conversation_id = parts[0]
            author = parts[2]
            words = parts[3]
            parsed.append(Line(conversation_id, author, words, index))

    return parsed


def analyze_frequency(input_path, min_freq=2, output_format="bigrams"):
    """
    Analyze word and bigram frequencies in a chat log.

    Args:
        input_path: Path to the cleaned log file
        min_freq: Minimum frequency to include in results
        output_format: "bigrams" for bigram analysis, "words" for word frequency

    Yields:
        Tuples of (item, count) or formatted strings depending on format
    """
    input_path = Path(input_path)

    with open(input_path, encoding="utf-8", errors="replace") as f:
        log = parse_log(f.readlines())

    # Combine all text
    all_text = " ".join(line.words for line in log)
    tokens = nltk.word_tokenize(all_text)

    if output_format == "words":
        fdist = FreqDist(tokens)
        for word, count in fdist.most_common():
            if count >= min_freq:
                yield f"{word},{count}"
    else:
        # Bigram analysis
        finder = BigramCollocationFinder.from_words(tokens)

        # Filter out punctuation and numbers
        punctuation = set("!\"'#$%&()*+,-./:;<=>?@[]^_`{|}~")
        digits = set("0123456789")
        finder.apply_word_filter(lambda w: w in punctuation or w in digits)
        finder.apply_freq_filter(min_freq)

        for ngram, count in finder.ngram_fd.items():
            if count >= min_freq:
                the_gram = f"{ngram[0]} {ngram[1]}".replace(",", "")
                yield f"{the_gram},{count}"


def main():
    """CLI entry point for frequency analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze word and bigram frequencies in chat logs")
    parser.add_argument(
        "input",
        help="Path to the cleaned log file",
    )
    parser.add_argument(
        "-m",
        "--min-freq",
        type=int,
        default=2,
        help="Minimum frequency to include (default: 2)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["bigrams", "words"],
        default="bigrams",
        help="Output format (default: bigrams)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file (default: stdout)",
    )
    args = parser.parse_args()

    # Ensure NLTK data is available
    try:
        nltk.word_tokenize("test")
    except LookupError:
        print("Downloading required NLTK data...", file=sys.stderr)
        nltk.download("punkt")

    output = sys.stdout
    if args.output:
        output = open(args.output, "w", encoding="utf-8")

    try:
        for line in analyze_frequency(args.input, args.min_freq, args.format):
            print(line, file=output)
    finally:
        if args.output:
            output.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
