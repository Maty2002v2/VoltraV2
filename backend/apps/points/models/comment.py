from django.db import models


class Comment(models.Model):
    text = models.TextField(verbose_name='treść')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    division = models.ForeignKey(
        'points.Point',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='dywyzja',
    )

    class Meta(object):
        verbose_name = 'komentarz'
        verbose_name_plural = 'komentarze'

    def __str__(self):
        return self.text
