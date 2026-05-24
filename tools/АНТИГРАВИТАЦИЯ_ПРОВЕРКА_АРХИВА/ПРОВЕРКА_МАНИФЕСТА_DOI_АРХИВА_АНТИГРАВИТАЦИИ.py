#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Проверка CSV-манифеста DOI-архива направления Антигравитация."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys


REQUIRED_COLUMNS = [
    "ИМЯ_ФАЙЛА",
    "ПУТЬ_В_ПАКЕТЕ",
    "ТИП_ФАЙЛА",
    "ВЕРСИЯ_ПАКЕТА",
    "РАЗМЕР_БАЙТ",
    "SHA256",
    "ПУБЛИЧНЫЙ_СТАТУС",
    "GITHUB_COMMIT",
    "BITRIX24_FILE_ID",
    "DOI_ИЛИ_АРХИВНЫЙ_URL",
    "ЛИЦЕНЗИЯ",
    "КОММЕНТАРИЙ",
]

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
COMMIT_RE = re.compile(r"^[a-f0-9]{7,40}$")
BITRIX_RE = re.compile(r"^[0-9]+$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9._-]+)?$")
PLACEHOLDER_RE = re.compile(r"^ТРЕБУЕТ_")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Проверяет CSV-манифест DOI-архива Антигравитации."
    )
    parser.add_argument("--manifest", required=True, help="Путь к CSV-манифесту.")
    parser.add_argument(
        "--base-dir",
        required=True,
        help="Базовая папка, относительно которой проверяется ПУТЬ_В_ПАКЕТЕ.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Запрещает поля ТРЕБУЕТ_* и требует реальные хэши, размеры, commit и Bitrix24 file ID.",
    )
    return parser.parse_args()


def add_error(errors: list[str], row_number: int, message: str) -> None:
    errors.append(f"строка {row_number}: {message}")


def validate_row(row: dict[str, str], row_number: int, base_dir: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for column in REQUIRED_COLUMNS:
        value = (row.get(column) or "").strip()
        if not value:
            add_error(errors, row_number, f"пустая обязательная колонка {column}")

    version = (row.get("ВЕРСИЯ_ПАКЕТА") or "").strip()
    if version and not VERSION_RE.match(version):
        add_error(errors, row_number, "ВЕРСИЯ_ПАКЕТА не похожа на SemVer")

    public_status = (row.get("ПУБЛИЧНЫЙ_СТАТУС") or "").strip()
    if public_status not in {"DRAFT", "PUBLIC_CANDIDATE", "RELEASE_CANDIDATE", "RELEASED", "PRIVATE"}:
        add_error(errors, row_number, "ПУБЛИЧНЫЙ_СТАТУС вне допустимого набора")

    license_value = (row.get("ЛИЦЕНЗИЯ") or "").strip()
    if license_value not in {"CC_BY_4_0", "MIT", "INTERNAL", "ТРЕБУЕТ_REVIEW"}:
        add_error(errors, row_number, "ЛИЦЕНЗИЯ вне допустимого набора")

    package_path_value = (row.get("ПУТЬ_В_ПАКЕТЕ") or "").strip()
    if package_path_value.startswith("/") or ".." in Path(package_path_value).parts:
        add_error(errors, row_number, "ПУТЬ_В_ПАКЕТЕ должен быть относительным и без '..'")
        package_path = None
    else:
        package_path = base_dir / package_path_value

    if package_path and package_path.exists():
        actual_size = package_path.stat().st_size
        actual_hash = sha256_file(package_path)

        size_value = (row.get("РАЗМЕР_БАЙТ") or "").strip()
        if size_value.isdigit() and int(size_value) != actual_size:
            add_error(errors, row_number, f"размер не совпадает: manifest={size_value}, actual={actual_size}")
        elif PLACEHOLDER_RE.match(size_value):
            warnings.append(f"строка {row_number}: размер еще не зафиксирован")

        hash_value = (row.get("SHA256") or "").strip()
        if SHA256_RE.match(hash_value) and hash_value != actual_hash:
            add_error(errors, row_number, f"SHA256 не совпадает: manifest={hash_value}, actual={actual_hash}")
        elif PLACEHOLDER_RE.match(hash_value):
            warnings.append(f"строка {row_number}: SHA256 еще не зафиксирован")
    elif package_path:
        add_error(errors, row_number, f"файл не найден: {package_path}")

    hash_value = (row.get("SHA256") or "").strip()
    if not SHA256_RE.match(hash_value) and not PLACEHOLDER_RE.match(hash_value):
        add_error(errors, row_number, "SHA256 должен быть 64 hex символа или временным ТРЕБУЕТ_*")

    commit_value = (row.get("GITHUB_COMMIT") or "").strip()
    if not COMMIT_RE.match(commit_value) and not PLACEHOLDER_RE.match(commit_value):
        add_error(errors, row_number, "GITHUB_COMMIT должен быть git hash или временным ТРЕБУЕТ_*")

    bitrix_value = (row.get("BITRIX24_FILE_ID") or "").strip()
    if not BITRIX_RE.match(bitrix_value) and not PLACEHOLDER_RE.match(bitrix_value):
        add_error(errors, row_number, "BITRIX24_FILE_ID должен быть числом или временным ТРЕБУЕТ_*")

    if strict:
        for column in ["РАЗМЕР_БАЙТ", "SHA256", "GITHUB_COMMIT", "BITRIX24_FILE_ID", "DOI_ИЛИ_АРХИВНЫЙ_URL"]:
            value = (row.get(column) or "").strip()
            if PLACEHOLDER_RE.match(value):
                add_error(errors, row_number, f"strict-режим запрещает временное значение в {column}")

    return errors, warnings


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve()
    base_dir = Path(args.base_dir).resolve()

    if not manifest_path.exists():
        print(json.dumps({"ok": False, "ошибка": "манифест не найден"}, ensure_ascii=False, indent=2))
        return 2
    if not base_dir.exists():
        print(json.dumps({"ok": False, "ошибка": "base-dir не найден"}, ensure_ascii=False, indent=2))
        return 2

    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in header]
        extra = [column for column in header if column not in REQUIRED_COLUMNS]
        rows = list(reader)

    errors: list[str] = []
    warnings: list[str] = []
    if missing:
        errors.append(f"нет обязательных колонок: {', '.join(missing)}")
    if extra:
        warnings.append(f"есть дополнительные колонки: {', '.join(extra)}")

    seen_names: set[str] = set()
    for index, row in enumerate(rows, start=2):
        name = (row.get("ИМЯ_ФАЙЛА") or "").strip()
        if name in seen_names:
            add_error(errors, index, f"дубликат ИМЯ_ФАЙЛА: {name}")
        seen_names.add(name)
        row_errors, row_warnings = validate_row(row, index, base_dir, args.strict)
        errors.extend(row_errors)
        warnings.extend(row_warnings)

    result = {
        "ok": not errors,
        "manifest": str(manifest_path),
        "base_dir": str(base_dir),
        "rows": len(rows),
        "strict": bool(args.strict),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
