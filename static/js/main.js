/* =========================================================
   UDUAK-ABASI 2027
   MAIN JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       MOBILE NAVIGATION
    ===================================================== */

    const menuButton = document.getElementById("mobile-menu-button");
    const mobileMenu = document.getElementById("mobile-menu");

    if (menuButton && mobileMenu) {

        menuButton.addEventListener("click", () => {

            const isOpen =
                !mobileMenu.classList.contains("hidden");

            mobileMenu.classList.toggle("hidden");

            menuButton.setAttribute(
                "aria-expanded",
                String(!isOpen)
            );
        });

    }


    /* =====================================================
       CLOSE MOBILE MENU WHEN LINK IS CLICKED
    ===================================================== */

    const mobileLinks =
        document.querySelectorAll("#mobile-menu a");

    mobileLinks.forEach((link) => {

        link.addEventListener("click", () => {

            if (mobileMenu) {
                mobileMenu.classList.add("hidden");
            }

            if (menuButton) {
                menuButton.setAttribute(
                    "aria-expanded",
                    "false"
                );
            }

        });

    });


    /* =====================================================
       CURRENT YEAR
    ===================================================== */

    const yearElement =
        document.getElementById("current-year");

    if (yearElement) {
        yearElement.textContent =
            new Date().getFullYear();
    }


    /* =====================================================
       HEADER SHADOW ON SCROLL
    ===================================================== */

    const header =
        document.getElementById("site-header");

    if (header) {

        window.addEventListener("scroll", () => {

            if (window.scrollY > 20) {

                header.classList.add(
                    "shadow-lg"
                );

            } else {

                header.classList.remove(
                    "shadow-lg"
                );

            }

        });

    }

});