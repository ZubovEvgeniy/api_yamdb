import time

from csv import DictReader
from django.core.management import BaseCommand

from tqdm import tqdm

from reviews.models import Comment, Review, User


filename = 'comments'
ALREDY_LOADED_ERROR_MESSAGE = """
Если необходимо перезагрузить данные из csv файла,
то сначала нужно удалить таблицу {} через администратора.
После удаления нужной таблицы,
можно снова выполнить команду по загрузке данных.
""".format(filename)


class Command(BaseCommand):
    help = f'Loads data from {filename}.csv'

    def handle(self, *args, **options):
        if Comment.objects.exists():
            self.stdout.write(f'{filename} data already exiting.')
            self.stdout.write(ALREDY_LOADED_ERROR_MESSAGE)
            return

        for row in tqdm(
            list(
                DictReader(
                    open('static/data/comments.csv', 'r', encoding='utf-8')
                )
            )
        ):
            review = Comment(
                id=row['id'],
                review=Review.objects.get(pk=int(row['review_id'])),
                text=row['text'],
                author=User.objects.get(pk=int(row['author'],)),
                pub_date=row['pub_date']
            )
            review.save()
            time.sleep(0.10)
