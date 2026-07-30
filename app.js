/* =========================================================
   NeuraMatch – AI Recommendation Engine
   Core Algorithm: Weighted Cosine Similarity
   DecodeLabs · AI Project 3
   ========================================================= */

// ─── DATASET ──────────────────────────────────────────────

const CATALOG = {
  movies: {
    tags: ['Action','Comedy','Drama','Sci-Fi','Horror','Romance','Thriller','Animation','Mystery','Fantasy'],
    items: [
      { title:'Inception',                        meta:'2010 · Christopher Nolan',     emoji:'🌀', tags:['Sci-Fi','Thriller','Mystery','Drama'] },
      { title:'The Dark Knight',                  meta:'2008 · Christopher Nolan',     emoji:'🦇', tags:['Action','Drama','Thriller','Mystery'] },
      { title:'Interstellar',                     meta:'2014 · Christopher Nolan',     emoji:'🚀', tags:['Sci-Fi','Drama','Fantasy','Mystery'] },
      { title:'Parasite',                         meta:'2019 · Bong Joon-ho',          emoji:'🎭', tags:['Drama','Thriller','Mystery','Comedy'] },
      { title:'Get Out',                          meta:'2017 · Jordan Peele',          emoji:'😨', tags:['Horror','Thriller','Mystery','Drama'] },
      { title:'La La Land',                       meta:'2016 · Damien Chazelle',       emoji:'🎺', tags:['Romance','Drama','Comedy','Fantasy'] },
      { title:'Avengers: Endgame',                meta:'2019 · Russo Brothers',        emoji:'⚡', tags:['Action','Sci-Fi','Fantasy','Drama'] },
      { title:'Spider-Man: Into the Spider-Verse',meta:'2018 · Animation',             emoji:'🕸️', tags:['Animation','Action','Sci-Fi','Fantasy'] },
      { title:'Everything Everywhere All at Once',meta:'2022 · EEAAO',                emoji:'🥢', tags:['Sci-Fi','Comedy','Action','Fantasy','Drama'] },
      { title:'Arrival',                          meta:'2016 · Denis Villeneuve',      emoji:'🛸', tags:['Sci-Fi','Drama','Mystery','Thriller'] },
      { title:'Knives Out',                       meta:'2019 · Rian Johnson',          emoji:'🔪', tags:['Mystery','Comedy','Thriller','Drama'] },
      { title:'Spirited Away',                    meta:'2001 · Hayao Miyazaki',        emoji:'🌊', tags:['Animation','Fantasy','Drama','Romance'] },
    ]
  },
  music: {
    tags: ['Pop','Hip-Hop','Rock','Electronic','Jazz','Classical','R&B','Indie','Metal','Lo-Fi'],
    items: [
      { title:'Random Access Memories',   meta:'Daft Punk · 2013',      emoji:'🤖', tags:['Electronic','Pop','Indie','Jazz'] },
      { title:'To Pimp a Butterfly',      meta:'Kendrick Lamar · 2015', emoji:'🦋', tags:['Hip-Hop','R&B','Jazz','Indie'] },
      { title:'The Dark Side of the Moon',meta:'Pink Floyd · 1973',      emoji:'🌙', tags:['Rock','Classical','Electronic','Indie'] },
      { title:'Blonde',                   meta:'Frank Ocean · 2016',    emoji:'🌊', tags:['R&B','Indie','Pop','Electronic'] },
      { title:'Midnights',                meta:'Taylor Swift · 2022',   emoji:'✨', tags:['Pop','Indie','Electronic','R&B'] },
      { title:'Demon Days',               meta:'Gorillaz · 2005',       emoji:'👹', tags:['Electronic','Hip-Hop','Rock','Indie'] },
      { title:'Discovery',                meta:'Daft Punk · 2001',      emoji:'💿', tags:['Electronic','Pop','R&B','Indie'] },
      { title:'Kind of Blue',             meta:'Miles Davis · 1959',    emoji:'🎷', tags:['Jazz','Classical','Indie'] },
      { title:'Nevermind',                meta:'Nirvana · 1991',        emoji:'🐟', tags:['Rock','Metal','Indie'] },
      { title:'Currents',                 meta:'Tame Impala · 2015',    emoji:'🌀', tags:['Indie','Electronic','Pop','Rock'] },
      { title:'Ctrl',                     meta:'SZA · 2017',            emoji:'🌺', tags:['R&B','Pop','Hip-Hop','Indie'] },
      { title:'Lofi Hip Hop Essentials',  meta:'Various Artists',       emoji:'☕', tags:['Lo-Fi','Hip-Hop','Jazz','Indie'] },
    ]
  },
  books: {
    tags: ['Fiction','Sci-Fi','Mystery','Fantasy','Non-Fiction','Romance','Thriller','Horror','Biography','Philosophy'],
    items: [
      { title:'Dune',                     meta:'Frank Herbert · 1965',         emoji:'🏜️', tags:['Sci-Fi','Fiction','Fantasy','Philosophy'] },
      { title:'The Name of the Wind',     meta:'Patrick Rothfuss · 2007',      emoji:'🌬️', tags:['Fantasy','Fiction','Romance','Mystery'] },
      { title:'Project Hail Mary',        meta:'Andy Weir · 2021',             emoji:'🛸', tags:['Sci-Fi','Fiction','Mystery','Non-Fiction'] },
      { title:'Gone Girl',                meta:'Gillian Flynn · 2012',         emoji:'💔', tags:['Thriller','Mystery','Fiction','Horror'] },
      { title:'Sapiens',                  meta:'Yuval Noah Harari · 2011',     emoji:'🦴', tags:['Non-Fiction','Biography','Philosophy','Sci-Fi'] },
      { title:"The Hitchhiker's Guide",   meta:'Douglas Adams · 1979',         emoji:'🌌', tags:['Sci-Fi','Fiction','Fantasy','Philosophy'] },
      { title:'Normal People',            meta:'Sally Rooney · 2018',          emoji:'💬', tags:['Romance','Fiction','Philosophy'] },
      { title:'The Shining',             meta:'Stephen King · 1977',          emoji:'🏨', tags:['Horror','Thriller','Mystery','Fiction'] },
      { title:'Thinking, Fast and Slow',  meta:'Daniel Kahneman · 2011',      emoji:'🧠', tags:['Non-Fiction','Philosophy','Biography'] },
      { title:'Mistborn',                 meta:'Brandon Sanderson · 2006',     emoji:'⚗️', tags:['Fantasy','Fiction','Mystery','Thriller'] },
      { title:'The Midnight Library',     meta:'Matt Haig · 2020',             emoji:'📚', tags:['Fiction','Fantasy','Philosophy','Romance'] },
      { title:'Atomic Habits',            meta:'James Clear · 2018',           emoji:'⚛️', tags:['Non-Fiction','Philosophy','Biography'] },
    ]
  },
  games: {
    tags: ['RPG','Action','Strategy','Horror','Puzzle','Open World','Shooter','Indie','Adventure','Simulation'],
    items: [
      { title:'The Witcher 3',         meta:'CD Projekt Red · 2015',    emoji:'⚔️', tags:['RPG','Open World','Action','Adventure'] },
      { title:'Elden Ring',            meta:'FromSoftware · 2022',      emoji:'💀', tags:['RPG','Action','Open World','Horror'] },
      { title:'Hollow Knight',         meta:'Team Cherry · 2017',       emoji:'🦋', tags:['Indie','Action','Adventure','Puzzle'] },
      { title:'Portal 2',             meta:'Valve · 2011',             emoji:'🔵', tags:['Puzzle','Indie','Adventure'] },
      { title:'Civilization VI',       meta:'2K Games · 2016',          emoji:'🌍', tags:['Strategy','Simulation','Open World'] },
      { title:'Resident Evil 4',       meta:'Capcom · 2023',            emoji:'🧟', tags:['Horror','Action','Shooter','Adventure'] },
      { title:'Stardew Valley',        meta:'ConcernedApe · 2016',      emoji:'🌾', tags:['Simulation','Indie','RPG','Open World'] },
      { title:'Hades',                 meta:'Supergiant Games · 2020',  emoji:'🔱', tags:['Action','RPG','Indie','Adventure'] },
      { title:'Outer Wilds',           meta:'Mobius Digital · 2019',    emoji:'🌠', tags:['Adventure','Puzzle','Open World','Indie'] },
      { title:'DOOM Eternal',          meta:'id Software · 2020',       emoji:'🔫', tags:['Shooter','Action','Horror'] },
      { title:'Disco Elysium',         meta:'ZA/UM · 2019',             emoji:'🕵️', tags:['RPG','Adventure','Puzzle','Indie'] },
      { title:'Total War: Shogun 2',   meta:'Creative Assembly · 2011', emoji:'⛩️', tags:['Strategy','Simulation','Action'] },
    ]
  }
};

