import argparse
import json
from pathlib import Path
import re


def configure(repository):
    repository = repository.strip().removeprefix('https://github.com/').rstrip('/').removesuffix('.git')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+', repository):
        raise ValueError('Ожидается адрес GitHub или имя в формате пользователь/репозиторий')
    root = Path(__file__).resolve().parent
    path = root / 'KR22_PDN_GitHub_Colab.ipynb'
    notebook = json.loads(path.read_text(encoding='utf-8'))
    cell = notebook['cells'][5]
    source, replacements = re.subn(
        r'^GITHUB_REPOSITORY = .*$',
        'GITHUB_REPOSITORY = ' + json.dumps(repository),
        ''.join(cell['source']), count=1, flags=re.MULTILINE,
    )
    if replacements != 1:
        raise ValueError('Не найдена настройка загрузки модели')
    cell['source'] = source.splitlines(keepends=True)
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    readme_path = root / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    readme = re.sub(r'colab\.research\.google\.com/github/[^\s)]+',
                    f'colab.research.google.com/github/{repository}/blob/main/KR22_PDN_GitHub_Colab.ipynb', readme)
    readme = re.sub(r'https://github\.com/[^\s)]+/releases/tag/v1\.0\.0',
                    f'https://github.com/{repository}/releases/tag/v1.0.0', readme)
    readme_path.write_text(readme, encoding='utf-8')
    print(f'Репозиторий: https://github.com/{repository}')
    print(f'Colab: https://colab.research.google.com/github/{repository}/blob/main/{path.name}')
    print('Изменены блокнот и README. Загрузите их в ветку main.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Настройка ссылок на репозиторий перед публикацией')
    parser.add_argument('repository', help='пользователь/репозиторий или адрес GitHub')
    arguments = parser.parse_args()
    configure(arguments.repository)
