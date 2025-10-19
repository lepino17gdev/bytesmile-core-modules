  (function () {
  function qs(sel, el = document) { return el.querySelector(sel); }
  function qsa(sel, el = document) { return Array.from(el.querySelectorAll(sel)); }
  
  function handleSidebarBehavior() {
    const dropdown = qs("#appointments-dropdown");
    if (!dropdown) return;

    dropdown.addEventListener("click", () => {
      const sidebar = qs(".sidebar");
      console.log(sidebar);
      if (sidebar && !sidebar.classList.contains("expanded")) {
        document.getElementById('toggleSidebar').click(); // ✅ Expand sidebar if collapsed
      }
    });
  }

    document.addEventListener("DOMContentLoaded", () => {

        handleSidebarBehavior();
    });
  })();