// Vanilla-JS form for building a presentation's input JSON.
//
// Re-renders a whole section (top fields / one page card) on structural
// changes (add/remove/reorder) but never on plain typing — text inputs
// update `state` in place via event delegation so the cursor/focus never
// jumps mid-edit.

const state = INITIAL_DATA ? JSON.parse(JSON.stringify(INITIAL_DATA)) : {
  project_id: "",
  location_name: "",
  city: "",
  language: "de",
  theme_worlds: [""],
  pages: [],
};
if (!state.theme_worlds || state.theme_worlds.length === 0) state.theme_worlds = [""];
if (!state.pages) state.pages = [];
// Every page always has a `fields` object, even if empty, so lookups below
// never need an extra guard.
state.pages.forEach(p => { if (!p.fields) p.fields = {}; });

const topFieldsEl = document.getElementById("top-fields");
const pagesEl = document.getElementById("pages");
const messagesEl = document.getElementById("messages");
const jsonPreviewEl = document.getElementById("json-preview");

function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function buildPayload() {
  return {
    project_id: state.project_id.trim(),
    location_name: state.location_name.trim(),
    city: state.city.trim(),
    language: state.language,
    theme_worlds: state.theme_worlds.map(t => t.trim()).filter(Boolean),
    pages: state.pages.map(p => {
      const fields = {};
      for (const [k, v] of Object.entries(p.fields)) {
        if (v && String(v).trim()) fields[k] = String(v).trim();
      }
      return { page_type: p.page_type, fields };
    }),
  };
}

function updateJsonPreview() {
  jsonPreviewEl.textContent = JSON.stringify(buildPayload(), null, 2);
}

function showMessage(text, isError) {
  messagesEl.innerHTML = `<div class="${isError ? "error" : "success"}">${escapeHtml(text)}</div>`;
}

// ---------- Top-level fields ----------

function renderTopFields() {
  const themeWorldsHtml = state.theme_worlds.map((t, i) => `
    <div class="list-row">
      <input type="text" maxlength="25" value="${escapeHtml(t)}" data-theme-index="${i}" placeholder="Theme world name">
      <button type="button" class="button small" data-theme-remove="${i}">Remove</button>
    </div>
  `).join("");

  topFieldsEl.innerHTML = `
    <div class="field-grid">
      <label>project_id
        <input type="text" data-top="project_id" value="${escapeHtml(state.project_id)}" placeholder="e.g. basel_2026">
      </label>
      <label>location_name
        <input type="text" data-top="location_name" value="${escapeHtml(state.location_name)}" placeholder="e.g. Basler Weihnachtsmarkt">
      </label>
      <label>city
        <input type="text" data-top="city" value="${escapeHtml(state.city)}" placeholder="e.g. Basel">
      </label>
      <label>language
        <select data-top="language">
          <option value="de" ${state.language === "de" ? "selected" : ""}>de</option>
        </select>
      </label>
    </div>
    <h3>Theme worlds</h3>
    <div id="theme-worlds-list">${themeWorldsHtml}</div>
    <button type="button" class="button small" id="add-theme-btn">+ Add theme world</button>
  `;
  updateJsonPreview();
}

topFieldsEl.addEventListener("input", (e) => {
  const top = e.target.dataset.top;
  if (top) { state[top] = e.target.value; updateJsonPreview(); return; }
  const themeIndex = e.target.dataset.themeIndex;
  if (themeIndex !== undefined) { state.theme_worlds[themeIndex] = e.target.value; updateJsonPreview(); }
});

topFieldsEl.addEventListener("click", (e) => {
  if (e.target.id === "add-theme-btn") {
    state.theme_worlds.push("");
    renderTopFields();
  } else if (e.target.dataset.themeRemove !== undefined) {
    const i = Number(e.target.dataset.themeRemove);
    state.theme_worlds.splice(i, 1);
    if (state.theme_worlds.length === 0) state.theme_worlds.push("");
    renderTopFields();
  }
});

// ---------- Pages ----------

function fieldRowHtml(pageIndex, field, value) {
  const label = `${field.name}${field.required ? " *" : ""}`;
  if (field.kind === "image") {
    const previewSrc = value ? `/image-preview/${value}` : "";
    return `
      <div class="field-row image-field">
        <label>${escapeHtml(label)}</label>
        <input type="text" class="path-input" data-page-index="${pageIndex}" data-field-name="${field.name}"
               value="${escapeHtml(value)}" placeholder="images/... (or upload below)">
        <input type="file" accept=".jpg,.jpeg,.png" data-upload-page-index="${pageIndex}" data-upload-field-name="${field.name}">
        <img class="thumb" src="${previewSrc}" style="${value ? "" : "display:none"}" data-thumb-for="${pageIndex}:${field.name}">
      </div>
    `;
  }
  const maxLen = field.max_length ? ` maxlength="${field.max_length}"` : "";
  const counter = field.max_length ? `<span class="char-count" data-count-for="${pageIndex}:${field.name}">${(value || "").length}/${field.max_length}</span>` : "";
  return `
    <div class="field-row">
      <label>${escapeHtml(label)}</label>
      <input type="text" data-page-index="${pageIndex}" data-field-name="${field.name}" value="${escapeHtml(value)}"${maxLen}>
      ${counter}
    </div>
  `;
}

