const API_BASE = "http://127.0.0.1:8000";

let selectedPerformerId = null;
let sectionsMap = {};
let scoreStatusMap = {};

// LOAD FUNCTIONS

// Fetch sections and build lookup map
async function loadSections() {
    const res = await fetch(`${API_BASE}/sections`);
    const sections = await res.json();

    const sectionSelect = document.getElementById("new-section");

    // Clear existing map + dropdown (prevents duplicates)
    sectionsMap = {};
    
    if (sectionSelect) {
        sectionSelect.innerHTML = `<option value="">Select section</option>`;
    }

    sections.forEach(section => {
        // Build lookup map
        sectionsMap[section.section_id] = section.instrument_name;

        // Populate dropdown
        if (sectionSelect) {
            const option = document.createElement("option");
            option.value = section.section_id;
            option.textContent = section.instrument_name;
            sectionSelect.appendChild(option);
        }
    });
}

async function loadScoreStatus() {
    const res = await fetch(`${API_BASE}/performer-score-status`);
    const statuses = await res.json();

    scoreStatusMap = {};

    statuses.forEach(status => {
        scoreStatusMap[status.performer_id] = status.has_score;
    });
}

// Fetch performers using API from uvicorn backend
async function loadPerformers() {
    const res = await fetch(`${API_BASE}/performers`);
    const performers = await res.json();

    renderPerformers(performers);
    updateProgress(performers);
}

function renderPerformers(performers) {
    const container = document.getElementById("performer-list");

    if (!container) {
        console.error("performer-list div not found");
        return;
    }

    container.innerHTML = "";

    performers.forEach(performer => {
        const performerDiv = document.createElement("div");

        const statusText = scoreStatusMap[performer.performer_id] ? "Scored" : "Pending";
        const statusClass = scoreStatusMap[performer.performer_id] ? "status-scored" : "status-pending";

        performerDiv.innerHTML = `
            <div class="performer-row">
                <div>
                    <span class="performer-name">${performer.first_name} ${performer.last_name}</span>
                    <span>- ${sectionsMap[performer.section_id] ?? "Unknown Section"}</span>
                </div>

                <div>
                    <span class="status-badge ${statusClass}">${statusText}</span>
                    <button class="delete-btn" onclick="deletePerformer(${performer.performer_id})">
                    Delete
                    </button>
            </div>
        `;

        performerDiv.style.cursor = "pointer";
        performerDiv.onclick = () => loadPerformerDetail(performer.performer_id);

        container.appendChild(performerDiv);
    });
}

function updateProgress(performers) {
    const totalCount = document.getElementById("total-count");
    const scoredCount = document.getElementById("scored-count");
    const pendingCount = document.getElementById("pending-count");

    const total = performers.length;

    // for now, we do not have score status wired into the performer list,
    // so everyone is treated as pending until adjudicator fills out scores.
    const scored = performers.filter(p => scoreStatusMap[p.performer_id]).length;
    const pending = total - scored;

    totalCount.textContent = total;
    scoredCount.textContent = scored;
    pendingCount.textContent = pending;
}

