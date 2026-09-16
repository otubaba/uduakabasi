document.addEventListener("DOMContentLoaded", function () {

    const formContainer =
        document.getElementById("constituency-form");

    const lga =
        document.getElementById("id_local_government");

    const ward =
        document.getElementById("id_ward");

    const pu =
        document.getElementById("id_polling_unit");


    /* ==========================================
       CHECK REQUIRED ELEMENTS
       ========================================== */

    if (
        !formContainer ||
        !lga ||
        !ward ||
        !pu
    ) {
        console.warn(
            "Constituency form elements were not found."
        );

        return;
    }


    /* ==========================================
       AJAX URLS
       ========================================== */

    const wardsUrl =
        formContainer.dataset.wardsUrl;

    const pollingUnitsUrl =
        formContainer.dataset.pollingUnitsUrl;


    if (!wardsUrl || !pollingUnitsUrl) {

        console.error(
            "Constituency AJAX URLs are missing."
        );

        return;
    }


    /* ==========================================
       HELPERS
       ========================================== */

    function resetWard() {

        ward.innerHTML =
            '<option value="">Select Ward</option>';

        ward.disabled = true;
    }


    function resetPollingUnit() {

        pu.innerHTML =
            '<option value="">Select Polling Unit</option>';

        pu.disabled = true;
    }


    /* ==========================================
       INITIAL STATE
       ========================================== */

    ward.disabled = true;
    pu.disabled = true;


    /* ==========================================
       LGA → WARD
       ========================================== */

    lga.addEventListener(
        "change",
        function () {

            const lgaId = this.value;


            resetWard();

            resetPollingUnit();


            if (!lgaId) {
                return;
            }


            const url =
                `${wardsUrl}?lga=${encodeURIComponent(lgaId)}`;


            fetch(url)

                .then(response => {

                    if (!response.ok) {

                        throw new Error(
                            "Failed to load wards."
                        );
                    }

                    return response.json();
                })

                .then(data => {

                    if (
                        !data.wards ||
                        data.wards.length === 0
                    ) {

                        ward.innerHTML =
                            '<option value="">No wards available</option>';

                        return;
                    }


                    ward.innerHTML =
                        '<option value="">Select Ward</option>';


                    data.wards.forEach(item => {

                        const option =
                            document.createElement(
                                "option"
                            );

                        option.value =
                            item.id;

                        option.textContent =
                            `${item.code} — ${item.name}`;

                        ward.appendChild(
                            option
                        );
                    });


                    ward.disabled = false;
                })

                .catch(error => {

                    console.error(
                        "Ward loading error:",
                        error
                    );

                    ward.innerHTML =
                        '<option value="">Unable to load wards</option>';

                });
        }
    );


    /* ==========================================
       WARD → POLLING UNIT
       ========================================== */

    ward.addEventListener(
        "change",
        function () {

            const wardId = this.value;


            resetPollingUnit();


            if (!wardId) {
                return;
            }


            const url =
                `${pollingUnitsUrl}?ward=${encodeURIComponent(wardId)}`;


            fetch(url)

                .then(response => {

                    if (!response.ok) {

                        throw new Error(
                            "Failed to load polling units."
                        );
                    }

                    return response.json();
                })

                .then(data => {

                    if (
                        !data.polling_units ||
                        data.polling_units.length === 0
                    ) {

                        pu.innerHTML =
                            '<option value="">No polling units available</option>';

                        return;
                    }


                    pu.innerHTML =
                        '<option value="">Select Polling Unit</option>';


                    data.polling_units.forEach(item => {

                        const option =
                            document.createElement(
                                "option"
                            );

                        option.value =
                            item.id;

                        option.textContent =
                            item.label;

                        pu.appendChild(
                            option
                        );
                    });


                    pu.disabled = false;
                })

                .catch(error => {

                    console.error(
                        "Polling unit loading error:",
                        error
                    );

                    pu.innerHTML =
                        '<option value="">Unable to load polling units</option>';

                });
        }
    );

});