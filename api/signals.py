import logging

from .models import UserLoginActivity, Investor
# for logging - define "error" named logging handler and logger in settings.py
from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

error_log = logging.getLogger('error')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                     login_username=user.username,
                                                     user_agent_info=user_agent_info,
                                                     status=UserLoginActivity.SUCCESS)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))


@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=credentials['username'],
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.FAILED)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    使用Profile模式扩展User，添加User时需要创建与其相对应的Investor
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # if created:
    #     Investor.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """
    使用Profile模式扩展User, 更新User时需要保存与其相对应的Investor
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # if created:
    #     instance.investor.save()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    保存系统用户同时保存自定义用户
    """
    if created:
        Investor.objects.create(user=instance)
    instance.investor.save()