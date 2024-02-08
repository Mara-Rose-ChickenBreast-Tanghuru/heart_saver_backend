from rest_framework import serializers

from member.models import Member, HeartRate


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class HeartRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartRate
        fields = '__all__'


class HeartRateDTOSerializer(serializers.ModelSerializer):
    priority = serializers.IntegerField(read_only=True)

    class Meta:
        model = HeartRate
        fields = ['hrv', 'priority']
