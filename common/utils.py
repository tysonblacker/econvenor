from common.models import GroupUpdate, UserUpdate

def snapshot_user_details(user, **kwargs):
    """
    Saves a shapshot of a user's details. Invoke this function immedately
    after any changes are made to any of a user's details.
    """
    try:
        password = kwargs['password']
    except:
        pass
    new_details = UserUpdate()
    new_details.user = user
    new_details.email = user.email
    new_details.username = user.username
    new_details.first_name = user.first_name
    new_details.last_name = user.last_name
    new_details.password = password
    new_details.save()


def snapshot_group_details(group):
    """
    Saves a shapshot of a group's details. Invoke this function immedately
    after any changes are made to any of a group's details.
    """
    new_details = GroupUpdate()
    new_details.group = group
    new_details.aim = group.aim
    new_details.country = group.country
    new_details.focus = group.focus
    new_details.logo = group.logo
    new_details.name = group.name
    new_details.slug = group.slug
    new_details.account_status = group.account_status
    new_details.account_type = group.account_type
    new_details.save()
    new_details.users = group.users
    new_details.save()
