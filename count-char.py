with open("output.txt", 'r', encoding='utf-8-sig') as f:
    data = f.read()
    print(f"Total number of characters: {len(data)}")