# Caprica

A digital doppelganger chatbot that draws from historical instant messenger logs to construct conversations between past versions of ourselves.

Created by Eric Mika and Michael Edgcumbe at NYU ITP, Spring 2010.

## How it works

The chat log acts as a question/answer training set. Given a query, the system finds the closest matching line in the log using synonym expansion (via WordNet), then walks forward to retrieve a response. Scores are normalized by line length to prevent longer messages from dominating.

## Installation

```bash
uv sync
```

This will also install NLTK. On first run, required NLTK data (wordnet, punkt) will be downloaded automatically.

## Usage

```bash
# Interactive mode - chat with a persona
uv run caprica --persona obrigado
uv run caprica --persona edgwired

# Automatic mode - watch two personas converse
uv run caprica --auto
```

## Data format

Chat logs use CSV format: `CHATID,TIMESTAMP,AUTHOR,TEXT`

Place your cleaned logs in the `data/` directory:

- `edgwired.txt` for the edgwired persona
- `obrigado.txt` for the obrigado persona

## Utilities

```bash
# Parse AIM logs to Caprica format
uv run caprica-parse-aim input.txt -o output.txt

# Chunk consecutive messages from same author
uv run caprica-chunk input.txt -o output.txt

# Analyze bigram frequencies
uv run caprica-freq input.txt -o output.txt
```
