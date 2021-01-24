from datetime import datetime
import math


class NRService:
    def __init__(self, obj):
        self.raw = obj

    def origin(self):
        return self.raw['origin']['location'][0]['locationName']

    def destination(self):
        return self.raw['destination']['location'][0]['locationName']

    def planned_arrival(self):
        return self.__format_time_to_datetime__(self.raw['std'])

    def estimated_arrival(self):
        if (self.raw['etd'] == 'On time'):
            return self.__format_time_to_datetime__(self.raw['std'])
        elif (self.raw['etd'] == 'Cancelled' or self.raw['etd'] == 'Delayed'):
            return None
        else:
            return self.__format_time_to_datetime__(self.raw['etd'])

    def status(self):
        if (self.raw['etd'] == 'On time' or self.raw['etd'] == 'Cancelled'
                or self.raw['etd'] == 'Delayed'):
            return self.raw['etd']
        elif (datetime.now() > self.estimated_arrival()):
            return 'Overdue'
        else:
            return 'Late'

    def delay(self):
        if (self.raw['etd'] == 'On time' or self.raw['etd'] == 'Cancelled'
                or self.raw['etd'] == 'Delayed'):
            return None
        else:
            delay_minutes = math.ceil(
                (self.estimated_arrival() - self.planned_arrival()).seconds /
                60)

            return '{} minutes'.format(delay_minutes)

    def length(self):
        return str(self.raw['length'])

    def minutes_to_arrival(self):
        time_now = datetime.now()

        if (self.raw['etd'] == 'Cancelled' or self.raw['etd'] == 'Delayed'):
            return None
        elif (time_now > self.estimated_arrival()):
            return None
        else:
            diff_minutes = math.ceil(
                (self.estimated_arrival() - time_now).seconds / 60)

            return '{} minutes'.format(diff_minutes)

    # Private

    def __extract_etd__(self):
        etd = self.raw['etd']

        if (etd == 'On time' or etd == 'Cancelled'):
            return self.__format_time_to_datetime__(self.raw['std'])
        else:
            return self.__format_time_to_datetime__(etd)

    def __extract_std__(self):
        return self.__format_time_to_datetime__(self.raw['std'])

    def __format_time_to_datetime__(self, time):
        current_time = datetime.now()

        dt = datetime.strptime(
            '{} {}'.format(
                str(current_time.date()),
                time,
            ), '%Y-%m-%d %H:%M')

        return dt
