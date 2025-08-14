#!/bin/bash
# Simple notes helper

# Always use ~/notes as the notes folder
NOTES_DIR="$HOME/notes"
mkdir -p "$NOTES_DIR"

case "$1" in
  # List all notes
  list|"")
    echo "Your notes in $NOTES_DIR:"
    ls -1 "$NOTES_DIR"
    ;;

  # Create a new note (opens Nano). Optional title after 'new'
  new)
    shift
    if [ -z "$1" ]; then
      read -rp "Title (optional): " TITLE
    else
      TITLE="$*"
    fi
    # Sanitize title: spaces -> underscores; keep letters/numbers/_/.- only
    SAFE_TITLE=$(echo "$TITLE" | tr ' ' '_' | tr -cd '[:alnum:]_.-')
    FNAME="$(date +%Y-%m-%d_%H%M)-${SAFE_TITLE:-note}.txt"
    nano "$NOTES_DIR/$FNAME"
    echo "Saved $FNAME"
    ;;

  # Edit a note in Nano
  view)
    if [ -z "$2" ]; then
      echo "Usage: ./notes.sh view <filename>"; exit 1
    fi
    FILE="$NOTES_DIR/$2"
    if [ -f "$FILE" ]; then
      nano "$FILE"
    else
      echo "File not found. Try: ./notes.sh list"
    fi
    ;;

  # Show a note (read-only)
  show)
    if [ -z "$2" ]; then
      echo "Usage: ./notes.sh show <filename>"; exit 1
    fi
    FILE="$NOTES_DIR/$2"
    if [ -f "$FILE" ]; then
      cat "$FILE"
    else
      echo "File not found. Try: ./notes.sh list"
    fi
    ;;

  # Search across all notes (case-insensitive)
  search)
    shift
    if [ -z "$1" ]; then
      echo "Usage: ./notes.sh search <term>"
      exit 1
    fi
    TERM="$*"
    grep -n -i -- "$TERM" "$NOTES_DIR"/*.txt 2>/dev/null || echo "No matches."
    ;;

  # Help
  *)
    echo "Usage:"
    echo "  ./notes.sh list"
    echo "  ./notes.sh new [title]"
    echo "  ./notes.sh view <filename>"
    echo "  ./notes.sh show <filename>"
    echo "  ./notes.sh search <term>"
    ;;
esac
