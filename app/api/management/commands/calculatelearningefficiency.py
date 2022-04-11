from django.core.management.base import BaseCommand
from api.models import BrowsingMemoCount, DmLearningEfficiency, Note, MemoCategory, Purpose, Memo, User, DmLearningEfficiencyBatchLog
import math
from django.db.models import Max
import datetime

now = datetime.datetime.now()
today = datetime.datetime.now().date()
print("バッチ処理開始日時：{}".format(str(now)))


#DmLearningEfficiencyにデータを追加する際、外部キーはモデルインスタンスである必要があるため、全モデルデータを取得
notes = Note.objects.filter(is_active=True)
parent_memo_categories = MemoCategory.objects.filter(is_active=True, parent_memo_category__isnull=True)
child_memo_categories = MemoCategory.objects.filter(is_active=True, parent_memo_category__isnull=False)
purposes = Purpose.objects.filter(is_active=True)
memos = Memo.objects.filter(is_active=True)
users = User.objects.filter(is_active=True)


def calculate_learning_efficiency(latest_browsing_datetime):
    subtract_datetime = now - latest_browsing_datetime
    elapsed_minutes = math.ceil(subtract_datetime.total_seconds() / 60)
    learning_efficiency = round(100 * (1.84 / ((math.log10(elapsed_minutes) ** 1.25) + 1.84)),1)
    
    return learning_efficiency


def create_learning_efficiency_record(latest_browsing_memo):
    return DmLearningEfficiency(
        id="{}{}".format(today, latest_browsing_memo["memo"]),
        aggregate_date=today,
        learning_efficiency_rate=calculate_learning_efficiency(latest_browsing_memo["max_datetime"]),
        note=notes.get(pk=latest_browsing_memo["memo__note"]),
        parent_memo_category=parent_memo_categories.get(pk=latest_browsing_memo["memo__parent_memo_category"]),
        child_memo_category=child_memo_categories.get(pk=latest_browsing_memo["memo__child_memo_category"]),
        # purpose=purposes.get(pk=latest_browsing_memo["memo__purpose"]),
        memo=memos.get(pk=latest_browsing_memo["memo"]),
        user=users.get(pk=latest_browsing_memo["user"])
    )


def update_learning_efficiency_record(latest_browsing_memo):
    return DmLearningEfficiency(
        pk="{}{}".format(today, latest_browsing_memo["memo"]),
        learning_efficiency_rate=calculate_learning_efficiency(latest_browsing_memo["max_datetime"]),
        note=notes.get(pk=latest_browsing_memo["memo__note"]),
        parent_memo_category=parent_memo_categories.get(pk=latest_browsing_memo["memo__parent_memo_category"]),
        child_memo_category=child_memo_categories.get(pk=latest_browsing_memo["memo__child_memo_category"]),
        # purpose=purposes.get(pk=latest_browsing_memo["memo__purpose"]),
        memo=memos.get(pk=latest_browsing_memo["memo"]),
        user=users.get(pk=latest_browsing_memo["user"])
    )


class Command(BaseCommand):
    def handle(self, *args, **options):
        latest_browsing_memos = BrowsingMemoCount.objects.filter(
            memo__is_active=True,
            memo__note__is_active=True,
            memo__parent_memo_category__is_active=True,
            memo__child_memo_category__is_active=True,
            # memo__purpose__is_active=True,
            ).values(
                'memo__note',
                'memo__parent_memo_category',
                'memo__child_memo_category',
                'memo__purpose',
                'memo',
                'user').annotate(max_datetime=Max('updated_at'))

        is_aggregated_today = DmLearningEfficiencyBatchLog.objects.filter(aggregate_date=today).values('is_aggregated_today')

        learning_efficiencies = []
        if is_aggregated_today:
            print('update処理を開始')

            for latest_browsing_memo in latest_browsing_memos:
                learning_efficiencies.append(update_learning_efficiency_record(latest_browsing_memo))
            
            DmLearningEfficiency.objects.bulk_update(learning_efficiencies, [
                'learning_efficiency_rate',
                'note',
                'parent_memo_category',
                'child_memo_category',
                'purpose',
                'memo',
                'user'
            ])

            print('update処理を終了')

        else:
            print('insert処理を開始')

            print('insert処理前に発生したレコードの削除')
            dm_learning_efficiency_today = DmLearningEfficiency.objects.filter(aggregate_date=today)
            dm_learning_efficiency_today.delete()

            for latest_browsing_memo in latest_browsing_memos:
                learning_efficiencies.append(create_learning_efficiency_record(latest_browsing_memo))

            DmLearningEfficiency.objects.bulk_create(learning_efficiencies)
            
            DmLearningEfficiencyBatchLog.objects.create(aggregate_date=today)
            
            print('insert処理を終了')

