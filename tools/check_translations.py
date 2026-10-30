import json
from pathlib import Path

batches = sorted(Path('VietHoa/work/batches').glob('ui_patch_*.json'))

for b in batches:
    with open(b, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"=== {b.name} ===")
    for item in data['items'][:6]:
        print(f"[{item['id']}]")
        print(f"  SRC: {repr(item['source'])}")
        print(f"  TGT: {repr(item['target'])}")
