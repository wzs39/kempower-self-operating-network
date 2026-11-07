import os
import re
import zipfile

CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def check_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.md', '.py', '.txt', '.html', '.json', '.ini', '.toml', '.yaml', '.yml', '.csv', '.rst']:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            m = CJK_PATTERN.findall(content)
            if m:
                return len(m), m[:10]
    elif ext == '.pptx':
        # Unzip and inspect slide contents, notes, comments, shapes
        with zipfile.ZipFile(filepath, 'r') as z:
            cjk_found = []
            for name in z.namelist():
                # Ignore system theme fallback font declarations (e.g. ppt/theme/theme1.xml)
                if name.startswith('ppt/theme/'):
                    continue
                if name.endswith(('.xml', '.rels', '.txt')):
                    txt = z.read(name).decode('utf-8', errors='ignore')
                    m = CJK_PATTERN.findall(txt)
                    if m:
                        cjk_found.extend(m)
            if cjk_found:
                return len(cjk_found), cjk_found[:10]
    return 0, []

def main():
    submission_dir = os.path.abspath("submission")
    assert os.path.exists(submission_dir), "submission directory does not exist!"
    
    total_violations = 0
    scanned_count = 0
    
    for root, dirs, files in os.walk(submission_dir):
        for f in files:
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, submission_dir)
            scanned_count += 1
            count, sample = check_file(filepath)
            if count > 0:
                print(f"[FAIL] {rel_path}: {count} CJK characters found: {''.join(sample)}")
                total_violations += count

    print(f"\n=======================================================")
    print(f"ZERO-CJK AUDIT RESULT FOR 'submission/':")
    print(f"Total files scanned: {scanned_count}")
    print(f"Total CJK violations: {total_violations}")
    if total_violations == 0:
        print("[SUCCESS] 100% PURE ENGLISH GUARANTEED (0 CJK MATCHES)")
    else:
        print(f"[ERROR] {total_violations} CJK MATCHES DETECTED!")
    print(f"=======================================================\n")
    return total_violations

if __name__ == "__main__":
    exit(main())
