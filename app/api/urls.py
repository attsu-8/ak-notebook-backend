from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "user"

router = DefaultRouter()
router.register("profile", views.ProfileViewSet)
router.register("note", views.NoteViewSet)
router.register("parent-memo-category", views.ParentMemoCategoryViewSet)
router.register("child-memo-category", views.ChildMemoCategoryViewSet)
router.register("purpose", views.PurposeViewSet)
router.register("memo", views.MemoViewSet)
router.register("sticky-note-category", views.StickyNoteCategoryViewSet)
router.register("sticky-note", views.StickyNoteViewSet)
router.register("browsing-memo-count", views.BrowsingMemoCountViewSet)
router.register("dm-browsing-memo-count", views.DmBrowsingMemoCountViewSet)
router.register("dm-learning-efficiency", views.DmLearningEfficiencyViewSet)

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("myprofile/", views.MyProfileListView.as_view(), name="myprofile"),
    path(
        "filter/parent-memo-category/",
        views.ParentMemoCategoryFilterListView.as_view(),
        name="parent-memo-category-filter",
    ),
    path(
        "filter/child-memo-category/",
        views.ChildMemoCategoryFilterListView.as_view(),
        name="child-memo-category-filter",
    ),
    path("filter/purpose/", views.PurposeFilterListView.as_view(), name="purpose-filter"),
    path("filter/memo/", views.MemoFilterListView.as_view(), name="memo-filter"),
    path("dm/today-learning-efficiency-rate/", views.TodayLearningEfficiencyListView.as_view(), name="dm-today"),
    path(
        "dm/three-month-ago-avg-learning-efficiency-rate/",
        views.ThreeMonthAverageLearningEfficiencyListView.as_view(),
        name="dm-three-month-ago-avg",
    ),
    path(
        "dm/each-note-learning-efficiency-rate/",
        views.EachNoteLearningEfficiencyListView.as_view(),
        name="dm-each-note",
    ),
    path(
        "dm/each-parent-memo-category-learning-efficiency-rate/",
        views.EachParentMemoCategoryLearningEfficiencyListView.as_view(),
        name="dm-each-note",
    ),
    path(
        "dm/each-memo-learning-efficiency-rate/",
        views.EachMemoLearningEfficiencyListView.as_view(),
        name="dm-each-note",
    ),
    path("", include(router.urls)),
    path("healthcheck/", lambda request: HttpResponse()),  # ヘルスチェック用
    path("initial-data/", views.initialize_user_data, name="initial-data"),
]
