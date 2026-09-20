const API_URL =
    "https://hls7qob2vf.execute-api.ap-south-1.amazonaws.com/moderate";

const form = document.getElementById("moderationForm");
const imageUrlInput = document.getElementById("imageUrl");
const imageFileInput = document.getElementById("imageFile");
const moderateButton = document.getElementById("moderateButton");

const previewContainer = document.getElementById("previewContainer");
const imagePreview = document.getElementById("imagePreview");

const loading = document.getElementById("loading");
const errorCard = document.getElementById("errorCard");
const errorMessage = document.getElementById("errorMessage");
const resultCard = document.getElementById("resultsSection");

const decisionBadge = document.getElementById("decisionBadge");
const decisionValue = document.getElementById("decisionValue");
const severityValue = document.getElementById("severityValue");
const requestIdValue = document.getElementById("requestIdValue");
const labelsContainer = document.getElementById("labelsContainer");
const labelCount = document.getElementById("labelCount");
const timestampValue = document.getElementById("timestampValue");

let selectedImageFile = null;

/* URL preview */

imageUrlInput.addEventListener("input", () => {
    if (imageUrlInput.value.trim()) {
        imageFileInput.value = "";
        selectedImageFile = null;

        imagePreview.src = imageUrlInput.value.trim();

        imagePreview.onload = () => {
            previewContainer.classList.remove("hidden");
        };

        imagePreview.onerror = () => {
            previewContainer.classList.add("hidden");
        };
    }
});

/* Laptop image selection */

imageFileInput.addEventListener("change", () => {
    const file = imageFileInput.files[0];

    if (!file) {
        selectedImageFile = null;
        return;
    }

    if (!file.type.startsWith("image/")) {
        showError("Please select a valid image file.");
        imageFileInput.value = "";
        selectedImageFile = null;
        return;
    }

    if (file.size > 5 * 1024 * 1024) {
        showError("Image size must be less than 5 MB.");
        imageFileInput.value = "";
        selectedImageFile = null;
        return;
    }

    selectedImageFile = file;
    imageUrlInput.value = "";

    const previewUrl = URL.createObjectURL(file);
    imagePreview.src = previewUrl;
    previewContainer.classList.remove("hidden");
});

/* Example image buttons */

document.querySelectorAll(".sample-button").forEach((button) => {
    button.addEventListener("click", () => {
        const sampleUrl = button.dataset.url;

        imageUrlInput.value = sampleUrl;
        imageFileInput.value = "";
        selectedImageFile = null;

        imagePreview.src = sampleUrl;

        imagePreview.onload = () => {
            previewContainer.classList.remove("hidden");
        };

        imagePreview.onerror = () => {
            previewContainer.classList.add("hidden");
        };
    });
});

/* Form submission */

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const imageUrl = imageUrlInput.value.trim();

    if (!imageUrl && !selectedImageFile) {
        showError("Please enter an image URL or upload an image.");
        return;
    }

    resetInterface();
    loading.classList.remove("hidden");
    moderateButton.disabled = true;
    moderateButton.innerHTML =
        '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

    try {
        let requestBody;

        if (selectedImageFile) {
            const base64Image = await convertFileToBase64(
                selectedImageFile
            );

            requestBody = {
                imageBase64: base64Image,
                fileName: selectedImageFile.name,
                contentType: selectedImageFile.type
            };
        } else {
            requestBody = {
                imageUrl: imageUrl
            };
        }

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.message ||
                data.error ||
                "The moderation request failed."
            );
        }

        displayResult(data);
    } catch (error) {
        showError(
            error.message ||
            "Unable to connect to the moderation API."
        );
    } finally {
        loading.classList.add("hidden");
        moderateButton.disabled = false;
        moderateButton.innerHTML =
            '<i class="fa-solid fa-shield-halved"></i> Analyze Image';
    }
});

/* Convert local file to Base64 */

function convertFileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = () => {
            const base64String = reader.result.split(",")[1];
            resolve(base64String);
        };

        reader.onerror = () => {
            reject(new Error("Unable to read the selected image."));
        };

        reader.readAsDataURL(file);
    });
}

/* Interface helpers */

function resetInterface() {
    errorCard.classList.add("hidden");
    resultCard.classList.add("hidden");
    errorMessage.textContent = "";
}

function showError(message) {
    resetInterface();
    errorMessage.textContent = message;
    errorCard.classList.remove("hidden");
}

/* Display moderation result */

function displayResult(data) {
    resultCard.classList.remove("hidden");

    const decision =
        data.decision ||
        data.status ||
        data.verdict ||
        "UNKNOWN";

    const severity =
        data.severity ||
        data.risk_level ||
        "N/A";

    const requestId =
        data.requestId ||
        data.request_id ||
        "N/A";

    const timestamp =
        data.timestamp ||
        new Date().toISOString();

    const labels =
        data.labels ||
        data.detected_labels ||
        [];

    decisionBadge.textContent = decision;
    decisionBadge.className = "decision-badge";

    if (decision.toUpperCase() === "APPROVED") {
        decisionBadge.classList.add("approved");
    } else if (decision.toUpperCase() === "FLAGGED") {
        decisionBadge.classList.add("flagged");
    }

    decisionValue.textContent = decision;
    severityValue.textContent = severity;
    requestIdValue.textContent = requestId;
    timestampValue.textContent = timestamp;

    labelCount.textContent =
        `${Array.isArray(labels) ? labels.length : 0} labels`;

    renderLabels(labels);
}

function renderLabels(labels) {
    labelsContainer.innerHTML = "";

    if (!Array.isArray(labels) || labels.length === 0) {
        labelsContainer.innerHTML =
            '<p class="empty-labels">No moderation labels detected.</p>';
        return;
    }

    labels.forEach((label) => {
        const labelItem = document.createElement("div");
        labelItem.className = "label-item";

        let labelName = "Unknown label";
        let confidence = "";

        if (typeof label === "string") {
            labelName = label;
        } else {
            labelName =
                label.Name ||
                label.name ||
                label.label ||
                "Unknown label";

            const confidenceValue =
                label.Confidence ??
                label.confidence ??
                label.score;

            if (confidenceValue !== undefined) {
                confidence = `${Number(confidenceValue).toFixed(2)}%`;
            }
        }

        labelItem.innerHTML = `
            <span class="label-name">
                ${escapeHtml(labelName)}
            </span>

            <span class="label-confidence">
                ${escapeHtml(confidence)}
            </span>
        `;

        labelsContainer.appendChild(labelItem);
    });
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}
