import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import AkNotebookCommonModel


def upload_avatar_path(instance, filename):
    now = datetime.now()
    ext = filename.split(".")[-1]
    return "/".join(
        ["avatars", str(instance.user.user_id) + str(instance.profile_nickname) + str(now) + str(".") + str(ext)]
    )


class UserManager(BaseUserManager):
    def create_user(self, user_email, password=None):

        if not user_email:
            raise ValueError("email is must")

        user = self.model(user_email=self.normalize_email(user_email))
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, user_email, password):

        user = self.create_user(user_email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, AkNotebookCommonModel, PermissionsMixin):

    user_id = models.UUIDField(verbose_name="ユーザーID", default=uuid.uuid4, primary_key=True, editable=False)
    user_email = models.EmailField(verbose_name="ユーザーメールアドレス", max_length=254, unique=True)
    is_staff = models.BooleanField(verbose_name="スタッフ権限", help_text="Trueの場合はスタッフ権限が有効", default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_email"

    class Meta:
        db_table = "m_users"
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザーテーブル"

    def __str__(self):
        return self.user_email


class Profile(AkNotebookCommonModel):

    profile_id = models.UUIDField(verbose_name="プロフィールID", default=uuid.uuid4, primary_key=True, editable=False)
    profile_nickname = models.CharField(verbose_name="ニックネーム", max_length=30)
    profile_image = models.ImageField(verbose_name="プロフィール画像", blank=True, null=True, upload_to=upload_avatar_path)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE, related_name="User_Profile"
    )

    class Meta:
        db_table = "m_profiles"
        verbose_name = "プロフィール"
        verbose_name_plural = "プロフィールテーブル"

    def __str__(self):
        return self.profile_nickname


class Note(AkNotebookCommonModel):

    note_id = models.UUIDField(verbose_name="ノートID", default=uuid.uuid4, primary_key=True, editable=False)
    note_name = models.CharField(
        verbose_name="ノート名",
        max_length=50,
    )
    note_color = models.CharField(verbose_name="ノートカラー", max_length=7)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE, related_name="User_Note"
    )

    class Meta:
        db_table = "m_notes"
        verbose_name = "ノート"
        verbose_name_plural = "ノートテーブル"

    def __str__(self):
        return self.note_name


class MemoCategory(AkNotebookCommonModel):

    memo_category_id = models.UUIDField(verbose_name="メモカテゴリID", default=uuid.uuid4, primary_key=True, editable=False)
    memo_category_name = models.CharField(
        verbose_name="メモカテゴリ名",
        max_length=50,
    )
    memo_category_icon = models.TextField(
        verbose_name="メモカテゴリアイコン",
        null=True,
    )
    parent_memo_category = models.ForeignKey(
        "self",
        verbose_name="親メモカテゴリID",
        on_delete=models.CASCADE,
        null=True,
        related_name="ParentMemoCategory_ChildMemoCategory",
    )
    note = models.ForeignKey(Note, verbose_name="ノートID", on_delete=models.CASCADE, related_name="Note_MemoCategory")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE, related_name="User_MemoCategory"
    )

    class Meta:
        db_table = "m_memo_categories"
        verbose_name = "メモカテゴリ"
        verbose_name_plural = "メモカテゴリテーブル"

    def __str__(self):
        return str(self.memo_category_icon) + str(self.memo_category_name)


class Purpose(AkNotebookCommonModel):

    purpose_id = models.UUIDField(verbose_name="目的ID", default=uuid.uuid4, primary_key=True, editable=False)
    purpose_name = models.CharField(verbose_name="目的名", max_length=100)
    purpose_icon = models.TextField(verbose_name="目的アイコン", null=True)
    note = models.ForeignKey(Note, verbose_name="ノートID", on_delete=models.CASCADE, related_name="Note_Purpose")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE, related_name="User_Purpose"
    )

    class Meta:
        db_table = "m_purposes"
        verbose_name = "目的"
        verbose_name_plural = "目的テーブル"
        constraints = [models.UniqueConstraint(fields=["note", "purpose_name"], name="Note_PurposeName_Unique")]

    def __str__(self):
        return self.purpose_name


class Memo(AkNotebookCommonModel):

    memo_id = models.UUIDField(verbose_name="メモID", default=uuid.uuid4, primary_key=True, editable=False)
    memo_title = models.TextField(verbose_name="メモ件名", null=True)
    memo_priority = models.IntegerField(
        verbose_name="優先度",
        help_text="1~5までのレベルで優先度を表現5が一番優先度高い",
        validators=[MinValueValidator(1, "優先度は1以上で設定が必要"), MaxValueValidator(5, "優先度は5以下で設定が必要")],
    )
    memo_text = models.JSONField(verbose_name="テキストメモ", null=True)
    note = models.ForeignKey(Note, verbose_name="ノートID", on_delete=models.CASCADE, related_name="Note_Memo")
    parent_memo_category = models.ForeignKey(
        MemoCategory, verbose_name="親メモカテゴリID", on_delete=models.CASCADE, related_name="ParentMemoCategory_Memo"
    )
    child_memo_category = models.ForeignKey(
        MemoCategory, verbose_name="子メモカテゴリID", on_delete=models.CASCADE, related_name="ChildMemoCategory_Memo"
    )
    purpose = models.ForeignKey(
        Purpose, verbose_name="目的ID", null=True, on_delete=models.CASCADE, related_name="Purpose_Memo"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE, related_name="User_Memo"
    )

    class Meta:
        db_table = "t_memos"
        verbose_name = "メモ"
        verbose_name_plural = "メモテーブル"

    def __str__(self):
        return str(self.memo_title)


