"""
LH Nautical - Incidium Directory Organizer & Comment-Free Deduplicator
Author: Senior AI Analyst
"""

import os
import shutil
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

work_dir = r"c:\Users\stama\OneDrive\Documentos\Trabalho"
incidium_dir = os.path.join(work_dir, "incidium")

if os.path.exists(incidium_dir):
    shutil.rmtree(incidium_dir)
os.makedirs(incidium_dir, exist_ok=True)

print(f"Criando e copiando arquivos para a pasta 'incidium': {incidium_dir}")

def strip_all_comments(code_str: str) -> str:
    lines = code_str.splitlines()
    clean_lines = []
    in_multiline = False
    delimiter = None

    for line in lines:
        stripped = line.strip()

        if not in_multiline:
            if stripped.startswith('"""') or stripped.startswith("'''"):
                delimiter = stripped[:3]
                if stripped.count(delimiter) >= 2:
                    continue
                else:
                    in_multiline = True
                    continue
            elif stripped.startswith("#"):
                continue
        else:
            if delimiter in stripped:
                in_multiline = False
                delimiter = None
            continue

        if in_multiline:
            continue

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

# 1. Copy files to incidium
for item in os.listdir(work_dir):
    src_path = os.path.join(work_dir, item)
    dst_path = os.path.join(incidium_dir, item)
    
    if item in ["incidium", "python_originals_backup", "python_no_comments", "organize_incidium.py"]:
        continue
        
    if os.path.isdir(src_path):
        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    else:
        shutil.copy2(src_path, dst_path)

print("[OK] Copia inicial para 'incidium' concluida.")

# 2. Deduplicate and clean Python files inside incidium
incidium_files = os.listdir(incidium_dir)

nocomments_files = [f for f in incidium_files if f.endswith("_nocomments.py")]

for ncf in nocomments_files:
    base_name = ncf.replace("_nocomments.py", ".py")
    ncf_path = os.path.join(incidium_dir, ncf)
    base_path = os.path.join(incidium_dir, base_name)
    
    # Move the clean nocomments file over the base file
    shutil.move(ncf_path, base_path)
    print(f"  --> Consolidado: '{ncf}' -> '{base_name}' (sem duplicata e sem comentarios)")

# 3. Clean any remaining .py files in incidium
for f in os.listdir(incidium_dir):
    file_path = os.path.join(incidium_dir, f)
    if os.path.isfile(file_path) and f.endswith(".py"):
        with open(file_path, "r", encoding="utf-8", errors="replace") as file_in:
            raw_code = file_in.read()
        
        clean_code = strip_all_comments(raw_code)
        
        with open(file_path, "w", encoding="utf-8") as file_out:
            file_out.write(clean_code)

print("\n==========================================================================")
print("RESUMO DA ORGANIZACAO NA PASTA 'incidium'")
print("==========================================================================")
final_files = os.listdir(incidium_dir)
for f in sorted(final_files):
    f_path = os.path.join(incidium_dir, f)
    if os.path.isdir(f_path):
        print(f"[PASTA]   {f}/ ({len(os.listdir(f_path))} arquivos)")
    else:
        size_kb = os.path.getsize(f_path) / 1024
        print(f"[ARQUIVO] {f:<35s} ({size_kb:6.2f} KB) - SEM COMENTARIOS")
print("==========================================================================")
