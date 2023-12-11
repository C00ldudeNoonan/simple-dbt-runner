import json
with open('/Users/geoffkaufman/Downloads/bicycle-health-dev-ba0e5cffcad9.json', 'r') as f:
    d = json.loads(f.read())
    print(json.dumps(d))