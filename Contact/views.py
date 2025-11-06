from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactMessageSerializer
from .models import ContactMessage
from .tasks import send_contact_email  # will implement for celery
# if not using celery you can call send_contact_email.sync_send(...)

class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            msg = serializer.save()
            # send email in background (Celery)
            try:
                send_contact_email.delay(msg.id)
            except Exception:
                # fallback: call synchronous function (if you prefer)
                from .emails import sync_send_contact_email
                try:
                    sync_send_contact_email(msg.id)
                except Exception as e:
                    msg.error = str(e)
                    msg.save()
            return Response({'detail': 'Message received'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
