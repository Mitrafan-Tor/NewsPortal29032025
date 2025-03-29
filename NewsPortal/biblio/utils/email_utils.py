from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_new_post_notification(post, subscribers_emails):
    category = post.categories.first()  # Получаем первую категорию

    html_content = render_to_string(
        'email/new_post_notification.html',  # Используем единый шаблон
        {
            'post': post,
            'category': category,
            'site_url': settings.SITE_URL
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Новая публикация в категории "{category.name}"' if category else f'Новая публикация: {post.title}',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()