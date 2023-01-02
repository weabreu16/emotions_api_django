from rest_framework import serializers

class DateRangeValidator:
    """
    Validator for checking a start date and end date field.
    """
    
    def __init__(self, start_date_field="start_date", end_date_field="end_date"):
        self.start_date_field = start_date_field
        self.end_date_field = end_date_field

    def __call__(self, attrs):
        start_date = attrs[self.start_date_field]
        end_date = attrs[self.end_date_field]

        if start_date >= end_date:
            raise serializers.ValidationError({
                self.end_date_field: "Must be after start date."
            })
