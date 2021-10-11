from datetime import datetime
from django.http import StreamingHttpResponse
from .rawcsv import RawCSVReport


def get_fields(serializer_class, include_additional_fields, show_display_fields):
    serializer = serializer_class(
        include_additional_fields=include_additional_fields,
        show_display_fields=show_display_fields,
    )
    if show_display_fields is True:
        return [f.display for f in serializer.get_fields()]
    else:
        return [f.alias or f.column_path for f in serializer.get_fields()]


def get_data(
    serializer_class, queryset, include_additional_fields, show_display_fields
):
    serializer = serializer_class(
        queryset,
        include_additional_fields=include_additional_fields,
        show_display_fields=show_display_fields,
    )
    return serializer.get_serialized_data() or []


def _get_csv_response(file_name, fields, data):
    report = RawCSVReport()
    stream = report.stream(fields, data)

    response = StreamingHttpResponse(stream, content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{file_name}"'
    return response


def get_csv_response(
    queryset,
    serializer_class,
    file_name_prefix="fieldreport",
    include_additional_fields=False,
    show_display_fields=False,
):
    fields = get_fields(
        serializer_class,
        include_additional_fields=include_additional_fields,
        show_display_fields=show_display_fields,
    )
    serialized_data = get_data(
        serializer_class,
        queryset,
        include_additional_fields=include_additional_fields,
        show_display_fields=show_display_fields,
    )

    timestamp = datetime.utcnow().strftime("%Y%m%d")
    file_name = f"{file_name_prefix}-{timestamp}.csv".lower()
    return _get_csv_response(file_name, fields, serialized_data)
