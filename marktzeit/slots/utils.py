import datetime
from typing import Dict

from django.utils.timezone import get_current_timezone

from marktzeit.slots.models import Slot
from marktzeit.supermarkets.models import Supermarket


def calculate_slots_for_supermarket(
    supermarket: Supermarket, date: datetime.date
) -> Dict[float, Slot]:
    """Calculate all the possible slots for the given supermarket on the given
    date.

    :param supermarket: The supermarket for which to calculate the slots.
    :param date date: The date for which to calculate the slots.

    :returns: Dict with the key being the timestamp of the slot's start time
        (to make it easier to sort) and the value being a Slot object
        (not saved in the DB!)
    """
    tz = get_current_timezone()

    opening_hours_set = supermarket.openinghours_set.filter(
        weekday=date.isoweekday()
    )

    slots = {}
    # generate the slots for the day
    for opening_hours in opening_hours_set:
        start_datetime = tz.localize(datetime.datetime.combine(
            date, opening_hours.opening_time
        ))
        closing_datetime = tz.localize(datetime.datetime.combine(
            date, opening_hours.closing_time
        ))
        while start_datetime < closing_datetime:
            end_datetime = start_datetime + datetime.timedelta(
                seconds=supermarket.minutes_per_slot * 60
            )
            slots[start_datetime.timestamp()] = Slot(
                supermarket=supermarket,
                start_time=start_datetime,
                end_time=end_datetime,
            )
            start_datetime = end_datetime

    return slots


def get_slots_for_supermarket(
    supermarket: Supermarket, date: datetime.date
) -> Dict[float, Slot]:
    """Get all the possible slots for the given supermarket for the given date
    and fill the slots that do exist in the database.

    :param supermarket: The supermarket for which to calculate the slots.
    :param date date: The date for which to calculate the slots.
    """
    tz = get_current_timezone()
    start_of_day = tz.localize(
        datetime.datetime.combine(date, datetime.time(0, 0))
    )
    end_of_day = start_of_day + datetime.timedelta(days=1)

    # all the slots that have already been created for the given date
    existing_slots = supermarket.slot_set.filter(
        start_time__range=(start_of_day, end_of_day)
    )

    possible_slots = calculate_slots_for_supermarket(supermarket, date)

    # replace the generated slots with actual slots
    for existing_slot in existing_slots:
        possible_slots[existing_slot.start_time.timestamp()] = existing_slot

    return possible_slots
