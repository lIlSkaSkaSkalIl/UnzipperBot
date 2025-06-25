import os
import shutil
import logging
import patoolib
from pathlib import Path

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = [".zip", ".rar", ".tar", ".gz", ".7z"]

def extract_archive(file_path: str, output_dir: str = "downloads") -> list[str]:
    """
    Mengekstrak file arsip ke dalam direktori output.

    Args:
        file_path (str): Path ke file arsip
        output_dir (str): Folder tujuan ekstrak

    Returns:
        list[str]: Daftar path file hasil ekstraksi
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File tidak ditemukan: {file_path}")

    ext = Path(file_path).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise Exception(f"❌ Ekstensi {ext} tidak didukung untuk ekstraksi.")

    extract_dir = os.path.join(output_dir, Path(file_path).stem)
    os.makedirs(extract_dir, exist_ok=True)

    logger.info(f"🧩 Mengekstrak {file_path} ke {extract_dir}")
    try:
        patoolib.extract_archive(file_path, outdir=extract_dir, verbosity=-1)
    except Exception as e:
        logger.exception("❌ Gagal saat mengekstrak file:")
        raise e

    # Hapus file asli setelah ekstraksi
    os.remove(file_path)
    logger.info(f"🗑️ File arsip dihapus: {file_path}")

    # Ambil semua path file di dalam folder hasil ekstraksi
    extracted_files = []
    for root, _, files in os.walk(extract_dir):
        for name in files:
            extracted_files.append(os.path.join(root, name))

    logger.info(f"✅ Ekstraksi selesai: {len(extracted_files)} file ditemukan.")
    return extracted_files
