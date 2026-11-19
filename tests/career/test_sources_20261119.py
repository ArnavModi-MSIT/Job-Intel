"""Registration and parsing checks for the 19 November 2026 sources (offline)."""
import unittest
from unittest.mock import patch

import backend.config as config
from backend.config.career_sources_20261119 import INDIA_BOARDS, SOURCES
from backend.core.location import parse_country
from backend.fetchers import avature, standard, successfactors


def _keys(group):
    return [item if isinstance(item, str) else item.get('company') or item.get('company_id')
            for item in getattr(config, group.upper())]


class RegistrationTests(unittest.TestCase):
    def test_unique_sources_registered_once_and_named(self):
        self.assertEqual(len(SOURCES), 22)
        self.assertEqual(len({row['key'] for row in SOURCES}), 22)
        for row in SOURCES:
            with self.subTest(company=row['key']):
                self.assertEqual(_keys(row['group']).count(row['key']), 1)
                self.assertEqual(config.DISPLAY_NAMES[row['key']], row['name'])
                self.assertTrue(row['career_url'].startswith('https://'))

    def test_global_boards_are_strictly_india_scoped(self):
        self.assertEqual(INDIA_BOARDS, {'zinnia', 'tripactions', 'inizio', 'simpplr', 'headout'})
        self.assertTrue(INDIA_BOARDS <= standard.INDIA_BOARDS)
        self.assertEqual(standard._expansion_location('Paris, FR'), '')

    def test_large_successfactors_tenants_are_capped(self):
        rows = {row['key']: row['config'] for row in SOURCES}
        for key in ('ey', 'nttdata'):
            self.assertEqual(rows[key]['country_scoped'], 'India')
            self.assertLessEqual(rows[key]['max_pages'], successfactors.MAX_PAGES)


def _page(start, count):
    rows = ''.join(
        f'<tr class="data-row"><td><a class="jobTitle-link" href="/ey/job/x-{n}/{1000 + n}/">Analyst {n}</a>'
        f'<span class="jobLocation">Gurugram, HR, IN, 122002</span></td></tr>' for n in range(start, start + count))
    return f'<span class="paginationLabel">Results 1 – 25 of 500</span><table>{rows}</table>'


class ClassicSuccessFactorsTests(unittest.TestCase):
    def test_max_pages_and_country_scoped_location(self):
        cfg = {'company': 'ey', 'host': 'careers.ey.com', 'path': '/ey/search/',
               'extra_query': 'locationsearch=India', 'country_scoped': 'India', 'max_pages': 2}
        calls = []

        def page(host, startrow, **extra):
            calls.append((startrow, extra))
            return _page(startrow, 25)
        with patch.object(successfactors, '_search_page', side_effect=page), patch.object(successfactors.time, 'sleep'):
            jobs = successfactors.fetch_successfactors(cfg)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][1], {'path': '/ey/search/', 'extra_query': 'locationsearch=India'})
        self.assertEqual(len(jobs), 50)
        self.assertEqual(jobs[0]['location'], 'Gurugram, India')
        self.assertEqual(parse_country(jobs[0]['location']), 'India')
        # Without the rewrite the parser reads "IN" as Indiana.
        self.assertEqual(parse_country('Gurugram, HR, IN, 122002'), 'United States')


METLIFE_LISTING = """<div>1-2 of 2 Results</div>
<article class="article article--result"><h3><a class="link"
 href="https://www.metlifecareers.com/en_US/ml/JobDetail/BI-Developer-II/21300">BI Developer II</a></h3>
<span class="list-item-location">Noida, India</span></article>
<article class="article article--result"><h3><a class="link"
 href="https://www.metlifecareers.com/en_US/ml/JobDetail/Analyst/21301">Analyst</a></h3>
<span class="list-item-location">Seoul, Korea, Republic of</span></article>"""

METLIFE_DETAIL = """<h2 class="banner__text__title title title--banner">BI Developer II</h2>
<article class="article article--details"><div class="article__header"><h3 class="article__header__text__title">General Information</h3></div>
<div class="article__content"><div class="article__content__view__field">Location Noida</div></div></article>
<article class="article article--details"><div class="article__header"><h3 class="article__header__text__title">Description and Requirements</h3></div>
<div class="article__content"><div class="article__content__view__field">Build Power BI reports with SQL.</div></div></article>"""


class MetLifeAvatureTests(unittest.TestCase):
    def test_path_ids_location_span_and_capitalised_total(self):
        jobs, total, rows = avature.parse_results(METLIFE_LISTING, 'www.metlifecareers.com')
        self.assertEqual((total, rows), (2, 2))
        self.assertEqual([(j['source_id'], j['location']) for j in jobs], [('21300', 'Noida, India')])

    def test_description_section_only(self):
        title, text = avature.parse_detail(METLIFE_DETAIL)
        self.assertEqual(title, 'BI Developer II')
        self.assertEqual(text, 'Build Power BI reports with SQL.')


BAIN_LISTING = """<div>1 - 3 of 251</div>
<article class="article article--result"><div class="article__header__text"><h3>
<a href="https://careers.bain.com/jobs/FolderDetail/Associate-Data-Engineer/111001">Associate - Data Engineer</a></h3>
<div class="article__header__text__subtitle"><span>New Delhi</span></div></div></article>
<article class="article article--result"><div class="article__header__text"><h3>
<a href="https://careers.bain.com/jobs/FolderDetail/Analyst/111002">Analyst</a></h3>
<div class="article__header__text__subtitle"><span>Kuala Lumpur, Bengaluru</span></div></div></article>
<article class="article article--result"><div class="article__header__text"><h3>
<a href="https://careers.bain.com/jobs/FolderDetail/Accountant/111003">Accountant</a></h3>
<div class="article__header__text__subtitle"><span>Warsaw</span></div></div></article>"""


class BainAvatureTests(unittest.TestCase):
    def test_folder_ids_plain_subtitle_and_india_offices_only(self):
        jobs, total, rows = avature.parse_results(BAIN_LISTING, 'careers.bain.com')
        self.assertEqual(rows, 3)
        self.assertEqual([(j['source_id'], j['location']) for j in jobs],
                         [('111001', 'New Delhi, India'), ('111002', 'Bengaluru, India')])

    def test_banner_title(self):
        html = '<h2 class="banner__text__title">Analyst</h2>' + METLIFE_DETAIL.split('</h2>', 1)[1]
        self.assertEqual(avature.parse_detail(html)[0], 'Analyst')


if __name__ == '__main__':
    unittest.main()
