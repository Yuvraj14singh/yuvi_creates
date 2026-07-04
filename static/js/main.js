const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");

if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
        const isOpen = navLinks.classList.toggle("open");
        navToggle.setAttribute("aria-expanded", String(isOpen));
    });
}

document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
        const target = document.querySelector(link.getAttribute("href"));
        if (target) {
            event.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    });
});

document.querySelectorAll(".faq-item button").forEach((button) => {
    button.addEventListener("click", () => {
        button.closest(".faq-item").classList.toggle("open");
    });
});

document.querySelectorAll(".payment-card input").forEach((input) => {
    const updateCards = () => {
        document.querySelectorAll(".payment-card").forEach((card) => {
            card.classList.toggle("selected", Boolean(card.querySelector("input:checked")));
        });
    };
    input.addEventListener("change", updateCards);
    updateCards();
});

const revealObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                revealObserver.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.12 }
);

document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));
