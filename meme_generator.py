import MemePy
from typing import Dict, Any
import json
import io

TEMPLATES = {}


def get_templates() -> Dict[str, int]:
    '''
        Возвращает список возможных шаблонов для мемов
    '''
    result = {}
    memes = MemePy.MemeLibJsonDecoder.generate_standard_meme_dict()

    for meme in memes.keys():
        result[meme] = memes[meme].count_non_optional()

    return result


def generate(template, *params) -> Any:
    params = list(params)

    for i in range(len(params)):
        while '_' in params[i]:
            params[i] = params[i].replace('_', ' ')

    meme_pill = MemePy.MemeGenerator.get_meme_image(template, params)
    output = io.BytesIO()
    meme_pill.save(output, format='png')

    return output.getvalue()


TEMPLATES = get_templates()
