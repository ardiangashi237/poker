from django.db import models
from django.db.models import Q, Sum, Max
from django.contrib.auth.models import User
from django.contrib.localflavor.us import models as us_models
from django.utils import timezone
from django.conf import settings
import datetime

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


LEGAL_STATES = (
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('HI', 'Hawaii'),
    ('IL', 'Illinois'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MA', 'Massachusetts'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

class RegistrationProfile(models.Model):
    email = models.EmailField()
    activation_key = models.CharField(max_length=40)
    joined_via_fb = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=20, blank=True)
    client_ip = models.CharField(blank=True, max_length=30)
    client_host = models.CharField(blank=True, max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class RegistrationProfileVerification(models.Model):
    registration_profile = models.OneToOneField(RegistrationProfile, related_name="verification")
    client_ip = models.CharField(blank=True, max_length=30)
    client_host = models.CharField(blank=True, max_length=100)
    verified = models.DateTimeField(auto_now_add=True)

class SecurityQuestion(models.Model):
    question = models.CharField(max_length=100)

    def __unicode__(self):
        return self.question

class MembershipLevel(models.Model):
    name = models.CharField('membership level', max_length=20)
    daily_top_up_threshold = models.IntegerField()
    ad_required_for_top_up = models.BooleanField(default=True)
    allow_chip_purchases = models.BooleanField()
    signup_award = models.IntegerField(default=200)
    monthly_award = models.IntegerField(default=200)
    
    def __unicode__(self):
        return self.name

class UserMembershipLevelHistory(models.Model):
    user = models.ForeignKey(User)
    level = models.ForeignKey(MembershipLevel)
    effective_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)


    def user_first_name (self):
        return self.user.first_name 
        user_first_name.short_description = 'first name'

    def user_last_name (self):
        return self.user.last_name
        user_last_name.short_description = 'last name'

    def user_user_name (self):
        return self.user.username
        user_user_name.short_description = 'user name'

    def user_email(self):
        return self.user.email
        user_email.short_description = 'email address'

    class Meta:
        verbose_name_plural = "User membership history"

#def get_default_member_level():
#    return MembershipLevel.objects.get(id=1)
class CHIP_TX_TYPES:
    DAILY_TOP_UP = "TOP"
    PURCHASE = "PUR"
    MONTHLY_AWARD = "MON"
    BANK_TRANSFER  = "TXF"

CHIP_TX_CHOICES = (
    (CHIP_TX_TYPES.DAILY_TOP_UP, "Daily Top-Up"),
    (CHIP_TX_TYPES.PURCHASE, "Chip Purchase"),
    (CHIP_TX_TYPES.MONTHLY_AWARD, "Monthly Award"),
    (CHIP_TX_TYPES.BANK_TRANSFER, "Bank Transfer"),
)


class ChipTransaction(models.Model):
    user = models.ForeignKey(User)
    real_chips = models.IntegerField()
    bank_chips = models.IntegerField()
    type = models.CharField(max_length=3, choices=CHIP_TX_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    initiating_tx_id = models.IntegerField(null=True)


class UserProfile(models.Model):
    PIN_DELIVERY_CHOICES = (
        ("TXT", "Text Message"),
        ("VOC", "Voice Call"),
    )

    user = models.OneToOneField(User)
    facebook_id = models.CharField(max_length=20, blank=True)
    current_member_level = models.ForeignKey(MembershipLevel) #, default=get_default_member_level) 
    current_level_effective_date = models.DateField("Effective Date", blank=True, null=True)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(blank=True, max_length=255)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, choices=LEGAL_STATES)
    zip = models.CharField(max_length=64)
    security_question = models.ForeignKey(SecurityQuestion)
    security_answer = models.CharField(max_length=50)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = us_models.PhoneNumberField()
    pin_delivery = models.CharField(choices=PIN_DELIVERY_CHOICES, max_length=3)

    def at_table(self):
        # find buyins for this user where live_chips > 0 or real_chips > 0
        # if we have any buyins that meet these criteria, user is at table
        return self.user.buyin_set.filter(
                Q(real_chips__gt=0) | Q(live_chips__gt=0)
            ).count() > 0


    def chips_this_week(self):
        ''' Returns the number of chips earned/purchased/assigned to this user
                since Monday. Included in the count are chips tranferred in from
                user's chip bank, purchased, and those earned from affiliate
                offers and friend referrals. Conversely, sign up awards, monthly 
                awards, and daily top-ups do not contribute to this number. '''
        # begin by figuring out when Monday was (based on today)
        # again, note settings.TIME_ZONE must be set properly to America/New_York
        local_now = timezone.localtime(timezone.now())
        # for weekday(), 0=MON, 1=TUE...6=SUN, so we can subtract it to get to monday
        delta_from_mon = datetime.timedelta(days=local_now.weekday())
        mon = local_now - delta_from_mon
        # now set mon's time to 00:00:00, which is when weekly max resets
        mon_min = datetime.datetime.combine(mon, datetime.time.min)
        # combine() returns a naive datetime, so now we must localize it
        mon_min = timezone.get_current_timezone().localize(mon_min)

        # now query chip transactions that have occurred since then and sum the chips
        txs_since_mon = self.user.chiptransaction_set.filter(
                                                    type=CHIP_TX_TYPES.PURCHASE,
                                                    timestamp__gte=mon_min)

        chips_this_week = txs_since_mon.aggregate(Sum('real_chips'))['real_chips__sum']
        return int(chips_this_week or 0)


    def topped_up_today(self):
        # find max top-up timestamp for this user
        most_recent = self.user.chiptransaction_set.filter(
                                                        type=CHIP_TX_TYPES.DAILY_TOP_UP
                                                    ).aggregate( 
                                                        Max('timestamp') 
                                                    )['timestamp__max']
        if most_recent == None: return False
        # Note that timezone.localtime is NYC time due to settings.TIME_ZONE
        ordinal_most_recent = timezone.localtime(most_recent).toordinal()
        ordinal_now = timezone.localtime(timezone.now()).toordinal()
        # should be impossible for ordinal_most_recent to be > ordinal_now
        return ordinal_most_recent >= ordinal_now


    def upgrade_to_premium(self):
        # finalize current history record
        effective_date = timezone.now()

        try:
            curr_level = UserMembershipLevelHistory.objects.get(user=self.user, end_date__isnull=True)
            curr_level.end_date = effective_date
            curr_level.save()
        except UserMembershipLevelHistory.DoesNotExist:
            # don't worry about this for now
            pass

        premium = MembershipLevel.objects.get(pk=2)

        # write record for this new transaction
        UserMembershipLevelHistory.objects.create(user=self.user, level=premium)

        # finally upgrade the user's current status
        self.current_member_level = premium
        self.current_level_effective_date = effective_date

        self.save()


    def perform_top_up(self):
        # make doubly sure user has not already topped up
        if self.topped_up_today(): raise Exception()

        # top up the user's chips and log it
        top_up_level = self.current_member_level.daily_top_up_threshold
        chips_to_add = top_up_level - self.user_real_chip_balance()
        self.user.userchipcount.real_chips += chips_to_add
        self.user.userchipcount.save()

        ChipTransaction.objects.create(user=self.user, real_chips=chips_to_add, bank_chips=0, type=CHIP_TX_TYPES.DAILY_TOP_UP)


    def purchase_chip_package(self, chip_package_id):
        # TODO; write purchase record a la order_header
        package = ChipPackage.objects.get(pk=chip_package_id)
        chips_to_add = min((settings.WEEKLY_CHIP_MAX - self.chips_this_week()), package.chip_qty)
        chips_to_bank = package.chip_qty - chips_to_add

        self.user.userchipcount.real_chips += chips_to_add
        self.user.userchipcount.bank_chips += chips_to_bank
        self.user.userchipcount.save()

        ChipTransaction.objects.create(user=self.user, real_chips=chips_to_add, bank_chips=chips_to_bank, type=CHIP_TX_TYPES.PURCHASE)
  
    def current_join_date(self):
        curr_level = UserMembershipLevelHistory.objects.get(user=self.user, end_date__isnull=True)
        return curr_level.effective_date 
   
    def member_level(self):
        return self.current_member_level.name
    member_level.short_description = 'level'
 
    def user_first_name(self):
        return self.user.first_name 
    user_first_name.short_description = 'first name'

    def user_last_name(self):
        return self.user.last_name
    user_last_name.short_description = 'last name'

    def user_user_name(self):
        return self.user.username
    user_user_name.short_description = 'user name'

    def user_email(self):
        return self.user.email
    user_email.short_description = 'email address'

    def user_password(self):
        return self.user.password
    user_password.short_description = 'password'

    def user_real_chip_balance(self):
        ''' Base chip count plus table buy-ins. '''
        chips_base = self.user.userchipcount.real_chips
        return chips_base + self.real_chips_in_play()
    user_real_chip_balance.short_description = 'real chip balance'

    def real_chips_in_play(self):
        chips_at_table = self.user.buyin_set.aggregate(Sum('real_chips'))['real_chips__sum']
        return int(chips_at_table or 0) # if sum is None, make it 0

    def real_chips_available(self):
        return self.user_real_chip_balance() - self.real_chips_in_play()

    def user_live_chip_balance(self):
        chips_base = self.user.userchipcount.live_chips
        return chips_base + self.live_chips_in_play() + self.live_chips_in_auction()
    user_live_chip_balance.short_description = 'live chip balance'

    def live_chips_in_play(self):
        chips_at_table = self.user.buyin_set.aggregate(Sum('live_chips'))['live_chips__sum']
        return int(chips_at_table or 0) # if sum is None, make it 0

    def live_chips_in_auction(self):
        return 0

    def live_chips_available(self):
        return self.user_live_chip_balance() - self.live_chips_in_play() - self.live_chips_in_auction()

    def total_chips(self):
        return self.user_real_chip_balance() + self.user_live_chip_balance()

class Badge(models.Model):
    earned_filename = models.CharField(max_length=255)
    unearned_filename = models.CharField(max_length=255)
    sequence = models.IntegerField()
    timestamp = models.DateField(auto_now_add=True)
    alt_text = models.CharField(max_length=100)

class Avatar(models.Model):
    AVATAR_CHOICES = (
        ("F", "Freemium"),
        ("P", "Premium"),
    )

    type = models.CharField(choices=AVATAR_CHOICES, max_length=1)
    active = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class PokernetUser(models.Model):
    serial = models.AutoField(primary_key=True)
    created = models.IntegerField()
    name = models.CharField(max_length=192)
    email = models.CharField(max_length=255, unique=True, blank=True)
    affiliate = models.IntegerField()
    skin_url = models.CharField(max_length=765)
    skin_outfit = models.TextField(blank=True)
    skin_image = models.TextField(blank=True)
    skin_image_type = models.CharField(max_length=96, blank=True)
    password = models.CharField(max_length=96)
    privilege = models.IntegerField()
    locale = models.CharField(max_length=96)
    rating = models.IntegerField()
    future_rating = models.FloatField()
    games_count = models.IntegerField()
    class Meta:
        db_table = u'users'



class PokernetChipCount(models.Model):
    user_serial = models.IntegerField(primary_key=True)
    currency_serial = models.IntegerField(primary_key=True)
    amount = models.BigIntegerField()
    rake = models.BigIntegerField()
    points = models.BigIntegerField()
    class Meta:
        db_table = u'user2money'




class UserChipCount(models.Model):
    user = models.OneToOneField(User, null=True)
    serial = models.IntegerField()
    real_chips = models.IntegerField()
    live_chips = models.IntegerField()
    bank_chips = models.IntegerField()



class ChipPackage(models.Model):
    name = models.CharField(max_length=20)
    chip_qty = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.name


class PokerTable(models.Model):
    serial = models.IntegerField(primary_key=True)
    resthost_serial = models.IntegerField()
    seats = models.IntegerField(null=True, blank=True)
    average_pot = models.IntegerField(null=True, blank=True)
    hands_per_hour = models.IntegerField(null=True, blank=True)
    percent_flop = models.IntegerField(null=True, blank=True)
    players = models.IntegerField(null=True, blank=True)
    observers = models.IntegerField(null=True, blank=True)
    waiting = models.IntegerField(null=True, blank=True)
    player_timeout = models.IntegerField(null=True, blank=True)
    muck_timeout = models.IntegerField(null=True, blank=True)
    currency_serial = models.IntegerField()
    name = models.CharField(max_length=765)
    variant = models.CharField(max_length=765)
    betting_structure = models.CharField(max_length=765)
    skin = models.CharField(max_length=765)
    tourney_serial = models.IntegerField()
    class Meta:
        db_table = u'pokertables'

    @property
    def variant_name(self):
        if self.variant == 'holdem':
            if self.betting_structure.endswith('-no-limit'):
                return 'No Limit Holdem'
            else:
                return 'Limit Holdem'
        elif self.variant == 'omaha':
            return 'Omaha'
        else:
            return self.variant

    @property
    def blinds(self):
        parts = self.betting_structure.split('-')
        return "%s/%s" % (parts[0], parts[1])


class BuyIn(models.Model):
    user = models.ForeignKey(User)
    table = models.ForeignKey(PokerTable)
    real_chips = models.IntegerField()
    live_chips = models.IntegerField()


class PublicProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ForeignKey(Avatar)
    hometown = models.CharField(blank=True, max_length=100)
    favorite_player = models.CharField(blank=True, max_length=100)
    favorite_game = models.CharField(blank=True, max_length=50)
    interest = models.CharField(blank=True, max_length=100)
 
