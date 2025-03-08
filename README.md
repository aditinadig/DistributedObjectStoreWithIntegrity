# **Distributed Object Store with Integrity**

This project implements a **fault-tolerant distributed storage system** using **erasure coding** and **integrity verification**.

---

## **🔹 Setup Instructions**

### **1️⃣ Install Dependencies**
Ensure you have Python installed (Python 3.8+ recommended). Then, install the required packages:
```sh
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# For Windows, use: venv\Scripts\activate
pip install reedsolo pycryptodome
```

---

### **2️⃣ Set Up Storage Nodes**
Run the following command to create the necessary storage folders:
```sh
python setup_storage.py
```
This will create a **distributed_storage/** directory with **node_0/**, **node_1/**, etc.

---

### **3️⃣ Create a Large Text File (for Testing)**
#### **Option 1: Download a Public Domain Book**
```sh
curl -o large_text.txt https://www.gutenberg.org/cache/epub/1342/pg1342.txt
```

#### **Option 2: Generate a Large Repetitive Text File**
```sh
yes "Lorem ipsum dolor sit amet, consectetur adipiscing elit." | head -c 1M > large_text.txt
```
This creates a **1MB text file** filled with repeating text.

#### **Option 3: Duplicate a Small File Multiple Times**
```sh
cat example.txt example.txt example.txt > large_text.txt
```

---

### **4️⃣ Encode the File with Erasure Coding**
Run the encoding process to split the file across nodes:
```sh
python erasure_coding.py
```
This will **split** `large_text.txt` into **multiple fragments** and store them across nodes.

---

### **5️⃣ Generate Fingerprints for Integrity Verification**
```sh
python fingerprinting.py
```
This ensures that each fragment is **fingerprinted for integrity checks**.

---

### **6️⃣ Verify Data Integrity**
Check if stored fragments match their fingerprints:
```sh
python verify_fragments.py
```
If everything is correct, you should see:
```
✅ Fragment 0 is VALID.
✅ Fragment 1 is VALID.
✅ Fragment 2 is VALID.
✅ Enough valid fragments available for reconstruction.
```

---

### **7️⃣ Reconstruct the File from Fragments**
```sh
python reconstruct_file.py
```
If successful, you should see:
```
✅ File successfully reconstructed as 'reconstructed.txt'
```

---

### **8️⃣ Verify the Reconstructed File**
Check if the file was properly restored:
```sh
ls -lh large_text.txt reconstructed.txt  # Compare file sizes
diff large_text.txt reconstructed.txt    # Should show no output
head reconstructed.txt                    # Check the first few lines
tail reconstructed.txt                    # Check the last few lines
```

---

## **🔹 Notes**
- If a fragment is missing or corrupt, **reconstruction should still work as long as at least 2 valid fragments exist**.
- If reconstruction fails, debug using:
```sh
python verify_fragments.py
python reconstruct_file.py
```
- For larger files, **increase the number of nodes** in `setup_storage.py` and `erasure_coding.py`.

🚀 **Your fault-tolerant storage system is now ready!** 🚀

