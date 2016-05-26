from behave import step


@step(u'I setup user with email "{user_email}"')
def setup_user(context, user_email):
    if context.mist_config['SETUP_ENVIRONMENT']:
        from mist.core.user.models import User
        from mist.core.user.models import Owner
        if context.mist_config.get(user_email):
            user_email = context.mist_config.get(user_email)
        try:
            Owner.objects.get(email=user_email)
        except Owner.DoesNotExist:
            user = User()
            user.email = user_email
            user.set_password(context.mist_config['PASSWORD1'])
            user.save()


@step(u'I make sure user with email "{user_email}" is absent')
def setup_user(context, user_email):
    if context.mist_config['SETUP_ENVIRONMENT']:
        from mist.core.user.models import Owner
        if context.mist_config.get(user_email):
            user_email = context.mist_config.get(user_email)
        try:
            Owner.objects.get(email=user_email).delete()
        except Owner.DoesNotExist:
            pass