// ─── STATE ────────────────────────────────────────────────

let state = { category: 'movies', selectedTags: new Set(), weights: {} };

// ─── INIT ─────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.category = btn.dataset.cat;
      state.selectedTags.clear();
      state.weights = {};
      renderTags();
      renderSliders();
      hideResults();
    });
  });
  renderTags();
});

// ─── RENDER TAGS ──────────────────────────────────────────

function renderTags() {
  const cloud = document.getElementById('tagCloud');
  cloud.innerHTML = '';
  CATALOG[state.category].tags.forEach(tag => {
    const btn = document.createElement('button');
    btn.className = 'tag' + (state.selectedTags.has(tag) ? ' selected' : '');
    btn.textContent = tag;
    btn.addEventListener('click', () => toggleTag(tag, btn));
    cloud.appendChild(btn);
  });
}

function toggleTag(tag, btn) {
  if (state.selectedTags.has(tag)) {
    state.selectedTags.delete(tag);
    delete state.weights[tag];
    btn.classList.remove('selected');
  } else {
    state.selectedTags.add(tag);
    state.weights[tag] = 5;
    btn.classList.add('selected');
  }
  renderSliders();
  hideResults();
}

// ─── RENDER SLIDERS ───────────────────────────────────────

function renderSliders() {
  const container = document.getElementById('slidersContainer');
  if (state.selectedTags.size === 0) {
    container.innerHTML = '<div class="empty-hint">← Select interests in Step 2 first</div>';
    return;
  }
  container.innerHTML = '';
  state.selectedTags.forEach(tag => {
    const val = state.weights[tag] ?? 5;
    const pct = ((val - 1) / 9 * 100).toFixed(0);
    const row = document.createElement('div');
    row.className = 'slider-row';
    row.innerHTML = `
      <span class="slider-label">${tag}</span>
      <div class="slider-track">
        <input type="range" min="1" max="10" value="${val}" style="--pct:${pct}%"
          id="slider-${tag.replace(/\s/g,'-')}" aria-label="${tag} weight" />
      </div>
      <span class="slider-val" id="val-${tag.replace(/\s/g,'-')}">${val}</span>
    `;
    const slider  = row.querySelector('input');
    const display = row.querySelector('.slider-val');
    slider.addEventListener('input', () => {
      const v = parseInt(slider.value);
      state.weights[tag] = v;
      display.textContent = v;
      slider.style.setProperty('--pct', ((v-1)/9*100).toFixed(0) + '%');
    });
    container.appendChild(row);
  });
}

