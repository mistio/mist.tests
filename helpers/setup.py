from tests import config


def setup_user_if_not_exists(context, user_email):
    if config['SETUP_ENVIRONMENT']:
        from mist.core.user.models import User
        from mist.core.user.models import Owner
        if context.mist_config.get(user_email):
            user_email = context.mist_config.get(user_email)
        try:
            user = Owner.objects.get(email=user_email)
        except Owner.DoesNotExist:
            user = User()
            user.email = user_email
        user.set_password(context.mist_config['PASSWORD1'])
        user.status = 'confirmed'
        user.save()


def remove_user(context, user_email):
    if config['SETUP_ENVIRONMENT']:
        from mist.core.user.models import Owner
        if context.mist_config.get(user_email):
            user_email = context.mist_config.get(user_email)
        try:
            Owner.objects.get(email=user_email).delete()
        except Owner.DoesNotExist:
            pass
