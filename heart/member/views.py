from django.core.cache import cache
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from member.models import Member
from member.serializers import MemberSerializer, HeartRateSerializer, HeartRateDTOSerializer


@api_view(['GET'])
def GetMemberAPI(request, nickname):
    if not nickname:
        return Response({'error': 'Nickname is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        member = Member.objects.get(nickname=nickname)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MemberSerializer(member)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def CreateOrUpdateMemberAPI(request):
    nickname = request.data.get('nickname')

    member, created = Member.objects.get_or_create(
        nickname=nickname,
        defaults=request.data
    )

    if created:
        serializer = MemberSerializer(member)
    else:
        serializer = MemberSerializer(instance=member, data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetNearByMembersAPI(request, nickname):
    if not nickname:
        return Response({'error': 'Nickname is required.'}, status=status.HTTP_400_BAD_REQUEST)

    redis_client = cache.client.get_client()
    results = redis_client.georadiusbymember("locations", nickname, 1, unit="km", withcoord=True)

    locations = []
    for result in results:
        member_nickname, (longitude, latitude) = result
        locations.append({
            "longitude": longitude,
            "latitude": latitude
        })

    return Response(locations, status=status.HTTP_200_OK)


@api_view(['GET'])
def GetHRVAPI(request, nickname):
    if not nickname:
        return Response({'error': 'Nickname is required.'}, status=status.HTTP_400_BAD_REQUEST)

    member = Member.objects.get(nickname=nickname)
    heart_rates = member.heart_rates.all().order_by('-created_at')[:5]

    # todo. AI에 보내 판단 후 결과 도출 -> 위험이면 비동기 noti 추가

    heart_rates_dto = [
        {**HeartRateDTOSerializer(heart_rate).data, "priority": idx + 1}
        for idx, heart_rate in enumerate(heart_rates)
    ]

    return Response(heart_rates_dto, status=status.HTTP_200_OK)


@api_view(['POST'])
def UpdateHRVAPI(request):
    with transaction.atomic():
        nickname = request.data.get('nickname')
        member = Member.objects.get(nickname=nickname)

        heart_rate_data = request.data.copy()
        heart_rate_data['member'] = member.id

        serializer = HeartRateSerializer(data=heart_rate_data)
        if serializer.is_valid():
            heart_rates = member.heart_rates.all().order_by('created_at')

            if len(heart_rates) == 5:
                heart_rates.first().delete()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def HelpAPI(request):
    nickname = request.data.get('nickname')
    coordinates = request.data.get('coordinates')

    longitude = float(coordinates.get('longitude'))
    latitude = float(coordinates.get('latitude'))

    redis_client = cache.client.get_client()
    results = redis_client.georadiusbymember("locations", nickname, 1, unit="km", withcoord=True)

    # todo. results의 멤버들에게 긴급 noti 보내기

    return Response("OK", status=status.HTTP_200_OK)
