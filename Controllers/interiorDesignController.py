"""Validate company and project input before persistence."""
from datetime import date
import re


class InteriorDesignController:
    def __init__(self, entity):
        self.entity = entity

    def validate(self, form, project=False):
        keys = ('name','description','progress','start_date','end_date') if project else (
            'name','address','hours','email','phone','established','description')
        values = {key: form.get(key, '').strip() for key in keys}
        required = [key for key in keys if key != 'end_date']
        if project and values['progress'] == 'Completed':
            required.append('end_date')
        errors = {key: 'This field is required.' for key in required if not values[key]}
        for key, value in values.items():
            if len(value) > (5000 if key == 'description' else 255):
                errors[key] = 'This value is too long.'
        if project and values['progress'] not in ('Ongoing', 'Completed'):
            errors['progress'] = 'Choose Ongoing or Completed.'
        if not project and values['email'] and not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', values['email']):
            errors['email'] = 'Enter a valid email address.'
        for key in (('start_date','end_date') if project else ('established',)):
            if values[key]:
                try:
                    date.fromisoformat(values[key])
                except ValueError:
                    errors[key] = 'Enter a valid date.'
        if project:
            if values['progress'] == 'Ongoing':
                values['end_date'] = None
                errors.pop('end_date', None)
            elif not errors.get('start_date') and not errors.get('end_date') and values['end_date'] < values['start_date']:
                errors['end_date'] = 'End date must be on or after the start date.'
        return values, errors