// Fetch one performer
async function loadPerformerDetail(id) {
    selectedPerformerId = id;
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
            <div id="score-message" class="score-message"></div>
            <button id="apply-scores-btn">Apply Scores</button>
        </div>
    `;

    setupScoreCalculation();
    setupApplyScoresButton();

}


// Asynchronous POST Functions

// async function to save the score for the selected performer. It first checks if a performer is selected, then it gathers the individual scores from the input fields, calculates the total score, and constructs a payload object to send to the backend API.
async function saveScore() {
    if (!selectedPerformerId) {
        alert("Please select a performer first.");
        return;
    }

    const performanceScore = Number(document.getElementById("performance-score").value) || 0;
    const timingScore = Number(document.getElementById("timing-score").value) || 0;
    const rhythmScore = Number(document.getElementById("rhythm-score").value) || 0;
    const totalScore = performanceScore + timingScore + rhythmScore;

    const payload = {
        performance_score: performanceScore,
        timing_score: timingScore,
        rhythm_score: rhythmScore,
        total_score: totalScore,
        comments: null
    };

    // The post request to the backend API to save the score for selected performer.
    const res = await fetch(`${API_BASE}/performers/${selectedPerformerId}/scores`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });
    // Score button message div to display success or failure
    const messageDiv = document.getElementById("score-message");
    
    
    if (!res.ok) {
        if (messageDiv) {
            messageDiv.textContent = `Error saving score: ${res.statusText}`;
            messageDiv.style.color = "red";
        }
        return; // Exit the function if response is not ok to avoid trying to parse JSON from an error response.
    }

    const result = await res.json();
     
    if (messageDiv) {
        messageDiv.textContent = `Score saved successfully! (ID: ${result.score_id})`;
        messageDiv.style.color = "green";
    }

    await loadScoreStatus();
    await loadPerformers();
}


async function addPerformer() {
    const firstName = document.getElementById("new-first-name").value;
    const lastName = document.getElementById("new-last-name").value;
    const age = Number(document.getElementById("new-age").value);
    const email = document.getElementById("new-email").value;
    const sectionId = Number(document.getElementById("new-section").value);

    const payload = {
        first_name: firstName,
        last_name: lastName,
        age: age,
        email: email,
        section_id: sectionId
    };

    const res = await fetch(`${API_BASE}/performers`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    if (!res.ok) {
        console.error("Error adding performer:", await res.json());
        return;
    }

    document.getElementById("new-first-name").value = "";
    document.getElementById("new-last-name").value = "";
    document.getElementById("new-age").value = "";
    document.getElementById("new-email").value = "";
    document.getElementById("new-section").value = "";

    await loadPerformers();

    document.getElementById("add-performer-form").classList.add("hidden");
    document.getElementById("toggle-add-performer-btn").textContent = "+ Add Performer";
}


// DELETE FUNCTIONS // 
async function deletePerformer(performerId) {
    const confirmDelete = confirm("Are you sure you want to delete this performer?");
    if (!confirmDelete) return;

    const res = await fetch(`${API_BASE}/performers/${performerId}`, {
        method: "DELETE"
    });

    if (!res.ok) {
        alert("Failed to delete performer");
        return;
    }

    // refresh UI
    await loadPerformers();
    await loadScoreStatus();

    // clear right panel if needed
    const detail = document.getElementById("performer-detail");
    if (detail) {
        detail.innerHTML = "<p>Select a performer</p>";
    }
}


// SETUP FUNCTIONS //

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

function setupApplyScoresButton() {
    const button = document.getElementById("apply-scores-btn");
    if (!button) {
        console.error("Apply Scores button not found");
        return;
    }
    button.addEventListener("click", saveScore); // Attaching save score function to the click action on the button
}

// setup toggle functionality so the add performer form can be hidden ONLY when the user chooses to reveal it. 
function setupAddPerformerToggle() {
    const toggleButton = document.getElementById("toggle-add-performer-btn");
    const form = document.getElementById("add-performer-form");

    if (!toggleButton || !form) {
        return;
    }

    toggleButton.addEventListener("click", () => {
        form.classList.toggle("hidden");

        if (form.classList.contains("hidden")) {
            toggleButton.textContent = "+ Add Performer";
        } else {
            toggleButton.textContent = "Cancel";
        }
    });
}

function setupAddPerformerButton() {
    const button = document.getElementById("add-performer-btn");

    if (!button) {
        return;
    }

    button.addEventListener("click", addPerformer);
}

// INITIALIZATION --> the main function. 
async function init() {
    try {
        await loadSections();
        await loadScoreStatus();
        await loadPerformers(); //This is what loads the performers when the uvicorn server is up and running. It calls the loadPerformers function which fetches the performer data from the backend API and then renders it in the UI.

        setupAddPerformerToggle();
        setupAddPerformerButton();

    } catch (error) {
        console.error("Error loading UI:", error);
    }
}

init();