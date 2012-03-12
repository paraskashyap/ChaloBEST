from django.contrib.gis import admin
from django import forms
from mumbai.models import *
from django.contrib.contenttypes import generic

class RouteScheduleInline(admin.StackedInline):
    model = RouteSchedule
    extra = 0

class AlternativeNameInline(generic.GenericStackedInline):
    extra = 3
    model = AlternativeName


class AreaAdmin(admin.OSMGeoAdmin):
    list_display = ("code","display_name", "name_mr", "name", "slug")
    list_editable = ("display_name", "name_mr",)
    readonly_fields = ("code", "name")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    default_lon = 8110203.9998955
    default_lat = 2170000.4068373
    default_zoom = 10
    search_fields = ("name","display_name", "name_mr","slug")
    inlines = [AlternativeNameInline]

class RoadAdmin(admin.OSMGeoAdmin):
    list_display = ("code","display_name", "name_mr", "name", "slug")
    list_editable = ("display_name", "name_mr",)
    readonly_fields = ("code", "name")
    search_fields = ("name","display_name", "name_mr","slug")

    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

    default_lon = 8110203.9998955
    default_lat = 2170000.4068373
    default_zoom = 10
    inlines = [AlternativeNameInline]

class FareAdmin(admin.ModelAdmin):
    list_display = ("slab","ordinary","limited","express","ac","ac_express")
    readonly_fields = ("slab","ordinary","limited","express","ac","ac_express")    
    
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    
class UniqueRouteAdmin(admin.ModelAdmin):
    list_display = ("route","from_stop", "to_stop","distance","is_full")
    readonly_fields = ("route","distance","is_full")
    search_fields = ("route__alias", "from_stop__name", "to_stop__name")
    ordering = ('route',)
    list_per_page = 50

    inlines = [RouteScheduleInline]


class StopForm(forms.ModelForm):
    
    class Meta:
        model = Stop
        

class StopAdmin(admin.OSMGeoAdmin):
    list_display = ("code","display_name", "name_mr","name", "road","area","depot", "has_point")
    list_editable = ("display_name", "name_mr","depot",)
    readonly_fields = ("code","name","road","area","depot","chowki" )
    search_fields = ("code",'name', 'depot__name', "road__name", "area__name")
    ordering = ('name',)
    list_per_page = 20

    
    """
    fieldsets = (
        (None, {
            'fields': ('name', 'area', 'road')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('code', 'chowki', 'depot')
        }),
    )
    form = StopForm
    """
    # For mapping widget
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

    default_lon = 8110203.9998955
    default_lat = 2170000.4068373
    default_zoom = 10
    inlines = [AlternativeNameInline]


class RouteDetailAdmin(admin.ModelAdmin):
    list_display = ("route_code","serial","stop","stage","km")
    readonly_fields = ("route_code","serial","stop","stage","km")
    search_fields = ("route_code","stop__name")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class RouteAdmin(admin.ModelAdmin):
    list_display = ("alias","code","from_stop","to_stop","distance","stages")
    search_fields = ("alias","from_stop__name","to_stop__name")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class RouteTypeAdmin(admin.ModelAdmin):
    list_display = ("code","rtype","faretype")    
    readonly_fields = ("code","rtype","faretype") 
    search_fields = ("code","rtype","faretype")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class HardCodedRouteAdmin(admin.ModelAdmin):
    list_display = ("code","alias","faretype")
    readonly_fields = ("code","alias","faretype")
    search_fields = ("code","alias","faretype")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    
class LandmarkAdmin(admin.OSMGeoAdmin):
    list_display = ("name", "display_name", "name_mr", "slug", "point" )
    list_editable = ("display_name","name_mr")
    search_fields = ("name", "display_name", "name_mr","slug")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

    default_lon = 8110203.9998955
    default_lat = 2170000.4068373
    default_zoom = 10
    inlines = [AlternativeNameInline]

class StopLocationAdmin(admin.OSMGeoAdmin):
    list_display = ("stop", "direction", "point")

    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

    default_lon = 8110203.9998955
    default_lat = 2170000.4068373
    default_zoom = 10



class DepotAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "stop")
    readonly_fields = ("code", "name", "stop")
    search_fields =  ("code", "name", "stop__name")
    #list_editable = ("name",) 
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class HolidayAdmin(admin.ModelAdmin):
    list_display = ("date", "name") 
    readonly_fields =  ("date", "name")    
    search_fields =  ("name", "date")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }



admin.site.register(Area, AreaAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Fare,FareAdmin)

admin.site.register(Stop, StopAdmin)
admin.site.register(RouteDetail, RouteDetailAdmin)
admin.site.register(Route, RouteAdmin)

admin.site.register(RouteType, RouteTypeAdmin)
admin.site.register(HardCodedRoute, HardCodedRouteAdmin)

admin.site.register(Landmark, LandmarkAdmin)
admin.site.register(Depot,DepotAdmin)
admin.site.register(Holiday,HolidayAdmin)
admin.site.register(StopLocation,StopLocationAdmin)
admin.site.register(UniqueRoute, UniqueRouteAdmin)
