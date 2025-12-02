from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

User = get_user_model()
token_generator = PasswordResetTokenGenerator() 

@receiver(post_save, sender=User)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        user = instance
        token = token_generator.make_token(user)

        confirm_url = f"http://localhost:8000/auth/confirm-email/{user.pk}/{token}/"

        subject = "Confirm your email"
        from_email = "no-reply@example.com"
        to_email = user.email

        html_content = render_to_string("emails/confirm_email.html", {
            "confirm_url": confirm_url
        })

        email = EmailMultiAlternatives(
            subject=subject,
            body="Please confirm your email.",
            from_email=from_email,
            to=[to_email],
        )

        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
