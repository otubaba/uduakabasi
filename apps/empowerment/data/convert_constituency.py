import json
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

SOURCE = BASE_DIR / "constituency_raw.js"
OUTPUT = BASE_DIR / "constituency.py"


# ============================================================
# LOAD RAW JAVASCRIPT DATA
# ============================================================

def load_raw_data():

    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE}"
        )

    text = SOURCE.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Remove:
    #
    # const data =
    # --------------------------------------------------------

    text = re.sub(
        r"^\s*const\s+data\s*=\s*",
        "",
        text,
        count=1,
    )

    text = text.strip()

    # --------------------------------------------------------
    # Remove trailing semicolon
    # --------------------------------------------------------

    if text.endswith(";"):
        text = text[:-1]

    text = text.strip()

    # --------------------------------------------------------
    # Convert JavaScript single-quoted strings to JSON strings
    # --------------------------------------------------------

    text = re.sub(
        r"'([^']*)'",
        lambda match: json.dumps(
            match.group(1)
        ),
        text,
    )

    # --------------------------------------------------------
    # Convert unquoted JavaScript object keys
    # --------------------------------------------------------

    text = re.sub(
        r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:',
        r'\1"\2":',
        text,
    )

    try:

        return json.loads(text)

    except json.JSONDecodeError as exc:

        print("\nERROR: Could not parse constituency_raw.js\n")
        print(
            f"Line: {exc.lineno}"
        )
        print(
            f"Column: {exc.colno}"
        )
        print(
            f"Message: {exc.msg}"
        )

        raise


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    value = str(value)

    value = value.replace(
        "\t",
        " ",
    )

    value = value.replace(
        "\n",
        " ",
    )

    value = value.replace(
        "\r",
        " ",
    )

    # Collapse repeated spaces
    value = " ".join(
        value.split()
    )

    return value.strip()


# ============================================================
# NORMALIZE POLLING UNIT TYPE
# ============================================================

def normalize_type(value):

    value = clean_text(
        value
    ).lower()

    if "new" in value:
        return "new"

    return "existing"


# ============================================================
# PARSE A POLLING UNIT
# ============================================================

def parse_polling_unit(raw):

    # --------------------------------------------------------
    # Case 1:
    # Already an array/list:
    #
    # [
    #     "001",
    #     "SCHOOL",
    #     "EXISTING PU"
    # ]
    # --------------------------------------------------------

    if isinstance(
        raw,
        (list, tuple),
    ):

        if len(raw) != 3:

            print(
                "Could not parse polling unit:",
                raw,
            )

            return None

        code = clean_text(
            raw[0]
        )

        name = clean_text(
            raw[1]
        )

        pu_type = normalize_type(
            raw[2]
        )

        if not code or not name:
            print(
                "Invalid polling unit:",
                raw,
            )

            return None

        return (
            code,
            name,
            pu_type,
        )

    # --------------------------------------------------------
    # Case 2:
    # Raw string
    # --------------------------------------------------------

    if not isinstance(
        raw,
        str,
    ):

        print(
            "Unsupported polling unit:",
            raw,
        )

        return None

    raw = raw.strip()

    if not raw:
        return None

    # --------------------------------------------------------
    # First try TAB-separated data
    # --------------------------------------------------------

    parts = [
        clean_text(part)
        for part in raw.split("\t")
    ]

    parts = [
        part
        for part in parts
        if part
    ]

    if len(parts) >= 3:

        code = parts[0]

        name = parts[1]

        pu_type = normalize_type(
            parts[2]
        )

        # Sometimes the type is accidentally attached
        # to the polling-unit name.
        if (
            "existing" in name.lower()
            or "new pu" in name.lower()
        ):

            if (
                "new pu"
                in name.lower()
            ):

                pu_type = "new"

                name = re.sub(
                    r"\bNEW\s+PU\b",
                    "",
                    name,
                    flags=re.IGNORECASE,
                )

            else:

                pu_type = "existing"

                name = re.sub(
                    r"\bEXISTING(?:\s+PU)?\b",
                    "",
                    name,
                    flags=re.IGNORECASE,
                )

            name = clean_text(
                name
            )

        return (
            code,
            name,
            pu_type,
        )

    # --------------------------------------------------------
    # Case 3:
    #
    # Nsit Ibom style:
    #
    # 001 SOME POLLING UNIT EXISTING PU
    # --------------------------------------------------------

    match = re.match(
        r"^(\S+)\s+(.+?)\s+(EXISTING\s+PU|NEW\s+PU)$",
        raw,
        re.IGNORECASE,
    )

    if match:

        code = clean_text(
            match.group(1)
        )

        name = clean_text(
            match.group(2)
        )

        pu_type = normalize_type(
            match.group(3)
        )

        return (
            code,
            name,
            pu_type,
        )

    # --------------------------------------------------------
    # Case 4:
    #
    # Type accidentally embedded in name
    # --------------------------------------------------------

    match = re.match(
        r"^(\S+)\s+(.+?)\s+(EXISTING|NEW)(?:\s+PU)?$",
        raw,
        re.IGNORECASE,
    )

    if match:

        code = clean_text(
            match.group(1)
        )

        name = clean_text(
            match.group(2)
        )

        pu_type = normalize_type(
            match.group(3)
        )

        return (
            code,
            name,
            pu_type,
        )

    # --------------------------------------------------------
    # Could not parse
    # --------------------------------------------------------

    print(
        "Could not parse:",
        raw,
    )

    return None


# ============================================================
# NORMALIZE COMPLETE DATASET
# ============================================================

def normalize(data):

    result = {}

    skipped = 0
    imported = 0

    for lga_name, wards in data.items():

        lga_name = clean_text(
            lga_name
        )

        result[lga_name] = {}

        for ward_name, polling_units in wards.items():

            ward_name = clean_text(
                ward_name
            )

            result[lga_name][ward_name] = []

            for raw in polling_units:

                parsed = parse_polling_unit(
                    raw
                )

                if parsed is None:

                    skipped += 1

                    continue

                code, name, pu_type = parsed

                result[lga_name][ward_name].append(
                    (
                        code,
                        name,
                        pu_type,
                    )
                )

                imported += 1

    print()
    print(
        "======================================"
    )
    print(
        "NORMALIZATION COMPLETE"
    )
    print(
        "======================================"
    )
    print(
        f"Polling units imported: {imported}"
    )
    print(
        f"Polling units skipped:  {skipped}"
    )
    print(
        "======================================"
    )
    print()

    return result


# ============================================================
# WRITE DJANGO PYTHON DATA FILE
# ============================================================

def write_python(data):

    content = """# Auto-generated from constituency_raw.js
# Do not edit this file manually.

CONSTITUENCY_DATA = """

    content += repr(
        data
    )

    content += "\n"

    OUTPUT.write_text(
        content,
        encoding="utf-8",
    )

    print(
        f"Created: {OUTPUT}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "======================================"
    )
    print(
        "CONSTITUENCY DATA CONVERTER"
    )
    print(
        "======================================"
    )
    print(
        f"Source: {SOURCE}"
    )
    print(
        f"Output: {OUTPUT}"
    )
    print(
        "======================================"
    )
    print()

    raw = load_raw_data()

    normalized = normalize(
        raw
    )

    write_python(
        normalized
    )

    print()
    print(
        "Conversion completed successfully."
    )