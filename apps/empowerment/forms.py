from django import forms

from .models import (
    EmpowermentApplication,
    LocalGovernment,
    Ward,
    PollingUnit,
)


class EmpowermentApplicationForm(forms.ModelForm):

    class Meta:
        model = EmpowermentApplication

        fields = [
            "first_name",
            "last_name",
            "other_names",
            "gender",
            "date_of_birth",

            "phone",
            "email",
            "address",

            "community",
            "local_government",
            "ward",
            "polling_unit",
            "vin",

            "occupation",
            "employment_status",
            "educational_background",

            "reason_for_applying",
            "proposed_use",
            "relevant_experience",
            "expected_impact",
        ]

        widgets = {

            # =====================================================
            # PERSONAL INFORMATION
            # =====================================================

            "first_name": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "Enter your first name",
                    "autocomplete": "given-name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "Enter your last name",
                    "autocomplete": "family-name",
                }
            ),

            "other_names": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "Other names (optional)",
                    "autocomplete": "additional-name",
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "cursor-pointer "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "type": "date",
                }
            ),

            # =====================================================
            # CONTACT INFORMATION
            # =====================================================

            "phone": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "08012345678",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "Enter your residential address",
                    "autocomplete": "street-address",
                }
            ),

            # =====================================================
            # CONSTITUENCY
            # =====================================================

            "community": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "Enter your community",
                }
            ),

            "local_government": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "cursor-pointer "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "id": "id_local_government",
                }
            ),

            "ward": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "cursor-pointer "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20 "
                        "disabled:cursor-not-allowed "
                        "disabled:bg-slate-100 "
                        "disabled:text-slate-500"
                    ),
                    "id": "id_ward",
                }
            ),

            "polling_unit": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "cursor-pointer "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20 "
                        "disabled:cursor-not-allowed "
                        "disabled:bg-slate-100 "
                        "disabled:text-slate-500"
                    ),
                    "id": "id_polling_unit",
                }
            ),

            # =====================================================
            # VOTER INFORMATION
            # =====================================================

            "vin": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": (
                        "Enter your Voters Identification Number (VIN)"
                    ),
                    "autocomplete": "off",
                    "maxlength": "50",
                    "inputmode": "text",
                }
            ),

            # =====================================================
            # BACKGROUND
            # =====================================================

            "occupation": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "e.g. Trader, Farmer, Student, Artisan",
                }
            ),

            "employment_status": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": (
                        "e.g. Employed, Self-employed, Unemployed"
                    ),
                }
            ),

            "educational_background": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "placeholder": "Highest educational qualification",
                }
            ),

            # =====================================================
            # APPLICATION QUESTIONS
            # =====================================================

            "reason_for_applying": forms.Textarea(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none resize-y "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "rows": 5,
                    "placeholder": (
                        "Tell us why you are applying for this "
                        "empowerment programme."
                    ),
                }
            ),

            "proposed_use": forms.Textarea(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none resize-y "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "rows": 4,
                    "placeholder": (
                        "Explain how you intend to use the support "
                        "if selected."
                    ),
                }
            ),

            "relevant_experience": forms.Textarea(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none resize-y "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "rows": 4,
                    "placeholder": (
                        "Describe any relevant skills, training, "
                        "business or work experience."
                    ),
                }
            ),

            "expected_impact": forms.Textarea(
                attrs={
                    "class": (
                        "w-full rounded-xl border border-slate-300 "
                        "bg-white px-4 py-3 text-sm text-slate-900 "
                        "shadow-sm outline-none resize-y "
                        "placeholder:text-slate-400 "
                        "focus:border-blue-600 focus:ring-2 "
                        "focus:ring-blue-600/20"
                    ),
                    "rows": 4,
                    "placeholder": (
                        "How will this opportunity benefit you, "
                        "your family or your community?"
                    ),
                }
            ),
        }

    def __init__(self, *args, programme=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.programme = programme

        # =========================================================
        # LOCAL GOVERNMENT
        # =========================================================

        self.fields["local_government"].queryset = (
            LocalGovernment.objects
            .filter(active=True)
            .order_by(
                "display_order",
                "name",
            )
        )

        # =========================================================
        # DEFAULT DEPENDENT QUERYSETS
        # =========================================================

        self.fields["ward"].queryset = Ward.objects.none()

        self.fields["polling_unit"].queryset = PollingUnit.objects.none()

        # =========================================================
        # GET CURRENT / SUBMITTED VALUES
        # =========================================================

        lga_id = None
        ward_id = None

        if self.is_bound:

            lga_id = self.data.get("local_government")
            ward_id = self.data.get("ward")

        elif self.instance and self.instance.pk:

            lga_id = self.instance.local_government_id
            ward_id = self.instance.ward_id

        # =========================================================
        # LOAD WARDS FOR SELECTED LGA
        # =========================================================

        if lga_id:

            self.fields["ward"].queryset = (
                Ward.objects
                .filter(
                    local_government_id=lga_id,
                    active=True,
                )
                .order_by(
                    "display_order",
                    "name",
                )
            )

        # =========================================================
        # LOAD POLLING UNITS FOR SELECTED WARD
        # =========================================================

        if ward_id:

            self.fields["polling_unit"].queryset = (
                PollingUnit.objects
                .filter(
                    ward_id=ward_id,
                    active=True,
                )
                .order_by(
                    "display_order",
                    "code",
                )
            )

        # =========================================================
        # EMPTY LABELS
        # =========================================================

        self.fields["gender"].empty_label = "Select gender"

        self.fields["local_government"].empty_label = (
            "Select Local Government Area"
        )

        self.fields["ward"].empty_label = "Select Ward"

        self.fields["polling_unit"].empty_label = (
            "Select Polling Unit"
        )

    # =============================================================
    # PHONE VALIDATION
    # =============================================================

    def clean_phone(self):

        phone = self.cleaned_data.get("phone")

        if not phone:
            return phone

        phone = (
            phone.strip()
            .replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if phone.startswith("0") and len(phone) == 11:
            phone = "+234" + phone[1:]

        elif phone.startswith("234") and len(phone) == 13:
            phone = "+" + phone

        elif phone.startswith("+234") and len(phone) == 14:
            pass

        else:
            raise forms.ValidationError(
                "Please enter a valid Nigerian phone number."
            )

        return phone

    # =============================================================
    # VIN VALIDATION
    # =============================================================

    def clean_vin(self):

        vin = self.cleaned_data.get("vin")
        date_of_birth = self.cleaned_data.get("date_of_birth")

        # VIN is optional for applicants below 16 years
        if date_of_birth:
            from datetime import date

            today = date.today()

            age = (
                today.year
                - date_of_birth.year
                - (
                    (today.month, today.day)
                    < (date_of_birth.month, date_of_birth.day)
                )
            )

            if age < 16:
                if not vin:
                    return ""

        # VIN is required for applicants aged 16 and above
        if not vin:
            raise forms.ValidationError(
                "Voters Identification Number (VIN) is required "
                "for applicants aged 16 years and above."
            )

        return vin.strip().upper()
    
    # =============================================================
    # FORM VALIDATION
    # =============================================================

    def clean(self):

        cleaned_data = super().clean()

        programme = self.programme

        phone = cleaned_data.get("phone")
        vin = cleaned_data.get("vin")

        local_government = cleaned_data.get("local_government")
        ward = cleaned_data.get("ward")
        polling_unit = cleaned_data.get("polling_unit")

        # ---------------------------------------------------------
        # DUPLICATE PHONE APPLICATION
        # ---------------------------------------------------------

        if phone and programme:

            existing_application = (
                EmpowermentApplication.objects
                .filter(
                    programme=programme,
                    phone=phone,
                )
                .exclude(status="withdrawn")
                .exclude(pk=self.instance.pk)
                .first()
            )

            if existing_application:

                self.add_error(
                    "phone",
                    "An application using this phone number has "
                    "already been submitted for this programme. "
                    "If you believe this is an error, please "
                    "contact the campaign office.",
                )

        # ---------------------------------------------------------
        # DUPLICATE VIN APPLICATION
        # ---------------------------------------------------------

        if vin and programme:

            existing_application = (
                EmpowermentApplication.objects
                .filter(
                    programme=programme,
                    vin=vin,
                )
                .exclude(status="withdrawn")
                .exclude(pk=self.instance.pk)
                .first()
            )

            if existing_application:

                self.add_error(
                    "vin",
                    "An application using this Voters Identification "
                    "Number (VIN) has already been submitted for this "
                    "programme.",
                )

        # ---------------------------------------------------------
        # WARD MUST BELONG TO LGA
        # ---------------------------------------------------------

        if (
            local_government
            and ward
            and ward.local_government_id != local_government.id
        ):

            self.add_error(
                "ward",
                "The selected ward does not belong to the "
                "selected Local Government Area.",
            )

        # ---------------------------------------------------------
        # POLLING UNIT MUST BELONG TO WARD
        # ---------------------------------------------------------

        if (
            ward
            and polling_unit
            and polling_unit.ward_id != ward.id
        ):

            self.add_error(
                "polling_unit",
                "The selected polling unit does not belong "
                "to the selected ward.",
            )

        return cleaned_data