"""Check the current portfolio and its official-source dashboard interactions."""
import csv
from decimal import Decimal, ROUND_HALF_UP
import io
import json
import os
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
BASE = os.environ.get('PORTFOLIO_BASE_URL', ROOT.as_uri() + '/').rstrip('/') + '/'
projects = json.loads((ROOT / 'assets/projects.js').read_text().removeprefix('window.PORTFOLIO_PROJECTS = ').strip().removesuffix(';')) + json.loads((ROOT / 'assets/expansion.js').read_text().removeprefix('window.PORTFOLIO_NEW_PROJECTS = ').strip().removesuffix(';')) + json.loads((ROOT / 'assets/portfolio-additions.js').read_text().removeprefix('window.PORTFOLIO_ADDITIONS = ').strip().removesuffix(';'))


def open_page(browser, path, width):
    page = browser.new_page(viewport={'width': width, 'height': 900}, accept_downloads=True)
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(BASE + path, wait_until='domcontentloaded')
    return page, errors


def check_width(page, width):
    assert page.evaluate('document.documentElement.scrollWidth') <= width + 2, (page.url, width, 'horizontal overflow')


def check_home(browser):
    for width in (375, 768, 1440):
        page, errors = open_page(browser, '', width) if not BASE.startswith('file:') else open_page(browser, 'index.html', width)
        assert page.locator('.project-card').count() == len(projects)
        assert page.locator('.strip-grid strong').all_inner_texts() == ['10', '9', '7']
        assert page.locator('.project-card .badge').all_inner_texts().count('Real public data') == 9
        assert page.locator('.project-card .badge').all_inner_texts().count('Professional experience') == 1
        assert page.locator('h1').count() == 1
        for group in ('system', 'population', 'business', 'all'):
            page.locator(f'[data-filter="{group}"]').click()
            assert page.locator('.project-card:visible').count() == (len(projects) if group == 'all' else sum(p['group'] == group for p in projects))
        assert len(page.locator('.project-card a[href^="project.html?case="]').all()) == len(projects)
        if width == 375:
            page.locator('.menu-button').click()
            assert page.locator('.menu-button').get_attribute('aria-expanded') == 'true'
            page.keyboard.press('Escape')
            assert page.locator('.menu-button').get_attribute('aria-expanded') == 'false'
        check_width(page, width)
        assert not errors, errors
        page.close()
    print('PASS: homepage projects, filters, menu and responsive layouts')


def rounded(value, digits):
    return '—' if value is None else format(Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP), f',.{digits}f')


SOURCE_DOWNLOADS = {
    'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1310046501': 'https://www150.statcan.gc.ca/n1/tbl/csv/13100465-eng.zip',
    'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044201': 'https://www150.statcan.gc.ca/n1/tbl/csv/14100442-eng.zip',
}


def check_values(page, view, rows):
    visible = [r for r in rows if r['value'] is not None]
    ordered = visible + [r for r in rows if r['value'] is None]
    with_ci = any(r.get('ciLower') is not None for r in rows)
    with_status = any(r.get('status') for r in rows)
    table = page.locator('#table-body tr').evaluate_all("trs => trs.map(tr => ({cells: [...tr.cells].map(c => c.textContent), url: tr.querySelector('a')?.href}))")
    assert len(table) == len(ordered)
    for actual, row in zip(table, ordered):
        expected = [row['label'], rounded(row['value'], view.get('digits', 1))]
        if with_ci:
            digits = 2 if row.get('sourceId', '').startswith('CIHI') else 1
            expected.append('—' if row.get('ciLower') is None else rounded(row['ciLower'], digits) + '–' + rounded(row['ciUpper'], digits))
        if with_status:
            expected.append(row.get('status') or '—')
        expected.append(str(row['n']))
        assert actual['cells'] == expected, (view['name'], row['label'], actual['cells'], expected)
        assert actual['url'] == SOURCE_DOWNLOADS.get(row['sourceUrl'], row['sourceUrl']), (view['name'], row['label'], actual['url'])
    if view.get('chart') == 'line':
        assert page.locator('#chart circle').count() == len(visible)
        assert page.locator('#chart .forecast-point').count() == sum(r['status'] == 'Forecast' for r in visible)
    else:
        assert page.locator('#chart .data-row').count() == len(visible)
        assert page.locator('#chart .bar-value').all_text_contents() == [rounded(r['value'], view.get('digits', 1)) for r in visible]


