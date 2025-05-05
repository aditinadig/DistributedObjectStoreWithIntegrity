import subprocess
import time
import os
from tc_utils import delete_file, overwrite_file, reset_all_nodes

EXPECTED_CONTENT = "Hi this is a sample test file for checking distributed object store integrity."

def run_shell(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def run_all_pipeline():
    if os.path.exists("reconstructed.txt"):
        os.remove("reconstructed.txt")
    run_shell("python3 scripts/erasure_coding.py")
    run_shell("python3 scripts/fingerprinting.py")

def run_verify_and_reconstruct():
    run_shell("python3 scripts/verify_fragments.py")
    run_shell("python3 scripts/reconstruct_file.py")

def show_result():
    print("\n📄 Final reconstructed.txt content:\n")
    if os.path.exists("reconstructed.txt"):
        with open("reconstructed.txt", "r") as f:
            print(f.read())
    else:
        print("(No reconstructed.txt file found)")
    print("-" * 50)

def validate():
    if not os.path.exists("reconstructed.txt"):
        print("❌ Test Case FAILED: reconstructed.txt not found.")
        return

    try:
        with open("reconstructed.txt", "r") as f:
            content = f.read().strip()
        if content == EXPECTED_CONTENT:
            print("✅ Test Case PASSED: File reconstructed correctly.")
        else:
            print("❌ Test Case FAILED: File content incorrect or corrupted.")
    except Exception as e:
        print(f"❌ Test Case FAILED: Error reading file — {str(e)}")

def run_test_case(tc_id):
    print(f"\n========================")
    print(f"🧪 Running Test Case: {tc_id}")
    print(f"========================")

    if os.path.exists("reconstructed.txt"):
        os.remove("reconstructed.txt")

    reset_all_nodes()
    time.sleep(1)

    run_all_pipeline()
    time.sleep(1)  # Allow remote updates to settle

    # === Inject fault per test case ===
    if tc_id == "TC1":
        pass
    elif tc_id == "TC2":
        delete_file(1, "fragment_001")
    elif tc_id == "TC3":
        delete_file(0, "fragment_000")
        delete_file(1, "fragment_001")
    elif tc_id == "TC4":
        delete_file(0, "fragment_000")
        delete_file(1, "fragment_001")
        delete_file(2, "fragment_002")
    elif tc_id == "TC5":
        overwrite_file(2, "fragment_002", "XXXXX\n")
    elif tc_id == "TC6":
        overwrite_file(1, "fragment_001", "BAD1\n")
        overwrite_file(2, "fragment_002", "BAD2\n")
    elif tc_id == "TC7":
        overwrite_file(0, "fragment_000", "C0\n")
        overwrite_file(1, "fragment_001", "C1\n")
        overwrite_file(2, "fragment_002", "C2\n")
    elif tc_id == "TC8":
        delete_file(1, "fingerprint_001.txt")
    elif tc_id == "TC9":
        # 1 valid, 4 corrupted (only keep fragment_001 valid)
        overwrite_file(0, "fragment_000", "CORRUPT0\n")
        # fragment_001 is left valid
        overwrite_file(2, "fragment_002", "CORRUPT2\n")
        overwrite_file(3, "fragment_003", "CORRUPT3\n")
        overwrite_file(4, "fragment_004", "CORRUPT4\n")
    elif tc_id == "TC10":
        overwrite_file(1, "fingerprint_001.txt", "1234567890abcdef")
    elif tc_id == "TC11":
        delete_file(1, "fragment_001")
        overwrite_file(2, "fragment_002", "MIXED_ERROR\n")
    elif tc_id == "TC12":
        delete_file(0, "fragment_000")
        delete_file(1, "fragment_001")
        overwrite_file(2, "fragment_002", "BAD\n")
    elif tc_id == "TC13":
        delete_file(0, "fragment_000")
        delete_file(1, "fragment_001")
        delete_file(2, "fragment_002")
        overwrite_file(3, "fragment_003", "CORRUPT\n")
    elif tc_id == "TC14":
        delete_file(3, "fragment_003")
        delete_file(3, "fingerprint_003.txt")
    elif tc_id == "TC15":
        overwrite_file(0, "fingerprint_000.txt", "FAKEFINGERPRINT")
        overwrite_file(1, "fingerprint_001.txt", "WRONGHASH")
    elif tc_id == "TC16":
        delete_file(1, "fragment_001")
        delete_file(2, "fragment_002")
        delete_file(3, "fragment_003")
    elif tc_id == "TC17":
        delete_file(0, "fragment_000")
        delete_file(1, "fingerprint_001.txt")
        overwrite_file(2, "fragment_002", "CORRUPTED\n")
    else:
        print(f"❌ Unknown test case ID: {tc_id}")
        return

    time.sleep(1)  # Wait for deletion/corruption effects
    run_verify_and_reconstruct()
    show_result()
    validate()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 run_tc.py TC<number>")
    else:
        run_test_case(sys.argv[1])