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

from os.path import join, dirname
from ovos_skills_manager.github import get_skill_json

readme_file = join(dirname(dirname(__file__)), "README.md")
metadata_path = join(dirname(dirname(__file__)), "skill_metadata")
branch = 'dev'


def get_skill_urls_from_readme():
    with open(readme_file) as f:
        lines = f.readlines()
    skills = list()
    for line in lines:
        if '(' in line:
            skill_url = line.split('(', )[1].rsplit(')', 1)[0]
            if skill_url:
                skills.append(skill_url)
            else:
                print(f"Error parsing: {line}")
    for skill in skills:
        if not skill:
            print("ERROR")
        try:
            skill_json = get_skill_json(skill, branch)
            skill_name = skill_json['skillname']
            print(skill_name or skill)
            with open(join(metadata_path, f'{skill_name}.json'), "w+") as f:
                json.dump(skill_json, f, indent=2)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    get_skill_urls_from_readme()
