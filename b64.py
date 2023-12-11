import base64 

with open('/Users/geoffkaufman/Downloads/bicycle-health-dev-ba0e5cffcad9.json', 'r') as f:
    sample_string = f.read()
sample_string_bytes = sample_string.encode("ascii") 
  
base64_bytes = base64.b64encode(sample_string_bytes) 
base64_string = base64_bytes.decode("ascii") 
  
print(f"Encoded string: {base64_string}") 