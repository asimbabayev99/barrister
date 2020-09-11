from django.db import models
from account.models import CustomUser
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import random
from datetime import datetime, date, timedelta
from django.core.validators import FileExtensionValidator


from dateutil.rrule import (
    DAILY,
    FR,
    HOURLY,
    MINUTELY,
    MO,
    MONTHLY,
    SA,
    SECONDLY,
    SU,
    TH,
    TU,
    WE,
    WEEKLY,
    YEARLY,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

freqs = (
    ("YEARLY", _("Yearly")),
    ("MONTHLY", _("Monthly")),
    ("WEEKLY", _("Weekly")),
    ("DAILY", _("Daily")),
    ("HOURLY", _("Hourly")),
    ("MINUTELY", _("Minutely")),
    ("SECONDLY", _("Secondly")),
)


TASK_STATUS = (
    ('completed', 'completed'),
    ('in progress', 'in progress'),
)

# Create your models here.




class Rule(models.Model):
    """
    This defines a rule by which an event will recur.  This is defined by the
    rrule in the dateutil documentation.

    * name - the human friendly name of this kind of recursion.
    * description - a short description describing this type of recursion.
    * frequency - the base recurrence period
    * param - extra params required to define this type of recursion. The params
      should follow this format:

        param = [rruleparam:value;]*
        rruleparam = see list below
        value = int[,int]*

      The options are: (documentation for these can be found at
      https://dateutil.readthedocs.io/en/stable/rrule.html#module-dateutil.rrule
        ** count
        ** bysetpos
        ** bymonth
        ** bymonthday
        ** byyearday
        ** byweekno
        ** byweekday
        ** byhour
        ** byminute
        ** bysecond
        ** byeaster
    """

    name = models.CharField(_("name"), max_length=32)
    description = models.TextField(_("description"))
    frequency = models.CharField(_("frequency"), choices=freqs, max_length=10)
    params = models.TextField(_("params"), blank=True)

    _week_days = {"MO": MO, "TU": TU, "WE": WE, "TH": TH, "FR": FR, "SA": SA, "SU": SU}

    class Meta:
        verbose_name = _("rule")
        verbose_name_plural = _("rules")

    def rrule_frequency(self):
        compatibility_dict = {
            "DAILY": DAILY,
            "MONTHLY": MONTHLY,
            "WEEKLY": WEEKLY,
            "YEARLY": YEARLY,
            "HOURLY": HOURLY,
            "MINUTELY": MINUTELY,
            "SECONDLY": SECONDLY,
        }
        return compatibility_dict[self.frequency]

    def _weekday_or_number(self, param):
        """
        Receives a rrule parameter value, returns a upper case version
        of the value if its a weekday or an integer if its a number
        """
        try:
            return int(param)
        except (TypeError, ValueError):
            uparam = str(param).upper()
            if uparam in Rule._week_days:
                return Rule._week_days[uparam]

    def get_params(self):
        """
        >>> rule = Rule(params = "count:1;bysecond:1;byminute:1,2,4,5")
        >>> rule.get_params()
        {'count': 1, 'byminute': [1, 2, 4, 5], 'bysecond': 1}
        """
        params = self.params.split(";")
        param_dict = []
        for param in params:
            param = param.split(":")
            if len(param) != 2:
                continue

            param = (
                str(param[0]).lower(),
                [
                    x
                    for x in [self._weekday_or_number(v) for v in param[1].split(",")]
                    if x is not None
                ],
            )

            if len(param[1]) == 1:
                param_value = self._weekday_or_number(param[1][0])
                param = (param[0], param_value)
            param_dict.append(param)
        return dict(param_dict)

    def __str__(self):
        """Human readable string for Rule"""
        return "Rule {} params {}".format(self.name, self.params)




class EventCategory(models.Model):
    name = models.CharField(max_length=64)
    bg_color = models.CharField(max_length=16, null=False, blank=False)
    text_color = models.CharField(max_length=16, null=False, blank=False)
    icon = models.FileField(upload_to='event-categories/', validators=[FileExtensionValidator(allowed_extensions=['svg'])], null=False, blank=False)


    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name',]),
        ]



