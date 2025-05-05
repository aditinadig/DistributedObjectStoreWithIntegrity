# 🛡️ Distributed Object Store with Integrity – Test Suite

This repository verifies data integrity and fault tolerance in a distributed object store using erasure coding and cryptographic fingerprinting.

---

## ✅ How to Run a Test Case

Each test case simulates specific faults (like deletion or corruption of fragments or fingerprints) and verifies if the system can reconstruct the original file.

### 🧪 Run a Test Case:

```bash
python3 test_cases/run_tc.py TC<number>
```

Example:
```bash
python3 test_cases/run_tc.py TC4
```

---

## 📊 Test Case Summary Table (TC1–TC17)

| TC   | What It Does                                      | Effect on Reconstructed Text                          | Outcome | Run Command                                  |
|------|---------------------------------------------------|--------------------------------------------------------|---------|----------------------------------------------|
| TC1  | No faults                                         | Full file reconstructed                                | ✅ PASS | `python3 test_cases/run_tc.py TC1`           |
| TC2  | Delete `fragment_001`                             | 4 fragments remain; enough for reconstruction          | ✅ PASS | `python3 test_cases/run_tc.py TC2`           |
| TC3  | Delete fragments `000` and `001`                  | 3 fragments remain; still reconstructable              | ✅ PASS | `python3 test_cases/run_tc.py TC3`           |
| TC4  | Delete `000`, `001`, `002`                        | Only 2 fragments left; reconstruction fails            | ❌ FAIL | `python3 test_cases/run_tc.py TC4`           |
| TC5  | Corrupt `fragment_002`                            | 4 valid fragments remain                               | ✅ PASS | `python3 test_cases/run_tc.py TC5`           |
| TC6  | Corrupt `fragment_001` and `fragment_002`         | 3 valid fragments remain                               | ✅ PASS | `python3 test_cases/run_tc.py TC6`           |
| TC7  | Corrupt `fragment_000`, `001`, `002`              | Only 2 valid fragments remain                          | ❌ FAIL | `python3 test_cases/run_tc.py TC7`           |
| TC8  | Delete `fingerprint_001.txt`                      | Fragment skipped during verify; rest valid             | ✅ PASS | `python3 test_cases/run_tc.py TC8`           |
| TC9  | Corrupt `fragment_000`, `002`, `003`, `004`       | Only 1 valid fragment remains                          | ❌ FAIL | `python3 test_cases/run_tc.py TC9`           |
| TC10 | Overwrite `fingerprint_001.txt`                   | Fingerprint mismatch skipped                           | ✅ PASS | `python3 test_cases/run_tc.py TC10`          |
| TC11 | Delete `fragment_001`, corrupt `002`              | 3 valid fragments left                                 | ✅ PASS | `python3 test_cases/run_tc.py TC11`          |
| TC12 | Delete `000`, `001`; corrupt `002`                | Only 2 fragments valid                                 | ❌ FAIL | `python3 test_cases/run_tc.py TC12`          |
| TC13 | Corrupt `fragment_003`                            | 4 valid fragments remain                               | ✅ PASS | `python3 test_cases/run_tc.py TC13`          |
| TC14 | Delete `fragment_003` and `fingerprint_003.txt`   | 4 valid fragments remain                               | ✅ PASS | `python3 test_cases/run_tc.py TC14`          |
| TC15 | Overwrite `fingerprint_000.txt`                   | Fingerprint mismatch skipped                           | ✅ PASS | `python3 test_cases/run_tc.py TC15`          |
| TC16 | Delete fragments `001`, `002`, `003`              | Only 2 fragments remain                                | ❌ FAIL | `python3 test_cases/run_tc.py TC16`          |
| TC17 | Delete `000`, `fingerprint_001.txt`; corrupt `002`| Only 2 fragments valid                                 | ❌ FAIL | `python3 test_cases/run_tc.py TC17`          |

---

## 📁 Project Structure

- `scripts/`: Core functionality for encoding, fingerprinting, verification, reconstruction.
- `test_cases/`: Fault injection test runner (`run_tc.py`)
- `tc_utils.py`: SSH utilities for corrupting/deleting remote files
- `reconstructed.txt`: Final output after running reconstruction

---

## 🛠️ Requirements

- Python 3.6+
- `zfec` library
- SSH access and key setup to 5 remote nodes

---