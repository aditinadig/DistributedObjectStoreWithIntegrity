# 🧪 Distributed Object Store with Integrity

This project simulates a distributed storage system with integrity verification. It splits a file into fragments, uploads them to remote nodes, computes fingerprints, and supports fault scenarios like fragment loss or corruption. The system verifies integrity and reconstructs the original file accordingly.

## 📁 Project Structure

```
.
├── scripts/                  # Main logic: encoding, verification, reconstruction
├── remote/                  # Remote config and upload utilities
├── fragments/               # Local fragment directory
├── fingerprints/            # Local fingerprint directory
├── test_cases/              # Test case runner and test mutation logic
├── reconstruction_temp/     # Temporary files for reconstruction
├── encryption/              # Key management for encryption layer
├── simple_text.txt          # Input file to split and upload
└── reconstructed.txt        # Final output file after reconstruction
```

## ▶️ Running the Interface

To launch the CLI interface:
```bash
python3 interface.py
```

Options:
- `[1] Run a test case` – Provide a test case ID (e.g., TC1–TC11)
- `[2] Exit` – Quit the interface

## 🧪 Run All Test Cases at Once

To run all test cases and compare outputs:
```bash
bash test_cases/run_all_tests.sh
```

## 📊 Test Case Behavior Reference

Each test simulates a specific fault condition. Here's what to expect in the final `reconstructed.txt`:

| Test Case | Description | Expected Output |
|-----------|-------------|-----------------|
| TC1 | No errors | Full original text |
| TC2 | Missing fragment 1 | Placeholder `[MISSING FRAGMENT]` in the middle |
| TC3 | Missing fragments 0 and 1 | Two placeholders at the beginning |
| TC4 | All fragments missing | Three placeholders |
| TC5 | Fragment 2 corrupted | Placeholder `[CORRUPT]` at the end |
| TC6 | Fragments 1 & 2 corrupted | Two `[CORRUPT]` placeholders at the end |
| TC7 | All fragments corrupted | All placeholders `[CORRUPT]` |
| TC8 | Missing fingerprint 1 | Placeholder `[MISSING FINGERPRINT]` in the middle |
| TC9 | Missing both fragment & fingerprint 1 | Placeholder `[MISSING FINGERPRINT]` in the middle |
| TC10 | Wrong fingerprint for fragment 1 | Placeholder `[CORRUPT]` in the middle |
| TC11 | Fragment 1 missing, fragment 2 corrupted | One `[CORRUPT]` and one `[MISSING FRAGMENT]` |

## 🔐 Security Layer

- Files are encrypted using Fernet before upload.
- Fingerprints are computed on the encrypted binary.

## 🧼 Cleanup

After each test case, all temporary files (local and remote) are reset for a clean run.

## ✅ Requirements

- Python 3.6+
- `cryptography` and `rich` packages
```bash
pip install cryptography rich
```

## 📬 Contact

Project by: Aditi Arun Nadig
