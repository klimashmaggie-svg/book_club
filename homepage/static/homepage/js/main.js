document.addEventListener("DOMContentLoaded", () => {
  const year = document.querySelector("#current-year");
  if (year) {
    year.textContent = new Date().getFullYear();
  }

  const currentPath = window.location.pathname;
  const links = [...document.querySelectorAll(".nav-link")];
  const activeLink = links
    .filter((link) => {
      const linkPath = new URL(link.href).pathname;
      return linkPath === "/"
        ? currentPath === "/"
        : currentPath.startsWith(linkPath);
    })
    .sort((first, second) => second.pathname.length - first.pathname.length)[0];

  if (activeLink) {
    activeLink.classList.add("active");
    activeLink.setAttribute("aria-current", "page");
  }
});
