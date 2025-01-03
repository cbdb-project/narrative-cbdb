import sqlite3
import os

def get_person_biographies(person_ids):
    conn = sqlite3.connect('cbdb.db')  # 連接到 SQLite 資料庫
    cursor = conn.cursor()
    
    biographies = []
    counter = 0
    for person_id in person_ids:
        counter += 1
        if counter % 5000 == 0:
            print(f"已處理 {counter}/{len(person_ids)} 人物 ID")
        # 獲取人物的中文姓名 (`c_name_chn`)
        cursor.execute("""
        SELECT c_name_chn 
        FROM BIOG_MAIN
        WHERE c_personid=?
        """, (person_id,))
        person_name = cursor.fetchone()
        person_name = person_name[0] if person_name else "未知人物"
        
        person_name_with_id = f"{person_name} (person id: {person_id})"
        biography = f"人物 {person_name_with_id} 的基本資料是: "
        
        
        # 基本資訊
        cursor.execute("""
        SELECT c_name AS EngName, c_name_chn AS ChName, c_birthyear AS YearBirth, c_deathyear AS YearDeath, 
               c_death_age AS YearsLived, c_notes AS Notes
        FROM BIOG_MAIN
        WHERE c_personid=?
        """, (person_id,))
        basic_info = cursor.fetchone()
        
        if basic_info:
            EngName, ChName, YearBirth, YearDeath, YearsLived, Notes = basic_info
            biography += f"出生於 {YearBirth} 年，逝世於 {YearDeath} 年，享年 {YearsLived} 歲。"
            if Notes:
                biography += f"\n{person_name_with_id}的備註資訊是: {Notes}。"
        
        # 來源
        cursor.execute("""
        SELECT (SELECT c_title_chn FROM TEXT_CODES WHERE c_textid=BIOG_SOURCE_DATA.c_textid) AS Source, c_pages AS Pages
        FROM BIOG_SOURCE_DATA
        WHERE c_personid=?
        """, (person_id,))
        sources = cursor.fetchall()
        if sources:
            source_list = f"。\n{person_name_with_id}資訊的來源有：".join(f"{source} (頁數: {pages})" for source, pages in sources)
            biography += f"\n{person_name_with_id}資訊的來源有: {source_list}。"
        
        # 別名與別名類型
        cursor.execute("""
        SELECT 
            (SELECT c_name_type_desc_chn FROM ALTNAME_CODES WHERE c_name_type_code=ALTNAME_DATA.c_alt_name_type_code) AS AliasType,
            ALTNAME_DATA.c_alt_name_chn AS AliasName
        FROM ALTNAME_DATA
        WHERE c_personid=?
        """, (person_id,))
        aliases = cursor.fetchall()
        if aliases:
            alias_list = f"。\n{person_name_with_id}的別名有:".join(f"{alias_name} (類型: {alias_type})" for alias_type, alias_name in aliases)
            biography += f"\n{person_name_with_id}的別名有: {alias_list}。"
        
        # 地址與類型
        cursor.execute("""
        SELECT 
            (SELECT c_addr_desc_chn FROM BIOG_ADDR_CODES WHERE c_addr_type=BIOG_ADDR_DATA.c_addr_type) AS AddrType,
            (SELECT c_name_chn FROM ADDR_CODES WHERE c_addr_id=BIOG_ADDR_DATA.c_addr_id) AS AddrName
        FROM BIOG_ADDR_DATA
        WHERE c_personid=?
        """, (person_id,))
        addresses = cursor.fetchall()
        if addresses:
            addr_list = f"。\n{person_name_with_id}的傳記地址有:".join(f"{addr_name} (類型: {addr_type})" for addr_type, addr_name in addresses)
            biography += f"\n{person_name_with_id}的傳記地址有: {addr_list}。"
        
        # 入仕資訊
        cursor.execute("""
        SELECT c_year AS EntryYear, c_age AS EntryAge, 
               (SELECT c_entry_desc_chn FROM ENTRY_CODES WHERE c_entry_code = ENTRY_DATA.c_entry_code) AS RuShiType
        FROM ENTRY_DATA
        WHERE c_personid=?
        """, (person_id,))
        entries = cursor.fetchall()
        if entries:
            entry_list = f"。\n{person_name_with_id}的入仕資訊有:".join(f"於 {entry_year} 年， {entry_age} 歲入仕，入仕類型: {entry_type}。" for entry_year, entry_age, entry_type in entries)
            biography += f"\n{person_name_with_id}的入仕資訊有: {entry_list}。"
        
        # 官職
        cursor.execute("""
        SELECT OFFICE_CODES.c_office_chn AS OfficeName, POSTED_TO_OFFICE_DATA.c_firstyear AS FirstYear
        FROM POSTED_TO_OFFICE_DATA
        INNER JOIN OFFICE_CODES ON POSTED_TO_OFFICE_DATA.c_office_id = OFFICE_CODES.c_office_id
        WHERE POSTED_TO_OFFICE_DATA.c_personid=?
        """, (person_id,))
        postings = cursor.fetchall()
        if postings:
            posting_list = f"。\n{person_name_with_id}的任官有:".join(f"{office_name} (任職年份: {first_year})" for office_name, first_year in postings)
            biography += f"\n{person_name_with_id}的任官有: {posting_list}。"
        
        # 社會狀態
        cursor.execute("""
        SELECT (SELECT c_status_desc_chn FROM STATUS_CODES WHERE c_status_code=STATUS_DATA.c_status_code) AS StatusName
        FROM STATUS_DATA
        WHERE c_personid=?
        """, (person_id,))
        statuses = cursor.fetchall()
        if statuses:
            status_list = f"。\n{person_name_with_id}的社會狀態有:".join(status[0] for status in statuses if status[0])
            biography += f"\n{person_name_with_id}的社會狀態有: {status_list}。"
        
        # 親屬關係
        cursor.execute("""
        SELECT (SELECT c_name_chn FROM BIOG_MAIN WHERE c_personid=KIN_DATA.c_kin_id) AS KinPersonName,
               (SELECT c_kinrel_chn FROM KINSHIP_CODES WHERE c_kincode=KIN_DATA.c_kin_code) AS KinRelName
        FROM KIN_DATA
        WHERE c_personid=?
        """, (person_id,))
        kinships = cursor.fetchall()
        if kinships:
            kinship_list = f"。\n".join(f"{person_name_with_id} 的 {kin_rel} 是 {kin_name}" for kin_name, kin_rel in kinships)
            biography += f"\n{person_name_with_id}的親屬關係有: {kinship_list}。"
        
        # 社會關係
        cursor.execute("""
        SELECT (SELECT c_name_chn FROM BIOG_MAIN WHERE c_personid=ASSOC_DATA.c_assoc_id) AS AssocPersonName,
               (SELECT c_assoc_desc_chn FROM ASSOC_CODES WHERE c_assoc_code=ASSOC_DATA.c_assoc_code) AS AssocName
        FROM ASSOC_DATA
        WHERE c_personid=?
        """, (person_id,))
        associations = cursor.fetchall()
        if associations:
            assoc_list = f"。\n".join(f"{person_name_with_id} 的 {assoc_desc} 關係是 {assoc_name}" for assoc_name, assoc_desc in associations)
            biography += f"\n{person_name_with_id}的社會關係有: {assoc_list}。"
        
        # 文本
        cursor.execute("""
        SELECT TEXT_CODES.c_title_chn AS TextName, TEXT_CODES.c_text_year AS TextYear
        FROM TEXT_CODES
        INNER JOIN BIOG_TEXT_DATA ON TEXT_CODES.c_textid = BIOG_TEXT_DATA.c_textid
        WHERE BIOG_TEXT_DATA.c_personid=?
        """, (person_id,))
        texts = cursor.fetchall()
        if texts:
            text_list = f"。\n{person_name_with_id}的著作有: ".join(f"{text_name} ({text_year}年)" for text_name, text_year in texts)
            biography += f"\n{person_name_with_id}的著作有: {text_list}。"
        
        biographies.append(biography.strip())  # 去掉多餘的空格和標點
    
    conn.close()
    return biographies

def get_personid():
    conn = sqlite3.connect('cbdb.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c_personid
    FROM BIOG_MAIN
    """)
    output_list = cursor.fetchall()
    conn.close()
    output_list = [i[0] for i in output_list]
    return output_list

with open('4 person_ids.txt', 'r', encoding='utf-8-sig') as f:
    personid_list_subset = [int(line.strip()) for line in f.readlines()]

personid_list = get_personid()

print("personid list:")
print(personid_list[:10])

print("personid list subset:")
print(personid_list_subset[:10])

personid_list = list(set(personid_list) & set(personid_list_subset))

print(len(personid_list))

# sampling
# personid_list = personid_list[:200]

# skip personid = 0 (unknown person)
output_list = get_person_biographies(list(personid_list[1:]))

# save the output to a text file
with open('output.txt', 'w', encoding='utf-8-sig') as f:
    for item in output_list:
        f.write("%s\n" % item)
print("已完成，請查看 output.txt 檔案")