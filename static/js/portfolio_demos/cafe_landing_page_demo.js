document.documentElement.dataset.portfolioDemo = "cafe";

document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector(".cafe-nav");
    const toggle = document.querySelector(".cafe-menu-toggle");
    toggle?.addEventListener("click", () => {
        const open = nav.classList.toggle("menu-open");
        toggle.setAttribute("aria-expanded", String(open));
    });
    document.querySelectorAll(".cafe-links a").forEach((link) => link.addEventListener("click", () => {
        nav?.classList.remove("menu-open");
        toggle?.setAttribute("aria-expanded", "false");
    }));

    const tabs = document.querySelectorAll("[data-menu-tab]");
    tabs.forEach((tab) => tab.addEventListener("click", () => {
        tabs.forEach((item) => item.classList.remove("active"));
        document.querySelectorAll("[data-menu-panel]").forEach((panel) => panel.classList.remove("active"));
        tab.classList.add("active");
        document.querySelector(`[data-menu-panel="${tab.dataset.menuTab}"]`)?.classList.add("active");
    }));

    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
        }
    }), { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach((item) => observer.observe(item));
});
