#!/usr/bin/env python3
"""Extract and merge RevealJS speaker notes to/from separate files.

Usage:
  python notes-tool.py extract day1/part1.html
    → creates day1/part1-notes.html  (all notes, labeled by slide)
    → creates day1/part1-slim.html   (presentation without notes)

  python notes-tool.py merge day1/part1-slim.html
    → reads day1/part1-notes.html
    → writes day1/part1.html          (merged output)

  python notes-tool.py merge day1/part1-slim.html day1/part1-notes.html day1/output.html
    → explicit paths for notes input and merged output
"""

import re
import sys
import os


def extract_notes(html_path):
    """Extract notes from HTML into a notes file, create slim HTML."""
    dir_path = os.path.dirname(html_path)
    base = os.path.splitext(os.path.basename(html_path))[0]
    notes_path = os.path.join(dir_path, f"{base}-notes.html")
    slim_path = os.path.join(dir_path, f"{base}-slim.html")

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all aside notes
    pattern = r'<aside class="notes"[^>]*>(.*?)</aside>'
    matches = list(re.finditer(pattern, html, re.DOTALL))

    if not matches:
        print("No notes found!")
        return

    print(f"Found {len(matches)} note sections")

    # For each note, find the nearest preceding h2 for labeling
    notes_parts = []
    for i, match in enumerate(matches):
        preceding = html[:match.start()]
        heading_matches = list(re.finditer(r'<h[12][^>]*>(.*?)</h[12]>', preceding, re.DOTALL))
        title = "Unknown"
        if heading_matches:
            title = re.sub(r'<[^>]+>', '', heading_matches[-1].group(1)).strip()

        slide_id = f"slide-{i+1:02d}"
        content = match.group(1)

        notes_parts.append(f'<!-- {slide_id}: {title} -->{content}\n')

    # Write notes file
    with open(notes_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(notes_parts))

    # Create slim HTML: replace each aside with a marker
    counter = [0]
    def replace_with_marker(match):
        counter[0] += 1
        return f'<aside class="notes"><!-- slide-{counter[0]:02d} --></aside>'

    slim = re.sub(pattern, replace_with_marker, html, flags=re.DOTALL)

    with open(slim_path, 'w', encoding='utf-8') as f:
        f.write(slim)

    # Stats
    orig_lines = html.count('\n')
    slim_lines = slim.count('\n')
    notes_lines = sum(p.count('\n') for p in notes_parts)
    print(f"Original:  {orig_lines} lines")
    print(f"Slim HTML: {slim_lines} lines ({100*slim_lines//orig_lines}% of original)")
    print(f"Notes:     {notes_lines} lines")
    print(f"\nFiles created:")
    print(f"  {notes_path}")
    print(f"  {slim_path}")


def merge_notes(slim_path, notes_path=None, output_path=None):
    """Merge notes back into slim HTML."""
    dir_path = os.path.dirname(slim_path)
    base = os.path.splitext(os.path.basename(slim_path))[0]

    if base.endswith('-slim'):
        orig_base = base[:-5]
    else:
        orig_base = base

    if notes_path is None:
        notes_path = os.path.join(dir_path, f"{orig_base}-notes.html")
    if output_path is None:
        output_path = os.path.join(dir_path, f"{orig_base}.html")

    with open(slim_path, 'r', encoding='utf-8') as f:
        slim_html = f.read()
    with open(notes_path, 'r', encoding='utf-8') as f:
        notes_content = f.read()

    # Parse notes file: split by <!-- slide-NN: ... --> markers
    note_pattern = r'<!-- (slide-\d+):.*?-->(.*?)(?=\n<!-- slide-\d+:|$)'
    note_matches = re.findall(note_pattern, notes_content, re.DOTALL)
    notes_dict = {k: v.rstrip('\n') for k, v in note_matches}

    print(f"Loaded {len(notes_dict)} note sections from {notes_path}")

    # Replace markers in slim HTML with actual notes
    missing = []
    def replace_marker(match):
        slide_id = match.group(1)
        content = notes_dict.get(slide_id)
        if content is None:
            missing.append(slide_id)
            return match.group(0)
        return f'<aside class="notes">{content}</aside>'

    output = re.sub(
        r'<aside class="notes"><!-- (slide-\d+) --></aside>',
        replace_marker,
        slim_html
    )

    if missing:
        print(f"WARNING: No notes found for: {', '.join(missing)}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Merged output saved to: {output_path}")


def verify(original_path, merged_path):
    """Verify that extract+merge produces the same output as the original."""
    with open(original_path, 'r', encoding='utf-8') as f:
        original = f.read()
    with open(merged_path, 'r', encoding='utf-8') as f:
        merged = f.read()

    if original == merged:
        print("PASS: Merged output matches original exactly.")
    else:
        # Find first difference
        for i, (a, b) in enumerate(zip(original, merged)):
            if a != b:
                line = original[:i].count('\n') + 1
                print(f"FAIL: First difference at character {i} (line {line})")
                print(f"  Original: ...{repr(original[max(0,i-20):i+20])}...")
                print(f"  Merged:   ...{repr(merged[max(0,i-20):i+20])}...")
                break
        else:
            shorter = min(len(original), len(merged))
            print(f"FAIL: Files differ in length (original={len(original)}, merged={len(merged)})")
            print(f"  Extra content starts at character {shorter}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'extract':
        extract_notes(sys.argv[2])
    elif cmd == 'merge':
        merge_notes(
            sys.argv[2],
            sys.argv[3] if len(sys.argv) > 3 else None,
            sys.argv[4] if len(sys.argv) > 4 else None
        )
    elif cmd == 'verify':
        if len(sys.argv) < 4:
            print("Usage: python notes-tool.py verify <original.html> <merged.html>")
            sys.exit(1)
        verify(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
