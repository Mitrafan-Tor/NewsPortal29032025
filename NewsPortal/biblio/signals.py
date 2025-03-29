from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Post, CategorySubscriber


@receiver(m2m_changed, sender=Post.categories.through)
def notify_about_new_post(sender, instance, action, **kwargs):
    if action == "post_add":
        try:
            # Получаем все категории поста
            categories = instance.categories.all()

            # Собираем всех подписчиков этих категорий
            subscribers_emails = set()

            for category in categories:
                # Получаем всех подписчиков категории
                subscribers = CategorySubscriber.objects.filter(category=category)
                subscribers_emails.update([sub.user.email for sub in subscribers if sub.user.email])

            # Если есть подписчики - отправляем уведомления
            if subscribers_emails:
                send_post_notification(instance, categories.first(), list(subscribers_emails))

        except Exception as e:
            # Логирование ошибки (можно заменить на logger.error в production)
            print(f"Ошибка при отправке уведомлений: {str(e)}")


def send_post_notification(post, category, recipients):
    """
    Отправка email-уведомления о новой публикации
    """
    try:
        subject = f'Новая публикация в категории "{category.name}"'

        # Рендеринг HTML-шаблона письма
        html_content = render_to_string(
            'email/new_post_notification.html',
            {
                'post': post,
                'category': category,
                'site_url': settings.SITE_URL
            }
        )

        # Создание и отправка письма
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',  # Текстовое содержимое (пустое, так как используем html)
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        print(f"Ошибка при формировании письма: {str(e)}")