from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Avg, F, Func, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.authentication.create_initial_user_data import create_initial_user_data

from . import serializers
from .models import (
    BrowsingMemoCount,
    DmBrowsingMemoCount,
    DmLearningEfficiency,
    Memo,
    MemoCategory,
    Note,
    Profile,
    Purpose,
    StickyNote,
    StickyNoteCategory,
)


class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s, 1)"


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user_id=self.request.user.user_id)

    # 新規作成するとき呼ばれる
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.user_id)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(user_id=self.request.user.user_id, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class ParentMemoCategoryViewSet(viewsets.ModelViewSet):
    queryset = MemoCategory.objects.all()
    serializer_class = serializers.ParentMemoCategorySerializer

    def get_queryset(self):
        return MemoCategory.objects.filter(
            user_id=self.request.user.user_id, parent_memo_category_id__isnull=True, is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(
            user_id=self.request.user.user_id,
            parent_memo_category_id=None,
        )


class ParentMemoCategoryFilterListView(generics.ListAPIView):
    queryset = MemoCategory.objects.all()
    serializer_class = serializers.ParentMemoCategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["note"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        return MemoCategory.objects.filter(
            user_id=self.request.user.user_id, parent_memo_category_id__isnull=True, is_active=True
        )


class ChildMemoCategoryViewSet(viewsets.ModelViewSet):
    queryset = MemoCategory.objects.all()
    serializer_class = serializers.ChildMemoCategorySerializer

    def get_queryset(self):
        return MemoCategory.objects.filter(
            user_id=self.request.user.user_id, parent_memo_category_id__isnull=False, is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class ChildMemoCategoryFilterListView(generics.ListAPIView):
    queryset = MemoCategory.objects.all()
    serializer_class = serializers.ChildMemoCategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["parent_memo_category"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        return MemoCategory.objects.filter(
            user_id=self.request.user.user_id, parent_memo_category_id__isnull=False, is_active=True
        )


class PurposeViewSet(viewsets.ModelViewSet):
    queryset = Purpose.objects.all()
    serializer_class = serializers.PurposeSerializer

    def get_queryset(self):
        return Purpose.objects.filter(user_id=self.request.user.user_id, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class PurposeFilterListView(generics.ListAPIView):
    queryset = Purpose.objects.all()
    serializer_class = serializers.PurposeSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["note"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        return Purpose.objects.filter(user_id=self.request.user.user_id, is_active=True)


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    serializer_class = serializers.MemoSerializer

    def get_queryset(self):
        return Memo.objects.filter(user_id=self.request.user.user_id, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class MemoFilterListView(generics.ListAPIView):
    queryset = Memo.objects.all()
    serializer_class = serializers.MemoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["memo_id", "parent_memo_category", "child_memo_category"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        return Memo.objects.filter(user_id=self.request.user.user_id, is_active=True)


class StickyNoteCategoryViewSet(viewsets.ModelViewSet):
    queryset = StickyNoteCategory.objects.all()
    serializer_class = serializers.StickyNoteCategorySerializer


class StickyNoteViewSet(viewsets.ModelViewSet):
    queryset = StickyNote.objects.all()
    serializer_class = serializers.StickyNoteSerializer

    def get_queryset(self):
        return StickyNote.objects.filter(user_id=self.request.user.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class BrowsingMemoCountViewSet(viewsets.ModelViewSet):
    queryset = BrowsingMemoCount.objects.all()
    serializer_class = serializers.BrowsingMemoCountSerializer

    def get_queryset(self):
        return BrowsingMemoCount.objects.filter(user_id=self.request.user.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class DmBrowsingMemoCountViewSet(viewsets.ModelViewSet):
    queryset = DmBrowsingMemoCount.objects.all()
    serializer_class = serializers.DmBrowsingMemoCountSerializer

    def get_queryset(self):
        return DmBrowsingMemoCount.objects.filter(user_id=self.request.user.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class DmLearningEfficiencyViewSet(viewsets.ModelViewSet):
    queryset = DmLearningEfficiency.objects.all()
    serializer_class = serializers.DmLearningEfficiencySerializer

    def get_queryset(self):
        return DmLearningEfficiency.objects.filter(user_id=self.request.user.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


class TodayLearningEfficiencyListView(generics.ListAPIView):
    queryset = DmLearningEfficiency.objects.all()
    serializer_class = serializers.TodayLearningEfficiencySerializer
    filter_backends = [OrderingFilter]

    def get_queryset(self):
        aggregate_date_today = date.today()
        aggregate_date_yesterday = date.today() - timedelta(1)

        return (
            DmLearningEfficiency.objects.filter(
                user_id=self.request.user.user_id,
                note__is_active=True,
                parent_memo_category__is_active=True,
                child_memo_category__is_active=True,
                memo__is_active=True,
                aggregate_date__gte=aggregate_date_yesterday,
                aggregate_date__lte=aggregate_date_today,
            )
            .order_by("-aggregate_date")
            .values("aggregate_date")
            .annotate(average_learning_efficiency_rate=Round(Avg("learning_efficiency_rate")))
        )


class ThreeMonthAverageLearningEfficiencyListView(generics.ListAPIView):
    queryset = DmLearningEfficiency.objects.all()
    serializer_class = serializers.ThreeMonthAverageLearningEfficiencySerializer

    def get_queryset(self):
        aggregate_date_today = date.today()
        aggregate_date_three_month_ago = date.today() - timedelta(89)
        aggregate_date_yesterday = date.today() - timedelta(1)
        aggregate_date_three_month_ago_yesterday = date.today() - timedelta(90)

        # unionを利用して昨日時点の３ヶ月平均も出力
        return (
            DmLearningEfficiency.objects.filter(
                user_id=self.request.user.user_id,
                aggregate_date__gte=aggregate_date_three_month_ago,
                aggregate_date__lte=aggregate_date_today,
            )
            .extra(select={"aggregate_unit": "'today'"})
            .values("user_id", "aggregate_unit")
            .annotate(average_learning_efficiency_rate=Round(Avg("learning_efficiency_rate")))
            .union(
                DmLearningEfficiency.objects.filter(
                    user_id=self.request.user.user_id,
                    note__is_active=True,
                    parent_memo_category__is_active=True,
                    child_memo_category__is_active=True,
                    memo__is_active=True,
                    aggregate_date__gte=aggregate_date_three_month_ago_yesterday,
                    aggregate_date__lte=aggregate_date_yesterday,
                )
                .extra(select={"aggregate_unit": "'yesterday'"})
                .values("user_id", "aggregate_unit")
                .annotate(average_learning_efficiency_rate=Round(Avg("learning_efficiency_rate")))
            )
        )


class EachNoteLearningEfficiencyListView(generics.ListAPIView):
    queryset = DmLearningEfficiency.objects.all()
    serializer_class = serializers.EachNoteLearningEfficiencySerializer

    def get_queryset(self):
        aggregate_date_today = date.today()

        return (
            DmLearningEfficiency.objects.filter(
                user_id=self.request.user.user_id,
                note__is_active=True,
                parent_memo_category__is_active=True,
                child_memo_category__is_active=True,
                memo__is_active=True,
                aggregate_date=aggregate_date_today,
            )
            .values("aggregate_date", "note_id", note_color=F("note__note_color"), note_name=F("note__note_name"))
            .annotate(average_learning_efficiency_rate=Round(Avg("learning_efficiency_rate")))
        )


class EachParentMemoCategoryLearningEfficiencyListView(generics.ListAPIView):
    queryset = DmLearningEfficiency.objects.all()
    serializer_class = serializers.EachParentMemoCategoryLearningEfficiencySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["note"]

    def get_queryset(self):
        aggregate_date_today = date.today()

        return (
            DmLearningEfficiency.objects.filter(
                user_id=self.request.user.user_id,
                note__is_active=True,
                parent_memo_category__is_active=True,
                child_memo_category__is_active=True,
                memo__is_active=True,
                aggregate_date=aggregate_date_today,
            )
            .values(
                "aggregate_date",
                "note_id",
                "parent_memo_category_id",
                parent_memo_category_name=F("parent_memo_category__memo_category_name"),
                parent_memo_category_icon=F("parent_memo_category__memo_category_icon"),
            )
            .annotate(average_learning_efficiency_rate=Round(Avg("learning_efficiency_rate")))
        )


class EachMemoLearningEfficiencyListView(generics.ListAPIView):
    queryset = DmLearningEfficiency.objects.all()
    serializer_class = serializers.EachMemoLearningEfficiencySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["parent_memo_category"]

    def get_queryset(self):
        aggregate_date_today = date.today()

        return (
            DmLearningEfficiency.objects.filter(
                user_id=self.request.user.user_id,
                note__is_active=True,
                parent_memo_category__is_active=True,
                child_memo_category__is_active=True,
                memo__is_active=True,
                aggregate_date=aggregate_date_today,
            )
            .extra(select={"elapsed_date_count": "DATEDIFF(CURRENT_TIMESTAMP,t_memos.created_at)"})
            .values(
                "id",
                "aggregate_date",
                "note_id",
                "parent_memo_category_id",
                "child_memo_category_id",
                "memo_id",
                "learning_efficiency_rate",
                "elapsed_date_count",
                child_memo_category_name=F("child_memo_category__memo_category_name"),
                child_memo_category_icon=F("child_memo_category__memo_category_icon"),
                memo_title=F("memo__memo_title"),
                memo_priority=F("memo__memo_priority"),
            )
        )


# ユーザー登録時に作成するチュートリアルデータを作成する
@api_view(["GET"])
def initialize_user_data(request):
    create_initial_user_data(request.user)
    return Response({"message": "Created Initial Data!"})
