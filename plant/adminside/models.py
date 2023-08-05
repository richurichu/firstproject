from django.db import models

# Create your models here.
class ReferralProgram(models.Model):
    description = models.TextField()
    referrer_bonus_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=10.00)
    referrer_max_bonus_amount = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    referee_bonus_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=5.00)
    referee_max_bonus_amount = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)

    def __str__(self):
        return "Referral Program"
