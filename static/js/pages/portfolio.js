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
    let level = "all";
    const levelFilters = Array.from(document.querySelectorAll("[data-level-filter]"));
    function normalize(value) { return (value || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim().replace(/\s+/g, " "); }
    function apply() {
        const words = normalize(input && input.value).split(" ").filter(Boolean);
        let visible = 0;
        cards.forEach(function (card) {
            const categoryMatch = category === "all" || card.dataset.category === category;
            const levelMatch = level === "all" || card.dataset.level === level;
            const haystack = normalize(card.dataset.search + " " + card.textContent);
            const textMatch = words.every(function (word) { return haystack.includes(word); });
            card.hidden = !(categoryMatch && levelMatch && textMatch);
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
    levelFilters.forEach(function (button) { button.addEventListener("click", function () {
        level = button.dataset.levelFilter;
        levelFilters.forEach(function (item) { const active = item === button; item.classList.toggle("is-active", active); item.setAttribute("aria-pressed", String(active)); });
        apply();
    }); });
    if (searchForm) searchForm.addEventListener("submit", function (event) { event.preventDefault(); apply(); });
    if (reset) reset.addEventListener("click", function () { input.value = ""; category = "all"; level = "all"; filters.forEach(function (item) { const active = item.dataset.demoFilter === "all"; item.classList.toggle("is-active", active); item.setAttribute("aria-pressed", String(active)); }); levelFilters.forEach(function(item){const active=item.dataset.levelFilter==="all";item.classList.toggle("is-active",active);item.setAttribute("aria-pressed",String(active));}); apply(); input.focus(); });
    apply();
})();