// ─── COSINE SIMILARITY ────────────────────────────────────

function cosineSimilarity(userVec, itemVec, allTags) {
  let dot = 0, magU = 0, magI = 0;
  allTags.forEach(tag => {
    const u = userVec[tag] || 0;
    const i = itemVec[tag] || 0;
    dot  += u * i;
    magU += u * u;
    magI += i * i;
  });
  if (magU === 0 || magI === 0) return 0;
  return dot / (Math.sqrt(magU) * Math.sqrt(magI));
}

// ─── GENERATE RECOMMENDATIONS ─────────────────────────────

function generateRecommendations() {
  if (state.selectedTags.size === 0) {
    alert('Please select at least one interest tag first!');
    return;
  }
  const allTags = CATALOG[state.category].tags;
  const items   = CATALOG[state.category].items;
  const userVec = {};
  allTags.forEach(t => { userVec[t] = state.weights[t] || 0; });

  const scored = items.map(item => {
    const itemVec = {};
    allTags.forEach(t => { itemVec[t] = item.tags.includes(t) ? 1 : 0; });
    const score       = cosineSimilarity(userVec, itemVec, allTags);
    const matchedTags = item.tags.filter(t => state.selectedTags.has(t));
    return { ...item, score, matchedTags };
  });

  scored.sort((a, b) => b.score - a.score);
  renderScoreBars(scored);
  renderResults(scored);
}

