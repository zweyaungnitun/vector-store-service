const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const targetType = document.getElementById('target-type');
const fileList = document.getElementById('file-list');
const progressBar = document.getElementById('progress-bar');
const progressContainer = document.getElementById('progress-container');
const textIngestBtn = document.getElementById('text-ingest-btn');
const rawText = document.getElementById('raw-text');
const textTargetType = document.getElementById('text-target-type');

let selectedFiles = [];

// Tab Switching
window.switchTab = (tabId) => {
    document.querySelectorAll('.ingest-section').forEach(section => {
        section.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
    
    // Clear list when switching tabs
    fileList.innerHTML = '';
};

// Drag and drop handlers
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
});

dropZone.addEventListener('drop', e => {
    const dt = e.dataTransfer;
    handleFiles(dt.files);
});

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files);
});

function handleFiles(files) {
    selectedFiles = [...files];
    updateFileList();
    uploadBtn.disabled = selectedFiles.length === 0;
}

function updateFileList() {
    fileList.innerHTML = selectedFiles.map((file, index) => `
        <div class="file-item fade-in">
            <div class="file-info">
                <span>📄</span>
                <div>
                    <div style="font-weight: 600">${file.name}</div>
                    <small style="color: var(--text-dim)">${(file.size / 1024).toFixed(1)} KB</small>
                </div>
            </div>
            <div class="status-badge" id="status-${index}">Ready</div>
        </div>
    `).join('');
}

// File Upload Handler
uploadBtn.addEventListener('click', async () => {
    const target = targetType.value;
    uploadBtn.disabled = true;
    progressContainer.style.display = 'block';

    let processedCount = 0;

    for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];
        const formData = new FormData();
        formData.append('file', file);

        const statusLabel = document.getElementById(`status-${i}`);
        statusLabel.textContent = 'Uploading...';
        statusLabel.style.color = 'var(--primary)';

        try {
            const response = await fetch(`http://localhost:8000/api/v1/ingest/file?target=${target}`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                statusLabel.textContent = `Success (${result.count} recs)`;
                statusLabel.style.color = 'var(--success)';
            } else {
                const error = await response.json();
                statusLabel.textContent = `Error`;
                statusLabel.title = error.detail || 'Upload failed';
                statusLabel.style.color = 'var(--error)';
            }
        } catch (err) {
            statusLabel.textContent = 'Failed';
            statusLabel.style.color = 'var(--error)';
        }

        processedCount++;
        progressBar.style.width = `${(processedCount / selectedFiles.length) * 100}%`;
    }

    uploadBtn.disabled = false;
    setTimeout(() => {
        progressContainer.style.display = 'none';
        progressBar.style.width = '0%';
    }, 3000);
});

// Raw Text Ingestion Handler
textIngestBtn.addEventListener('click', async () => {
    const text = rawText.value.trim();
    if (!text) return;

    const target = textTargetType.value;
    textIngestBtn.disabled = true;
    
    // Create a temporary "file-like" entry in the list for feedback
    const index = 0;
    fileList.innerHTML = `
        <div class="file-item fade-in">
            <div class="file-info">
                <span>📝</span>
                <div>
                    <div style="font-weight: 600">Raw Text Snippet</div>
                    <small style="color: var(--text-dim)">${text.length} characters</small>
                </div>
            </div>
            <div class="status-badge" id="text-status">Ingesting...</div>
        </div>
    `;

    const statusLabel = document.getElementById('text-status');
    statusLabel.style.color = 'var(--primary)';

    try {
        // We reuse the /file endpoint by creating a Blob, or we could add a new endpoint.
        // For simplicity and reusing backend logic, we send a pseudo-file.
        const blob = new Blob([text], { type: 'text/plain' });
        const formData = new FormData();
        formData.append('file', blob, 'raw_text_ingestion.txt');

        const response = await fetch(`http://localhost:8000/api/v1/ingest/file?target=${target}`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            statusLabel.textContent = `Success`;
            statusLabel.style.color = 'var(--success)';
            rawText.value = '';
        } else {
            const error = await response.json();
            statusLabel.textContent = `Error`;
            statusLabel.style.color = 'var(--error)';
        }
    } catch (err) {
        statusLabel.textContent = 'Error';
        statusLabel.style.color = 'var(--error)';
    }

    textIngestBtn.disabled = false;
});
