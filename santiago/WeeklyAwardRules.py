from django.conf import settings
from santiago.models import UserChipCount

# for each player that has banked chips...
#   move up to 3000 from bank to RC count.
for chip_count in UserChipCount.objects.filter(bank_chips__gt=0):
    txfer = min(chip_count.bank_chips, settings.WEEKLY_CHIP_MAX)
    ChipTransaction.objects.create(user=chip_count.user, real_chips=txfer, bank_chips=0-txfer, type=CHIP_TX_TYPES.BANK_TRANSFER)
    chip_count.bank_chips -= txfer
    chip_count.real_chips += txfer
    chip_count.save()
    
    
