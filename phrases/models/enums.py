from django.db import models    


class PhraseLanguage(models.IntegerChoices):
    ENGLISH = 0, 'English'
    SPANISH = 1, 'Spanish'