function pageCardHtml(page, index) {
  const fieldsDef = FIELD_CATALOGUE[page.page_type] || [];
  const fieldsHtml = fieldsDef.length
    ? fieldsDef.map(f => fieldRowHtml(index, f, page.fields[f.name] || "")).join("")
    : `<p class="muted">No fields — this page's content is fixed/computed by the generator.</p>`;

  return `
    <div class="page-card">
      <div class="page-card-header">
        <strong>${index + 1}. ${page.page_type}</strong>
        <div class="page-card-controls">
          <button type="button" class="button small" data-page-move-up="${index}">&uarr;</button>
          <button type="button" class="button small" data-page-move-down="${index}">&darr;</button>
          <button type="button" class="button small danger" data-page-remove="${index}">Remove</button>
        </div>
      </div>
      ${fieldsHtml}
    </div>
  `;
}

function renderPages() {
  pagesEl.innerHTML = state.pages.map(pageCardHtml).join("") || `<p class="muted">No slides yet — add one below.</p>`;
  updateJsonPreview();
}

pagesEl.addEventListener("input", (e) => {
  const pageIndex = e.target.dataset.pageIndex;
  const fieldName = e.target.dataset.fieldName;
  if (pageIndex === undefined || !fieldName) return;
  state.pages[pageIndex].fields[fieldName] = e.target.value;

  const counter = pagesEl.querySelector(`[data-count-for="${pageIndex}:${fieldName}"]`);
  if (counter) counter.textContent = `${e.target.value.length}/${e.target.maxLength}`;

  if (e.target.classList.contains("path-input")) {
    const thumb = pagesEl.querySelector(`[data-thumb-for="${pageIndex}:${fieldName}"]`);
    if (thumb) {
      if (e.target.value.trim()) {
        thumb.src = `/image-preview/${e.target.value.trim()}`;
        thumb.style.display = "";
      } else {
        thumb.style.display = "none";
      }
    }
  }
  updateJsonPreview();
});

pagesEl.addEventListener("change", async (e) => {
  const pageIndex = e.target.dataset.uploadPageIndex;
  const fieldName = e.target.dataset.uploadFieldName;
  if (pageIndex === undefined || !fieldName) return;
  const file = e.target.files[0];
  if (!file) return;
  if (!state.project_id.trim()) {
    showMessage("Set project_id at the top before uploading images.", true);
    e.target.value = "";
    return;
  }

  const form = new FormData();
  form.append("project_id", state.project_id.trim());
  form.append("field_name", fieldName);
  form.append("file", file);

  const resp = await fetch("/api/upload-image", { method: "POST", body: form });
  const result = await resp.json();
  if (!resp.ok) {
    showMessage(result.error || "Upload failed.", true);
    return;
  }
  state.pages[pageIndex].fields[fieldName] = result.path;
  const pathInput = pagesEl.querySelector(`input.path-input[data-page-index="${pageIndex}"][data-field-name="${fieldName}"]`);
  if (pathInput) pathInput.value = result.path;
  const thumb = pagesEl.querySelector(`[data-thumb-for="${pageIndex}:${fieldName}"]`);
  if (thumb) { thumb.src = `/image-preview/${result.path}`; thumb.style.display = ""; }
  updateJsonPreview();
});

pagesEl.addEventListener("click", (e) => {
  if (e.target.dataset.pageRemove !== undefined) {
    state.pages.splice(Number(e.target.dataset.pageRemove), 1);
    renderPages();
  } else if (e.target.dataset.pageMoveUp !== undefined) {
    const i = Number(e.target.dataset.pageMoveUp);
    if (i > 0) [state.pages[i - 1], state.pages[i]] = [state.pages[i], state.pages[i - 1]];
    renderPages();
  } else if (e.target.dataset.pageMoveDown !== undefined) {
    const i = Number(e.target.dataset.pageMoveDown);
    if (i < state.pages.length - 1) [state.pages[i + 1], state.pages[i]] = [state.pages[i], state.pages[i + 1]];
    renderPages();
  }
});

// ---------- Add page / template select ----------

const addPageTypeSelect = document.getElementById("add-page-type");
addPageTypeSelect.innerHTML = PAGE_TYPES.map(pt => `<option value="${pt}">${pt}</option>`).join("");

document.getElementById("add-page-btn").addEventListener("click", () => {
  state.pages.push({ page_type: addPageTypeSelect.value, fields: {} });
  renderPages();
});

const templateSelect = document.getElementById("template-select");
templateSelect.innerHTML = AVAILABLE_TEMPLATES.map(t => `<option value="${escapeHtml(t)}">${escapeHtml(t)}</option>`).join("");

// ---------- Save / Generate ----------

function fieldErrorsToText(errors) {
  return errors.map(e => `${e.path}: ${e.message}`).join("\n");
}

document.getElementById("save-btn").addEventListener("click", async () => {
  const payload = buildPayload();
  const resp = await fetch("/api/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await resp.json();
  if (!resp.ok) {
    showMessage("Validation errors:\n" + fieldErrorsToText(result.errors || []), true);
    return;
  }
  showMessage(`Saved to data/${result.saved_to}`, false);
});

document.getElementById("generate-btn").addEventListener("click", async () => {
  const payload = buildPayload();
  showMessage("Generating…", false);
  const resp = await fetch("/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ data: payload, template: templateSelect.value }),
  });
  const result = await resp.json();
  if (result.errors) {
    showMessage("Validation errors:\n" + fieldErrorsToText(result.errors), true);
    return;
  }
  if (!result.ok) {
    showMessage("Generation failed:\n" + (result.log || ""), true);
    return;
  }
  const link = result.download
    ? ` <a href="/download/${encodeURIComponent(result.download)}">Download ${escapeHtml(result.download)}</a>`
    : "";
  messagesEl.innerHTML = `<div class="success">Generated.${link}</div><pre class="log">${escapeHtml(result.log)}</pre>`;
});

renderTopFields();
renderPages();
