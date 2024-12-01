# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import re

from os.path import join, dirname, isfile
from os import listdir

import requests
from tabulate import tabulate

skill_meta_path = join(dirname(dirname(__file__)), "skill_metadata")


def read_skill_json(skill_json: str):
    with open(skill_json) as f:
        data = json.load(f)
    return data


def update_readme():
    original_skills = list()
    modified_skills = list()
    premium_skills = list()
    retired_skills = list()
    wip_skills = list()
    for skill in listdir(skill_meta_path):
        skill_spec = read_skill_json(join(skill_meta_path, skill))
        if "Retired" in skill_spec["tags"]:
            retired_skills.append(skill_spec)
        elif any((x in skill_spec['tags']
                  for x in ('WIP', 'In-Progress', 'tag'))):
            wip_skills.append(skill_spec)
        elif "Neon Premium" in skill_spec["tags"]:
            premium_skills.append(skill_spec)
        elif "Mycroft AI" in skill_spec["credits"] or \
             "Neon Enhanced" in skill_spec["tags"]:
            modified_skills.append(skill_spec)
        elif "NeonGecko Original" in skill_spec["tags"]:
            original_skills.append(skill_spec)
        else:
            print(f"Missing tag or MycroftAI credit for: {skill_spec['title']}")
            original_skills.append(skill_spec)
    original_skills.sort(key=lambda s: s['title'])
    modified_skills.sort(key=lambda s: s['title'])
    premium_skills.sort(key=lambda s: s['title'])
    retired_skills.sort(key=lambda s: s['title'])
    wip_skills.sort(key=lambda s: s['title'])

    readme_file = join(dirname(dirname(__file__)), 'README.md')
    with open(readme_file, 'w') as f:
        f.write("# Neon Original Skills\n")
        for skill in original_skills:
            f.write(f'[{skill["title"]}]({skill["url"]}) - '
                    f'{skill["summary"]}\n\n')
        f.write('# Neon Enhanced Skills\n')
        for skill in modified_skills:
            f.write(f'[{skill["title"]}]({skill["url"]}) - '
                    f'{skill["summary"]}\n\n')
        f.write('# Neon Premium Skills\n')
        for skill in premium_skills:
            f.write(f'[{skill["title"]}]({skill["url"]}) - '
                    f'{skill["summary"]}\n\n')
        f.write('# In-Progress Skills\n')
        for skill in wip_skills:
            f.write(f'[{skill["title"]}]({skill["url"]}) - '
                    f'{skill["summary"]}\n\n')
        f.write('# Retired Skills\n')
        for skill in retired_skills:
            f.write(f'[{skill["title"]}]({skill["url"]}) - '
                    f'{skill["summary"]}\n\n')


def _format_skill_name_html(skill: dict) -> str:
    """
    Parse skill name from data into an HTML-safe hyperlink string
    """
    return f'\\<a href=\\"{skill["url"]}\\"\\>{skill["title"]}\\<a\\>'


def _format_list_html(to_format: list) -> str:
    """
    Parse a list of strings into an HTML-safe list
    """
    to_return = "\\<ul\\>\n"
    for el in to_format:
        to_return = f'{to_return}\\<li\\>{el}\\</li\\>\n'
    return to_return


def _format_list_to_html(data: list) -> str:
    """
    Parse a list of HTML-safe strings into an HTML table
    """
    formatted = tabulate(data, tablefmt='html')
    return formatted.replace("\\&lt;", "<").replace("\\&gt;", ">").replace('\\&quot;', '"')


def update_neon_skills_html():
    """
    Update `neon_skills.html` with current data from all skills
    """
    all_skills = list()
    for skill in listdir(skill_meta_path):
        skill = read_skill_json(join(skill_meta_path, skill))
        table_data = [
            _format_skill_name_html(skill),
            skill["short_description"],
            _format_list_html(skill.get('examples') or list())
        ]
        all_skills.append(table_data)
    all_skills.sort(key=lambda s: s[0].split('>')[1].split('\\<')[0])
    all_skills.insert(0, ["Skill", "Summary", "Examples"])
    all_skills_path = join(dirname(dirname(__file__)), 'html',
                           'neon_skills.html')

    with open(all_skills_path, 'w+') as f:
        f.write(_format_list_to_html(all_skills))


def update_neon_skills_csv():
    """
    Update `neon_skills.csv` with current data from all skills
    """
    all_skills = list()
    all_skills.insert(0, ["Skill", "URL", "Summary", "Examples"])

    for skill in listdir(skill_meta_path):
        skill = read_skill_json(join(skill_meta_path, skill))
        table_data = [
            skill["title"],
            skill["url"],
            skill["short_description"].replace('"', "'"),
            ",".join(skill.get('examples') or []).replace('"', "'") or
            "<No Examples Provided>"
        ]
        all_skills.append(table_data)
    data = tabulate(all_skills, tablefmt='tsv')
    csv_path = join(dirname(dirname(__file__)), 'csv',
                    'neon_skills.tsv')

    with open(csv_path, 'w+') as f:
        f.write(data)


def update_neon_mark_2_html():
    """
    Update `mark_2_default_skills.html` with current data from all skills
    """
    required = "https://raw.githubusercontent.com/NeonGeckoCom/NeonCore/master/requirements/skills_required.txt"
    essential = "https://raw.githubusercontent.com/NeonGeckoCom/NeonCore/master/requirements/skills_essential.txt"
    default = "https://raw.githubusercontent.com/NeonGeckoCom/NeonCore/master/requirements/skills_default.txt"
    extended = "https://raw.githubusercontent.com/NeonGeckoCom/NeonCore/master/requirements/skills_extended.txt"
    # TODO: Parse blacklist
    skills_list = list()
    for url in (required, essential, default, extended):
        skills = requests.get(url).text.split('\n')
        skills_list.extend((s for s in skills if s
                            and not s.strip().startswith('#')))
    for idx, skill in enumerate(skills_list):
        if 'git+' in skill:
            skills_list[idx] = skill.split('git+', 1)[1]
        elif skill.startswith('neon-'):
            skills_list[idx] = re.split(r'[^\w\-]', skill, 1)[0].replace('neon-', '', 1)

    all_skills = list()
    for skill_name in skills_list:
        local_json_file = join(skill_meta_path, f'{skill_name}.json')
        if isfile(local_json_file):
            skill_json = read_skill_json(local_json_file)
        elif skill_name.startswith('http'):
            # TODO: Try parsing skill.json
            skill_json = {"title": skill_name.rsplit('/', 1)[1],
                          "url": skill_name}
        else:
            print(f"No skill json or URL for: {skill_name}")
            continue
        table_data = [
            _format_skill_name_html(skill_json),
            skill_json.get("short_description", ""),
            _format_list_html(skill_json.get('examples') or list())
        ]
        all_skills.append(table_data)

    all_skills.sort(key=lambda s: s[0].split('>')[1].split('\\<')[0])
    all_skills.insert(0, ["Skill", "Summary", "Examples"])
    mk2_skills_path = join(dirname(dirname(__file__)), 'html',
                           'mark_2_default_skills.html')

    with open(mk2_skills_path, 'w+') as f:
        f.write(_format_list_to_html(all_skills))


if __name__ == "__main__":
    update_readme()
    update_neon_skills_csv()
    update_neon_skills_html()
    update_neon_mark_2_html()
