// Expand sidebar on Invites dropdown click
document.addEventListener("click", function(e) {
  if (e.target.closest("#staff_invites-dropdown")) {
    const sidebar = document.querySelector(".sidebar");
    if (sidebar && !sidebar.classList.contains("expanded")) {
      document.querySelector("#toggleSidebar")?.click();
    }
  }
});