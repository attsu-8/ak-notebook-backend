from django.db import models

class AkNotebookCommonModel(models.Model):
  """テーブル共通フィールド"""
  is_active = models.BooleanField(
    verbose_name='有効フラグ',
    help_text='Trueの場合はレコードが有効',
    default=True
    )
  created_at = models.DateTimeField(
    verbose_name='作成日時',
    auto_now_add=True
    )
  updated_at = models.DateTimeField(
    verbose_name='更新日時',
    auto_now=True
    )

  class Meta:
    ordering = ['created_at']
    abstract = True

