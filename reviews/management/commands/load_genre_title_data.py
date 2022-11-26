import time

from csv import DictReader
from django.core.management import BaseCommand

from tqdm import tqdm

from reviews.models import GenreTitle, Title, Genre


filename = 'genre_title'
ALREDY_LOADED_ERROR_MESSAGE = """
Если необходимо перезагрузить данные из csv файла,
то сначала нужно удалить таблицу {} через администратора.
После удаления нужной таблицы,
можно снова выполнить команду по загрузке данных.
""".format(filename)


class Command(BaseCommand):
    help = f'Loads data from {filename}.csv'

    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            self.stdout.write(f'{filename} data already exiting.')
            self.stdout.write(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in tqdm(
            list(
                DictReader(
                    open('static/data/genre_title.csv', 'r', encoding='utf-8')
                )
            )
        ):
            review = GenreTitle(
                id=row['id'],
                title=Title.objects.get(pk=int(row['title_id'])),
                genre=Genre.objects.get(pk=int(row['genre_id']))
            )
            review.save()
            time.sleep(0.10)
