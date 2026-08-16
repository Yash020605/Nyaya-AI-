// Base configuration
const API_BASE_URL = "http://localhost:8000/api/v1";

// Tab Switching Logic
document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".nav-btn");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            tab.classList.add("active");
            const activeTabId = tab.getAttribute("data-tab");
            document.getElementById(activeTabId).classList.add("active");
        });
    });

    // Setup Drafting sub-tabs
    const draftTabs = document.querySelectorAll(".draft-tab-btn");
    draftTabs.forEach(dTab => {
        dTab.addEventListener("click", () => {
            draftTabs.forEach(t => t.classList.remove("active"));
            dTab.classList.add("active");
            renderActiveDraftSection();
        });
    });

    // Bind action events
    document.getElementById("btn-search").addEventListener("click", handleSearch);
    document.getElementById("btn-draft").addEventListener("click", handleDraftCompile);
    document.getElementById("btn-ingest").addEventListener("click", handleIngestionSubmit);
    document.getElementById("btn-copy-draft").addEventListener("click", copyDraftToClipboard);
});

// Cache storage for active drafting outputs
let currentDrafts = null;

// =====================================================================
// Frontend Controller Logic (Maintained by Assistant)
// Handles API calls connecting the UI views to backend endpoints.
// =====================================================================

// 1. Research Fetch Handler
async function handleSearch() {
    const query = document.getElementById("search-query").value.trim();
    if (!query) return;

    const resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = '<div class="empty-state"><p>Querying backend databases...</p></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/research/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error("Search request failed.");
        
        const data = await response.json();
        renderSearchResults(data.results);
    } catch (error) {
        resultsContainer.innerHTML = `<div class="empty-state"><p style="color:#ef4444;">Error: ${error.message}</p></div>`;
    }
}

// 2. Document Fetch Handler (Details lookup)
async function fetchFullDocument(mongoId) {
    const viewerBody = document.getElementById("document-text");
    const badge = document.getElementById("doc-citation-badge");
    
    viewerBody.innerHTML = '<p>Retrieving case context from MongoDB...</p>';
    badge.innerText = "Connecting...";

    try {
        const response = await fetch(`${API_BASE_URL}/research/document/${mongoId}`);
        if (!response.ok) throw new Error("Could not retrieve document.");
        
        const data = await response.json();
        viewerBody.innerHTML = formatLegalText(data.full_text);
        badge.innerText = data.citation;
    } catch (error) {
        viewerBody.innerHTML = `<p style="color:#ef4444;">Error: ${error.message}</p>`;
        badge.innerText = "Error";
    }
}

// 3. Drafting Fetch Handler
async function handleDraftCompile() {
    const facts = document.getElementById("draft-facts").value.trim();
    const offences = document.getElementById("draft-offences").value.trim();
    
    if (!facts) {
        alert("Please enter case facts first.");
        return;
    }

    const outputDisplay = document.getElementById("draft-text-display");
    outputDisplay.innerHTML = '<div class="empty-state"><p>Compiling petition sections via LLM pipeline...</p></div>';

    try {
        const response = await fetch(`${API_BASE_URL}/drafting/draft`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ facts: facts, offences: offences })
        });
        
        if (!response.ok) throw new Error("Drafting compilation failed.");
        
        const data = await response.json();
        currentDrafts = data.drafts;
        renderActiveDraftSection();
    } catch (error) {
        outputDisplay.innerHTML = `<div class="empty-state"><p style="color:#ef4444;">Error: ${error.message}</p></div>`;
    }
}

// 4. Ingestion Fetch Handler
async function handleIngestionSubmit() {
    const title = document.getElementById("ingest-title").value.trim();
    const citation = document.getElementById("ingest-citation").value.trim();
    const text = document.getElementById("ingest-text").value.trim();

    if (!title || !citation || !text) {
        alert("All fields are required for ingestion.");
        return;
    }

    const jobsContainer = document.getElementById("ingest-jobs");
    if (jobsContainer.querySelector(".empty-state")) {
        jobsContainer.innerHTML = '';
    }

    try {
        const response = await fetch(`${API_BASE_URL}/admin/ingest`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, citation, text })
        });
        
        if (!response.ok) throw new Error("Ingestion dispatch failed.");
        
        const data = await response.json();
        addIngestionJobToQueue(title, data.mongo_id, data.status);
    } catch (error) {
        alert(`Ingestion Error: ${error.message}`);
    }
}

// UI Rendering Helpers
function renderSearchResults(results) {
    const container = document.getElementById("search-results");
    container.innerHTML = "";

    if (!results || results.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No matching criminal case records found.</p></div>';
        return;
    }

    results.forEach(item => {
        const card = document.createElement("div");
        card.className = "result-card";
        card.innerHTML = `
            <h4>${item.title}</h4>
            <p>${item.snippet}</p>
            <div class="meta">
                <span class="badge secondary">${item.citation}</span>
                <span>Match Score: ${(item.relevance_score * 100).toFixed(0)}%</span>
            </div>
        `;
        card.addEventListener("click", () => fetchFullDocument(item.mongo_id));
        container.appendChild(card);
    });
}

function renderActiveDraftSection() {
    const display = document.getElementById("draft-text-display");
    if (!currentDrafts) return;

    const activeSubTab = document.querySelector(".draft-tab-btn.active");
    const sectionKey = activeSubTab.getAttribute("data-draft-sec");

    display.innerText = currentDrafts[sectionKey] || "Section empty.";
}

