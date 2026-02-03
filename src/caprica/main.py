"""
Back to the Future IM Module
Eric Mika + Michael Edgcumbe
Learning Bit by Bit at NYU ITP, Spring 2010

A chatbot that uses historical chat logs to generate responses using
sentence similarity through synonym expansion.
"""

from pathlib import Path

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import wordnet

bigram_measures = nltk.collocations.BigramAssocMeasures()


class Line:
    """Holds chat data with synonym lookup capabilities."""

    def __init__(self, id_, author, words, index):
        self.id = id_
        self.author = author
        self.words = words
        self.lookup = []
        self.index = index
        self.ngrams = []
        self.synonymscore = 0.0
        self.ngramscore = 0
        self.used = 0


def lower_strings(word_list):
    """Convert all strings in a list to lowercase."""
    return [x.lower() for x in word_list]


def expand_words(words):
    """
    Expand words into lists of synonyms using WordNet.

    For example, "how about the weather" expands each word into a list
    of synonymous terms to increase matching opportunities.
    """
    tokens = words.split(" ")
    lookup = []

    for word in tokens:
        sense_list = wordnet.synsets(word)

        if sense_list:
            templist = []
            for sense in sense_list:
                templist.extend(lower_strings(sense.lemma_names()))
            lookup.append(templist)
        else:
            lookup.append([word])

    # Remove duplicates while preserving structure
    unique_lookup = []
    seen = set()
    for synonyms in lookup:
        unique_synonyms = []
        for syn in synonyms:
            if syn not in seen:
                unique_synonyms.append(syn)
                seen.add(syn)
        if unique_synonyms:
            unique_lookup.append(unique_synonyms)

    return unique_lookup


def parse_log(raw_log):
    """Parse raw log lines into Line objects."""
    parsed = []
    for index, row in enumerate(raw_log):
        row = row.strip()
        parts = row.split(",", 3)

        if len(parts) >= 4:
            conversation_id = parts[0]
            # time = parts[1]  # Available but not currently used
            author = parts[2]
            words = parts[3]
            parsed.append(Line(conversation_id, author, words, index))

    return parsed


def search(query, bank):
    """
    Search the chat bank for lines matching the query's synonyms.

    Returns unique hits sorted by synonym match score, normalized by line length.
    """
    hits = []
    unique_hits = []

    # Find matches between synonyms
    for message in bank:
        for synlists in query.lookup:
            for synonym in synlists:
                if synonym in message.words:
                    message.synonymscore += 1.0
                    hits.append(message)

    # Find unique hits
    for i in range(1, len(hits)):
        if hits[i - 1].index != hits[i].index:
            unique_hits.append(hits[i])

    # Normalize scores by line length
    for hit in unique_hits:
        word_count = len(hit.words.split(" "))
        if word_count > 0:
            hit.synonymscore = hit.synonymscore / float(word_count)

    return unique_hits


def rank_ngrams(query, possibilities):
    """
    Rank possibilities by bigram matches with the query.

    Note: This is computationally expensive and currently disabled in main loop.
    """
    query_tokens = nltk.wordpunct_tokenize(query.words)
    query.ngrams = BigramCollocationFinder.from_words(query_tokens)
    query_score = query.ngrams.score_ngrams(bigram_measures.jaccard)
    query_sort = sorted(bigram for bigram, score in query_score)

    for message in possibilities:
        tokens = nltk.wordpunct_tokenize(message.words)
        message.ngrams = BigramCollocationFinder.from_words(tokens)

    import string

    for message in possibilities:
        ngram_score = message.ngrams.score_ngrams(bigram_measures.jaccard)
        ngram_sort = sorted(bigram for bigram, score in ngram_score)
        for ngram in query_sort:
            for thing in ngram_sort:
                thing_0 = thing[0].lower()
                thing_1 = thing[1].lower()
                ngram_0 = ngram[0].lower()
                ngram_1 = ngram[1].lower()

                if thing_0 == ngram_0 and thing_1 == ngram_1 and thing_0 not in string.punctuation:
                    message.ngramscore += 1

    return possibilities