// ─── RENDER SCORE BARS ────────────────────────────────────

function renderScoreBars(scored) {
  const panel = document.getElementById('step-scores');
  const bars  = document.getElementById('scoreBars');
  panel.classList.remove('hidden');
  bars.innerHTML = '';
  const top = scored[0].score || 1;

  scored.forEach((item, i) => {
    const pct = top > 0 ? (item.score / top * 100).toFixed(1) : 0;
    const row = document.createElement('div');
    row.className = 'score-item';
    row.style.animationDelay = `${i * 0.06}s`;
    row.innerHTML = `
      <span class="score-name">${item.emoji} ${item.title}</span>
      <div class="score-bar-wrap"><div class="score-bar-fill" id="bar-${i}"></div></div>
      <span class="score-pct">${(item.score * 100).toFixed(1)}%</span>
    `;
    bars.appendChild(row);
    setTimeout(() => { document.getElementById(`bar-${i}`).style.width = pct + '%'; }, 50 + i * 60);
  });
  panel.scrollIntoView({ behavior:'smooth', block:'start' });
}

// ─── RENDER RESULTS ───────────────────────────────────────

const RANK_EMOJIS = ['🥇','🥈','🥉','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟','#️⃣','#️⃣'];

function renderResults(scored) {
  const panel = document.getElementById('step-results');
  const grid  = document.getElementById('resultsGrid');
  panel.classList.remove('hidden');
  grid.innerHTML = '';

  scored.slice(0, 6).forEach((item, i) => {
    const matchPct  = (item.score * 100).toFixed(0);
    const card      = document.createElement('div');
    card.className  = 'result-card';
    card.style.animationDelay = `${i * 0.08}s`;

    const allTagsHTML = item.tags.map(t =>
      `<span class="result-tag ${item.matchedTags.includes(t) ? 'matched' : ''}">${t}</span>`
    ).join('');

    card.innerHTML = `
      <div class="result-rank">${RANK_EMOJIS[i]}</div>
      <div class="result-title">${item.emoji} ${item.title}</div>
      <div class="result-meta">${item.meta}</div>
      <div class="result-tags">${allTagsHTML}</div>
      <div class="match-score">
        <span class="match-label">AI Match Score</span>
        <span class="match-value">${matchPct}%</span>
      </div>
    `;
    grid.appendChild(card);
  });
  panel.scrollIntoView({ behavior:'smooth', block:'start' });
}

// ─── HIDE RESULTS ─────────────────────────────────────────

function hideResults() {
  document.getElementById('step-scores').classList.add('hidden');
  document.getElementById('step-results').classList.add('hidden');
}

// ─── RESET ────────────────────────────────────────────────

function resetApp() {
  state.selectedTags.clear();
  state.weights = {};
  renderTags();
  renderSliders();
  hideResults();
  window.scrollTo({ top:0, behavior:'smooth' });
}
