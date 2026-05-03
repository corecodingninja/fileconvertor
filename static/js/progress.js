/* progress.js — Premium Polling Logic */

window.startPolling = function(jobId, progressBar, statusText) {
  const POLL_INTERVAL = 1500;
  const MAX_POLLS = 80; // 2 minutes
  let polls = 0;

  const interval = setInterval(async () => {
    polls++;
    if (polls > MAX_POLLS) {
      clearInterval(interval);
      handleError('Task timed out. Please try again.');
      return;
    }

    try {
      const res = await fetch(`/api/status/${jobId}`);
      if (!res.ok) throw new Error('Failed to fetch status');
      const data = await res.json();

      switch (data.status) {
        case 'pending':
          if (statusText) statusText.textContent = 'In Queue...';
          break;
        case 'processing':
          if (statusText) statusText.textContent = 'Converting...';
          const current = parseFloat(progressBar.style.width) || 50;
          progressBar.style.width = Math.min(current + 2, 95) + '%';
          break;
        case 'done':
          clearInterval(interval);
          if (progressBar) progressBar.style.width = '100%';
          if (statusText) statusText.textContent = 'Complete!';
          
          setTimeout(() => {
            showDone(jobId, data.original_filename);
          }, 500);
          break;
        case 'failed':
          clearInterval(interval);
          handleError(data.error_message || 'Conversion failed');
          break;
      }
    } catch (err) {
      console.error(err);
      // Don't clear interval on transient network errors, just wait for next poll
    }
  }, POLL_INTERVAL);

  function showDone(jobId, originalName) {
    const processingState = document.getElementById('processingState');
    const doneState = document.getElementById('doneState');
    const downloadBtn = document.getElementById('downloadBtn');
    const resultFileName = document.getElementById('resultFileName');

    if (doneState) {
      if (processingState) processingState.hidden = true;
      doneState.hidden = false;
      if (downloadBtn) downloadBtn.href = `/api/download/${jobId}`;
      if (resultFileName) resultFileName.textContent = `Successfully processed: ${originalName}`;
    } else {
      // Fallback for legacy templates
      window.location.href = `/result/${jobId}`;
    }
  }

  function handleError(msg) {
    const processingState = document.getElementById('processingState');
    const errorState = document.getElementById('errorState');
    const errorMessage = document.getElementById('errorMessage');

    if (processingState) processingState.hidden = true;
    if (errorState) {
      errorState.hidden = false;
      if (errorMessage) errorMessage.textContent = msg;
    } else {
      alert(msg);
      location.reload();
    }
  }
};
