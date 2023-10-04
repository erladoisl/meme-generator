import requests
from typing import List, Any

URL = 'https://api.memegen.link'
TEMPLATES = {}


def get_templates() -> List[str]:
    '''
        Возвращает список возможных шаблонов для мемов
    '''
    result = {}
    response = requests.get(
        f'{URL}/images', proxies={'http': 'http://proxy.server:3128'})

    if response.status_code == 200:
        templates = response.json()

        for template in templates:
            splited_url = template.get('url', '').split('/')
            if len(splited_url) > 6:
                result[splited_url[4]] = {'type': splited_url[-1].split('.')[-1],
                                          'params_count': len(splited_url) - 5}

    return result


def generate(template, *params) -> Any:
    response = requests.get(
        f'{URL}/images/{template}/{"/".join(params)}.{TEMPLATES.get(template, {}).get("type", "")}')

    return response.content


TEMPLATES = get_templates()
