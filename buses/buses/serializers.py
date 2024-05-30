from genericpath import exists
from rest_framework import serializers
from .models import *

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["driver"] = instance.driver.user.full_name
        rep["destination"] = instance.destination.name
        return rep
    
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["bus"] = BusSerializer(instance.bus).data
        return rep
        
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        
    def get_fields(self):
        fields = super().get_fields()
        if self.context.get("get"):
            fields["buyer"] = serializers.StringRelatedField()
            fields["trip"] = serializers.StringRelatedField()
            
        return fields
                        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["password"] = None
        return rep      