def check_dashboards(browser):
    total = 0
    for project in projects:
        path = 'project.html?case=' + project['id']
        for width in (375, 1440):
            page, errors = open_page(browser, path, width)
            assert page.locator('h1').inner_text() == project['title']
            assert page.locator('.intro-kickers .badge').inner_text() == ('Professional experience' if project['type'] == 'experience' else 'Real public data')
            assert page.locator('#project-picker option').count() == len(projects)
            if project['type'] == 'experience':
                assert page.locator('.process-step').count() == len(project['steps'])
                for index, step in enumerate(project['steps']):
                    button = page.locator(f'.process-step[data-step="{index}"]')
                    button.click()
                    assert button.get_attribute('aria-pressed') == 'true'
                    assert page.locator('#process-detail h3').inner_text() == step['name']
                assert page.locator('.table-panel tbody tr').count() == len(project['requirements'])
                assert page.locator('a[href="resources/process/workflow.zip"]').count() >= 1
                check_width(page, width)
                assert not errors, errors
                page.close()
                continue
            assert page.locator('#table-body tr').count() > 0
            check_width(page, width)
            if width == 1440:
                for index, view in enumerate(project['views']):
                    page.locator('#indicator').select_option(str(index))
                    assert page.locator('#selection-label').inner_text() == view['selectionLabel']
                    for year in view['years']:
                        if page.locator('#period').is_enabled():
                            page.locator('#period').select_option(year)
                        expected = [row for row in view['rows'] if str(row['year']) == year]
                        check_values(page, view, expected)
                        assert page.locator('#chart-title').inner_text() == view['name']
                        total += 1
                    if page.locator('#sort').is_visible():
                        page.locator('#sort').select_option('desc')
                        ordered = sorted([r for r in expected if r['value'] is not None], key=lambda r: -r['value']) + [r for r in expected if r['value'] is None]
                        check_values(page, view, ordered)
                with page.expect_download() as download:
                    page.locator('#download').click()
                data = download.value.path().read_text(encoding='utf-8')
                rows = list(csv.DictReader(io.StringIO(data)))
                assert len(rows) == len(expected)
                assert all(row['data_type'] == 'Real public data' and row['source_reference'] and row['source_url'] for row in rows)
            assert not errors, errors
            page.close()
        print('PASS:', project['id'])
    for slug in ('diabetes', 'ontario', 'mental-health', 'readmissions'):
        page, errors = open_page(browser, 'dashboards/' + slug + '.html', 1440)
        page.wait_for_url('**/project.html?case=' + slug)
        assert page.locator('h1').count() == 1 and not errors
        page.close()
    page, errors = open_page(browser, 'dashboards/index.html', 1440)
    page.wait_for_url('**/index.html#projects')
    assert page.locator('.project-card').count() == len(projects) and not errors
    page.close()
    print(f'PASS: {total} indicator-period combinations, CSV exports and legacy redirects')


with sync_playwright() as playwright:
    options = {'headless': True}
    if os.environ.get('CHROMIUM_PATH'):
        options['executable_path'] = os.environ['CHROMIUM_PATH']
    browser = playwright.chromium.launch(**options)
    if len(sys.argv) == 1 or sys.argv[1] == 'home':
        check_home(browser)
    if len(sys.argv) == 1 or sys.argv[1] == 'dashboards':
        check_dashboards(browser)
    browser.close()