class Event(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256, null=True, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    location = models.CharField(max_length=256)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    
    rule = models.ForeignKey(
        Rule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("rule"),
        help_text=_("Select '----' for a one time only event."),
    )
    remind_me = models.DateTimeField(null=True, blank=True)

    class Meta: 
        indexes = [
            models.Index(fields=['user', 'category', 'start', 'end']),
        ]




class Occurrence(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name=_("event"))
    title = models.CharField(_("title"), max_length=255, blank=True)
    description = models.TextField(_("description"), blank=True)
    start = models.DateTimeField(_("start"), db_index=True)
    end = models.DateTimeField(_("end"), db_index=True)
    cancelled = models.BooleanField(_("cancelled"), default=False)
    original_start = models.DateTimeField(_("original start"))
    original_end = models.DateTimeField(_("original end"))
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")
        index_together = (("start", "end"),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.title and self.event_id:
            self.title = self.event.title
        if not self.description and self.event_id:
            self.description = self.event.description

    def moved(self):
        return self.original_start != self.start or self.original_end != self.end

    moved = property(moved)

    def move(self, new_start, new_end):
        self.start = new_start
        self.end = new_end
        self.save()

    def cancel(self):
        self.cancelled = True
        self.save()

    def uncancel(self):
        self.cancelled = False
        self.save()

    @property
    def seconds(self):
        return (self.end - self.start).total_seconds()

    @property
    def minutes(self):
        return float(self.seconds) / 60

    @property
    def hours(self):
        return float(self.seconds) / 3600

    def get_absolute_url(self):
        if self.pk is not None:
            return reverse(
                "occurrence",
                kwargs={"occurrence_id": self.pk, "event_id": self.event.id},
            )
        return reverse(
            "occurrence_by_date",
            kwargs={
                "event_id": self.event.id,
                "year": self.start.year,
                "month": self.start.month,
                "day": self.start.day,
                "hour": self.start.hour,
                "minute": self.start.minute,
                "second": self.start.second,
            },
        )

    def get_cancel_url(self):
        if self.pk is not None:
            return reverse(
                "cancel_occurrence",
                kwargs={"occurrence_id": self.pk, "event_id": self.event.id},
            )
        return reverse(
            "cancel_occurrence_by_date",
            kwargs={
                "event_id": self.event.id,
                "year": self.start.year,
                "month": self.start.month,
                "day": self.start.day,
                "hour": self.start.hour,
                "minute": self.start.minute,
                "second": self.start.second,
            },
        )

    def get_edit_url(self):
        if self.pk is not None:
            return reverse(
                "edit_occurrence",
                kwargs={"occurrence_id": self.pk, "event_id": self.event.id},
            )
        return reverse(
            "edit_occurrence_by_date",
            kwargs={
                "event_id": self.event.id,
                "year": self.start.year,
                "month": self.start.month,
                "day": self.start.day,
                "hour": self.start.hour,
                "minute": self.start.minute,
                "second": self.start.second,
            },
        )

    def __str__(self):
        return gettext("%(start)s to %(end)s") % {
            "start": date(self.start, django_settings.DATE_FORMAT),
            "end": date(self.end, django_settings.DATE_FORMAT),
        }

    def __lt__(self, other):
        return self.end < other.end

    def __hash__(self):
        if not self.pk:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self.pk)

    def __eq__(self, other):
        return (
            isinstance(other, Occurrence)
            and self.original_start == other.original_start
            and self.original_end == other.original_end
        )


class News(models.Model):
    title = models.CharField(_("title"), max_length=255, blank=False)
    content = RichTextField(_("content"), blank=False)
    date = models.DateTimeField(_("date"), auto_now_add=True)
    image = models.ImageField(_("image"),upload_to='news', blank=False)
    slug = models.SlugField(max_length=20,blank=True,null=True,unique=True)
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,null=True,blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['date',]),
            models.Index(fields=['slug',]),
        ]         

    # def unique_slug(self,slug):
    #     if News.objects.filter(slug=slug):
    #         index = random.randrange(0,20)
    #         new_slug = "%s-%s"%(slug,index)
    #         slug = self.unique_slug(slug=new_slug)
    #     return slug  

    def get_absolute_url(self):
        return reverse("admin-update-news", kwargs={"slug": self.slug})
    


    def save(self,*args, **kwargs):
        if self.slug:
            if self.id == News.objects.get(slug=self.slug).id:
                super(News,self).save(*args,**kwargs)
            elif News.objects.filter(slug=self.slug).exists() == False:
                super(News,self).save(*args,**kwargs)

        else:
            self.slug = slugify(self.title)
            if News.objects.filter(slug=self.slug).exists():
                self.slug = "%s-%s"%(self.slug,random.randrange(0,20))
                super(News,self).save(*args,**kwargs)
            else:
                super(News,self).save(*args, **kwargs)


    def __str__(self):
        return self.title 



