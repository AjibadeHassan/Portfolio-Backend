import json
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

@csrf_exempt
def contact_message(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        email_data = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": os.getenv("TO_EMAIL")}],
            sender={"email": email, "name": name},
            subject=f"New Portfolio Message from {name}",
            html_content=f"""
                <h3>New message from your portfolio</h3>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {email}</p>
                <p><b>Message:</b><br>{message}</p>
            """
        )

        try:
            api_instance.send_transac_email(email_data)
            return JsonResponse({"status": "success"}, status=200)

        except ApiException as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

