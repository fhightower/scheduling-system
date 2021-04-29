'''
#---------------------------------------------------------------------------------+
| Welcome to the swingtime demo project. This project's theme is a Karate dojo    |
| and the database will be pre-populated with some data relative to today's date. |
#---------------------------------------------------------------------------------+
'''
import random
import os
import django
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime, date, time, timedelta
from django.conf import settings
from django.db.models import signals
from django.utils.termcolors import make_style
from django.core.management.color import color_style
from dateutil import rrule
from swingtime import models as swingtime

class Term:
    info  = staticmethod(make_style(opts=('bold',), fg='green'))
    warn  = staticmethod(make_style(opts=('bold',), fg='yellow', bg='black'))
    error = staticmethod(make_style(opts=('bold',), fg='red', bg='black'))


def create_sample_data():
    # Create the studio's event types
    ets = dict((
        (abbr, swingtime.EventType.objects.create(abbr=abbr, label=label))
        for abbr, label in (
            ('cs',  'C-Section'),
            ('ind',  'Induction'),
        )
    ))
    print(__doc__)
    print('Created event types: %s' % (
        ', '.join(['%s' % et for et in swingtime.EventType.objects.all()]),
    ))
    now = datetime.now()
    future = now + timedelta(7)

    # create a single occurrence event
    evt = swingtime.create_event(
        'Busy',
        ets['ind'],
        # description='C-Section',
        start_time=datetime.combine(now.date(), time(15)),
        end_time=datetime.combine(now.date(), time(17)),
        # note='C-Section for the Fair Weather OB Office'
    )
    print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))

    for i in range(1):
        # create an event with multiple occurrences by fixed count
        evt = swingtime.create_event(
            'Busy',
            ets['ind'],
            # description='Induction',
            start_time=datetime.combine(now.date(), time(random.randint(9, 16))),
            count=2,
            byweekday=(rrule.TU, rrule.TH),
            # note="Induction for the Fair Ponds OB Office"
        )
        print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))

    for i in range(2):
        # create an event with multiple occurrences by fixed count
        evt = swingtime.create_event(
            'Busy',
            ets['ind'],
            # description='Induction',
            start_time=datetime.combine(now.date(), time(random.randint(9, 16))),
            count=2,
            byweekday=(rrule.MO, rrule.WE, rrule.FR),
            # note="Induction for the Fair Game OB Office"
        )
        print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))

    for i in range(2):
        # create an event with multiple occurrences by fixed count
        evt = swingtime.create_event(
            'Busy',
            ets['ind'],
            # description='C-Section',
            start_time=datetime.combine(now.date(), time(random.randint(9, 16))),
            count=14,
            byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR),
            # note="C-Section for the Fair Ponds OB Office"
        )
        print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))

    for i in range(1):
        # create an event with multiple occurrences by fixed count
        evt = swingtime.create_event(
            'Busy',
            ets['ind'],
            # description='Induction',
            start_time=datetime.combine(future.date(), time(random.randint(9, 16))),
            count=14,
            byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR),
            # note="Induction for the Fair Water OB Office"
        )
        print('Created event "%s" with %d occurrences' % (evt, evt.occurrence_set.count()))


class Command(BaseCommand):
    help = 'Run the swingtime demo. If an existing demo database exists, it will recreated.'
    def handle(self, **options):
        dbpath = settings.DATABASES['default']['NAME']
        if os.path.exists(dbpath):
            self.stdout.write(Term.warn('Removing old database %s' % dbpath))
            os.remove(dbpath)
        self.stdout.write(Term.info('Creating database %s' % dbpath))

        call_command('migrate', no_input=True, interactive=False)
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
        print('Done.\n\nCreating sample data...')
        create_sample_data()
        print('Done\n')