class Publication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = RichTextField()
    file  = models.FileField(upload_to='publication')
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'date',]),
            models.Index(fields=['date']),
        ]




class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    text = models.CharField(max_length=2048, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['publication', 'date',]),
        ] 
    


class Task(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=50,blank=True,null=True)
    description = models.CharField(max_length=256,blank=True,null=True)
    media_file = models.FileField(upload_to='task', null=True, blank=True)
    status = models.CharField(max_length=32, choices=TASK_STATUS, default="in progress")
    added_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank = False, null = False)
    due_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
        ]
        
    
    
class City(models.Model):
    name = models.CharField(max_length=16, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name', ]),
        ]




class Contact(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(blank=True,null=True)
    adress = models.CharField(max_length=50,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'name']),
        ]



APPOINTMENT_STATUSES = [
    ('completed', 'completed'),
    ('not arrived', 'not arrived'),
    ('arrived', 'arrived')
]


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=32, choices=APPOINTMENT_STATUSES, null=False, blank=False)
    detail = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=32, null=True, blank=True)
    start = models.DateTimeField(null=False, blank=False)
    end = models.DateTimeField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status', 'start', 'end']),
        ]




EMAIL_FLAGS = [
    ('Answered', 'Answered'),
    ('Flagged', 'Flagged'),
    ('Drafts', 'Drafts'),
    ('Deleted', 'Deleted'),
    ('Seen', 'Seen'),
    ('$Forwarded', '$Forwarded'),
    ('$NotPhishing', '$NotPhishing'),
    ('$label1', '$label1'),
    ('$label2', '$label2'),
    ('$label3', '$label3'),
    ('$label4', '$label4'),
    ('$label5', '$label5'),
    ('Junk', 'Junk'),
    ('NotJunk', 'NotJund')
]


FOLDER_CHOICES = [
    ('Inbox', 'Inbox'),
    ('Drafts', 'Drafts'),
    ('Sent', 'Sent'),
    ('Deleted', 'Deleted')
]


class EmailAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(null=False, blank=False)
    password = models.CharField(max_length=64, null=False, blank=False)
    token = models.CharField(max_length=100,blank=True,null=True)
    

class Email(models.Model):
    user = models.ForeignKey(CustomUser, related_name='emails', on_delete=models.CASCADE)
    folder = models.CharField(max_length=64, choices=FOLDER_CHOICES)
    sender = models.EmailField(null=False, blank=False)
    receiver = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=128, blank=True, null=True)
    content = RichTextField(_("content"), blank=True, null=True)
    flag = models.CharField(max_length=64, choices=EMAIL_FLAGS)
    num = models.CharField(max_length=256)
    date = models.DateTimeField(null=False, blank=False)

    @property
    def is_today(self):
        return date.today() <= self.date

    @property
    def is_yesterday(self):
        return date.today() - datetime.timedelta(days=1) <= self.date


class Attachment(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='attachments', blank=False, null=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    file = models.FileField(upload_to='attachment', null=False, blank=False)


# class Folder(models.Model):
#     name = models.CharField(max_length=32, choices=FOLDER_CHOICES, null=False, blank=False)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     email = models.ManyToManyField(Email)


