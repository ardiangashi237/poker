
for player in User.objects.all():
    player.award_chips(player.current_member_level.monthly_award)
