from django.contrib.gis.db import models
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

STOP_CHOICES = ( ('U','Up'),
                 ('D', 'Down'),
                 )

DAYS = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday',
    8: 'Holiday'
    }

SCHED = {
    'MS':[1,2,3,4,5,6], 
    'HOL':[8], 
    'SUN':[7], 
    'MF&HOL':[1,2,3,4,5,8],  
    'SAT':[6], 
    'MF':[1,2,3,4,5], 
    'SH':[7,8], 
    'AD':[1,2,3,4,5,6,7,8], 
    'SAT&SUN':[6,7], 
    'MS&HOL':[1,2,3,4,5,6,8], 
    'FW':[1,2,3,4,5,6,7], 
    'SAT/SH':[6,7,8], 
    'FH':['???'], 
    'SAT&HOL':[6,8], 
    'SAT&SH':[6,7,8], 
    'SAT/SUND&HOL':[6,7,8], 
    'S/H':[7,8], 
    'SAT,SUN&HOL':[6,7,8], 
    '2nd &4th':['???']
    }

class Area(models.Model):
    code = models.IntegerField() #primary_key=True)
    slug = models.SlugField(null=True)
    name = models.TextField(blank=True, max_length=255)
    name_mr= models.TextField(null=True, blank=True, max_length=512) #null=True, 
    display_name = models.TextField(blank=True, max_length=255)
    geometry = models.PolygonField(blank=True, null=True)
    alt_names = generic.GenericRelation("AlternativeName")


    def __unicode__(self):
        return self.name   

    
class Road(models.Model):
    code = models.IntegerField()#primary_key=True)
    slug = models.SlugField(null=True)
    name = models.TextField(blank=True, max_length=255)
    name_mr= models.TextField(null=True, blank=True, max_length=512)
    display_name = models.TextField(blank=True, max_length=255)
    geometry = models.LineStringField(blank=True, null=True)
    alt_names = generic.GenericRelation("AlternativeName")

    def __unicode__(self):
        return self.name   


class Fare(models.Model):
    slab = models.DecimalField(max_digits=5, decimal_places=2) 
    ordinary = models.PositiveIntegerField()
    limited = models.PositiveIntegerField()
    express = models.PositiveIntegerField()
    ac = models.PositiveIntegerField()
    ac_express = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.slab)   


class Stop(models.Model):
    code = models.IntegerField()
    slug = models.SlugField(null=True)
    name = models.TextField(blank=True, max_length=255)
    display_name = models.TextField(blank=True, max_length=255)
    dbdirection = models.CharField(null=True, blank=True, max_length=5, choices=STOP_CHOICES) #stopfl - > direction
    chowki = models.NullBooleanField(null=True, blank=True) # this is nullable since in the next datafeed , they might have blank to represent a 0.
    road = models.ForeignKey(Road, default=None, null=True, blank=True)
    area = models.ForeignKey(Area, default=None, null=True, blank=True)
    depot = models.ForeignKey("Depot", default=None, null=True, blank=True, related_name="is_depot_for") #models.CharField(null=True, blank=True, max_length=5)
    name_mr= models.TextField(null=True, blank=True, max_length=512)#null=True, 

    point = models.PointField(null=True)
    alt_names = generic.GenericRelation("AlternativeName")

    def __unicode__(self):
        return self.name   


class Route(models.Model):
    code = models.TextField(max_length=255, unique=True)
    slug = models.SlugField(null=True)
    alias = models.TextField(max_length=255)
    from_stop_txt = models.TextField(max_length=500)
    to_stop_txt = models.TextField(max_length=500)
    from_stop = models.ForeignKey(Stop, related_name='routes_from', default=None, null=True, blank=True)
    to_stop = models.ForeignKey(Stop, related_name='routes_to', default=None, null=True, blank=True)
    distance = models.DecimalField(max_digits=3, decimal_places=1)
    stages =  models.IntegerField()

    def __unicode__(self):
        return self.alias


