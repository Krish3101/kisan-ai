import { $, setHTML, escapeHtml, API_BASE, withSpinner, toast } from './config.js';

// ============================
// Soil
// ============================
function soilSkeleton() {
    setHTML($("#soil-result"), `<div class="skel h-6"></div><div class="skel h-6 mt"></div>`);
}

export async function loadSoil(btn) {
    return withSpinner(btn, async () => {
        const field = ($("#soil-field")?.value || "default").trim();
        soilSkeleton();
        try {
            const r = await fetch(`${API_BASE}/soil?field=${encodeURIComponent(field)}`);
            const s = await r.json();
            setHTML($("#soil-result"), `
        <div class="space-y-1">
          ${s.soil_type ? `<p><b>Soil:</b> ${escapeHtml(s.soil_type)}</p>` : ""}
          ${s.ph ? `<p><b>pH:</b> ${escapeHtml(String(s.ph))}</p>` : ""}
          ${s.organic_carbon ? `<p><b>Organic Carbon:</b> ${escapeHtml(String(s.organic_carbon))}</p>` : ""}
          ${s.moisture ? `<p><b>Moisture:</b> ${escapeHtml(String(s.moisture))}</p>` : ""}
          ${s.nitrogen ? `<p><b>Nitrogen:</b> ${escapeHtml(String(s.nitrogen))}</p>` : ""}
          ${s.phosphorus ? `<p><b>Phosphorus:</b> ${escapeHtml(String(s.phosphorus))}</p>` : ""}
          ${s.potassium ? `<p><b>Potassium:</b> ${escapeHtml(String(s.potassium))}</p>` : ""}
          ${s.last_tested ? `<p class="text-xs text-slate-500 dark:text-slate-400">Last tested: ${escapeHtml(s.last_tested)}</p>` : ""}
        </div>
      `);
        } catch {
            setHTML($("#soil-result"), `<div class="text-red-600">Error loading soil</div>`);
        }
    });
}

export function openSoilModal() {
    const modal = $("#soil-modal");
    if (modal) modal.classList.remove("hidden");
}
window.closeSoilModal = () => {
    const modal = $("#soil-modal");
    if (modal) modal.classList.add("hidden");
}

window.saveSoil = async () => {
    const field = $("#s-field").value;
    const type = $("#s-type").value;
    const ph = $("#s-ph").value;
    if (!field || !type) return toast("Field name & type required");

    try {
        await fetch(`${API_BASE}/soil/add`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                field, soil_type: type, ph,
                nitrogen: $("#s-n").value,
                phosphorus: $("#s-p").value,
                potassium: $("#s-k").value,
                moisture: $("#s-moisture").value
            })
        });
        toast("Soil report saved");
        closeSoilModal();
        // Reload if the current field matches the saved one, or just clear
        loadSoil();
    } catch { toast("Failed to save"); }
};

// Expose for HTML
window.openSoilModal = openSoilModal;
