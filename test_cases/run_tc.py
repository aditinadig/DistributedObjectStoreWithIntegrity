import subprocess
import time
import os
import shutil
from tc_utils import delete_file, overwrite_file, reset_all_nodes

def try_delete_local(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

def run_shell(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def run_all_pipeline():
    out, err = run_shell("python3 scripts/verify_fragments.py")
    run_shell("python3 scripts/reconstruct_file.py")
    return out

def show_result():
    print("\n📄 Final reconstructed.txt content:\n")
    with open("reconstructed.txt", "r") as f:
        print(f.read())
    print("-" * 50)

def run_test_case(tc_id):
    print(f"\n========================")
    print(f"🧪 Running Test Case: {tc_id}")
    print(f"========================")

    reset_all_nodes()
    time.sleep(1)

    # Step 1: Encode and upload original data
    run_shell("python3 scripts/erasure_coding.py")

    # Step 2: Modify based on test case
    if tc_id == "TC1":
        pass

    elif tc_id == "TC2":
        run_shell("python3 scripts/fingerprinting.py")
        delete_file(1, "fragment_1.bin")
        delete_file(1, "fingerprint_1.txt")

    elif tc_id == "TC3":
        run_shell("python3 scripts/fingerprinting.py")
        for i in [0, 1]:
            delete_file(i, f"fragment_{i}.bin")
            delete_file(i, f"fingerprint_{i}.txt")

    elif tc_id == "TC4":
        run_shell("python3 scripts/fingerprinting.py")
        for i in [0, 1, 2]:
            delete_file(i, f"fragment_{i}.bin")
            delete_file(i, f"fingerprint_{i}.txt")

    elif tc_id == "TC5":
        run_shell("python3 scripts/fingerprinting.py")
        overwrite_file(2, "fragment_2.bin", "tampered content")

    elif tc_id == "TC6":
        run_shell("python3 scripts/fingerprinting.py")
        overwrite_file(1, "fragment_1.bin", "BAD DATA 1")
        overwrite_file(2, "fragment_2.bin", "BAD DATA 2")

    elif tc_id == "TC7":
        run_shell("python3 scripts/fingerprinting.py")
        for i in [0, 1, 2]:
            overwrite_file(i, f"fragment_{i}.bin", f"BAD{i}")

    elif tc_id == "TC8":
        run_shell("python3 scripts/fingerprinting.py")
        delete_file(1, "fragment_1.bin")
        overwrite_file(2, "fragment_2.bin", "junk")

    elif tc_id == "TC9":
        run_shell("python3 scripts/fingerprinting.py")
        for i in range(1, 5):
            overwrite_file(i, f"fragment_{i}.bin", "corrupted")
    
    elif tc_id == "TC10":
        for i in range(5):
            delete_file(i, f"fingerprint_{i}.txt")

    elif tc_id == "TC11":
        run_shell("python3 scripts/fingerprinting.py")
        delete_file(3, "fragment_3.bin")
        delete_file(4, "fragment_4.bin")

    elif tc_id == "TC12":
        # Simulate upload of only 3 fragments by deleting before fingerprinting
        delete_file(3, "fragment_3.bin")
        delete_file(4, "fragment_4.bin")
        run_shell("python3 scripts/fingerprinting.py")

    elif tc_id == "TC13":
        for i in range(1, 5):
            delete_file(i, f"fragment_{i}.bin")
            delete_file(i, f"fingerprint_{i}.txt")
        run_shell("python3 scripts/fingerprinting.py")

    elif tc_id == "TC14":
        run_shell("python3 scripts/fingerprinting.py")
        overwrite_file(1, "fragment_1.bin", "completely wrong file")

    elif tc_id == "TC15":
        run_shell("python3 scripts/fingerprinting.py")
        overwrite_file(1, "fingerprint_1.txt", "deadbeef1")
        overwrite_file(2, "fingerprint_2.txt", "deadbeef2")

    elif tc_id == "TC16":
        run_shell("python3 scripts/fingerprinting.py")
        for i in [0, 2, 4]:
            overwrite_file(i, f"fingerprint_{i}.txt", "forged")

    elif tc_id == "TC17":
        run_shell("python3 scripts/fingerprinting.py")  # fingerprints before corruption
        overwrite_file(1, "fragment_1.bin", "error1")
        overwrite_file(2, "fragment_2.bin", "error2")

    else:
        print(f"❌ Unknown test case: {tc_id}")
        return

    # Step 3: Run pipeline
    out = run_all_pipeline()
    show_result()

    # Step 4: Cleanup
    if os.path.exists("reconstruction_temp"):
        shutil.rmtree("reconstruction_temp")
    try: os.remove("reconstructed.txt")
    except: pass

    
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 run_tc.py TC<number>")
    else:
        run_test_case(sys.argv[1])