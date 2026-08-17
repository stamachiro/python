"""
LH Nautical - Script for Copying and Removing Comments from Python Files
Author: Senior AI Analyst
"""

import os
import glob
import shutil
import sys

def strip_comments_and_docstrings(source_code: str) -> str:
    """
    Strips all comments and docstrings from python source code cleanly.
    """
    lines = source_code.splitlines()
    clean_lines = []
    in_multiline_string = False
    delimiter = None

    for line in lines:
        stripped = line.strip()

        # Handle multiline docstrings (\"\"\" or ''')
        if not in_multiline_string:
            if stripped.startswith('"""') or stripped.startswith("'''"):
                delimiter = stripped[:3]
                if stripped.count(delimiter) >= 2:
                    continue
                else:
                    in_multiline_string = True
                    continue
            elif stripped.startswith("#"):
                continue
        else:
            if delimiter in stripped:
                in_multiline_string = False
                delimiter = None
            continue

        if in_multiline_string:
            continue

        # Handle inline comments
        if "#" in line:
            code_part = ""
            in_q = False
            q_char = None
            for char in line:
                if char in ('"', "'"):
                    if not in_q:
                        in_q = True
                        q_char = char
                    elif q_char == char:
                        in_q = False
                        q_char = None
                if char == "#" and not in_q:
                    break
                code_part += char
            line = code_part

        if line.rstrip():
            clean_lines.append(line.rstrip())

    return "\n".join(clean_lines) + "\n"


def process_python_files(work_dir="./"):
    work_path = os.path.abspath(work_dir)
    
    backup_dir = os.path.join(work_path, "python_originals_backup")
    clean_dir = os.path.join(work_path, "python_no_comments")
    
    os.makedirs(backup_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)
    
    py_files = [
        f for f in glob.glob(os.path.join(work_path, "*.py")) 
        if "create_clean_copies" not in f and not f.endswith("_nocomments.py")
    ]

    print(f"Found {len(py_files)} Python base files to process.")
    
    summary = []

    for file_path in py_files:
        filename = os.path.basename(file_path)
        
        # 1. Backup original copy
        backup_path = os.path.join(backup_dir, filename)
        shutil.copy2(file_path, backup_path)

        # 2. Read original
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # 3. Strip comments
        clean_content = strip_comments_and_docstrings(content)

        # 4. Save to clean_dir
        clean_file_path = os.path.join(clean_dir, filename)
        with open(clean_file_path, "w", encoding="utf-8") as f:
            f.write(clean_content)

        # 5. Save side-by-side _nocomments.py
        name_without_ext, ext = os.path.splitext(filename)
        side_clean_path = os.path.join(work_path, f"{name_without_ext}_nocomments{ext}")
        with open(side_clean_path, "w", encoding="utf-8") as f:
            f.write(clean_content)

        summary.append((filename, backup_path, clean_file_path, side_clean_path))

    print("\n==========================================================================")
    print("RESUMO DA CRIACAO DAS COPIAS E REMOCAO DE COMENTARIOS")
    print("==========================================================================")
    for orig, bkp, cln, sde in summary:
        print(f"[OK] Base File: {orig}")
        print(f"     |-- Backup Original: {os.path.basename(bkp)}")
        print(f"     |-- Clean File (Folder): {os.path.basename(cln)}")
        print(f"     +-- Clean File (Side-by-side): {os.path.basename(sde)}")
        print("-" * 74)


if __name__ == "__main__":
    process_python_files(r"c:\Users\stama\OneDrive\Documentos\Trabalho")
