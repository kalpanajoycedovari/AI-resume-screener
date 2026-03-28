const API = '';
let selectedFiles = [];
let currentJobId = null;

async function createJob() {
  const title = document.getElementById('job-title').value.trim();
  const desc = document.getElementById('job-desc').value.trim();
  const reqSkills = document.getElementById('req-skills').value.trim();
  const niceSkills = document.getElementById('nice-skills').value.trim();
  const exp = document.getElementById('exp-years').value;

  if (!title || !desc) return showResult('job-result', 'error', 'Please fill in at least the job title and description.');

  const body = {
    title,
    description: desc,
    required_skills: reqSkills ? reqSkills.split(',').map(s => s.trim()) : [],
    nice_to_have_skills: niceSkills ? niceSkills.split(',').map(s => s.trim()) : [],
    experience_years: parseInt(exp) || 0
  };

  try {
    const res = await fetch(API + '/jobs/', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body) });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to create job');
    currentJobId = data.job_id;
    showResult('job-result', 'success', 'Job created! ID: <strong>' + data.job_id + '</strong>. You can now screen resumes against this job.');
    loadJobs();
  } catch(e) {
    showResult('job-result', 'error', 'Error: ' + e.message);
  }
}

async function loadJobs() {
  try {
    const res = await fetch(API + '/jobs/');
    const data = await res.json();
    const select = document.getElementById('screen-job-select');
    select.innerHTML = '<option value="">-- Select a job --</option>';
    (data.jobs || []).forEach(id => {
      const opt = document.createElement('option');
      opt.value = id;
      opt.textContent = id.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
      select.appendChild(opt);
    });
  } catch(e) { console.error('Could not load jobs', e); }
}

function handleFiles(input) {
  selectedFiles = Array.from(input.files);
  const list = document.getElementById('file-list');
  list.innerHTML = '';
  selectedFiles.forEach(f => {
    const div = document.createElement('div');
    div.className = 'file-item';
    div.innerHTML = '<span>&#128196;</span>' + f.name;
    list.appendChild(div);
  });
}

async function rankResumes() {
  const jobId = document.getElementById('screen-job-select').value;
  if (!jobId) return showResult('screen-result', 'error', 'Please select a job first.');
  if (selectedFiles.length === 0) return showResult('screen-result', 'error', 'Please upload at least one resume.');

  const formData = new FormData();
  selectedFiles.forEach(f => formData.append('files', f));

  showLoading(true);
  hideResult('screen-result');

  try {
    const res = await fetch(API + '/resumes/rank/' + jobId, { method: 'POST', body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Screening failed');
    showLoading(false);
    showResult('screen-result', 'success', 'Ranked ' + data.total_candidates + ' candidates! Scroll down to see the rankings.');
    renderRankings(data.rankings);
    document.getElementById('rankings').scrollIntoView({behavior: 'smooth'});
  } catch(e) {
    showLoading(false);
    showResult('screen-result', 'error', 'Error: ' + e.message);
  }
}

async function screenSingle() {
  const jobId = document.getElementById('screen-job-select').value;
  if (!jobId) return showResult('screen-result', 'error', 'Please select a job first.');
  if (selectedFiles.length === 0) return showResult('screen-result', 'error', 'Please upload a resume.');

  const formData = new FormData();
  formData.append('file', selectedFiles[0]);

  showLoading(true);
  hideResult('screen-result');

  try {
    const res = await fetch(API + '/resumes/screen/' + jobId, { method: 'POST', body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Screening failed');
    showLoading(false);
    showResult('screen-result', 'success', 'Screened successfully! Score: <strong>' + data.score + '/100</strong>');
    renderRankings([{rank:1, ...data}]);
    document.getElementById('rankings').scrollIntoView({behavior: 'smooth'});
  } catch(e) {
    showLoading(false);
    showResult('screen-result', 'error', 'Error: ' + e.message);
  }
}

function renderRankings(rankings) {
  const container = document.getElementById('rankings-container');
  if (!rankings || rankings.length === 0) return;

  container.innerHTML = '';
  rankings.forEach((r, i) => {
    const isTop = i === 0;
    const scorePercent = Math.round(r.score);
    const breakdown = r.score_breakdown || {};

    const bars = Object.entries(breakdown).map(([k, v]) => {
      const label = k.replace(/_/g, ' ');
      const max = k.includes('skill') ? 40 : k.includes('exp') ? 25 : k.includes('edu') ? 20 : 15;
      const pct = Math.min(100, Math.round((v / max) * 100));
      return '<div class="score-bar-row"><span class="score-bar-label">' + label + '</span><div class="score-bar-track"><div class="score-bar-fill" style="width:' + pct + '%"></div></div></div>';
    }).join('');

    const skills = (r.skills || []).slice(0,6).map(s => '<span class="skill-tag">' + s + '</span>').join('');

    const card = document.createElement('div');
    card.className = 'rank-card' + (isTop ? ' top-rank' : '');
    card.innerHTML =
      '<div class="rank-badge' + (isTop ? ' gold' : '') + '">' + r.rank + '</div>' +
      '<div class="rank-info">' +
        '<div class="rank-name">' + (r.name || 'Unknown') + '</div>' +
        '<div class="rank-email">' + (r.email || '') + '</div>' +
        '<div class="rank-skills">' + skills + '</div>' +
        '<div class="rank-recommendation">' + (r.recommendation || '') + '</div>' +
      '</div>' +
      '<div class="rank-score-block">' +
        '<div class="rank-score">' + scorePercent + '</div>' +
        '<div class="rank-score-label">out of 100</div>' +
        '<div class="score-bars">' + bars + '</div>' +
      '</div>';

    container.appendChild(card);
  });
}

function showResult(id, type, msg) {
  const el = document.getElementById(id);
  el.className = 'result-box ' + type;
  el.innerHTML = msg;
}

function hideResult(id) {
  const el = document.getElementById(id);
  el.className = 'result-box hidden';
}

function showLoading(show) {
  document.getElementById('screen-loading').classList.toggle('hidden', !show);
}

window.addEventListener('load', loadJobs);
