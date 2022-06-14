from Attendance.models import Attendance


def get_daily_report_by_user(user_id: int):
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

def get_daily_index_by_user(user_id: int):
    daily_atts = Attendance.objects.all().filter(emp=user_id)
    result = {}
    for index, att in enumerate(daily_atts):
        stri = str(index + 1)
        str_date = att.date.strftime("%d/%m/%Y")
        if str_date not in result:
            if att.check_in:
                result[str_date] = {f"{stri}-In": att.check_in}
            if att.check_out:
                result[str_date] = {f"{stri}-Out": att.check_out}
        else:
            if att.check_in:
                result[str_date][f"{stri}-In"] = att.check_in
            if att.check_out:
                result[str_date][f"{stri}-Out"] = att.check_out
    return result