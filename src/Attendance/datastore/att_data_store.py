from Attendance.models import Attendance


def get_daily_report(user_id: int):
    daily_atts = (
        Attendance.objects.all()
        .filter(emp=user_id)
        .values_list("date", flat=True)
        .distinct()
    )
    result = {}
    for date in daily_atts:
        str_date = date.strftime("%d/%m/%Y")
        # get last check in and out
        first_check_in = (
            Attendance.objects.all()
            .filter(date=date)
            .order_by("check_in")
            .exclude(check_in__isnull=True)[0]
            .check_in
        )
        last_check_out = (
            Attendance.objects.all().filter(date=date).latest("check_out").check_out
        )
        result[str_date] = {
            "Arrival": "Late"
            if Attendance.check_late(first_check_in)
            else "Within Time",
            "Leaving": "Early"
            if Attendance.check_early_leave(last_check_out)
            else "Within Time",
            "Working Time": Attendance.calculate_wroking_time(
                check_in=first_check_in, check_out=last_check_out
            ),
            "check in": first_check_in,
            "check_out": last_check_out,
        }
    return result
