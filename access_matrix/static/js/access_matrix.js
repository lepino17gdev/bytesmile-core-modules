async function loadAccess() {
  const res = await fetch("/api/access_matrix/");
  const data = await res.json();
  const tbody = document.querySelector("#accessTable tbody");
  tbody.innerHTML = "";

  data.forEach(row => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.id}</td>
      <td>${row.role_id ?? "-"}</td>
      <td>${row.user_id ?? "-"}</td>
      <td>${row.module}</td>
      <td>${row.permission}</td>
      <td>
        <button class="btn btn-danger btn-sm" onclick="deleteAccess(${row.id})">🗑️ Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function addAccess() {
  const payload = {
    role_id: parseInt(document.getElementById("role_id").value),
    user_id: parseInt(document.getElementById("user_id").value) || null,
    module: document.getElementById("module").value,
    permission: document.getElementById("permission").value,
  };

  const res = await fetch("/api/access_matrix/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (res.ok) {
    alert("✅ Access rule added.");
    loadAccess();
  } else {
    const err = await res.json();
    alert("❌ Error: " + err.detail);
  }
}

async function deleteAccess(id) {
  if (!confirm("Delete this access rule?")) return;

  const res = await fetch(`/api/access_matrix/${id}`, { method: "DELETE" });
  if (res.ok) {
    alert("🗑️ Deleted successfully.");
    loadAccess();
  } else {
    alert("❌ Failed to delete.");
  }
}

// Auto-load table on page load
document.addEventListener("DOMContentLoaded", loadAccess);
