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

const tiltCard = document.querySelector("[data-tilt]");
if (tiltCard && window.matchMedia("(pointer: fine)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    tiltCard.addEventListener("pointermove", (event) => {
        const rect = tiltCard.getBoundingClientRect();
        const rotateY = ((event.clientX - rect.left) / rect.width - 0.5) * 8;
        const rotateX = (0.5 - (event.clientY - rect.top) / rect.height) * 6;
        tiltCard.style.transform = `perspective(1100px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });
    tiltCard.addEventListener("pointerleave", () => {
        tiltCard.style.transform = "perspective(1100px) rotateY(-4deg) rotateX(2deg)";
    });
}

const canTilt = window.matchMedia("(pointer: fine)").matches && !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (canTilt) {
    document.querySelectorAll(".service-card, .price-card, .portfolio-card, .industry-card").forEach((card) => {
        card.addEventListener("pointermove", (event) => {
            const rect = card.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width;
            const y = (event.clientY - rect.top) / rect.height;
            card.style.setProperty("--ry", `${(x - 0.5) * 5}deg`);
            card.style.setProperty("--rx", `${(0.5 - y) * 4}deg`);
            card.style.setProperty("--mx", `${x * 100}%`);
            card.style.setProperty("--my", `${y * 100}%`);
        });
        card.addEventListener("pointerleave", () => {
            card.style.removeProperty("--ry");
            card.style.removeProperty("--rx");
            card.style.removeProperty("--mx");
            card.style.removeProperty("--my");
        });
    });
}
