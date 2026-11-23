'use strict';

const projects = [...window.PORTFOLIO_PROJECTS, ...window.PORTFOLIO_NEW_PROJECTS, ...window.PORTFOLIO_ADDITIONS];
const home = document.body.dataset.page === 'home';
const format = (value, digits = 1) => Number(value).toLocaleString('en-CA', {minimumFractionDigits: digits, maximumFractionDigits: digits});
const typeName = p => p.type === 'experience' ? 'Professional experience' : 'Real public data';
const projectHref = p => 'project.html?case=' + encodeURIComponent(p.id);
const external = (url, label) => '<a href="' + escapeHtml(url) + '" target="_blank" rel="noopener noreferrer">' + label + '</a>';
const escapeHtml = str => String(str).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const workflow = p => p.repoUrl.startsWith('resources/') ? '<a href="' + escapeHtml(p.repoUrl) + '" download>' + (p.type === 'experience' ? 'Download case study workflow' : 'Download Python &amp; SQL') + '</a>' : external(p.repoUrl, 'View code');
const dataBadge = p => '<span class="badge ' + (p.type === 'experience' ? 'experience' : 'actual') + '"><span class="badge-dot"></span>' + typeName(p) + '</span>';

function initMenu() {
  const button = document.querySelector('.menu-button');
  const links = document.querySelector('.nav-links');
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!expanded));
    links.classList.toggle('open', !expanded);
  });
  links.addEventListener('click', e => {
    if (e.target.closest('a')) {
      button.setAttribute('aria-expanded', 'false');
      links.classList.remove('open');
    }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && links.classList.contains('open')) {
      links.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
      button.focus();
    }
  });
}

function createHome() {
  const heroChart = document.querySelector('#hero-chart');
  const series = projects[0].views[0].rows.filter(r => r.year === '2019–2024 · actual/revised');
  const max = Math.max(...series.map(r => r.value));
  series.forEach(r => {
    const bar = document.createElement('div');
    bar.className = 'hero-bar';
    bar.setAttribute('title', r.label + ' · $' + format(r.value, 2) + 'B');
    bar.setAttribute('aria-label', r.label + ': ' + format(r.value, 2) + ' billion Canadian dollars');
    bar.innerHTML = '<span class="hero-bar-track"><span class="hero-bar-fill" style="height:' + (r.value / max * 100) + '%"></span></span><span class="bar-year">' + r.label + '</span>';
    heroChart.append(bar);
  });

  const groups = document.querySelector('#project-groups');
  for (const type of ['system', 'population', 'business']) {
    const section = document.createElement('section');
    section.className = 'data-group';
    section.dataset.group = type;
    section.setAttribute('aria-labelledby', 'group-' + type);
    const groupProjects = projects.filter(p => p.group === type);
    const label = {system:'Health system & finance', population:'Population health & equity', business:'Workforce & business analytics'}[type];
    const desc = {system:'Explore expenditure, access to surgery and hospital performance using published health system data.', population:'Explore disease surveillance, mental health and regional health equity using published population estimates.', business:'Explore labour markets, sales forecasting, procurement analysis and business process improvement.'}[type];
    section.innerHTML = '<div class="group-head"><div><h3 id="group-' + type + '">' + label + '</h3><p>' + desc + '</p></div></div><div class="project-grid"></div>';
    for (const p of groupProjects) section.querySelector('.project-grid').append(createCard(p));
    groups.append(section);
  }
  const filterButtons = document.querySelectorAll('.filter');
  filterButtons.forEach(button => button.addEventListener('click', () => {
    const active = button.dataset.filter;
    filterButtons.forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    document.querySelectorAll('.data-group').forEach(group => {
      group.hidden = active !== 'all' && active !== group.dataset.group;
    });
    document.getElementById('filter-status').textContent = 'Showing ' + (active === 'all' ? projects.length : projects.filter(p => p.group === active).length) + ' projects';
  }));
}

