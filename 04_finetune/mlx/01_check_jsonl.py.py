import json
import os
import sys


def check_jsonl_files(root_dir, log_filename="check_jsonl.log"):
    found_issues = False

    # Membuka file log untuk menulis hasil
    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(f"--- LAPORAN PEMERIKSAAN JSONL ---\n")
        log_file.write(f"Direktori target: {os.path.abspath(root_dir)}\n\n")

        # Berjalan di semua subfolder (recursive)
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".jsonl"):
                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()

                            if not lines:
                                log_file.write(f"⚠️ [KOSONG] {file_path}\n")
                                continue

                            for index, line in enumerate(lines):
                                line_content = line.strip()
                                if not line_content:
                                    continue  # Lewati baris kosong

                                try:
                                    # Validasi format JSON per baris
                                    json.loads(line_content)
                                except json.JSONDecodeError as e:
                                    found_issues = True
                                    log_file.write(f"❌ [ERROR] File: {file_path}\n")
                                    log_file.write(f"   Baris: {index + 1}\n")
                                    log_file.write(f"   Pesan Error: {e.msg}\n")
                                    log_file.write(
                                        f"   Potongan Teks: {line_content[:100]}\n"
                                    )
                                    log_file.write("-" * 50 + "\n")
                    except Exception as ex:
                        log_file.write(
                            f"🚫 [GAGAL BACA] Tidak bisa membuka file {file_path}: {str(ex)}\n"
                        )

        if not found_issues:
            log_file.write(
                "\n✅ Selesai! Semua file JSONL valid. Tidak ada masalah format ditemukan.\n"
            )
        else:
            log_file.write(
                "\n⚠️ Pemeriksaan selesai dengan beberapa kesalahan ditemukan. Silakan cek detail di atas.\n"
            )

    print(
        f"Pemeriksaan selesai! Silakan buka file '{log_filename}' untuk melihat hasilnya."
    )


if __name__ == "__main__":
    target_folder = "/Users/novay/Applications/Project/Enterwind/lexindo/python/lexindo-llm/03_finetune_dataset/dataset"
    if os.path.exists(target_folder):
        check_jsonl_files(target_folder)
    else:
        print(f"Folder '{target_folder}' tidak ditemukan.")
