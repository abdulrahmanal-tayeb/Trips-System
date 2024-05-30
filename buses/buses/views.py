from multiprocessing import managers
from rest_framework.views import APIView
import serial
from django.db import transaction
from buses.buses.utils import is_valid_date
from buses.serializers import BusSerializer, TicketSerializer, TripSerializer
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .decorators import managers_only

class SignInAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not (email and password):
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        data = {
            "access": str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_200_OK)
    
    
class SignUpAPIView(APIView):
    authentication_classes = []
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        confirmation = request.data.get("confirmation")

        if not (email and password and confirmation):
            return Response({"error": "Email, password, and confirmation are required."}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirmation:
            return Response({"error": "Password and confirmation do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(email=email, password=password)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        data = {
            "access": str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_201_CREATED)


class BusAPIView(APIView):

    @managers_only
    def post(self, request):
        driver = Driver.objects.filter(user__id=request.data.get("driver"), is_available=True).first()
        if not driver:
            return Response({"errm": "No driver available found."}, status=404)

        serialized = BusSerializer(data={**request.data, "driver": driver.id})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        
        return Response(status=201)
    
    def get(self, request):
        bus_id = request.GET.get("id")
        if bus_id:
            bus = Bus.objects.filter(id=bus_id).first()
            if not bus:
                return Response(status=404)
            return Response(BusSerializer(bus).data, status=200)
        
        return Response(BusSerializer(Bus.objects.select_related("driver").all(), many=True).data, status=200)
    
    @managers_only
    def put(self, request, id):
        bus = Bus.objects.filter(id=id).first()
        if not bus:
            return Response(status=404)
        serialized = BusSerializer(bus, data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(status=204)
    
    
class TicketAPIView(APIView):
    @managers_only
    def post(self, request):
        trip = Trip.objects.select_related("trip").filter(id=request.data.get("trip")).first()
        if not trip:
            return Response(status=404)
        
        if trip.passengers == trip.bus.seats:
            return Response({"errm": "Trip already full."}, status=403)
        
        serialized = TicketSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        trip.passengers += 1
        with transaction.atomic():
            trip.save()
            serialized.save()
            
        return Response(status=200)
    
    @managers_only
    def get(self, request):
        id = request.GET.get("id")
        if not id:
            return Response(status=400)
        
        try:
            ticket = Ticket.objects.select_related("buyer", "trip__bus__destination").get(id=id)
        except Ticket.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            print("EXCEPTION : ", e)
            return Response(status=500)
    
        return Response(TicketSerializer(ticket, context={"get": True}).data, status=200)
     
     
class TicketHistoryAPIView(APIView):
    def get(self, request):
        tickets = Ticket.objects.filter(buyer__id=request.user.id)
        return Response(TicketSerializer(tickets, many=True, context={"get": True}).data, status=200)


class TripAPIView(APIView):
    def get(self, request):
        return Response(
            TripSerializer(
                Trip.objects.select_related("bus__driver", "bus__destination").all(),
                many=True
            ).data
            , status=200
        )

    @managers_only
    def post(self, request):
        print("REQUEST DATA: ", request.data)
        if not is_valid_date(request.data.get("date")):
            return Response({"errm": "Invalid Date"}, status=400)
        
        serialized = TripSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(status=status.HTTP_201_CREATED)
    
class DestinationAPIView(APIView):
    @managers_only
    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response(status=400)
        
        Destination.objects.get_or_create(name__icontains=name)
        return Response(status=200)
    
        
@api_view(["GET"])
def trip_search(request):
    trip_name = request.GET.get("tname")
    trips = Trip.objects.select_related("bus__destination").filter(bus__destination__name__icontains=trip_name, **({"available_seats__gt": 0} if request.GET.get("ao") else {}))
    return Response(TripSerializer(trips, many=True).data, status=200)
