$(".sidebar").on("click", "#appointments-dropdown", function () { 
  const sidebar = $(".sidebar");
  console.log(sidebar);
  if (sidebar.length && !sidebar.hasClass("expanded")) {
    console.log("Expanding sidebar")
    $("#toggleSidebar").click(); // Expand sidebar if collapsed
  }
})