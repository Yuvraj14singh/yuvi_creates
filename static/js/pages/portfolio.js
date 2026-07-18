(function () {
    "use strict";
    let market = "IN";
    try { market = localStorage.getItem("yuviPricingMarket") || "IN"; } catch (error) {}
    if (!["IN", "US_INTL", "UK", "AU", "CA"].includes(market)) market = "IN";
    document.querySelectorAll("[data-package-base]").forEach(function (link) {
        link.href = link.dataset.packageBase + "?market=" + encodeURIComponent(market);
    });
    const input = document.getElementById("demo-search-input");
    const searchForm = document.querySelector("[data-demo-search-form]");
    const cards = Array.from(document.querySelectorAll("[data-demo-card]"));
    const filters = Array.from(document.querySelectorAll("[data-demo-filter]"));
    const count = document.querySelector("[data-demo-count]");
    const empty = document.querySelector("[data-demo-empty]");
    const reset = document.querySelector("[data-demo-reset]");
    let category = "all";
    function normalize(value) { return (value || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim().replace(/\s+/g, " "); }
    function apply() {
        const words = normalize(input && input.value).split(" ").filter(Boolean);
        let visible = 0;
        cards.forEach(function (card) {
            const categoryMatch = category === "all" || card.dataset.category === category;
            const haystack = normalize(card.dataset.search + " " + card.textContent);
            const textMatch = words.every(function (word) { return haystack.includes(word); });
            card.hidden = !(categoryMatch && textMatch);
            if (!card.hidden) visible += 1;
        });
        if (count) count.textContent = visible + (visible === 1 ? " demo found" : " demos found");
        if (empty) empty.hidden = visible !== 0;
    }
    try { const initial = new URLSearchParams(window.location.search).get("search"); if (input && initial) input.value = initial; } catch (error) {}
    filters.forEach(function (button) { button.addEventListener("click", function () {
        category = button.dataset.demoFilter;
        filters.forEach(function (item) { const active = item === button; item.classList.toggle("is-active", active); item.setAttribute("aria-pressed", String(active)); });
        apply();
    }); });
    if (searchForm) searchForm.addEventListener("submit", function (event) { event.preventDefault(); apply(); });
    if (reset) reset.addEventListener("click", function () { input.value = ""; category = "all"; filters.forEach(function (item) { const active = item.dataset.demoFilter === "all"; item.classList.toggle("is-active", active); item.setAttribute("aria-pressed", String(active)); }); apply(); input.focus(); });
    apply();
})();
