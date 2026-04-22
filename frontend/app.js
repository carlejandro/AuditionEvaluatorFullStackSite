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

// Fetch performers using API from uvicorn backend
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
        
        // This is what actually populates the UI with the performers and their sections. It uses the sectionsMap to get the instrument name based on the section_id of each performer. If the section_id is not found in the map, it defaults to "Unknown Section".
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
        // This populates the performer detail section of the UI with the selected performer's information, 
        // including their name, age, email, and section. It also includes a form for entering scores for performance, timing, and rhythm, along with a real-time total score calculation.
        // the "container is the performer detail div. innerHTML allows injection of HTML content"
        container.innerHTML = `
        <h2>${performer.first_name} ${performer.last_name}</h2>
        <p><span class="detail-label">Age:</span> ${performer.age}</p>
        <p><span class="detail-label">Email:</span> ${performer.email}</p>
        <p><span class="detail-label">Section:</span> ${sectionsMap[performer.section_id] ?? "Unknown Section"}</p>

        <div class="score-form">
            <h3>Enter Scores</h3>

            <label for="performance-score">Performance Score</label>
            <input type="number" id="performance-score" min="0" max="100" value="0">

            <label for="timing-score">Timing Score</label>
            <input type="number" id="timing-score" min="0" max="100" value="0">

            <label for="rhythm-score">Rhythm Score</label>
            <input type="number" id="rhythm-score" min="0" max="100" value="0">

            <div class="total-score-box">
                <span class="detail-label">Total Score:</span>
                <span id="total-score">0</span>
            </div>

            <button id="apply-scores-btn">Apply Scores</button>
        </div>
    `;

    setupScoreCalculation();

}


// sets up score calculation logic, look at UML For reference
function setupScoreCalculation() {
    // These correspond to the UML class diagram attributes for the scores. They allow the user to input scores for performance, timing, and rhythm, and then calculate the total score by summing these three values. The total score is displayed in real-time as the user inputs the individual scores.
    
    const performanceInput = document.getElementById("performance-score");
    const timingInput = document.getElementById("timing-score");
    const rhythmInput = document.getElementById("rhythm-score");
    const totalScoreDisplay = document.getElementById("total-score");

    function updateTotal() {
        const performance = Number(performanceInput.value) || 0;
        const timing = Number(timingInput.value) || 0;
        const rhythm = Number(rhythmInput.value) || 0;

        const total = performance + timing + rhythm;
        totalScoreDisplay.textContent = total;
    }
    // these event listeners trigger the updateTotal function whenever the user changes any of the score inputs, ensuring that the total score is always up to date as they enter their scores.
    performanceInput.addEventListener("input", updateTotal);
    timingInput.addEventListener("input", updateTotal);
    rhythmInput.addEventListener("input", updateTotal);
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