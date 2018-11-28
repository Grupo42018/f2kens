from oauth2_provider import models as tokensmod
from django.conf import settings

from oauthlib.common import generate_token

from ..models import * 


def get_or_create_token(device):

    token = tokensmod.AccessToken.objects.filter(
        user=device.parent.user).order_by("-id").first()

    if not token:
        token = tokensmod.AccessToken.objects.create(
            user=device.parent.user,
            application=settings.F2KENS_APPLICATION,
            expires=datetime.date(
                year=datetime.date.today().year,
                month=12,
                day=20),
            token=generate_token())

        reftok = tokensmod.RefreshToken.objects.create(
            user=device.parent.user,
            application=settings.F2KENS_APPLICATION,
            token=generate_token(),
            access_token=token)

    else:
        reftok = tokensmod.RefreshToken.objects.get(access_token=token)
    
    return token, reftok