function createCard(p) {
  const card = document.createElement('article');
  card.className = 'project-card';
  card.innerHTML = '<div class="card-meta">' + dataBadge(p) + '<span class="period">' + escapeHtml(p.period) + '</span></div>' +
    '<p class="domain">' + escapeHtml(p.category) + '</p><h3>' + escapeHtml(p.title) + '</h3>' +
    '<p class="card-summary">' + escapeHtml(p.summary) + '</p>' +
    '<div class="card-metric"><div><div class="metric-number">' + escapeHtml(p.highlightValue) +
    '</div><div class="metric-label">' + escapeHtml(p.highlight) + '</div></div></div>' +
    '<div class="tags">' + p.tools.map(tool => '<span>' + escapeHtml(tool) + '</span>').join('') + '</div>' +
    '<div class="card-actions"><a href="' + projectHref(p) + '" aria-label="Explore ' + escapeHtml(p.title) + (p.type === 'experience' ? ' case study">Explore case study</a>' : ' dashboard">Explore dashboard</a>') +
    workflow(p) + '</div>';
  return card;
}

function createProject() {
  const root = document.querySelector('#project-detail');
  const id = new URLSearchParams(location.search).get('case');
  const p = projects.find(project => project.id === id);
  if (!p) {
    root.innerHTML = '<section class="shell no-results"><h1>Choose a case study</h1><p>Explore one of ten projects and case studies.</p><a class="button primary" href="index.html#projects">View projects</a></section>';
    return;
  }
  document.title = p.title + ' | Ikenna Nwogu';
  const statusText = p.statusText || (p.id === 'expenditure' ? 'CIHI’s published national figures distinguish historical actual and revised spending from forecasts for 2025–2026.' :
    p.id === 'ontario' ? 'The FAO publishes aggregate Ontario figures. Surgery figures from March 2021 onward include an estimation assumption. Waiting times are estimated from surgical throughput and waitlist data.' :
    'Published Nova Scotia statistics based on Canadian Chronic Disease Surveillance System data. The dashboard reports crude prevalence for adults aged 20 and older.');
  const idx = projects.indexOf(p);
  const previous = projects[(idx + projects.length - 1) % projects.length];
  const next = projects[(idx + 1) % projects.length];
  if (p.type === 'experience') { createExperienceCase(root, p, previous, next); return; }
  root.innerHTML = '<section class="project-intro"><div class="shell">' +
    '<div class="breadcrumb"><a href="index.html#projects">All projects</a><label class="project-picker">Switch project<select id="project-picker">' +
    projects.map(x => '<option value="' + x.id + '" ' + (x === p ? 'selected' : '') + '>' + escapeHtml(x.title) + '</option>').join('') + '</select></label></div>' +
    '<div class="intro-kickers">' + dataBadge(p) + '<span class="domain">' + escapeHtml(p.category) + '</span><span class="period">' + escapeHtml(p.period) + '</span></div>' +
    '<h1>' + escapeHtml(p.title) + '</h1><p class="question">' + escapeHtml(p.question) + '</p><p class="intro-summary">' + escapeHtml(p.summary) + '</p>' +
    '<div class="data-status ' + p.type + '"><strong>' + 'Official-source data' + '</strong><span>' + escapeHtml(statusText) + '</span></div><p class="intro-source">' + 'Source: ' + external(p.sourceUrl, escapeHtml(p.source)) + '</p></div></section>' +
    '<section class="project-body"><div class="shell"><div class="summary-grid">' +
    p.cards.map(c => '<div class="summary-card ' + p.type + (c.label.toLowerCase().includes('forecast') ? ' forecast-card' : '') + '"><strong>' + escapeHtml(c.value) + '</strong><span>' + escapeHtml(c.label) + '</span></div>').join('') + '</div>' +
    '<div class="dashboard-layout"><div class="dashboard-main"><section class="dashboard-panel"><div class="panel-heading"><div><h2>Explore the dashboard</h2><p>Select an indicator and reporting period to compare results.</p></div>' + dataBadge(p) + '</div>' +
    '<div class="controls"><label class="control" for="indicator">Indicator<select id="indicator"></select></label><label class="control" for="period">Reporting period<select id="period"></select></label></div>' +
    '<div class="chart-top"><h3 id="chart-title">Data comparison</h3><label class="sort-label" id="sort-wrap">Sort<select id="sort"><option value="original">Source order</option><option value="desc">Highest first</option><option value="asc">Lowest first</option><option value="alpha">Name A–Z</option></select></label></div>' +
    '<p id="chart-explain" class="chart-explain"></p><div id="chart" class="chart" aria-label="Interactive chart"></div><div class="legend" id="legend" hidden></div>' +
    '<div class="chart-footer"><p id="selection-info" role="status"></p><button class="download" id="download" type="button">Download selection CSV</button></div></section>' +
    '<section class="dashboard-panel table-panel"><h2>Data table</h2><p class="chart-explain">Review the exact chart values, data-quality flags and source references.</p><div class="table-scroll" tabindex="0" aria-label="Scrollable data table"><table><thead id="table-head"></thead><tbody id="table-body"></tbody></table></div><p class="table-caption" id="table-caption"></p></section></div>' +
    '<aside aria-label="Case study information"><section class="side-panel"><h2>Case study details</h2><h3>Coverage</h3><p>' + escapeHtml(p.coverage) + '</p><h3>Methods</h3><ul>' + p.methods.map(m => '<li>' + escapeHtml(m) + '</li>').join('') + '</ul>' +
    '<div class="tags">' + p.tools.map(tool => '<span>' + escapeHtml(tool) + '</span>').join('') + '</div><div class="source-block"><h3>' + 'Data source' + '</h3><p>' + escapeHtml(p.source) + '</p>' +
    external(p.sourceUrl, 'Open official source') +
    (p.sourceLinks || []).map(link => external(link.url, escapeHtml(link.name))).join('') +
    external(p.evidence, 'Findings and methodology') + workflow(p) + (p.biLink ? '<a download href="' + escapeHtml(p.biLink.url) + '">' + escapeHtml(p.biLink.label) + '</a>' : '') + '</div></section>' +
    (p.findings ? '<section class="side-panel findings-panel"><h2>Key findings</h2><ul>' + p.findings.map(f => '<li>' + escapeHtml(f) + '</li>').join('') + '</ul></section>' : '') +
    '<section class="side-panel limits-panel ' + p.type + '"><h2>Interpretation &amp; limitations</h2><p>' + escapeHtml(p.limits) + '</p></section></aside></div></div></section>' +
    '<div class="project-nav"><div class="shell project-nav-inner"><a href="' + projectHref(previous) + '">Previous: ' + escapeHtml(previous.title) + '</a><a class="button secondary" href="index.html#projects">All projects</a><a href="' + projectHref(next) + '">Next: ' + escapeHtml(next.title) + '</a></div></div>';
  document.getElementById('project-picker').addEventListener('change', e => {
    location.href = 'project.html?case=' + encodeURIComponent(e.target.value);
  });
  setupDashboard(p);
}


