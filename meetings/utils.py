from docs.models import Item


def create_first_item(request, meeting_number):
    item = Item(item_no=1,
                meeting_id=int(meeting_number),
                owner=request.user
               )
    item.save()

