import hashlib
import datetime

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        block_string = block_string.encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        block = Block(0, "Genesis Block", "0")
        self.chain.append(block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_index = last_block.index + 1
        new_block = Block(new_index, data, last_block.hash)
        self.chain.append(new_block)

    def is_valid(self):
        for i in (1, len(self.chain) - 1):
            current_chain = self.chain[i]
            previous = self.chain[i - 1]

            #Hash toàn vẹn: hash đang lưu trong block có bằng calculate_hash() tính lại không? Nếu không → trả về False
            if current_chain.hash != current_chain.calculate_hash():
                return False
            
            #Liên kết đúng: previous_hash của block hiện tại có bằng hash của block trước không? Nếu không → trả về False
            if current_chain.previous_hash != previous.hash:
                return False
        
        #Nếu duyệt hết chuỗi mà không phát hiện lỗi → trả về True
        return True

def main():
    # Khởi tạo các giao dịch
    block = Blockchain()
    block.add_block("Alice gửi 50 BTC cho Bob")
    block.add_block("Bob gửi 20 BTC cho Carol")
    block.add_block("Carol gửi 10 BTC cho Dave")

    #In toàn bộ thông tin các Block trong Blockchain
    for i in block.chain:
        print(f"===== Block {i.index} =====")
        print(f"Data: {i.data}")
        print(f"Timestamp: {i.timestamp}")
        print(f"Hash: {i.hash}")
        print(f"Previous Hash: {i.previous_hash}")
        print()

    # Kiểm tra chuỗi hợp lệ
    valid_before = block.is_valid()
    print(f"Chuỗi hợp lệ: {valid_before}")
    print()

    # Kiểm tra chuỗi sau khi bị chỉnh sửa
    block.chain[1].data = "Alice gửi 100 BTC cho Carol"
    valid_after = block.is_valid()
    print(f"Sau khi giả mạo: {valid_after}")

    """
    Khi thay đổi dữ liệu trong block thì giá trị trong hàm calculate_hash() bị thay đổi và khi so sánh với hash cũ thì sẽ trả về giá trị False
    """

if __name__ == "__main__":
    main()