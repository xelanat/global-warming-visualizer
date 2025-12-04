// main.js - Global Warming Visualizer
// Loads frames from img/ and enables slider/play controls

const IMG_DIR = 'img/';
const EXT = '.png';
const MAX_FRAMES = 200; // safety limit
const PLAY_INTERVAL = 100; // ms per frame

const frameImage = document.getElementById('frameImage');
const frameRange = document.getElementById('frameRange');
const frameLabel = document.getElementById('frameLabel');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const loading = document.getElementById('loading');

let frames = [];
let current = 0;
let playing = false;
let playTimer = null;

async function fetchFramesList() {
  try {
    const resp = await fetch(IMG_DIR + 'frames.json');
    if (!resp.ok) throw new Error('frames.json not found');
    const list = await resp.json();
    console.log('Frames list loaded:', list);
    return list;
  } catch (err) {
    console.error('Error loading frames.json:', err);
    return [];
  }
}

function updateUI() {
  if (!frames.length) {
    frameImage.style.display = 'none';
    frameLabel.textContent = 'No frames found';
    frameRange.disabled = true;
    prevBtn.disabled = true;
    nextBtn.disabled = true;
    return;
  }
  frameImage.style.display = '';
  frameImage.src = frames[current].src;
  frameLabel.textContent = `Frame ${current + 1} / ${frames.length}`;
  frameRange.value = current;
  frameRange.max = frames.length - 1;
  frameRange.disabled = false;
  prevBtn.disabled = current === 0;
  nextBtn.disabled = current === frames.length - 1;
}

function gotoFrame(idx) {
  current = Math.max(0, Math.min(frames.length - 1, idx));
  updateUI();
}

function nextFrame() {
  if (current < frames.length - 1) {
    gotoFrame(current + 1);
    return true;
  }
  return false;
}

function prevFrame() {
  if (current > 0) {
    gotoFrame(current - 1);
    return true;
  }
  return false;
}

function play() {
  if (playing || !frames.length) return;
  playing = true;
  playTimer = setInterval(() => {
    if (!nextFrame()) {
      pause();
    }
  }, PLAY_INTERVAL);
}

function pause() {
  playing = false;
  if (playTimer) clearInterval(playTimer);
  playTimer = null;
}

function togglePlay() {
  if (playing) pause();
  else play();
}

frameRange.addEventListener('input', e => gotoFrame(Number(e.target.value)));
prevBtn.addEventListener('click', prevFrame);
nextBtn.addEventListener('click', nextFrame);
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft') prevFrame();
  if (e.key === 'ArrowRight') nextFrame();
});

window.addEventListener('DOMContentLoaded', async () => {
  loading.style.display = '';
  frames = await fetchFramesList();
  console.log(`Loaded ${frames.length} frames.`);
  loading.style.display = 'none';
  current = 0;
  updateUI();
});
