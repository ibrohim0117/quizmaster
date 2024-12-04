# import os
# import django
# from django.core.mail import send_mail
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizmaster.settings')
# django.setup()
#
# def task_send_mail(email, code):
#     subject = 'Tasdiqlash code'
#     message = f'{code}'
#     from_email = 'ibrohim.dev.uz@gmail.com'
#     recipient_list = [email]
#
#     return send_mail(subject, message, from_email, recipient_list)
#
#
# # task_send_mail('eabbduvoid@gmail.com', 123)