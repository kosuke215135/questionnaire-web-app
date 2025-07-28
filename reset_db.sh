rm polls/migrations/0*.py
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python sample_data.py
python dummy_answers.py



# from polls.models import AnswerType
# AnswerType.objects.get_or_create(name='single')
# AnswerType.objects.get_or_create(name='multiple')
# AnswerType.objects.get_or_create(name='text')
