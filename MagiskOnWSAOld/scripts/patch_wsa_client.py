import os
import sys

def patch_wsa_client(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
        
    with open(file_path, "rb") as f:
        data = bytearray(f.read())
        
    patched = False
    
    # Patch 1: Replace 81 FB 05 00 07 80 75 19 with 81 FB 05 00 07 80 EB 19
    pattern1 = b'\x81\xfb\x05\x00\x07\x80\x75\x19'
    idx1 = data.find(pattern1)
    if idx1 != -1:
        data[idx1 + 6] = 0xEB
        print(f"Applied Patch 1 (Bypass E_ACCESSDENIED) at offset {hex(idx1)}")
        patched = True
    else:
        print("Patch 1 pattern not found or already patched")
        
    # Patch 2: Replace 78 26 with 90 90 inside the pattern:
    # 15 8B 45 29 00 85 C0 78 26 48 8B 4D F0
    pattern2 = b'\x15\x8b\x45\x29\x00\x85\xc0\x78\x26\x48\x8b\x4d\xf0'
    idx2 = data.find(pattern2)
    if idx2 != -1:
        data[idx2 + 7] = 0x90
        data[idx2 + 8] = 0x90
        print(f"Applied Patch 2 (Bypass GetResults HRESULT check) at offset {hex(idx2)}")
        patched = True
    else:
        print("Patch 2 pattern not found or already patched")
        
    if patched:
        with open(file_path, "wb") as f:
            f.write(data)
        print("WsaClient.exe patched successfully!")
        return True
    else:
        print("No patches applied.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: patch_wsa_client.py <path_to_WsaClient.exe>")
        sys.exit(1)
    patch_wsa_client(sys.argv[1])
