import os
import asyncio
import aiofiles
import logging
import argparse
from pathlib import Path

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder):
    """Читає всі файли у вихідній папці та її підпапках."""
    files = []
    for root, _, filenames in os.walk(source_folder):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

async def copy_file(file_path, output_folder):
    """Копіює файл у відповідну підпапку на основі його розширення."""
    try:
        extension = Path(file_path).suffix[1:]  # Отримати розширення файлу
        target_folder = os.path.join(output_folder, extension)  # Створити шлях для цільової папки

        # Створити цільову папку, якщо вона не існує
        os.makedirs(target_folder, exist_ok=True)

        # Копіюємо файл
        target_file_path = os.path.join(target_folder, os.path.basename(file_path))
        async with aiofiles.open(file_path, 'rb') as source_file:
            content = await source_file.read()
            async with aiofiles.open(target_file_path, 'wb') as target_file:
                await target_file.write(content)

        logging.info(f'Файл скопійовано: {file_path} -> {target_file_path}')
    except Exception as e:
        logging.error(f'Помилка при копіюванні файлу {file_path}: {e}')

async def main(source_folder, output_folder):
    """Головна асинхронна функція для читання та копіювання файлів."""
    files = await read_folder(source_folder)
    tasks = [copy_file(file, output_folder) for file in files]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Шляхи до папок
    source_folder = r"C:\Users\roman\Reps\goit-cs-hw-05\Task 1\source_folder"
    output_folder = r"C:\Users\roman\Reps\goit-cs-hw-05\Task 1\output_folder"

    # Запускаємо асинхронну програму
    asyncio.run(main(source_folder, output_folder))


