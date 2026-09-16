from django.core.management.base import BaseCommand
from django.db import transaction

from apps.empowerment.data.constituency import (
    CONSTITUENCY_DATA,
)

from apps.empowerment.models import (
    LocalGovernment,
    Ward,
    PollingUnit,
)


LGA_CODES = {
    "ETINAN": "19",
    "NSIT_IBOM": "20",
    "NSIT_UBIUM": "21",
}


LGA_DISPLAY_NAMES = {
    "ETINAN": "Etinan",
    "NSIT_IBOM": "Nsit Ibom",
    "NSIT_UBIUM": "Nsit Ubium",
}


class Command(BaseCommand):

    help = (
        "Import the Etinan Federal Constituency "
        "Local Governments, Wards and Polling Units."
    )

    @transaction.atomic
    def handle(self, *args, **options):

        total_lgas = 0
        total_wards = 0
        total_polling_units = 0
        skipped_polling_units = 0

        for lga_order, (lga_key, wards) in enumerate(
            CONSTITUENCY_DATA.items(),
            start=1,
        ):

            # ==================================================
            # LOCAL GOVERNMENT
            # ==================================================

            lga_name = self.clean_text(
                LGA_DISPLAY_NAMES.get(
                    lga_key,
                    lga_key.replace("_", " ").title(),
                )
            )

            lga_code = self.clean_text(
                LGA_CODES.get(
                    lga_key,
                    str(lga_order),
                )
            )

            lga, created = (
                LocalGovernment.objects.update_or_create(
                    code=lga_code,
                    defaults={
                        "name": lga_name,
                        "active": True,
                        "display_order": lga_order,
                    },
                )
            )

            total_lgas += 1

            action = "Created" if created else "Updated"

            self.stdout.write(
                self.style.SUCCESS(
                    f"{action} LGA: {lga_name}"
                )
            )

            # ==================================================
            # WARDS
            # ==================================================

            for ward_order, (
                raw_ward_name,
                polling_units,
            ) in enumerate(
                wards.items(),
                start=1,
            ):

                ward_name = self.clean_text(
                    raw_ward_name
                )

                ward_code = self.extract_ward_code(
                    polling_units,
                    ward_order,
                )

                ward, ward_created = (
                    Ward.objects.update_or_create(
                        local_government=lga,
                        code=ward_code,
                        defaults={
                            "name": ward_name,
                            "active": True,
                            "display_order": ward_order,
                        },
                    )
                )

                total_wards += 1

                action = (
                    "Created"
                    if ward_created
                    else "Updated"
                )

                self.stdout.write(
                    f"    {action} Ward: {ward_name}"
                )

                # ==================================================
                # POLLING UNITS
                # ==================================================

                for pu_order, pu_data in enumerate(
                    polling_units,
                    start=1,
                ):

                    # ------------------------------------------------
                    # Protect against malformed tuples
                    # ------------------------------------------------

                    if not isinstance(
                        pu_data,
                        (tuple, list),
                    ):
                        skipped_polling_units += 1

                        self.stdout.write(
                            self.style.WARNING(
                                f"        SKIPPED malformed "
                                f"polling unit: {pu_data}"
                            )
                        )

                        continue

                    if len(pu_data) != 3:
                        skipped_polling_units += 1

                        self.stdout.write(
                            self.style.WARNING(
                                f"        SKIPPED malformed "
                                f"polling unit in "
                                f"{lga_name} / {ward_name}: "
                                f"{pu_data}"
                            )
                        )

                        continue

                    raw_code, raw_name, raw_type = (
                        pu_data
                    )

                    # ------------------------------------------------
                    # CLEAN VALUES
                    # ------------------------------------------------

                    code = self.clean_text(
                        raw_code
                    )

                    name = self.clean_text(
                        raw_name
                    )

                    pu_type = (
                        self.normalize_polling_unit_type(
                            raw_type
                        )
                    )

                    # ------------------------------------------------
                    # Check for accidental data corruption
                    # ------------------------------------------------

                    if not code:

                        skipped_polling_units += 1

                        self.stdout.write(
                            self.style.WARNING(
                                f"        SKIPPED polling unit "
                                f"with empty code in "
                                f"{lga_name} / {ward_name}"
                            )
                        )

                        continue

                    if not name:

                        skipped_polling_units += 1

                        self.stdout.write(
                            self.style.WARNING(
                                f"        SKIPPED polling unit "
                                f"{code} with empty name in "
                                f"{lga_name} / {ward_name}"
                            )
                        )

                        continue

                    # ------------------------------------------------
                    # SAVE POLLING UNIT
                    # ------------------------------------------------

                    polling_unit, pu_created = (
                        PollingUnit.objects.update_or_create(
                            code=code,
                            defaults={
                                "ward": ward,
                                "name": name,
                                "polling_unit_type": pu_type,
                                "active": True,
                                "display_order": pu_order,
                            },
                        )
                    )

                    total_polling_units += 1

                    action = (
                        "Created"
                        if pu_created
                        else "Updated"
                    )

                    self.stdout.write(
                        f"        {action} PU: "
                        f"{code} — {name}"
                    )

        # ======================================================
        # SUMMARY
        # ======================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "===================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "CONSTITUENCY IMPORT COMPLETED"
            )
        )

        self.stdout.write(
            f"Local Governments: {total_lgas}"
        )

        self.stdout.write(
            f"Wards: {total_wards}"
        )

        self.stdout.write(
            f"Polling Units: {total_polling_units}"
        )

        self.stdout.write(
            f"Skipped Polling Units: "
            f"{skipped_polling_units}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                "===================================="
            )
        )

    # ==========================================================
    # TEXT CLEANING
    # ==========================================================

    @staticmethod
    def clean_text(value):

        if value is None:
            return ""

        # Convert tabs/newlines to spaces
        value = str(value).replace(
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

        # Remove duplicate whitespace
        value = " ".join(
            value.split()
        )

        return value.strip()

    # ==========================================================
    # POLLING UNIT TYPE NORMALIZATION
    # ==========================================================

    @classmethod
    def normalize_polling_unit_type(
        cls,
        value,
    ):

        value = cls.clean_text(
            value
        ).lower()

        # Anything containing "new"
        # becomes "new"
        if "new" in value:
            return "new"

        # Everything else becomes "existing"
        return "existing"

    # ==========================================================
    # WARD CODE
    # ==========================================================

    @classmethod
    def extract_ward_code(
        cls,
        polling_units,
        fallback,
    ):

        if not polling_units:
            return f"{fallback:02d}"

        # Find the first usable polling-unit code
        for polling_unit in polling_units:

            if not isinstance(
                polling_unit,
                (tuple, list),
            ):
                continue

            if len(polling_unit) < 1:
                continue

            first_code = cls.clean_text(
                polling_unit[0]
            )

            if not first_code:
                continue

            # ----------------------------------------------
            # Codes such as:
            #
            # 03-07-01-001
            # 03-21-02-001
            #
            # The second-to-last section is the ward code.
            # ----------------------------------------------

            parts = first_code.split("-")

            if len(parts) >= 4:

                return cls.clean_text(
                    parts[-2]
                )

        # Nsit Ibom and malformed records
        # fall back to display order.
        return f"{fallback:02d}"