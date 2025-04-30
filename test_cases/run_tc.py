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

    # Step 1: Create and upload original fragments
    run_shell("python3 scripts/erasure_coding.py")

    # Step 2: Inject error conditions (mutate remote state)
    if tc_id == "TC1":
        pass
    elif tc_id == "TC2":
        run_shell("python3 scripts/fingerprinting.py")    # Generate + upload valid fingerprints
        delete_file(1, "fragment_1.bin")                  # Now simulate TC2 (delete remote fragment)
        try_delete_local("fragments/fragment_1.bin")
    elif tc_id == "TC3":
        delete_file(0, "fragment_0.bin")
        delete_file(1, "fragment_1.bin")
        try_delete_local("fragments/fragment_0.bin")
        try_delete_local("fragments/fragment_1.bin")
    elif tc_id == "TC4":
        delete_file(0, "fragment_0.bin")
        delete_file(1, "fragment_1.bin")
        delete_file(2, "fragment_2.bin")
        try_delete_local("fragments/fragment_0.bin")
        try_delete_local("fragments/fragment_1.bin")
        try_delete_local("fragments/fragment_2.bin")
    elif tc_id == "TC5":
        overwrite_file(2, "fragment_2.bin", "XXXXX\n")
    elif tc_id == "TC6":
        overwrite_file(1, "fragment_1.bin", "BAD1\n")
        overwrite_file(2, "fragment_2.bin", "BAD2\n")
    elif tc_id == "TC7":
        overwrite_file(0, "fragment_0.bin", "C0\n")
        overwrite_file(1, "fragment_1.bin", "C1\n")
        overwrite_file(2, "fragment_2.bin", "C2\n")
    elif tc_id == "TC8":
        run_shell("python3 scripts/fingerprinting.py")
        delete_file(1, "fingerprint_1.txt")
        run_all_pipeline()
        show_result()
        return
    elif tc_id == "TC9":
        run_shell("python3 scripts/fingerprinting.py")  # fingerprint first
        delete_file(1, "fragment_1.bin")                 # then delete fragment
        delete_file(1, "fingerprint_1.txt")              # and fingerprint
        run_all_pipeline()
        show_result()
        return
    elif tc_id == "TC10":
        run_shell("python3 scripts/fingerprinting.py")
        overwrite_file(1, "fingerprint_1.txt", "1234567890abcdef")
        run_all_pipeline()
        show_result()
        return
    elif tc_id == "TC11":
        delete_file(1, "fragment_1.bin")
        overwrite_file(2, "fragment_2.bin", "MIXED_ERROR\n")

    # Step 3: Run fingerprinting AFTER corruption
    run_shell("python3 scripts/fingerprinting.py")

    # Step 4: Verify and reconstruct
    run_all_pipeline()
    show_result()

        # Step 5: Local cleanup after test
    for i in range(3):
        try: os.remove(f"fragments/fragment_{i}.bin")
        except FileNotFoundError: pass
        try: os.remove(f"fingerprints/fingerprint_{i}.txt")
        except FileNotFoundError: pass

    if os.path.exists("reconstruction_temp"):
        shutil.rmtree("reconstruction_temp")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 run_tc.py TC<number>")
    else:
        run_test_case(sys.argv[1])