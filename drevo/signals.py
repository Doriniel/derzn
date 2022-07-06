import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from drevo.models import Znanie, Relation
from dz import settings

from drevo.sender import send_email
from loguru import logger

logger.add('logs/main.log',
           format="{time} {level} {message}", rotation='100Kb', level="INFO")


def notify(sender, instance: Znanie, created, **kwargs):
    if not instance.is_published or not instance.author or instance.tz.is_systemic:
        return
    user_to_notify = instance.author.subscribers.all()
    if not user_to_notify:
        return
    author_publication_url = settings.BASE_URL + instance.get_absolute_url()
    message_subject = 'Новое знание'
    message_content = 'Уважаемый {}{}!\n' \
                      f'{datetime.date.today()} было создано новое' \
                      f' знание:\n  {author_publication_url}\n' \
                      f'Автор: {instance.author}\n'
    for addressee in user_to_notify:
        patr = ''
        user_profile = addressee.profile
        if addressee.first_name and user_profile.patronymic:
            patr = ' ' + user_profile.patronymic
        appeal = addressee.first_name or 'пользователь'
        send_email(addressee.email, message_subject, False,
                   message_content.format(appeal, patr))


@receiver(post_save, sender=Relation)
def notify_new_interview(sender, instance, created, **kwargs):
    """
    Сигнал, который создает рассылку экспертам с коментенциями соответствующей категории и ее предков о
    публикации знания вида "Интервью"
    """
    if not created or not instance.bz.is_published or not instance.is_published or \
            instance.bz.tz.is_systemic or instance.bz.tz.name != 'Интервью':
        return
    message_subj = 'Новое интервью'
    knowledge_url = settings.BASE_URL + instance.bz.get_absolute_url()
    date = instance.rz.name.split('-')
    message_text = 'Уважаемый {}{}!\n' \
                   f'Приглашаем Вас принять участие в новом интервью, которое состоится с ' \
                   f'{date[0]} по {date[1]}.\n' \
                   f'{knowledge_url} - интервью, \n' \
                   f'Администрация портала «Дерево знаний»'
    categories = instance.bz.get_ancestors_category()
    for category in categories:
        experts = category.get_experts()
        if not experts:
            continue
        for expert in experts:
            patronymic = ''
            user = expert.expert
            user_profile = user.profile
            if user.first_name and user_profile.patronymic:
                patronymic = ' ' + user_profile.patronymic
            name = user.first_name or 'Пользователь'
            send_email(user.email, message_subj, False, message_text.format(name, patronymic))
