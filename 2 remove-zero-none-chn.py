with open('output.txt', 'r', encoding='utf-8-sig') as f:
    data = f.read()

replace_list =[ "(任職年份: None)", "於 0 年，", "於 None 年，", "0 歲入仕，", "None 歲入仕，", "出生於 0 年，", "逝世於 0 年，", "出生於 None 年，", "逝世於 None 年，", "享年 0 歲。", "享年 None 歲。", "(None)", "(None)年", "(0年)", "(任職年份: 0)", "(任職年份: None)"]
replace_list.sort(key=len, reverse=True)

for item in replace_list:
    data = data.replace(item, "")

data = data.replace("。。", "。")

with open('output_remove_zero_none.txt', 'w', encoding='utf-8-sig') as f:
    f.write(data)

print("Done!")