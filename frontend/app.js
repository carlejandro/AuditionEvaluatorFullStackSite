const API_BASE = "http://127.0.0.1:8000";

let sectionsMap = {};

// Fetch sections and build lookup map
async function loadSections() {
    const res = await fetch(`${API_BASE}/sections`);
    const sections = await res.json();

    sections.forEach(section => {
        sectionsMap[section.section_id] = section.instrument_name;
    });
}

// Fetch performers
async function loadPerformers() {
    const res = await fetch(`${API_BASE}/performers`);
    const performers = await res.json();

    renderPerformers(performers);
}

// Render performer list
function renderPerformers(performers) {
    const container = document.getElementById("performer-list");

    if (!container) {
        console.error("performer-list div not found");
        return;
    }

    container.innerHTML = "";

    performers.forEach(performer => {
        const performerDiv = document.createElement("div");

        performerDiv.innerHTML = `
            <strong>${performer.first_name} ${performer.last_name}</strong>
            - ${sectionsMap[performer.section_id] ?? "Unknown Section"}
        `;

        performerDiv.style.cursor = "pointer";
        performerDiv.onclick = () => loadPerformerDetail(performer.performer_id);

        container.appendChild(performerDiv);
    });
}

// Fetch one performer
async function loadPerformerDetail(id) {
    const res = await fetch(`${API_BASE}/performers/${id}`);
    const performer = await res.json();

    renderPerformerDetail(performer);
}

// Render selected performer detail
function renderPerformerDetail(performer) {
    const container = document.getElementById("performer-detail");

    if (!container) {
        console.error("performer-detail div not found");
        return;
    }

    container.innerHTML = `
        <h2>${performer.first_name} ${performer.last_name}</h2>
        <p>Age: ${performer.age}</p>
        <p>Email: ${performer.email}</p>
        <p>Section: ${sectionsMap[performer.section_id] ?? "Unknown Section"}</p>
    `;
}

// Initialize page
async function init() {
    try {
        await loadSections();
        await loadPerformers();
    } catch (error) {
        console.error("Error loading UI:", error);
    }
}

init();