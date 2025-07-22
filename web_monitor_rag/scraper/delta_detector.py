import json
import sys
import os
from difflib import unified_diff

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_dicts(old, new):
    changes = {}
    for key in new:
        if key not in old:
            changes[key] = {'old': None, 'new': new[key]}
        elif new[key] != old[key]:
            changes[key] = {'old': old[key], 'new': new[key]}
    for key in old:
        if key not in new:
            changes[key] = {'old': old[key], 'new': None}
    return changes

def main(old_path, new_path, output_path=None):
    old = load_json(old_path)
    new = load_json(new_path)
    delta = {}
    for site in new:
        delta[site] = compare_dicts(old.get(site, {}), new[site])
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(delta, f, indent=2, ensure_ascii=False)
        print(f"Delta written to {output_path}")
    else:
        print(json.dumps(delta, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python delta_detector.py <old_json> <new_json> [output_json]")
        sys.exit(1)
    old_path = sys.argv[1]
    new_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    main(old_path, new_path, output_path)
