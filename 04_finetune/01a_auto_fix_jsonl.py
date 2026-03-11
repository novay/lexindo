import json
import os
import re


def fix_json_content(line):
    """
    Mencoba memperbaiki baris JSON yang rusak karena tanda kutip ganda
    yang tidak di-escape di dalam string.
    """
    line = line.strip()
    if not line:
        return None

    try:
        # Jika sudah valid, kembalikan apa adanya
        json.loads(line)
        return line
    except json.JSONDecodeError:
        # Teknik Perbaikan:
        # Kita asumsikan struktur utamanya adalah {"from": "...", "value": "..."}
        # Kita akan mencari teks di antara separator kunci/nilai dan memperbaiki isinya.

        # Contoh Regex untuk menangkap isi dari 'value'
        # Pattern ini mencari teks di antara "value":" dan "} di akhir baris
        pattern = r'("value"\s*:\s*")(.*)("(\s*)\}\s*\]\s*\})'
        match = re.search(pattern, line)

        if match:
            prefix = match.group(1)  # "value":"
            content = match.group(2)  # Isi teks yang bermasalah
            suffix = match.group(3)  # "} ] }

            # Perbaikan: Escape tanda kutip yang tidak diawali backslash
            # tapi abaikan jika itu memang tanda kutip penutup (logic ini tricky)
            # Cara paling aman: ganti semua " jadi \" lalu kembalikan yang seharusnya
            fixed_content = content.replace('\\"', '"').replace('"', '\\"')

            fixed_line = (
                f"{line[: match.start(2)]}{fixed_content}{line[match.end(2) :]}"
            )

            # Validasi ulang hasil perbaikan
            try:
                json.loads(fixed_line)
                return fixed_line
            except:
                return None
        return None


def process_files(
    root_dir,
    log_filename="/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/fix_report.log",
):
    with open(log_filename, "w") as log:
        log.write("--- LAPORAN PERBAIKAN OTOMATIS ---\n\n")

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".jsonl"):
                    file_path = os.path.join(root, file)
                    corrected_lines = []
                    any_fix = False

                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    for i, line in enumerate(lines):
                        fixed = fix_json_content(line)
                        if fixed and fixed.strip() != line.strip():
                            corrected_lines.append(fixed + "\n")
                            any_fix = True
                            log.write(f"✅ FIXED: {file_path} (Baris {i + 1})\n")
                        elif fixed:
                            corrected_lines.append(line)
                        else:
                            corrected_lines.append(line)
                            log.write(
                                f"❌ GAGAL: {file_path} (Baris {i + 1}) - Struktur terlalu rusak.\n"
                            )

                    if any_fix:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.writelines(corrected_lines)

    print(f"Selesai! Cek '{log_filename}' untuk melihat apa saja yang diperbaiki.")


if __name__ == "__main__":
    process_files(
        "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/dataset"
    )
