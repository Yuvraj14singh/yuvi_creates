document.addEventListener("DOMContentLoaded", function () {
    const solutionLinks = Array.from(document.querySelectorAll("[data-solution-link]"));
    const solutionGroups = Array.from(document.querySelectorAll("[data-solution-group]"));
    const marketButtons = Array.from(document.querySelectorAll("[data-market]"));
    const marketSelect = document.querySelector("[data-market-select]");
    const modal = document.querySelector("[data-scope-modal]");
    const modalPanel = modal && modal.querySelector(".scope-modal-panel");
    const modalBody = modal && modal.querySelector("[data-modal-body]");
    const validMarkets = ["IN", "US_INTL", "UK", "AU", "CA"];
    let activeMarket = "IN";
    let activeCurrency = "INR";
    let modalTrigger = null;

    try {
        const stored = window.localStorage.getItem("yuviPricingMarket");
        if (validMarkets.includes(stored)) activeMarket = stored;
    } catch (error) {}

    function currencyForMarket(market) {
        return { IN: "INR", US_INTL: "USD", UK: "GBP", AU: "AUD", CA: "CAD" }[market] || "INR";
    }

    function updateMarket(market) {
        if (!validMarkets.includes(market)) market = "IN";
        activeMarket = market;
        activeCurrency = currencyForMarket(market);
        marketButtons.forEach(function (button) {
            button.classList.toggle("is-active", button.dataset.market === market);
            button.setAttribute("aria-pressed", String(button.dataset.market === market));
        });
        if (marketSelect) marketSelect.value = market;
        document.querySelectorAll("[data-market-price]").forEach(function (price) {
            price.hidden = price.dataset.marketPrice !== market;
        });
        document.querySelectorAll(".quote-link").forEach(function (link) {
            link.href = link.dataset.quoteBase + "&market=" + encodeURIComponent(market) + "&currency=" + encodeURIComponent(activeCurrency);
        });
        try { window.localStorage.setItem("yuviPricingMarket", market); } catch (error) {}
    }

    marketButtons.forEach(function (button) {
        button.addEventListener("click", function () { updateMarket(button.dataset.market); });
    });
    if (marketSelect) marketSelect.addEventListener("change", function () { updateMarket(marketSelect.value); });

    function closeModal() {
        if (!modal || modal.hidden) return;
        modal.hidden = true;
        modalBody.replaceChildren();
        document.body.classList.remove("modal-open");
        if (modalTrigger) modalTrigger.focus();
        modalTrigger = null;
    }

    function openModal(button) {
        const template = document.getElementById(button.dataset.scopeTemplate);
        if (!template || !modal) return;
        modalTrigger = button;
        modalBody.replaceChildren(template.content.cloneNode(true));
        const heading = modalBody.querySelector("h2");
        if (heading) heading.id = "scope-modal-title";
        modal.hidden = false;
        document.body.classList.add("modal-open");
        updateMarket(activeMarket);
        modalPanel.focus();
    }

    document.querySelectorAll(".scope-toggle").forEach(function (button) {
        button.addEventListener("click", function () { openModal(button); });
    });
    document.querySelectorAll("[data-modal-close]").forEach(function (button) {
        button.addEventListener("click", closeModal);
    });
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") closeModal();
        if (event.key === "Tab" && modal && !modal.hidden) {
            const focusable = Array.from(modalPanel.querySelectorAll("a[href],button:not([disabled]),[tabindex]:not([tabindex='-1'])"));
            if (!focusable.length) return;
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
            else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
        }
    });

    solutionLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            solutionLinks.forEach(function (item) { item.classList.remove("is-active"); });
            link.classList.add("is-active");
        });
    });
    document.querySelectorAll(".show-more-packages").forEach(function (button) {
        button.addEventListener("click", function () {
            const grid = button.previousElementSibling;
            const expanded = button.getAttribute("aria-expanded") === "true";
            grid.classList.toggle("is-expanded", !expanded);
            button.setAttribute("aria-expanded", String(!expanded));
            button.textContent = expanded ? "View all solutions" : "Show fewer solutions";
        });
    });
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                solutionLinks.forEach(function (link) { link.classList.toggle("is-active", link.dataset.solutionLink === entry.target.id); });
            });
        }, { rootMargin: "-30% 0px -60%", threshold: 0 });
        solutionGroups.forEach(function (group) { observer.observe(group); });
    }
    updateMarket(activeMarket);
});
