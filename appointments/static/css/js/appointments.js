// Appointments Module JS
(function () {
  const state = {
    page: 1,
    pageSize: 10,
    status: "all",
    search: "",
    rows: []
  };

  const sampleRows = [
    { id: 101, patient: "Juan Dela Cruz", dentist: "Dr. Santos", date: "2025-10-16 09:00", status: "pending" },
    { id: 102, patient: "Maria Reyes", dentist: "Dr. Dizon", date: "2025-10-16 10:30", status: "confirmed" },
    { id: 103, patient: "Pedro Marcos", dentist: "Dr. Santos", date: "2025-10-16 13:00", status: "cancelled" },
    { id: 104, patient: "Ana Lim", dentist: "Dr. Garcia", date: "2025-10-17 11:00", status: "confirmed" },
    { id: 105, patient: "Liza Cruz", dentist: "Dr. Dizon", date: "2025-10-17 14:30", status: "pending" }
  ];

  function qs(sel, el = document) { return el.querySelector(sel); }
  function qsa(sel, el = document) { return Array.from(el.querySelectorAll(sel)); }

  function statusBadge(status) {
    const s = String(status || "").toLowerCase();
    return `<span class="appointment-status ${s}">
      ${s === "pending" ? "⏳" : s === "confirmed" ? "✅" : s === "cancelled" ? "❌" : "•"} ${capitalize(s)}
    </span>`;
  }

  function capitalize(s) {
    return s ? s.replace(/\b\w/g, (m) => m.toUpperCase()) : "";
  }

  async function fetchRows() {
    try {
      const params = new URLSearchParams({
        page: state.page,
        page_size: state.pageSize,
        status: state.status === "all" ? "" : state.status,
        q: state.search
      });
      const res = await fetch(`/api/appointments?${params.toString()}`);
      if (!res.ok) throw new Error("No API yet");
      const data = await res.json();
      state.rows = Array.isArray(data.items) ? data.items : [];
    } catch {
      state.rows = sampleRows.slice();
    }
    renderTable();
  }

  function renderTable() {
    const tbody = qs(".appointments-table tbody");
    if (!tbody) return;

    const filtered = state.rows.filter(row => {
      const matchStatus = state.status === "all" || String(row.status).toLowerCase() === state.status;
      const matchSearch = !state.search || JSON.stringify(row).toLowerCase().includes(state.search.toLowerCase());
      return matchStatus && matchSearch;
    });

    const start = (state.page - 1) * state.pageSize;
    const pageRows = filtered.slice(start, start + state.pageSize);

    tbody.innerHTML = pageRows.map(r => `
      <tr>
        <td>#${r.id}</td>
        <td>${r.patient}</td>
        <td>${r.dentist}</td>
        <td>${r.date}</td>
        <td>${statusBadge(r.status)}</td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-primary" data-action="view" data-id="${r.id}">View</button>
          <button class="btn btn-sm btn-outline-secondary" data-action="resched" data-id="${r.id}">Resched</button>
          <button class="btn btn-sm btn-outline-danger" data-action="cancel" data-id="${r.id}">Cancel</button>
        </td>
      </tr>
    `).join("");

    renderPagination(filtered.length);
  }

  function renderPagination(total) {
    const wrap = qs(".appointments-pagination");
    if (!wrap) return;
    const totalPages = Math.max(1, Math.ceil(total / state.pageSize));

    wrap.innerHTML = `
      <div class="d-flex align-items-center gap-2">
        <button class="btn btn-sm btn-outline-secondary" data-page="prev" ${state.page <= 1 ? "disabled" : ""}>Prev</button>
        <span class="small">Page ${state.page} / ${totalPages}</span>
        <button class="btn btn-sm btn-outline-secondary" data-page="next" ${state.page >= totalPages ? "disabled" : ""}>Next</button>
      </div>
    `;
  }

  function handleToolbar() {
    qsa(".filter-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        qsa(".filter-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        state.status = chip.dataset.status || "all";
        state.page = 1;
        fetchRows();
      });
    });

    const searchInput = qs("#appointmentsSearch");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        state.search = e.target.value.trim();
        state.page = 1;
        fetchRows();
      });
    }

    const pageWrap = qs(".appointments-pagination");
    if (pageWrap) {
      pageWrap.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-page]");
        if (!btn) return;
        if (btn.dataset.page === "prev" && state.page > 1) state.page--;
        if (btn.dataset.page === "next") state.page++;
        fetchRows();
      });
    }
  }

  function handleRowActions() {
    const table = qs(".appointments-table");
    if (!table) return;
    table.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-action]");
      if (!btn) return;
      const id = btn.dataset.id;
      const action = btn.dataset.action;
      if (action === "view") {
        console.log("View appointment", id);
      } else if (action === "resched") {
        console.log("Reschedule", id);
      } else if (action === "cancel") {
        if (confirm("Cancel this appointment?")) {
          console.log("Cancelled", id);
        }
      }
    });
  }

  function handleSidebarBehavior() {
    const dropdown = qs("#appointments-dropdown");
    if (!dropdown) return;

    dropdown.addEventListener("click", () => {
      const sidebar = qs(".sidebar");
      if (sidebar && !sidebar.classList.contains("expanded")) {
        sidebar.classList.add("expanded"); // ✅ Expand sidebar if collapsed
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    handleToolbar();
    handleRowActions();
    handleSidebarBehavior(); // ✅ new behavior
    fetchRows();
  });
})();