class StickyNoteCategory(AkNotebookCommonModel):

    sticky_note_category_code = models.CharField(verbose_name="付箋カテゴリコード", max_length=4, primary_key=True)
    sticky_note_category_name = models.CharField(
        verbose_name="付箋カテゴリ名", help_text="input:インプット用の付箋 output:アウトプット用の付箋", max_length=30, unique=True
    )

    class Meta:
        db_table = "m_sticky_note_categories"
        verbose_name = "付箋カテゴリ"
        verbose_name_plural = "付箋カテゴリテーブル"

    def __str__(self):
        return self.sticky_note_category_name


class StickyNote(AkNotebookCommonModel):

    sticky_note_id = models.UUIDField(verbose_name="付箋ID", default=uuid.uuid4, primary_key=True, editable=False)
    sticky_note_text = models.TextField(verbose_name="付箋")
    sticky_note_category = models.ForeignKey(
        StickyNoteCategory,
        verbose_name="付箋カテゴリコード",
        db_column="sticky_note_category_code",
        on_delete=models.CASCADE,
        related_name="StickyNoteCategory_StickyNote",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE, related_name="User_StickyNote"
    )

    class Meta:
        db_table = "t_sticky_notes"
        verbose_name = "付箋"
        verbose_name_plural = "付箋テーブル"

    def __str__(self):
        return self.sticky_note_text


class BrowsingMemoCount(AkNotebookCommonModel):
    browsing_memo_count = models.IntegerField(
        verbose_name="メモ閲覧回数", help_text="メモを閲覧時に一行追加されることで閲覧とみなす", default=1, editable=False
    )
    memo = models.ForeignKey(
        Memo, verbose_name="メモID", on_delete=models.CASCADE, related_name="Memo_MemoBrowsingCount"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="ユーザーID",
        on_delete=models.CASCADE,
        related_name="User_MemoBrowsingCount",
    )

    class Meta:
        db_table = "t_browsing_memo_counts"
        verbose_name = "メモ閲覧回数"
        verbose_name_plural = "メモ閲覧回数テーブル"


class DmBrowsingMemoCount(AkNotebookCommonModel):
    total_browsing_memo_count = models.IntegerField(
        verbose_name="総メモ閲覧回数",
    )
    note = models.ForeignKey(Note, verbose_name="ノートID", on_delete=models.CASCADE, related_name="Note_DmBrowsingCount")
    parent_memo_category = models.ForeignKey(
        MemoCategory,
        verbose_name="親メモカテゴリID",
        on_delete=models.CASCADE,
        related_name="ParentMemoCategory_DmBrowsingCount",
    )
    child_memo_category = models.ForeignKey(
        MemoCategory,
        verbose_name="子メモカテゴリID",
        on_delete=models.CASCADE,
        related_name="ChildMemoCategory_DmBrowsingCount",
    )
    purpose = models.ForeignKey(
        Purpose, verbose_name="目的ID", null=True, on_delete=models.CASCADE, related_name="Purpose_DmBrowsingCount"
    )
    memo = models.OneToOneField(
        Memo, verbose_name="メモID", on_delete=models.CASCADE, related_name="Memo_DmBrowsingCount"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="ユーザーID", on_delete=models.CASCADE, related_name="User_DmBrowsingCount"
    )

    class Meta:
        db_table = "dm_browsing_memo_counts"
        verbose_name = "総メモ閲覧回数"
        verbose_name_plural = "総メモ閲覧回数データマート"

    def __str__(self):
        return str(self.memo) + str(self.total_browsing_memo_count)


class DmLearningEfficiency(AkNotebookCommonModel):
    id = models.CharField(verbose_name="ID", max_length=46, primary_key=True)
    aggregate_date = models.DateField(
        verbose_name="集計日付",
    )
    learning_efficiency_rate = models.FloatField(
        verbose_name="学習効率",
    )
    note = models.ForeignKey(
        Note, verbose_name="ノートID", on_delete=models.CASCADE, related_name="Note_DmLearningEfficiency"
    )
    parent_memo_category = models.ForeignKey(
        MemoCategory,
        verbose_name="親メモカテゴリID",
        on_delete=models.CASCADE,
        related_name="ParentMemoCategory_DmLearningEfficiency",
    )
    child_memo_category = models.ForeignKey(
        MemoCategory,
        verbose_name="子メモカテゴリID",
        on_delete=models.CASCADE,
        related_name="ChildMemoCategory_DmLearningEfficiency",
    )
    purpose = models.ForeignKey(
        Purpose, verbose_name="目的ID", null=True, on_delete=models.CASCADE, related_name="Purpose_DmLearningEfficiency"
    )
    memo = models.ForeignKey(
        Memo, verbose_name="メモID", on_delete=models.CASCADE, related_name="Memo_DmLearningEfficiency"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="ユーザーID",
        on_delete=models.CASCADE,
        related_name="User_DmLearningEfficiency",
    )

    class Meta:
        db_table = "dm_learning_efficiency"
        verbose_name = "学習効率"
        verbose_name_plural = "学習効率データマート"

    def __str__(self):
        return str(self.memo) + str(self.aggregate_date) + str(self.learning_efficiency_rate)


class DmLearningEfficiencyBatchLog(AkNotebookCommonModel):
    aggregate_date = models.DateField(verbose_name="集計日付", unique=True)
    is_aggregated_today = models.BooleanField(
        verbose_name="当日集計実行済フラグ", help_text="Trueの場合は当日分の新規集計処理終了", default=True
    )

    class Meta:
        db_table = "t_learning_efficiency_batch_log"
        verbose_name = "学習効率集計バッチログ"
        verbose_name_plural = "学習効率集計バッチログ"

    def __str__(self):
        return str(self.aggregate_date)
