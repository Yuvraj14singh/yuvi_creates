document.addEventListener("DOMContentLoaded", function () {
    const currency = document.querySelector("[data-currency-select]");
    const budget = document.querySelector("[data-budget-select]");
    if (!currency || !budget) return;
    const options = {
        INR: ["Under ₹25,000", "₹25,000 – ₹50,000", "₹50,000 – ₹1,00,000", "₹1,00,000 – ₹2,00,000", "₹2,00,000+", "Not sure yet"],
        USD: ["Under $750", "$750 – $1,500", "$1,500 – $3,000", "$3,000 – $5,000", "$5,000+", "Not sure yet"],
        GBP: ["Under £600", "£600 – £1,200", "£1,200 – £2,500", "£2,500 – £4,000", "£4,000+", "Not sure yet"],
        AUD: ["Under A$1,000", "A$1,000 – A$2,000", "A$2,000 – A$4,000", "A$4,000 – A$7,000", "A$7,000+", "Not sure yet"],
        CAD: ["Under C$900", "C$900 – C$1,800", "C$1,800 – C$3,500", "C$3,500 – C$6,000", "C$6,000+", "Not sure yet"],
        Other: ["Entry-level project", "Standard business project", "Premium business project", "Advanced/custom system", "Not sure yet"]
    };
    function updateBudgets() {
        const selected = budget.value;
        budget.replaceChildren(new Option("Select an optional budget range", ""));
        (options[currency.value] || options.Other).forEach(function (label) { budget.add(new Option(label, label)); });
        if (Array.from(budget.options).some(function (option) { return option.value === selected; })) budget.value = selected;
    }
    currency.addEventListener("change", updateBudgets);
    updateBudgets();
});
