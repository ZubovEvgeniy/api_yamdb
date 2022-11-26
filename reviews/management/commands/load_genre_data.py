import time

from csv import DictReader
from django.core.management import BaseCommand

from tqdm import tqdm

from reviews.models import Genre


filename = 'genre'
ALREDY_LOADED_ERROR_MESSAGE = """
Если необходимо перезагрузить данные из csv файла,
то сначала нужно удалить таблицу {} через администратора.
После удаления нужной таблицы,
можно снова выполнить команду по загрузке данных.
""".format(filename)


class Command(BaseCommand):
    help = f'Loads data from {filename}.csv'

    def handle(self, *args, **options):
        if Genre.objects.exists():
            self.stdout.write(f'{filename} data already exiting.')
            self.stdout.write(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in tqdm(
            list(
                DictReader(
                    open('static/data/genre.csv', 'r', encoding='utf-8')
                )
            )
        ):
            review = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            review.save()
            time.sleep(0.10)
