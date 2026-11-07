import os
import re

CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = CJK_PATTERN.findall(content)
            if matches:
                return len(matches), matches[:10]
    except Exception as e:
        pass
    return 0, []

def main():
    root_dir = os.path.abspath(".")
    cjk_files = []
    
    # Exclude .git and .agents directories from internal search if desired, 
    # but let's see what is everywhere first
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # We can inspect everything
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            # check text-based files
            if ext in ['.md', '.py', '.txt', '.json', '.html', '.toml', '.yaml', '.yml', '.csv', '.ini', '.rst']:
                full_path = os.path.join(dirpath, f)
                rel_path = os.path.relpath(full_path, root_dir)
                count, sample = scan_file(full_path)
                if count > 0:
                    cjk_files.append((rel_path, count, "".join(sample)))
                    
    print(f"Total files with CJK characters: {len(cjk_files)}")
    for rel_path, count, sample in sorted(cjk_files, key=lambda x: x[0]):
        print(f"{rel_path}: {count} CJK chars (sample: {sample})")

if __name__ == "__main__":
    main()
