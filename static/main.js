const socket = io();

const form = document.getElementById('downloadForm');
const status = document.getElementById('status');
const result = document.getElementById('result');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const url = document.getElementById('url').value.trim();
  const source = document.querySelector('input[name="source"]:checked').value;
  if (!url) return;
  status.textContent = 'Requesting download...';
  result.innerHTML = '';
  socket.emit('download', { url, source });
});

socket.on('download_complete', (data) => {
  status.textContent = 'Ready: ' + data.filename;
  result.innerHTML = '';
  const a = document.createElement('a');
  a.href = data.url;
  a.download = data.filename;
  a.textContent = 'Click to download ' + data.filename;
  result.appendChild(a);
  // optionally trigger automatic download
  setTimeout(() => a.click(), 300);
});

socket.on('error', (data) => {
  status.textContent = 'Error: ' + (data && data.message ? data.message : 'unknown');
});

socket.on('connect', () => {
  status.textContent = 'Connected';
});

socket.on('disconnect', () => {
  status.textContent = 'Disconnected';
});
