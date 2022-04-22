import datetime
import json
import random

from api.models import BrowsingMemoCount, DmLearningEfficiency, Memo, MemoCategory, Note


def create_initial_user_data(user):

    # テンプレートのJSONを読み込む
    initial_data = open("utils/authentication/initial_data/initial_data.json", "r")
    initial_data_json = json.load(initial_data)
    today = datetime.date.today()

    # 初期登録用のデータを作成する
    for note in initial_data_json:
        Note.objects.create(note_name=note["note_name"], note_color=note["note_color"], user=user)
        note_obj = Note.objects.get(note_name=note["note_name"], user=user)
        for parent_memo_category in note["parent_memo_categories"]:
            MemoCategory.objects.create(
                memo_category_name=parent_memo_category["memo_category_name"],
                memo_category_icon=parent_memo_category["memo_category_icon"],
                note=note_obj,
                user=user,
            )
            parent_memo_category_obj = MemoCategory.objects.get(
                memo_category_name=parent_memo_category["memo_category_name"],
                memo_category_icon=parent_memo_category["memo_category_icon"],
                parent_memo_category__isnull=True,
                user=user,
            )
            for child_memo_category in parent_memo_category["child_memo_categories"]:
                MemoCategory.objects.create(
                    memo_category_name=child_memo_category["memo_category_name"],
                    memo_category_icon=child_memo_category["memo_category_icon"],
                    note=note_obj,
                    parent_memo_category=parent_memo_category_obj,
                    user=user,
                )
                child_memo_category_obj = MemoCategory.objects.get(
                    memo_category_name=child_memo_category["memo_category_name"],
                    memo_category_icon=child_memo_category["memo_category_icon"],
                    note=note_obj,
                    parent_memo_category=parent_memo_category_obj,
                    user=user,
                )
                for memo in child_memo_category["memos"]:
                    memo_text = json.loads(memo["memo_text"])
                    aggregate_date_data = today - datetime.timedelta(days=memo["memo_aggregate_date_timedelta"])
                    Memo.objects.create(
                        memo_title=memo["memo_title"],
                        memo_priority=memo["memo_priority"],
                        memo_text=memo_text,
                        note=note_obj,
                        parent_memo_category=parent_memo_category_obj,
                        child_memo_category=child_memo_category_obj,
                        user=user,
                    )
                    memo_obj = Memo.objects.get(
                        memo_title=memo["memo_title"],
                        note=note_obj,
                        parent_memo_category=parent_memo_category_obj,
                        child_memo_category=child_memo_category_obj,
                        user=user,
                    )
                    BrowsingMemoCount.objects.create(
                        memo=memo_obj,
                        user=user,
                    )
                    DmLearningEfficiency.objects.create(
                        id="{}{}".format(today, memo_obj.memo_id),
                        aggregate_date=today,
                        learning_efficiency_rate=random.randint(30, 100),
                        note=note_obj,
                        parent_memo_category=parent_memo_category_obj,
                        child_memo_category=child_memo_category_obj,
                        memo=memo_obj,
                        user=user,
                    )
                    memo_obj.created_at = "{} 00:00:00".format(aggregate_date_data)
                    memo_obj.save()
