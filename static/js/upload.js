/* upload.js — Optimized for Premium UI */

const MAX_SIZE_MB = 20;
const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function getAcceptedExtensions(conversionType) {
  if (conversionType === 'word_to_pdf') return ['.docx', '.doc'];
  if (conversionType === 'pdf_to_word') return ['.pdf'];
  return ['.png', '.jpg', '.jpeg', '.webp', '.bmp'];
}

window.initConverter = function(conversionType) {
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const uploadState = document.getElementById('uploadState');
  const filePreview = document.getElementById('filePreview');
  const processingState = document.getElementById('processingState');
  const doneState = document.getElementById('doneState');
  const errorState = document.getElementById('errorState');
  
  // Optional elements (might not be in all templates)
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const convertBtn = document.getElementById('convertBtn');

  let selectedFile = null;

  if (!dropZone || !fileInput) return;

  /* ---------- Event Listeners ---------- */
  dropZone.addEventListener('click', (e) => {
    // Prevent double-firing if the click was already on the file input itself
    if (e.target === fileInput) return;
    fileInput.click();
  });
  
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length) handleFile(fileInput.files[0]);
  });

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });

  if (convertBtn) {
    convertBtn.addEventListener('click', () => {
      if (selectedFile) uploadFile(selectedFile);
    });
  }

  /* ---------- File Handling ---------- */
  function handleFile(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    const allowed = getAcceptedExtensions(conversionType);

    if (!allowed.includes(ext)) {
      showError(`Unsupported format "${ext}". Please use: ${allowed.join(', ')}`);
      return;
    }
    if (file.size > MAX_SIZE_BYTES) {
      showError(`File too large (${formatBytes(file.size)}). Max: ${MAX_SIZE_MB} MB.`);
      return;
    }

    selectedFile = file;
    
    // If we have a separate preview state (like in Word/PDF templates)
    if (filePreview) {
      if (fileName) fileName.textContent = file.name;
      if (fileSize) fileSize.textContent = formatBytes(file.size);
      uploadState.hidden = true;
      filePreview.hidden = false;
    } else {
      // Auto-upload for image tools
      uploadFile(file);
    }
  }

  function uploadFile(file) {
    if (filePreview) filePreview.hidden = true;
    if (uploadState) uploadState.hidden = true;
    if (processingState) processingState.hidden = false;

    const progressBar = document.getElementById('progressBar');
    const statusText = document.getElementById('statusText');

    if (statusText) statusText.textContent = 'Uploading file...';
    if (progressBar) progressBar.style.width = '20%';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', conversionType);

    fetch('/api/convert', {
      method: 'POST',
      body: formData,
    })
    .then(res => {
      if (!res.ok) return res.json().then(data => { throw new Error(data.error || 'Upload failed'); });
      return res.json();
    })
    .then(data => {
      if (statusText) statusText.textContent = 'Processing...';
      if (progressBar) progressBar.style.width = '50%';
      
      if (window.startPolling) {
        window.startPolling(data.job_id, progressBar, statusText);
      }
    })
    .catch(err => showError(err.message));
  }

  function showError(message) {
    if (uploadState) uploadState.hidden = true;
    if (filePreview) filePreview.hidden = true;
    if (processingState) processingState.hidden = true;
    if (errorState) {
      errorState.hidden = false;
      document.getElementById('errorMessage').textContent = message;
    } else {
      alert(message);
      location.reload();
    }
  }
};

/* Mobile Nav Toggle */
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('active');
      links.style.display = links.classList.contains('active') ? 'flex' : '';
      if (links.classList.contains('active')) {
        links.style.flexDirection = 'column';
        links.style.position = 'absolute';
        links.style.top = '80px';
        links.style.left = '0';
        links.style.right = '0';
        links.style.background = 'var(--bg-dark)';
        links.style.padding = '20px';
        links.style.borderBottom = '1px solid var(--border-glass)';
      }
    });
  }
});
