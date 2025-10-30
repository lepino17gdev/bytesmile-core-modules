console.log("Access Matrix module JS loaded.");
// Access Matrix Page Logic
(function () {
  const state = {
    page: 1,
    pageSize: 10,
    subject: "all", // all | role | user
    module: "",
    permission: "all",
    search: "",
    rows: []
  };

  function qs(sel, el = document) { return el.querySelector(sel); }
  function qsa(sel, el = document) { return Array.from(el.querySelectorAll(sel)); }

  function nice(s) { return (s || "").toString(); }
  function cap(s) { return nice(s).replace(/\b\w/g, m => m.toUpperCase()); }

  function pill(text, type) {
    const t = (type || "secondary");
    return `<span class="badge text-bg-${t}">${text}</span>`;
  }

  function subjectLabel(row) {
    if (row.subject_type === "role") {
      return `<i class="bi bi-people me-1"></i>${cap(row.role_name || "role " + row.role_id)}`;
    }
    return `<i class="bi bi-person me-1"></i>${row.user_email || ("user " + row.user_id)}`;
  }

  function permissionBadge(p) {
    const map = { view: "secondary", create: "info", edit: "warning", delete: "danger", manage: "primary" };
    return pill(p, map[p] || "secondary");
  }

  async function fetchRows() {
    // Try API, fallback to sample
    try {
      const params = new URLSearchParams({
        page: state.page, page_size: state.pageSize,
        subject: state.subject === "all" ? "" : state.subject,
        module: state.module || "",
        permission: state.permission === "all" ? "" : state.permission,
        q: state.search || ""
      });
      const res = await fetch(`/api/access-matrix/list?${params.toString()}`);
      if (!res.ok) throw new Error("No API yet");
      const data = await res.json();
      state.rows = Array.isArray(data.items) ? data.items : data || [];
    } catch (e) {
      // Fallback sample rows
      state.rows = [
        { id: 1, subject_type: "role", role_id: 2, role_name: "manager", module: "invites", permission: "manage" },
        { id: 2, subject_type: "user", user_id: 5, user_email: "dentist@example.com", module: "appointments", permission: "edit" },
        { id: 3, subject_type: "role", role_id: 3, role_name: "staff", module: "appointments", permission: "view" }
      ];
    }
    render();
  }

  function applyFilters(rows) {
    return rows.filter(r => {
      const subjectOk = (state.subject === "all") || (r.subject_type === state.subject);
      const moduleOk = !state.module || nice(r.module).toLowerCase().includes(state.module.toLowerCase());
      const permOk = (state.permission === "all") || (r.permission === state.permission);
      const hay = JSON.stringify(r).toLowerCase();
      const qOk = !state.search || hay.includes(state.search.toLowerCase());
      return subjectOk && moduleOk && permOk && qOk;
    });
  }

  function render() {
    const tbody = qs("#accessRows");
    if (!tbody) return;

    const filtered = applyFilters(state.rows);
    const start = (state.page - 1) * state.pageSize;
    const pageRows = filtered.slice(start, start + state.pageSize);

    tbody.innerHTML = pageRows.map(r => `
      <tr>
        <td>${subjectLabel(r)}</td>
        <td>${pill(cap(r.subject_type), r.subject_type === "role" ? "dark" : "secondary")}</td>
        <td><code>${r.module}</code></td>
        <td>${permissionBadge(r.permission)}</td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-danger" data-action="revoke" data-id="${r.id}">
            <i class="bi bi-x-circle me-1"></i> Revoke
          </button>
        </td>
      </tr>
    `).join("");

    const totalPages = Math.max(1, Math.ceil(filtered.length / state.pageSize));
    qs("#accessCount").textContent = `${filtered.length} item${filtered.length === 1 ? "" : "s"}`;
    qs("#pageInfo").textContent = `Page ${state.page} / ${totalPages}`;
    qs("#prevPage").disabled = state.page <= 1;
    qs("#nextPage").disabled = state.page >= totalPages;
  }

  function wireToolbar() {
    qs("#filterSubject").addEventListener("change", (e) => { state.subject = e.target.value; state.page = 1; fetchRows(); });
    qs("#filterModule").addEventListener("input", (e) => { state.module = e.target.value.trim(); state.page = 1; fetchRows(); });
    qs("#filterPermission").addEventListener("change", (e) => { state.permission = e.target.value; state.page = 1; fetchRows(); });
    qs("#filterSearch").addEventListener("input", (e) => { state.search = e.target.value.trim(); state.page = 1; fetchRows(); });

    qs("#prevPage").addEventListener("click", () => { if (state.page > 1) { state.page--; fetchRows(); } });
    qs("#nextPage").addEventListener("click", () => { state.page++; fetchRows(); });
  }

  function wireTableActions() {
    qs("#accessRows").addEventListener("click", async (e) => {
      const btn = e.target.closest("button[data-action]");
      if (!btn) return;
      if (btn.dataset.action === "revoke") {
        const id = btn.dataset.id;
        if (!id) return;
        if (!confirm("Revoke this permission?")) return;
        try {
          const res = await fetch("/api/access-matrix/revoke", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: Number(id) })
          });
          if (!res.ok) throw new Error("Failed to revoke");
          // remove locally
          state.rows = state.rows.filter(r => String(r.id) !== String(id));
          render();
        } catch (err) {
          alert("Failed to revoke permission.");
        }
      }
    });
  }

  function wireGrantForm() {
    const form = qs("#grantForm");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        subject_type: qs("#subjectType").value, // "role" | "user"
        subject_value: qs("#subjectValue").value.trim(), // role name OR user email
        module: qs("#moduleSlug").value.trim(),
        permission: qs("#permission").value
      };
      if (!payload.subject_value || !payload.module) {
        alert("Please fill the required fields.");
        return;
      }
      try {
        const res = await fetch("/api/access-matrix/grant", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error("Failed to grant");
        // refresh list
        await fetchRows();
        // close modal (if bootstrap available)
        const modalEl = document.getElementById("grantModal");
        if (window.bootstrap && bootstrap.Modal.getInstance(modalEl)) {
          bootstrap.Modal.getInstance(modalEl).hide();
        } else {
          // fallback: hide manually
          modalEl.classList.remove("show");
          modalEl.style.display = "none";
          document.body.classList.remove("modal-open");
          document.querySelector(".modal-backdrop")?.remove();
        }
        form.reset();
      } catch (err) {
        alert("Failed to grant permission.");
      }
    });
  }

  // Expand sidebar automatically when clicking the Access Matrix group from a collapsed sidebar
  document.addEventListener("click", (e) => {
    const trigger = e.target.closest("#access-matrix-dropdown");
    if (!trigger) return;
    const sidebar = document.querySelector(".sidebar");
    const toggleBtn = document.getElementById("toggleSidebar");
    if (sidebar && !sidebar.classList.contains("expanded") && toggleBtn) {
      toggleBtn.click();
    }
  });

  document.addEventListener("DOMContentLoaded", () => {
    wireToolbar();
    wireTableActions();
    wireGrantForm();
    fetchRows();
  });
})();
