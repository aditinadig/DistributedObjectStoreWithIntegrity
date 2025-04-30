# 🧠 Distributed Object Store with Integrity

This project implements a **fault-tolerant distributed storage system** that:
- Splits and distributes a file across multiple remote nodes.
- Generates fingerprints to ensure integrity.
- Supports test case simulation with fragment corruption/missing cases.
- Reconstructs the original file using verified fragments.
- Provides a **simple CLI interface** for test execution.

---

## 📁 Directory Structure

```
DistributedObjectStoreWithIntegrity/
├── scripts/
│   ├── interface.py          # CLI UI
│   ├── erasure_coding.py     # Split & upload fragments
│   ├── fingerprinting.py     # Fingerprint generation
│   ├── verify_fragments.py   # Fingerprint validation
│   ├── reconstruct_file.py   # Rebuild file from fragments
│   └── crypto_utils.py       # Encryption helpers (optional)
├── test_cases/
│   └── run_tc.py             # All test case automation
├── remote/
│   ├── remote_utils.py       # Remote SCP/SSH helpers
│   └── remote_config.py      # Remote IPs and SSH key
├── fragments/                # (Auto) Encrypted fragments
├── fingerprints/             # (Auto) Fingerprints
├── reconstruction_temp/      # (Auto) Temp download folder
├── reconstructed.txt         # ✅ Output file
└── simple_text.txt           # 📝 Input file
```

---

## ✅ Requirements

- Python 3.7+
- `rich` for colorful CLI

Install dependencies:
```bash
pip install rich
```

---

## 🚀 How to Run

### 1. Run the CLI Interface

```bash
python3 scripts/interface.py
```

### 2. Use the Menu

You'll see:
```
🔧 Distributed Object Store - Main Menu
[1] Run a test case
[2] Exit
```

### 3. Run a Test Case

Type a test case ID like:
```
TC1    # All valid
TC2    # Missing fragment
...
TC11   # Mixed corruption
```

It will:
- Reset nodes
- Run upload, corruption, fingerprint, verification
- Print final `reconstructed.txt` content

---

## 🧪 Example Output

```
✅ Fragment 0 is VALID.
❌ Fragment 1 is missing!
✅ Fragment 2 is VALID.
🔄 Replacing fragment 1 with placeholder: [MISSING FRAGMENT]

✅ File reconstructed as 'reconstructed.txt'
```

---

## 🛡️ Security (Optional Add-On)

You can enable **fragment encryption** using `cryptography.Fernet` in `crypto_utils.py`.

---

## 📌 Notes

- Update `remote/remote_config.py` with your actual EC2 IPs and `.pem` key path.
- Fragments and fingerprints are stored both locally and on remote nodes.
- Run `scripts/test_cases/run_tc.py TCx` manually if you want CLI-free automation.

---

## 🙌 Author

Project developed as part of a fault-tolerant systems course.
