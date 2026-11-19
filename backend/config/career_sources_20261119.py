"""Sources added 19 November 2026, chosen for Delhi-NCR data, analytics and GCC roles.

Each row was checked live that day with the fetcher that collects it, India scope applied:
RSM ~153 India postings (Gurugram, Hyderabad, Bengaluru), R1 RCM ~101 (Noida, Gurugram),
Stryker ~94 (mostly Gurugram), ICF 33 (mostly New Delhi), Pitney Bowes 7 (Noida, Pune),
Veradigm 58 (Pune), Carelon Global Solutions 23 (India-only site), Johnson & Johnson ~69+
(city facets), PTC 31 (Pune, Gurgaon), Kimberly-Clark 14, PVH 19, Sun Life 2 (Gurugram),
EY and NTT DATA (thousands; only the newest `max_pages` pages are read), Zinnia 12,
Navan 14 (Greenhouse board `tripactions`), Inizio 4, Simpplr 3, Headout 8, ixigo 8,
MetLife 64 (Avature, its own India filter; Pune, Noida, Jaipur, Hyderabad),
Bain & Company 102 of 251 global (Avature, India offices kept client-side; mostly New Delhi BCN).
Counts are dated observations, not live health. Registration implies nothing about pay
or fresher eligibility.
"""

