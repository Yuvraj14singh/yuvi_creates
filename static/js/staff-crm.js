const sidebar = document.querySelector("#staff-sidebar");
document.querySelectorAll("[data-sidebar-open]").forEach((button) => button.addEventListener("click", () => document.body.classList.add("sidebar-open")));
document.querySelectorAll("[data-sidebar-close]").forEach((button) => button.addEventListener("click", () => document.body.classList.remove("sidebar-open")));
document.querySelectorAll("form[data-confirm]").forEach((form) => form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
}));
document.querySelectorAll(".staff-message").forEach((message) => window.setTimeout(() => message.classList.add("fade"), 5000));
