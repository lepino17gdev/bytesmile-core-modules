// Expand sidebar on Sample dropdown click
document.addEventListener("click", function(e) {
  if (e.target.closest("#sample-dropdown")) {
    const sidebar = document.querySelector(".sidebar");
    if (sidebar && !sidebar.classList.contains("expanded")) {
      document.querySelector("#toggleSidebar")?.click();
    }
  }
});