def get_response(question, response_log):
    """
    Get a response from the log that best matches the question.

    Uses synonym expansion to find the best matching line, then walks
    forward to find an unused response from the log owner.
    """
    # Build the query line
    query = Line(0, "query", question, 0)
    query.lookup = expand_words(query.words)

    # Find possible responses
    possible_responses = search(query, response_log)

    if not possible_responses:
        return None

    # Find highest scoring response
    high_score = max(line.synonymscore for line in possible_responses)

    # Choose a high scoring response
    match_index = 0
    for line in possible_responses:
        if line.synonymscore == high_score:
            match_index = line.index

    # Walk forward to find first unused response from log owner
    for line in response_log[match_index:]:
        if line.author.lower() != "other" and line.used != 1:
            response_log[line.index].used = 1
            return line

    return None


def load_logs(data_dir=None):
    """Load chat logs from the data directory."""
    if data_dir is None:
        # Default to data directory relative to project root
        data_dir = Path(__file__).parent.parent.parent / "data"
    else:
        data_dir = Path(data_dir)

    edgwired_path = data_dir / "edgwired.txt"
    obrigado_path = data_dir / "obrigado.txt"

    edgwired_log = []
    obrigado_log = []

    if edgwired_path.exists():
        with open(edgwired_path, encoding="utf-8", errors="replace") as f:
            edgwired_log = parse_log(f.readlines())

    if obrigado_path.exists():
        with open(obrigado_path, encoding="utf-8", errors="replace") as f:
            obrigado_log = parse_log(f.readlines())

    return edgwired_log, obrigado_log


def run_automatic(edgwired_log, obrigado_log, initial_query="pics"):
    """Run automatic conversation mode between two logs."""
    asker = "eric"
    query = initial_query

    def choose_log(asker_name):
        return edgwired_log if asker_name == "eric" else obrigado_log

    while True:
        response = get_response(query, choose_log(asker))

        if response is None:
            print("No more responses available.")
            break

        print(f"{response.author}: {response.words}")

        # Flip the asker
        asker = "michael" if asker == "eric" else "eric"

        # Use the response as the next query
        query = response.words


def run_interactive(edgwired_log, obrigado_log, persona="obrigado"):
    """Run interactive mode where user can query the logs.

    Args:
        edgwired_log: Parsed log for edgwired persona
        obrigado_log: Parsed log for obrigado persona
        persona: Which persona to talk with ("obrigado" or "edgwired")
    """
    if persona == "edgwired":
        response_log = edgwired_log
    else:
        response_log = obrigado_log

    print(f"Caprica Interactive Mode - talking with {persona}")
    print("Type 'quit' to exit\n")

    while True:
        try:
            you_say = input("You say: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if you_say.lower() == "quit":
            break

        response = get_response(you_say, response_log)
        if response:
            print(f"{response.author}: {response.words}")
        else:
            print("No response found.")


def main():
    """Main entry point for the caprica CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="Caprica: A digital doppelgänger chatbot")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run in automatic conversation mode",
    )
    parser.add_argument(
        "--query",
        default="pics",
        help="Initial query for automatic mode (default: pics)",
    )
    parser.add_argument(
        "--data-dir",
        help="Path to data directory containing chat logs",
    )
    parser.add_argument(
        "--persona",
        choices=["obrigado", "edgwired"],
        default="obrigado",
        help="Which persona to talk with in interactive mode (default: obrigado)",
    )
    args = parser.parse_args()

    # Ensure NLTK data is available
    try:
        wordnet.synsets("test")
    except LookupError:
        print("Downloading required NLTK data...")
        nltk.download("wordnet")
        nltk.download("punkt")

    edgwired_log, obrigado_log = load_logs(args.data_dir)

    if not edgwired_log and not obrigado_log:
        print("Error: No chat logs found in data directory.")
        print("Please ensure edgwired.txt or obrigado.txt exists.")
        return 1

    if args.auto:
        run_automatic(edgwired_log, obrigado_log, args.query)
    else:
        run_interactive(edgwired_log, obrigado_log, args.persona)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
