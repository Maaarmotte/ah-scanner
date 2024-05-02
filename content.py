wakfu_items = {}
with open('content/items.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        args = line.split('=')
        wakfu_items[int(args[0])] = args[1].strip()


wakfu_categories = {}
with open('content/categories.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        args = line.split('=')
        wakfu_categories[int(args[0])] = args[1].strip()
