const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadBtn = document.getElementById('upload-btn');
const targetType = document.getElementById('target-type');
const fileList = document.getElementById('file-list');
const progressBar = document.getElementById('progress-bar');
const progressContainer = document.getElementById('progress-container');

let selectedFiles = [];

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
                    <div>${file.name}</div>
                    <small style="color: var(--text-dim)">${(file.size / 1024).toFixed(1)} KB</small>
                </div>
            </div>
            <div class="status-badge" id="status-${index}">Ready</div>
        </div>
    `).join('');
}

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
            // Updated to point to the correct Backend API port
            const response = await fetch(`http://localhost:8000/api/v1/ingest/file?target=${target}`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                statusLabel.textContent = `Success (${result.count} records)`;
                statusLabel.style.color = 'var(--success)';
            } else {
                const error = await response.json();
                statusLabel.textContent = `Error: ${error.detail || 'Upload failed'}`;
                statusLabel.style.color = 'var(--error)';
            }
        } catch (err) {
            statusLabel.textContent = 'Connection Error';
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
