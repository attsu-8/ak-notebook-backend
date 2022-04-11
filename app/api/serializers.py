from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Note, MemoCategory, Purpose, Memo, StickyNoteCategory, StickyNote, BrowsingMemoCount, DmBrowsingMemoCount, DmLearningEfficiency


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'user_id',
            'user_email',
            'password'
            )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = Profile
        fields = (
            'profile_id',
            'profile_nickname',
            'profile_image',
            'user',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class NoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = Note
        fields = (
            'note_id',
            'note_name',
            'note_color',
            'user',
            'is_active',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class ParentMemoCategorySerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = MemoCategory
        fields = (
            'memo_category_id',
            'memo_category_name',
            'memo_category_icon',
            'parent_memo_category',
            'note',
            'user',
            'is_active',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True},
            'parent_memo_category': {'read_only': True}
        }


class ChildMemoCategorySerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = MemoCategory
        fields = (
            'memo_category_id',
            'memo_category_name',
            'memo_category_icon',
            'parent_memo_category',
            'note',
            'user',
            'is_active',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True},
        }


class PurposeSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = Purpose
        fields = (
            'purpose_id',
            'purpose_name',
            'purpose_icon',
            'note',
            'user',
            'is_active',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True},
        }


class MemoSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = Memo
        fields = (
            'memo_id',
            'memo_title',
            'memo_priority',
            'memo_text',
            'note',
            'parent_memo_category',
            'child_memo_category',
            'purpose',
            'user',
            'is_active',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class StickyNoteCategorySerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = StickyNoteCategory
        fields = (
            'sticky_note_category_code',
            'sticky_note_category_name',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class StickyNoteSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = StickyNote
        fields = (
            'sticky_note_id',
            'sticky_note_text',
            'sticky_note_category',
            'user',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class BrowsingMemoCountSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = BrowsingMemoCount
        fields = (
            'browsing_memo_count',
            'memo',
            'user',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class DmBrowsingMemoCountSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    note_name = serializers.ReadOnlyField(source="note.note_name")
    parent_memo_category_icon = serializers.ReadOnlyField(source="parent_memo_category.memo_category_icon")
    parent_memo_category_name = serializers.ReadOnlyField(source="parent_memo_category.memo_category_name")
    child_memo_category_icon = serializers.ReadOnlyField(source="child_memo_category.memo_category_icon")
    child_memo_category_name = serializers.ReadOnlyField(source="child_memo_category.memo_category_name")
    purpose_icon = serializers.ReadOnlyField(source="purpose.purpose_icon")
    purpose_name = serializers.ReadOnlyField(source="purpose.purpose_name")

    class Meta:
        model = DmBrowsingMemoCount
        fields = (
            'total_browsing_memo_count',
            'note',
            'note_name',
            'parent_memo_category',
            'parent_memo_category_icon',
            'parent_memo_category_name',
            'child_memo_category_icon',
            'child_memo_category_name',
            'purpose_icon',
            'purpose_name',
            'child_memo_category',
            'purpose',
            'memo',
            'user',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }


class DmLearningEfficiencySerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",read_only=True)

    class Meta:
        model = DmLearningEfficiency
        fields = (
            'id',
            'aggregate_date',
            'learning_efficiency_rate',
            'note',
            'parent_memo_category',
            'child_memo_category',
            'purpose',
            'memo',
            'user',
            'created_at',
            'updated_at'
            )
        extra_kwargs = {
            'user': {'read_only': True}
        }



class TodayLearningEfficiencySerializer(serializers.ModelSerializer):
    average_learning_efficiency_rate = serializers.FloatField()
    class Meta:
        model = DmLearningEfficiency
        fields = (
            'aggregate_date',
            'average_learning_efficiency_rate',
            )


class ThreeMonthAverageLearningEfficiencySerializer(serializers.Serializer):
    aggregate_unit = serializers.CharField()
    average_learning_efficiency_rate = serializers.FloatField()
    # class Meta:
    #     model = DmLearningEfficiency
    #     fields = (
    #         'aggregate_date',
    #         'average_learning_efficiency_rate',
    #         )


#モデルシリアライザで定義したいがバグの解消ができず、違う方法で実装
class EachNoteLearningEfficiencySerializer(serializers.Serializer):
    aggregate_date = serializers.DateField()
    note_id = serializers.UUIDField()
    note_name = serializers.CharField()
    note_color = serializers.CharField()
    average_learning_efficiency_rate = serializers.FloatField()


class EachParentMemoCategoryLearningEfficiencySerializer(serializers.Serializer):
    aggregate_date = serializers.DateField()
    note_id = serializers.UUIDField()
    parent_memo_category_id = serializers.UUIDField()
    parent_memo_category_name = serializers.CharField()
    parent_memo_category_icon = serializers.CharField()
    average_learning_efficiency_rate = serializers.FloatField()


class EachMemoLearningEfficiencySerializer(serializers.Serializer):
    id=serializers.CharField()
    aggregate_date = serializers.DateField()
    note_id = serializers.UUIDField()
    parent_memo_category_id = serializers.UUIDField()
    child_memo_category_id = serializers.UUIDField()
    child_memo_category_name = serializers.CharField()
    child_memo_category_icon = serializers.CharField()
    memo_id = serializers.UUIDField()
    memo_title = serializers.CharField()
    learning_efficiency_rate = serializers.FloatField()
    elapsed_date_count = serializers.IntegerField()