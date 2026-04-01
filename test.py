items = ['B', '3', 'A', '1', 'C', '2']

# Sort using a tuple as the key
items.sort(key=lambda x: (x.isdigit(), x))

print(items)