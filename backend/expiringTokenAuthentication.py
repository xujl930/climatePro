# -*- coding:utf8 -*-
from rest_framework.authentication import TokenAuthentication
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.db import transaction

from rest_framework.authtoken.models import Token

import os
import hashlib

class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        # Token过期的验证，如果当前的时间大于Token指定，那么久返回Token已经过期
        if timezone.now() > (
            token.created + timedelta(days=15)):
            # 生成新的token并更新
            token_key = hashlib.sha1(os.urandom(24)).hexdigest()
            #created = timezone.now()
            user_id = token.user_id
            with transaction.atomic():
                sid = transaction.savepoint()
                token.delete()
                token = Token(key=token_key,user_id=user_id)
                print(token.created)
                token.save()
                transaction.savepoint_commit(sid)
            transaction.commit()
            #token.objects.create(key=token_key, created=timezone.now(), user_id = 6)
            raise exceptions.AuthenticationFailed(_('Token has expired'))

        return (token.user, token)