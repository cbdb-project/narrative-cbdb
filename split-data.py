import shutil, os

INPUT_FILE = "output.txt"
OUTPUT_PATH = "output"
SPLIT_ROWS = 15000

with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
    data = f.read()
    data = data.split("\n")
    data = [i for i in data if i]
    print(f"Total number of rows: {len(data)}")

if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)    
os.makedirs(OUTPUT_PATH)

for i in range(0, len(data), SPLIT_ROWS):
    with open(f"{OUTPUT_PATH}/output_{i//SPLIT_ROWS}.txt", 'w', encoding='utf-8-sig') as f:
        for item in data[i:i+SPLIT_ROWS]:
            f.write("%s\n" % item)
    print(f"File {i//SPLIT_ROWS} saved")

print("Done!")