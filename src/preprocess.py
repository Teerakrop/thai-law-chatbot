import os

def load_documents(data_folder='data'):
    """
    อ่านไฟล์ .txt จากโฟลเดอร์ data แล้วรวบรวมข้อมูลกฎหมาย
    โดยสมมุติว่าแต่ละไฟล์ .txt เป็นเอกสารของกฎหมายแต่ละฉบับ
    """
    documents = []
    if not os.path.exists(data_folder):
        print(f"โฟลเดอร์ '{data_folder}' ไม่พบ กรุณาตรวจสอบ path")
        return documents  # คืนค่า list ว่าง

    for filename in os.listdir(data_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(data_folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # สำหรับตัวอย่างนี้ เราจะถือว่าเอกสารทั้งหมดในไฟล์ .txt เป็นเอกสารเดียว
                    # หากไฟล์มีโครงสร้างหลายบทหรือมาตรา คุณอาจต้องแยกข้อมูลภายในไฟล์นี้ออกเป็นหลายส่วน
                    documents.append({
                        'title': filename,   # ใช้ชื่อไฟล์เป็น title
                        'section': 'ทั้งหมด', # กำหนดค่าเริ่มต้นหรือปรับปรุงตามความต้องการ
                        'content': content
                    })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    print(f"โหลดเอกสารกฎหมายมาได้ {len(documents)} รายการ")
    return documents

def chunk_text(text, max_length=500):
    """
    แบ่งข้อความเป็น chunk ที่มีความยาวไม่เกิน max_length คำ
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_length):
        chunk = ' '.join(words[i:i+max_length])
        chunks.append(chunk)
    return chunks

def process_documents(documents):
    """
    ทำการ chunk สำหรับแต่ละเอกสาร แล้วเก็บผลลัพธ์ลงใน list ใหม่
    """
    processed_docs = []
    if documents is None:
        print("Error: documents is None")
        return processed_docs
    for doc in documents:
        chunks = chunk_text(doc['content'])
        for idx, chunk in enumerate(chunks):
            processed_docs.append({
                'title': doc['title'],
                'section': doc['section'],
                'chunk_id': idx,
                'content': chunk
            })
    print(f"แบ่งข้อมูลออกเป็น {len(processed_docs)} ชิ้น")
    return processed_docs

if __name__ == '__main__':
    docs = load_documents('data')
    processed = process_documents(docs)