SOURCES = [
    {'key': 'rsm', 'name': 'RSM', 'group': 'workday_india',
     'career_url': 'https://rsm.wd1.myworkdayjobs.com/en-US/RSMCareers',
     'config': {'tenant': 'rsm', 'wd_server': 'wd1', 'site': 'RSMCareers', 'verify_detail_country': True}},
    {'key': 'r1rcm', 'name': 'R1 RCM', 'group': 'workday_india',
     'career_url': 'https://r1rcm.wd1.myworkdayjobs.com/en-US/R1RCM',
     'config': {'tenant': 'r1rcm', 'wd_server': 'wd1', 'site': 'R1RCM', 'verify_detail_country': True}},
    {'key': 'stryker', 'name': 'Stryker', 'group': 'workday_india',
     'career_url': 'https://stryker.wd1.myworkdayjobs.com/en-US/StrykerCareers',
     'config': {'tenant': 'stryker', 'wd_server': 'wd1', 'site': 'StrykerCareers', 'verify_detail_country': True}},
    {'key': 'icf', 'name': 'ICF', 'group': 'workday_india',
     'career_url': 'https://icf.wd5.myworkdayjobs.com/en-US/ICFExternal_Career_Site',
     'config': {'tenant': 'icf', 'wd_server': 'wd5', 'site': 'ICFExternal_Career_Site', 'verify_detail_country': True}},
    {'key': 'pitneybowes', 'name': 'Pitney Bowes', 'group': 'workday_india',
     'career_url': 'https://pitneybowes.wd1.myworkdayjobs.com/en-US/PBCareers',
     'config': {'tenant': 'pitneybowes', 'wd_server': 'wd1', 'site': 'PBCareers', 'verify_detail_country': True}},
    # The first bullet field is the country ("India") on every row; the requisition id is second.
    {'key': 'veradigm', 'name': 'Veradigm', 'group': 'workday_india',
     'career_url': 'https://veradigm.wd12.myworkdayjobs.com/en-US/VR',
     'config': {'tenant': 'veradigm', 'wd_server': 'wd12', 'site': 'VR', 'verify_detail_country': True, 'id_bullet_index': 1}},
    # India-only career site without a country facet; each detail page's country is verified.
    {'key': 'carelon', 'name': 'Carelon Global Solutions', 'group': 'workday_india',
     'career_url': 'https://elevancehealth.wd1.myworkdayjobs.com/en-US/carelonglobal_in',
     'config': {'tenant': 'elevancehealth', 'wd_server': 'wd1', 'site': 'carelonglobal_in', 'verify_global_country': True}},
    {'key': 'jnj', 'name': 'Johnson & Johnson', 'group': 'workday_india',
     'career_url': 'https://jj.wd5.myworkdayjobs.com/en-US/JJ',
     'config': {'tenant': 'jj', 'wd_server': 'wd5', 'site': 'JJ', 'verify_detail_country': True, 'india_facet_pattern': ', India$'}},
    {'key': 'ptc', 'name': 'PTC', 'group': 'workday_india',
     'career_url': 'https://ptc.wd1.myworkdayjobs.com/en-US/PTC',
     'config': {'tenant': 'ptc', 'wd_server': 'wd1', 'site': 'PTC', 'verify_detail_country': True, 'india_facet_pattern': ', India$'}},
    {'key': 'kimberlyclark', 'name': 'Kimberly-Clark', 'group': 'workday_india',
     'career_url': 'https://kimberlyclark.wd1.myworkdayjobs.com/en-US/GLOBAL',
     'config': {'tenant': 'kimberlyclark', 'wd_server': 'wd1', 'site': 'GLOBAL', 'verify_detail_country': True}},
    {'key': 'pvh', 'name': 'PVH', 'group': 'workday_india',
     'career_url': 'https://pvh.wd1.myworkdayjobs.com/en-US/PVH_Careers',
     'config': {'tenant': 'pvh', 'wd_server': 'wd1', 'site': 'PVH_Careers', 'verify_detail_country': True}},
    {'key': 'sunlife', 'name': 'Sun Life', 'group': 'workday_india',
     'career_url': 'https://sunlife.wd3.myworkdayjobs.com/en-US/Experienced-Jobs',
     'config': {'tenant': 'sunlife', 'wd_server': 'wd3', 'site': 'Experienced-Jobs', 'verify_detail_country': True}},
    # Classic SuccessFactors sites scoped to India by the server. Rows read "City, ST, IN, PIN",
    # which the location parser would take for Indiana, so country_scoped rewrites them.
    {'key': 'ey', 'name': 'EY', 'group': 'successfactors',
     'career_url': 'https://careers.ey.com/ey/search/?locationsearch=India',
     'config': {'host': 'careers.ey.com', 'path': '/ey/search/', 'extra_query': 'locationsearch=India',
                'country_scoped': 'India', 'fetch_details': True, 'max_pages': 8}},
    {'key': 'nttdata', 'name': 'NTT DATA', 'group': 'successfactors',
     'career_url': 'https://careers-inc.nttdata.com/search/?locationsearch=India',
     'config': {'host': 'careers-inc.nttdata.com', 'extra_query': 'locationsearch=India',
                'country_scoped': 'India', 'fetch_details': True, 'max_pages': 8}},
    {'key': 'zinnia', 'name': 'Zinnia', 'group': 'greenhouse',
     'career_url': 'https://job-boards.greenhouse.io/zinnia', 'config': {}},
    {'key': 'tripactions', 'name': 'Navan', 'group': 'greenhouse',
     'career_url': 'https://job-boards.greenhouse.io/tripactions', 'config': {}},
    {'key': 'inizio', 'name': 'Inizio', 'group': 'greenhouse',
     'career_url': 'https://job-boards.greenhouse.io/inizio', 'config': {}},
    {'key': 'simpplr', 'name': 'Simpplr', 'group': 'greenhouse',
     'career_url': 'https://job-boards.greenhouse.io/simpplr', 'config': {}},
    {'key': 'headout', 'name': 'Headout', 'group': 'ashby',
     'career_url': 'https://jobs.ashbyhq.com/headout', 'config': {}},
    {'key': 'ixigo', 'name': 'ixigo', 'group': 'smartrecruiters',
     'career_url': 'https://jobs.smartrecruiters.com/ixigo', 'config': {}},
    # Query copied from the employer's own India-filtered search URL.
    {'key': 'metlife', 'name': 'MetLife', 'group': 'employer_portals',
     'career_url': 'https://www.metlifecareers.com/en_US/ml/SearchJobs/?12310=%5B116642%5D&12310_format=9873&listFilterMode=1',
     'config': {'kind': 'avature', 'host': 'www.metlifecareers.com', 'path': '/en_US/ml',
                'query': '12310=%5B116642%5D&12310_format=9873&listFilterMode=1'}},
    # careers.bain.com robots.txt allows /jobs; www.bain.com's own search API refuses direct
    # access and its ?filters= pages are disallowed, so this reads the Avature portal instead.
    # No server-side India filter: all ~250 global rows are paged, India offices kept.
    {'key': 'bain', 'name': 'Bain & Company', 'group': 'employer_portals',
     'career_url': 'https://careers.bain.com/jobs/SearchJobs/',
     'config': {'kind': 'avature', 'host': 'careers.bain.com', 'path': '/jobs', 'query': '',
                'records_param': 'folderRecordsPerPage', 'offset_param': 'folderOffset',
                'detail_from_listing': True}},
]

# Global boards: keep explicit India postings only (Navan, Headout list Paris, London, Tokyo).
INDIA_BOARDS = {row['key'] for row in SOURCES if row['group'] in {'greenhouse', 'lever', 'ashby'}}


def register(namespace):
    for row in SOURCES:
        group = row['group'].upper()
        if group in {'GREENHOUSE', 'LEVER', 'ASHBY'}:
            namespace[group].append(row['key'])
        elif group == 'SMARTRECRUITERS':
            namespace[group].append({'company_id': row['key']})
        else:
            namespace[group].append({'company': row['key'], **row['config']})
        namespace['DISPLAY_NAMES'][row['key']] = row['name']