class RouteDetail(models.Model):
    route_code = models.TextField()
    route = models.ForeignKey(Route, to_field="code", null=True, blank=True)
    serial = models.PositiveIntegerField()
    stop = models.ForeignKey(Stop, null=True, blank=True)
    stage =  models.NullBooleanField()
    km  = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1)

    class Meta:
        verbose_name = 'Route Detail'
 
    def __unicode__(self):
        return self.route_code


class UniqueRoute(models.Model):
    route = models.ForeignKey(Route)
    from_stop_txt = models.CharField(max_length=255)
    to_stop_txt = models.CharField(max_length=255)
    from_stop = models.ForeignKey(Stop, related_name="unique_routes_from")
    to_stop = models.ForeignKey(Stop, related_name="unique_routes_to")
    distance = models.FloatField(blank=True, null=True)
    is_full = models.BooleanField()

    class Meta:
        verbose_name = 'Atlas'
        
    def __unicode__(self):
        return "%s: %s to %s" % (self.route.alias, self.from_stop_txt, self.to_stop_txt)


class RouteSchedule(models.Model):
    unique_route = models.ForeignKey(UniqueRoute)
    schedule_type = models.CharField(max_length=16)
    busesAM = models.IntegerField(blank=True, null=True)
    busesN = models.IntegerField(blank=True, null=True)
    busesPM = models.IntegerField(blank=True, null=True)
    bus_type = models.CharField(max_length=3, default="SD")
    depot_txt = models.CharField(max_length=16, blank=True)
    depot = models.ForeignKey("Depot", null=True)
    first_from = models.TimeField(blank=True, null=True)
    last_from = models.TimeField(blank=True, null=True)
    first_to = models.TimeField(blank=True, null=True)
    last_to = models.TimeField(blank=True, null=True)
    runtime1 = models.IntegerField(blank=True, null=True)
    runtime2 = models.IntegerField(blank=True, null=True)
    runtime3 = models.IntegerField(blank=True, null=True)
    runtime4 = models.IntegerField(blank=True, null=True)
    headway1 = models.IntegerField(blank=True, null=True)
    headway2 = models.IntegerField(blank=True, null=True)
    headway3 = models.IntegerField(blank=True, null=True)
    headway4 = models.IntegerField(blank=True, null=True)
    headway5 = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (unicode(self.unique_route), self.schedule_type,)


class RouteType(models.Model):
    code = models.TextField(max_length=50)
    rtype = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)

    def __unicode__(self):
        return self.rtype   

    class Meta:
        verbose_name = 'Route Type'


class HardCodedRoute(models.Model):
    code = models.TextField(max_length=50)    
    alias = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)

    class Meta:
        verbose_name = 'Hardcoded Route'

    def __unicode__(self):
        return self.code + " " +self.alias   


class Landmark(models.Model):
    slug = models.SlugField(null=True)
    name = models.TextField(max_length=500, blank=True, null=True)
    stops = models.ManyToManyField(Stop, related_name='is_near_to', blank=True)
    name_mr = models.TextField(max_length=512, blank=True, null=True)
    display_name = models.TextField(blank=True, max_length=255)
    point = models.PointField(blank=True, null=True)
    alt_names = generic.GenericRelation("AlternativeName")

    def __unicode__(self):
        return self.name 


class StopLocation(models.Model):
    stop = models.ForeignKey(Stop)
    point = models.PointField()
    direction = models.CharField(max_length=5, null=True, blank=True, choices=STOP_CHOICES)

    def __unicode__(self):
        return self.stop.name 


class Depot(models.Model):
    code = models.CharField(max_length=5)
    name = models.TextField(max_length=50)
    stop = models.IntegerField()


    def __unicode__(self):
        return self.name 


class Holiday(models.Model):
    date = models.DateField()
    name = models.TextField(max_length=100)

    def __unicode__(self):
        return self.name 
    

ALT_TYPE_CHOICES = (
    ('alt', 'General Alternative Name'),
    ('old', 'Old Name'),
    ('common', 'Common Name')
)

class AlternativeName(models.Model):
    name = models.CharField(max_length=512)
    name_mr = models.CharField(max_length=512, blank=True)
    typ = models.CharField(max_length=64, choices=ALT_TYPE_CHOICES, default="alt")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')    

    def __unicode__(self):
        return self.name
