from django.db import models
from django.conf import settings
from course.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class Payment(models.Model):
    CARD = 'Card'
    TRANSFER = 'Transfer'

    PAYMENT_METHOD_CHOICES = (
        (CARD, 'Card'),
        (TRANSFER, 'Transfer'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Payment Date', )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Payment Amount', )
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD_CHOICES,
                                      default=CARD, verbose_name='Payment Method', )
    course_payment = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='payments', )
    lesson_payment = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, related_name='payments', )

    payment_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Payment Owner')

    def __str__(self):
        return f"Payment from {self.user} for {self.course_payment if self.course_payment else self.lesson_payment}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']