function createExperienceCase(root, p, previous, next) {
  const options = projects.map(x => '<option value="' + escapeHtml(x.id) + '" ' + (x === p ? 'selected' : '') + '>' + escapeHtml(x.title) + '</option>').join('');
  const requirements = p.requirements.map(r => '<tr><th scope="row">' + escapeHtml(r.id) + '</th><td>' + escapeHtml(r.need) + '</td><td>' + escapeHtml(r.control) + '</td><td>' + escapeHtml(r.acceptance) + '</td></tr>').join('');
  root.innerHTML = '<section class="project-intro"><div class="shell"><div class="breadcrumb"><a href="index.html#projects">All projects</a><label class="project-picker">Switch project<select id="project-picker">' + options + '</select></label></div>' +
    '<div class="intro-kickers">' + dataBadge(p) + '<span class="domain">' + escapeHtml(p.category) + '</span><span class="period">' + escapeHtml(p.period) + '</span></div><h1>' + escapeHtml(p.title) + '</h1><p class="question">' + escapeHtml(p.question) + '</p><p class="intro-summary">' + escapeHtml(p.summary) + '</p>' +
    '<div class="data-status experience"><strong>Experience evidence and portfolio prototype</strong><span>' + escapeHtml(p.statusText) + '</span></div></div></section>' +
    '<section class="project-body"><div class="shell"><div class="summary-grid">' + p.cards.map(c => '<div class="summary-card experience"><strong>' + escapeHtml(c.value) + '</strong><span>' + escapeHtml(c.label) + '</span></div>').join('') + '</div>' +
    '<div class="dashboard-layout"><div class="dashboard-main"><section class="dashboard-panel"><div class="panel-heading"><div><h2>Explore the workflow</h2><p>Select a stage to review the activity, proposed control and handoff.</p></div></div><div class="process-steps" role="group" aria-label="Workflow stages">' + p.steps.map((step,i) => '<button type="button" class="process-step" data-step="' + i + '" aria-pressed="' + (i === 0) + '"><span>' + (i+1) + '</span><strong>' + escapeHtml(step.name) + '</strong></button>').join('') + '</div><div id="process-detail" class="process-detail" aria-live="polite"></div></section>' +
    '<section class="dashboard-panel table-panel"><h2>Requirements and acceptance criteria</h2><p class="chart-explain">Proposed controls for reliable reporting. These criteria form the portfolio analysis and prototype.</p><div class="table-scroll" tabindex="0" aria-label="Requirements matrix"><table><thead><tr><th scope="col">ID</th><th scope="col">Business need</th><th scope="col">Proposed control</th><th scope="col">Acceptance criterion</th></tr></thead><tbody>' + requirements + '</tbody></table></div></section>' +
    '<section class="dashboard-panel"><h2>Reporting automation prototype</h2><p class="chart-explain">Enter authorized aggregate counts in the blank CSV template. The Python workflow validates required fields, reconciles counts, rejects duplicate cycle identifiers and generates a reporting summary. It contains no actual participant data.</p><div class="actions"><a class="button primary" href="resources/process/workflow.zip" download>Download workflow</a><a class="button secondary" href="resources/process/aggregate_cycle_template.csv" download>Download blank CSV</a></div></section></div>' +
    '<aside aria-label="Case study information"><section class="side-panel"><h2>Case study details</h2><h3>Experience</h3><p>' + escapeHtml(p.coverage) + '</p><h3>Methods</h3><ul>' + p.methods.map(m => '<li>' + escapeHtml(m) + '</li>').join('') + '</ul><div class="tags">' + p.tools.map(t => '<span>' + escapeHtml(t) + '</span>').join('') + '</div><div class="source-block"><h3>Source context</h3><p>' + escapeHtml(p.source) + '</p>' + external(p.sourceUrl,'OFE organization information') + external(p.evidence,'Evidence and methodology') + workflow(p) + '</div></section>' +
    '<section class="side-panel findings-panel"><h2>Reported outcomes</h2><ul>' + p.findings.map(f => '<li>' + escapeHtml(f) + '</li>').join('') + '</ul></section><section class="side-panel limits-panel experience"><h2>Interpretation &amp; limitations</h2><p>' + escapeHtml(p.limits) + '</p></section></aside></div></div></section>' +
    '<div class="project-nav"><div class="shell project-nav-inner"><a href="' + projectHref(previous) + '">Previous: ' + escapeHtml(previous.title) + '</a><a class="button secondary" href="index.html#projects">All projects</a><a href="' + projectHref(next) + '">Next: ' + escapeHtml(next.title) + '</a></div></div>';
  document.getElementById('project-picker').addEventListener('change', e => { location.href = 'project.html?case=' + encodeURIComponent(e.target.value); });
  const buttons = [...document.querySelectorAll('.process-step')];
  function showStep(index) {
    const step = p.steps[index];
    buttons.forEach((button,i) => button.setAttribute('aria-pressed', String(i === index)));
    document.getElementById('process-detail').innerHTML = '<h3>' + escapeHtml(step.name) + '</h3><div class="process-facts"><div><strong>Role</strong><p>' + escapeHtml(step.role) + '</p></div><div><strong>Activity</strong><p>' + escapeHtml(step.activity) + '</p></div><div><strong>Proposed control</strong><p>' + escapeHtml(step.control) + '</p></div><div><strong>Deliverable</strong><p>' + escapeHtml(step.deliverable) + '</p></div></div>';
  }
  buttons.forEach((button,i) => button.addEventListener('click', () => showStep(i)));
  showStep(0);
}

