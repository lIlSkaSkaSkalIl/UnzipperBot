import os
import logging
import patoolib
from pathlib import Path

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = [".zip", ".rar", ".tar", ".gz", ".7z"]

def extract_archive(file_path: str, output_dir: str = "downloads") -> list[str]:
    """
    Mengekstrak file arsip dan mengembalikan daftar file hasil ekstraksi.

    Args:
        file_path (str): Path ke file arsip
        output_dir (str): Folder tujuan ekstraksi

    Returns:
        list[str]: Daftar file hasil ekstraksi
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File tidak ditemukan: {file_path}")

    ext = Path(file_path).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise Exception(f"❌ Ekstensi {ext} tidak didukung: {ext}")

    # Buat folder ekstraksi berdasarkan nama file (tanpa ekstensi)
    extract_dir = os.path.join(output_dir, Path(file_path).stem)
    os.makedirs(extract_dir, exist_ok=True)

    logger.info(f"🧩 Mengekstrak: {file_path} → {extract_dir}")
    try:
        patoolib.extract_archive(file_path, outdir=extract_dir, verbosity=-1)
    except Exception as e:
        logger.exception("❌ Gagal saat mengekstrak arsip:")
        raise e

    # Hapus file arsip setelah ekstraksi
    try:
        os.remove(file_path)
        logger.info(f"🗑️ File arsip dihapus: {file_path}")
    except Exception as e:
        logger.warning(f"⚠️ Gagal menghapus arsip: {file_path} → {e}")

    # Kumpulkan semua file hasil ekstraksi
    extracted_files = []
    for root, _, files in os.walk(extract_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            if os.path.isfile(full_path):
                extracted_files.append(full_path)

    logger.info(f"✅ Ekstraksi selesai: {len(extracted_files)} file ditemukan.")
    return extracted_files