function addIngestionJobToQueue(title, mongoId, status) {
    const queue = document.getElementById("ingest-jobs");
    const item = document.createElement("div");
    item.className = "job-item";
    item.innerHTML = `
        <div>
            <div class="title">${title}</div>
            <div style="font-size:0.75rem; color:var(--text-secondary);">Ref ID: ${mongoId}</div>
        </div>
        <span class="status-badge processing">${status.toUpperCase()}</span>
    `;
    queue.prepend(item);

    // Mock completion transition (4s delay representation)
    setTimeout(() => {
        const badge = item.querySelector(".status-badge");
        badge.className = "status-badge done";
        badge.innerText = "DONE";
    }, 4000);
}

function copyDraftToClipboard() {
    const display = document.getElementById("draft-text-display");
    if (display.querySelector(".empty-state")) return;
    
    navigator.clipboard.writeText(display.innerText)
        .then(() => alert("Section copied to clipboard!"))
        .catch(err => console.error("Could not copy text: ", err));
}

// 5. Prettify Legal Text Formatter Helper
function formatLegalText(text) {
    if (!text) return "";
    
    // Clean and convert <NAME>, <ORG>, <CITATION> placeholders into styled badges
    let formatted = text
        .replace(/<NAME>/g, '<span class="legal-badge name">NAME</span>')
        .replace(/<ORG>/g, '<span class="legal-badge org">ORG</span>')
        .replace(/<CITATION>/g, '<span class="legal-badge citation">CITATION</span>');

    // Parse specific headers from IL-TUR full text
    const fields = [
        { label: "Petitioner", key: "PETITIONER" },
        { label: "Respondent", key: "RESPONDENT" },
        { label: "Date of Judgment", key: "DATE OF JUDGMENT" },
        { label: "Bench", key: "BENCH" },
        { label: "Citation", key: "CITATION" }
    ];

    let extractedFields = [];
    let textToProcess = formatted;

    fields.forEach(field => {
        const regex = new RegExp(`${field.key}:\\s*(.*?)(?=\\s*(?:RESPONDENT|DATE OF JUDGMENT|BENCH|CITATION|CITATOR INFO|ACT|HEADNOTE|$))`, "i");
        const match = textToProcess.match(regex);
        if (match) {
            extractedFields.push({ label: field.label, value: match[1].trim() });
            textToProcess = textToProcess.replace(match[0], "");
        }
    });

    // Extract acts and headnotes
    const largeFields = [
        { label: "Acts & Statutory Sections", key: "ACT" },
        { label: "Headnote Synopsis", key: "HEADNOTE" }
    ];
    let largeFieldsHtml = "";
    largeFields.forEach(field => {
        const regex = new RegExp(`${field.key}:\\s*(.*?)(?=\\s*(?:CITATOR INFO|ACT|HEADNOTE|JUDGMENT|$))`, "is");
        const match = textToProcess.match(regex);
        if (match) {
            largeFieldsHtml += `
                <div class="legal-large-field">
                    <h5>${field.label}</h5>
                    <p>${match[1].trim()}</p>
                </div>
            `;
            textToProcess = textToProcess.replace(match[0], "");
        }
    });

    // Clean remaining headers
    textToProcess = textToProcess
        .replace(/CITATOR INFO\s*:\s*.*?(?=\s*(?:ACT|HEADNOTE|JUDGMENT|$))/is, "")
        .trim();

    let metaSectionHtml = "";
    if (extractedFields.length > 0) {
        metaSectionHtml = `
            <div class="legal-meta-card">
                <h4>Case Details</h4>
                <div class="legal-meta-grid">
                    ${extractedFields.map(f => `
                        <div class="meta-item">
                            <span class="meta-label">${f.label}</span>
                            <span class="meta-value">${f.value}</span>
                        </div>
                    `).join("")}
                </div>
            </div>
        `;
    }

    // Split remaining body text into structured paragraphs
    let paragraphs = textToProcess.split(/\n\n+/);
    if (paragraphs.length === 1 && paragraphs[0].includes("Legal Reasoning:")) {
        // Handle summary cases formatting
        const parts = paragraphs[0].split("Legal Reasoning:");
        paragraphs = [parts[0], "Legal Reasoning:\n" + (parts[1] || "")];
    }

    const bodyHtml = paragraphs.map(p => {
        const cleaned = p.trim();
        if (!cleaned) return "";
        
        if (cleaned.startsWith("Legal Reasoning:")) {
            return `
                <div class="legal-reasoning-card">
                    <h5>⚖️ Court's Legal Reasoning</h5>
                    <p>${cleaned.replace("Legal Reasoning:", "").trim()}</p>
                </div>
            `;
        }
        
        if (cleaned.match(/^\d+\./) || (cleaned.length < 60 && cleaned.toUpperCase() === cleaned)) {
            return `<h4 class="legal-section-title">${cleaned}</h4>`;
        }
        
        return `<p class="legal-paragraph">${cleaned}</p>`;
    }).join("");

    return `
        <div class="prettified-document">
            ${metaSectionHtml}
            ${largeFieldsHtml}
            <div class="legal-body-section">
                <h4>Case Judgment Text</h4>
                ${bodyHtml || "<p class='empty-state'>Text parsed above.</p>"}
            </div>
        </div>
    `;
}