function setupDashboard(p) {
  const indicator = document.getElementById('indicator');
  const period = document.getElementById('period');
  const sort = document.getElementById('sort');
  const chart = document.getElementById('chart');
  const legend = document.getElementById('legend');
  let rows = [];
  let allRows = [];
  let view;
  const optGroups = new Map();
  p.views.forEach((v,i) => {
    const option = new Option(v.name, String(i));
    if (v.section) {
      if (!optGroups.has(v.section)) {
        const group = document.createElement('optgroup');
        group.label = v.section;
        optGroups.set(v.section, group);
        indicator.append(group);
      }
      optGroups.get(v.section).append(option);
    } else {
      indicator.add(option);
    }
  });
  function setPeriods() {
    view = p.views[Number(indicator.value)];
    period.replaceChildren();
    for (const year of view.years) {
      period.add(new Option(year === 'All' ? (view.chart === 'line' ? 'All years' : 'Full sample') : year, year));
    }
    period.value = view.defaultYear || view.years[view.years.length - 1];
    period.disabled = period.options.length === 1;
    sort.value = 'original';
    document.getElementById('sort-wrap').hidden = view.chart === 'line';
  }
  function render() {
    view = p.views[Number(indicator.value)];
    allRows = view.rows.filter(row => String(row.year) === period.value);
    rows = allRows.filter(row => row.value !== null);
    if (sort.value === 'desc' && view.chart !== 'line') rows.sort((a,b) => b.value - a.value);
    if (sort.value === 'asc' && view.chart !== 'line') rows.sort((a,b) => a.value - b.value);
    if (sort.value === 'alpha' && view.chart !== 'line') rows.sort((a,b) => String(a.label).localeCompare(String(b.label)));
    const withheld = allRows.filter(row => row.value === null);
    const tableRows = [...rows, ...withheld];
    document.getElementById('chart-title').textContent = view.name;
    document.getElementById('chart-explain').textContent = view.explain;
    chart.className = 'chart';
    chart.replaceChildren();
    const forecast = rows.some(r => r.status === 'Forecast');
    const confidence = rows.some(r => r.ciLower != null && r.ciUpper != null);
    const caution = rows.some(r => r.status === 'Use with caution');
    legend.hidden = !forecast && !confidence && !caution;
    legend.innerHTML = (forecast ? '<span><i></i>Actual/revised</span><span><i class="forecast-key"></i>Forecast</span>' : '') +
      (confidence ? '<span><i class="confidence-key"></i>95% confidence interval</span>' : '') +
      (caution ? '<span><i class="caution-key"></i>Use with caution</span>' : '');
    if (view.chart === 'line') buildLineChart(chart, rows, view);
    else buildBarChart(chart, rows, view);
    const withStatus = tableRows.some(r => r.status);
    const withCI = tableRows.some(r => r.ciLower != null && r.ciUpper != null);
    document.getElementById('table-head').innerHTML = '<tr><th scope="col">Group / year</th><th scope="col" class="numeric">Value</th>' +
      (withCI ? '<th scope="col">95% CI</th>' : '') + (withStatus ? '<th scope="col">Status</th>' : '') +
      '<th scope="col">' + escapeHtml(view.denominatorLabel || 'Source / denominator') + '</th></tr>';
    const tbody = document.getElementById('table-body');
    tbody.replaceChildren();
    for (const r of tableRows) {
      const tr = document.createElement('tr');
      const th = document.createElement('th');
      th.scope = 'row';
      th.textContent = r.label;
      tr.append(th);
      const value = document.createElement('td');
      value.className = 'numeric';
      value.textContent = r.value === null ? '—' : format(r.value, view.digits ?? 1);
      tr.append(value);
      if (withCI) {
        const ci = document.createElement('td');
        ci.className = 'confidence-cell';
        ci.textContent = confidenceText(r);
        tr.append(ci);
      }
      if (withStatus) {
        const status = document.createElement('td');
        status.textContent = r.status || '—';
        if (r.status === 'Forecast') status.className = 'status-forecast';
        else if (r.status === 'Use with caution') status.className = 'status-caution';
        else if (r.value === null) status.className = 'status-withheld';
        tr.append(status);
      }
      const n = document.createElement('td');
      if (r.sourceUrl) {
        const link = document.createElement('a');
        link.href = r.sourceUrl; link.target = '_blank'; link.rel = 'noopener noreferrer';
        link.className = 'table-source-link'; link.textContent = r.n;
        n.append(link);
      } else n.textContent = r.n ?? '—';
      tr.append(n);
      tbody.append(tr);
    }
    document.getElementById('selection-info').textContent = rows.length + ' values' +
      (withheld.length ? ' · ' + withheld.length + ' withheld (table only)' : '') +
      (caution ? ' · quality flags shown' : '');
    document.getElementById('table-caption').textContent = typeName(p) + ' · ' + view.name +
      (withheld.length ? ' · suppressed or unavailable values are shown without a number.' : '');
  }
  indicator.addEventListener('change', () => { setPeriods(); render(); });
  period.addEventListener('change', render);
  sort.addEventListener('change', render);
  document.getElementById('download').addEventListener('click', () => {
    const quote = val => '"' + String(val ?? '').replaceAll('"','""') + '"';
    const headers = ['data_type','indicator','selection','group_or_year','value','unit','confidence_lower','confidence_upper','status','source_id','source_reference','source_url','source_context','notes'];
    const selectedRows = [...rows, ...allRows.filter(r => r.value === null)];
    const data = [headers, ...selectedRows.map(r => [typeName(p),view.name,period.value,r.label,r.value,r.unit || '',r.ciLower,r.ciUpper,r.status || '',r.sourceId || '',r.sourceRef || r.n || '',r.sourceUrl || p.sourceUrl,r.n || '',r.note || ''])];
    const blob = new Blob([data.map(row => row.map(quote).join(',')).join('\r\n') + '\r\n'], {type:'text/csv;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = p.id + '-' + p.type + '-selection.csv';
    document.body.append(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  setPeriods();
  render();
  let lastWidth = chart.clientWidth;
  const observer = new ResizeObserver(() => {
    if (view.chart === 'line' && chart.clientWidth !== lastWidth) {
      lastWidth = chart.clientWidth;
      render();
    }
  });
  observer.observe(chart);
}
function confidenceText(r) {
  if (r.ciLower == null || r.ciUpper == null) return '—';
  const digits = r.sourceId?.startsWith('CIHI') ? 2 : 1;
  return format(r.ciLower, digits) + '–' + format(r.ciUpper, digits);
}
function buildBarChart(chart, rows, view) {
  if (!rows.length) { chart.textContent = 'No groups meet the reporting criteria for this selection.'; return; }
  chart.classList.add('bar-chart');
  const max = Math.max(...rows.map(r => Math.max(r.value, r.ciUpper ?? r.value)), .001);
  const min = Math.min(0, ...rows.map(r => r.value));
  const span = max - min;
  const zero = -min / span * 100;
  for (const r of rows) {
    const item = document.createElement('div');
    item.className = 'data-row';
    item.tabIndex = 0;
    const ci = r.ciLower != null && r.ciUpper != null;
    const description = r.label + ', ' + format(r.value, view.digits ?? 1) +
      (ci ? ', 95% CI ' + confidenceText(r) : '') + (r.status === 'Use with caution' ? ', use with caution' : '');
    item.setAttribute('aria-label', description);
    item.title = description + ' · ' + (r.n ?? '');
    const whisker = ci ? '<i class="ci-range" style="left:' + (100*(r.ciLower-min)/span) + '%;width:' + (100*(r.ciUpper-r.ciLower)/span) + '%"></i>' : '';
    const left = r.value < 0 ? (r.value-min)/span*100 : zero;
    const length = Math.abs(r.value)/span*100;
    const zeroLine = min < 0 ? '<span class="zero-line" style="left:' + zero + '%"></span>' : '';
    item.innerHTML = '<span class="bar-label">' + escapeHtml(r.label) + '</span><span class="data-track" aria-hidden="true"><span class="data-fill' +
      (r.status === 'Use with caution' ? ' caution-fill' : '') + (r.value < 0 ? ' negative-fill' : '') + '" style="display:block;position:absolute;left:' + left + '%;width:' + length + '%"></span>' + zeroLine + whisker + '</span><span class="bar-value">' + format(r.value, view.digits ?? 1) + '</span>';
    chart.append(item);
  }
}
function buildLineChart(chart, rows, view) {
  if (!rows.length) { chart.textContent = 'No values for this selection.'; return; }
  const width = Math.max(280, Math.min(680, Math.floor(chart.clientWidth))), height = width < 450 ? 260 : 320;
  const left = width < 450 ? 54 : 70, right = width < 450 ? 13 : 27, top = 23, bottom = 42;
  const plotWidth = width - left - right, plotHeight = height - top - bottom;
  const maxValue = Math.max(...rows.map(r => Math.max(r.value, r.ciUpper ?? r.value)), .001);
  const step = Math.pow(10, Math.floor(Math.log10(maxValue))) / 2;
  const max = Math.ceil(maxValue / step) * step;
  const x = i => left + (rows.length === 1 ? plotWidth / 2 : i / (rows.length - 1) * plotWidth);
  const y = value => top + plotHeight - value / max * plotHeight;
  const fmt = v => Number(v).toLocaleString('en-CA', {maximumFractionDigits: max < 1 ? 3 : 1});
  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
  svg.setAttribute('class', 'line-chart');
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', view.name + ' over time. Each point is focusable, and all values are in the data table.');
  for (let i = 0; i <= 4; i++) {
    const val = max * i / 4;
    const py = y(val);
    svg.insertAdjacentHTML('beforeend','<line class="grid-line" x1="' + left + '" y1="' + py + '" x2="' + (width - right) + '" y2="' + py + '"></line><text class="axis-label" text-anchor="end" x="' + (left - 11) + '" y="' + (py + 4) + '">' + fmt(val) + '</text>');
  }
  svg.insertAdjacentHTML('beforeend','<line class="axis-line" x1="' + left + '" y1="' + y(0) + '" x2="' + (width-right) + '" y2="' + y(0) + '"/>');
  const actualPoints = [], forecastPoints = [];
  rows.forEach((row,i) => {
    const coords = x(i) + ',' + y(row.value);
    if (row.status === 'Forecast') {
      if (forecastPoints.length === 0 && actualPoints.length) forecastPoints.push(actualPoints[actualPoints.length-1]);
      forecastPoints.push(coords);
    } else actualPoints.push(coords);
  });
  if (actualPoints.length) svg.insertAdjacentHTML('beforeend', '<polyline class="actual-line" points="' + actualPoints.join(' ') + '"></polyline>');
  if (forecastPoints.length) svg.insertAdjacentHTML('beforeend', '<polyline class="forecast-line" points="' + forecastPoints.join(' ') + '"></polyline>');
  const labelStep = Math.max(1, Math.ceil((rows.length - 1) / (width < 450 ? 3 : 6)));
  rows.forEach((r,i) => {
    if (i % labelStep === 0 || i === rows.length-1 && (i-1)%labelStep !== 0) {
      svg.insertAdjacentHTML('beforeend', '<text class="axis-label" text-anchor="middle" x="' + x(i) + '" y="' + (height-16) + '">' + escapeHtml(r.axisLabel || r.label) + '</text>');
    }
  });
  const tooltip = document.createElement('div');
  tooltip.className = 'chart-tooltip';
  tooltip.hidden = true;
  tooltip.setAttribute('role','tooltip');
  rows.forEach((r,i) => {
    if (r.ciLower != null && r.ciUpper != null) {
      const px = x(i), lower = y(r.ciLower), upper = y(r.ciUpper);
      svg.insertAdjacentHTML('beforeend','<path class="line-ci" d="M' + (px-4) + ' ' + lower + ' H' + (px+4) + ' M' + px + ' ' + lower + ' V' + upper + ' M' + (px-4) + ' ' + upper + ' H' + (px+4) + '"></path>');
    }
    const point = document.createElementNS('http://www.w3.org/2000/svg','circle');
    point.setAttribute('class',r.status === 'Forecast' ? 'forecast-point' : 'actual-point');
    point.setAttribute('cx',x(i));
    point.setAttribute('cy',y(r.value));
    point.setAttribute('r',rows.length > 30 ? 3.3 : 4.8);
    point.setAttribute('tabindex','0');
    const description = r.label + ': ' + format(r.value, view.digits ?? 1) + (r.status ? ' · ' + r.status : '') +
      (r.ciLower != null && r.ciUpper != null ? ' · 95% CI ' + confidenceText(r) : '');
    point.setAttribute('aria-label',description);
    const show = () => {
      tooltip.textContent = description;
      tooltip.hidden = false;
      const c = chart.getBoundingClientRect(), s = svg.getBoundingClientRect();
      const pos = s.left - c.left + x(i) / width * s.width;
      tooltip.style.left = Math.min(c.width-68,Math.max(68,pos)) + 'px';
      tooltip.style.top = (s.top - c.top + y(r.value) / height * s.height) + 'px';
    };
    const hide = () => { tooltip.hidden = true; };
    point.addEventListener('mouseenter',show);
    point.addEventListener('focus',show);
    point.addEventListener('mouseleave',hide);
    point.addEventListener('blur',hide);
    svg.append(point);
  });
  chart.append(svg,tooltip);
}

initMenu();
if (home) createHome();
else createProject();
