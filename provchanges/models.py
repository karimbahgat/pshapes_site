from django.contrib.gis.db import models
from django.contrib.auth.models import User as OrigUser

# Create your models here.


class User(OrigUser):
    affiliation = models.CharField(max_length=400)
                             

class Vouch(models.Model):
    "A user vouches for a particular provchange id."
    user = models.CharField(max_length=200)
    changeid = models.IntegerField(null=True)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Active","Active"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)


class Issue(models.Model):
    "A user can raise issues, which can be general, country-specific, or related to a provchange id."
    user = models.CharField(max_length=200)
    country = models.CharField(max_length=200, blank=True)
    changeid = models.IntegerField(null=True)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Active","Active"),
                                       ("Resolved","Resolved"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=10000)


class IssueComment(models.Model):
    "An issuecomment can be added to an issue."
    user = models.CharField(max_length=200)
    issue = models.ForeignKey(Issue, blank=True, null=True)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Active","Active"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)
    text = models.CharField(max_length=10000)


class Comment(models.Model):
    "A note is assigned to a country, and optionally a prov changeid."
    # OLD, no longer used, to be deleted
    user = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    changeid = models.IntegerField(null=True)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Active","Active"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)


class Source(models.Model):
    """A textual source for information.
    These are typically specific to a country, such as a Statoids country page or a book. 
    A ProvChange can reference one or more sources.
    
    - is_resource
        Indicates that is a general resource to be used for more than one event or country.
        Examples include general reference works, encyclopedia, a global atlas, or a website.
    """
    status = models.CharField(choices=[("Active","Active"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)
    added = models.DateTimeField()
    modified = models.DateTimeField()
    
    title = models.CharField(max_length=500)
    citation = models.TextField()
    note = models.TextField(blank=True)
    url = models.URLField(max_length=2000, null=True)
    country = models.TextField(blank=True, verbose_name=u"Country")


class Map(models.Model):
    """A map reference.
    A Map belongs to a single source. 
    A ProvChange geometry is drawn after a single map.
    A ProvChange can also reference one or more maps (eg if the information came from comparing one or more maps).
    """
    status = models.CharField(choices=[("Active","Active"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)
    added = models.DateTimeField()
    modified = models.DateTimeField()
    
    title = models.CharField(max_length=500)
    year = models.IntegerField(null=True)
    note = models.TextField(blank=True)
    source = models.ForeignKey(Source, blank=True, null=True)
    url = models.URLField(max_length=2000, null=True)
    wms = models.URLField(max_length=2000, null=True)
    country = models.TextField(blank=True, verbose_name=u"Country")


class Milestone(models.Model):
    """A milestone.
    Describes a goal to be achieved, and
    the operationalizations of those goals,
    so that they can be tracked. 
    """
    status = models.CharField(choices=[("Active","Active"),
                                       ("Completed","Completed"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)
    added = models.DateTimeField()
    modified = models.DateTimeField()
    
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    country = models.TextField(blank=True)

    model = models.CharField(choices=[("ProvChange","ProvChange"),
                                       ("Map","Map"),
                                       ("Source","Source"),
                                       ("Issue","Issue"),
                                        ],
                              max_length=40)
    subset = models.TextField(blank=True)
    condition = models.TextField(blank=True)


class ProvChange(models.Model):

    # TODO: Add verbose_name=...

    changeid = models.IntegerField(null=True)
    bestversion = models.BooleanField(default=False)

    user = models.CharField(max_length=200)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Pending","Pending"),
                                       ("Accepted","Accepted"),
                                       ("NonActive","NonActive"),
                                        ],
                              default="Pending",
                              max_length=40)

    #import pycountries as pc
    date = models.DateField(verbose_name=u"Date of change")
    type = models.CharField(choices=[("NewInfo","NewInfo"),
                                       ("MergeNew","MergeNew"),
                                       ("TransferNew","TransferNew"),
                                     ("MergeExisting","MergeExisting"),
                                     ("TransferExisting","TransferExisting"),
                                       ("Breakaway","Breakaway"),
                                       ("SplitPart","SplitPart"),

                                       ("PartTransfer","PartTransfer"),
                                       ("FullTransfer","FullTransfer"),

                                     ("Begin","Begin"),
                                        ],
                            verbose_name=u"Type of Change",
                            max_length=40,)

    # should only show if changetype requires border delimitation...
    transfer_geom = models.MultiPolygonField(null=True, blank=True, verbose_name=u"Province geometry")

    # old meta
    sources = models.ManyToManyField(Source, # A ProvChange can reference one or more sources.
                                     blank=True,
                                     verbose_name=u"Sources of information") 
    mapsources = models.ManyToManyField(Map, # A ProvChange can also reference one or more maps (eg if the information came from comparing one or more maps).
                                        blank=True,
                                        related_name="mapsources_set",
                                         verbose_name=u"Maps used for information") 
    transfer_source = models.CharField(max_length=200, blank=True, verbose_name=u"Link to map data")
    transfer_reference = models.CharField(max_length=400, blank=True, verbose_name=u"Map description")

    # new meta
    source = models.CharField(max_length=10000, verbose_name=u"Source of information")
    transfer_map = models.ForeignKey(Map, # A ProvChange geometry is drawn after a single map.
                                     on_delete=models.PROTECT,
                                     blank=True, null=True, default=None,
                                     related_name="transfer_map_set",
                                     verbose_name=u"Map used to draw geometry")

    fromcountry = models.CharField(max_length=40, verbose_name=u"From country")
    fromname = models.CharField(max_length=40, verbose_name=u"From province name")
    fromalterns = models.CharField(max_length=40, blank=True, verbose_name=u"From alternate province names")
    fromiso = models.CharField(max_length=40, blank=True, verbose_name=u"From province ISO code")
    fromfips = models.CharField(max_length=40, blank=True, verbose_name=u"From province FIPS code")
    fromhasc = models.CharField(max_length=40, blank=True, verbose_name=u"From province HASC code")
    fromcapitalname = models.CharField(max_length=40, blank=True, verbose_name=u"From province capital (name change)")
    fromcapital = models.CharField(max_length=40, blank=True, verbose_name=u"From province capital (moved)")
    fromcapitalmove = models.PointField(null=True, blank=True, verbose_name=u"From province capital (moved)")
    fromtype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ("District","District"),
                                         ("County","County"),
                                         ("State","State"),
                                         ("Parish","Parish"),
                                         ("Region","Region"),
                                         ("Prefecture","Prefecture"),
                                         ("Department","Department"),
                                         ("Governate","Governate"),
                                         ("Territory","Territory"),
                                         ("Commune","Commune"),
                                         ("Circumscription","Circumscription"),
                                         ("Cercle","Cercle"),
                                         ("Division","Division"),
                                         ("Fiefdom","Fiefdom"),
                                         ("Other...","Other..."),
                                         ],
                                verbose_name=u"From province type",
                                max_length=40, blank=True)

    tocountry = models.CharField(max_length=40, verbose_name=u"To country")
    toname = models.CharField(max_length=40, verbose_name=u"To province name")
    toalterns = models.CharField(max_length=40, blank=True, verbose_name=u"To province alternate names")
    toiso = models.CharField(max_length=40, blank=True, verbose_name=u"To province ISO code")
    tofips = models.CharField(max_length=40, blank=True, verbose_name=u"To province FIPS code")
    tohasc = models.CharField(max_length=40, blank=True, verbose_name=u"To province HASC code")
    tocapitalname = models.CharField(max_length=40, blank=True, verbose_name=u"To province capital (name change)")
    tocapital = models.CharField(max_length=40, blank=True, verbose_name=u"To province capital (moved)")
    tocapitalmove = models.PointField(null=True, blank=True, verbose_name=u"To province capital (moved)")
    totype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ("District","District"),
                                         ("County","County"),
                                         ("State","State"),
                                         ("Parish","Parish"),
                                         ("Region","Region"),
                                         ("Prefecture","Prefecture"),
                                         ("Department","Department"),
                                         ("Governate","Governate"),
                                         ("Territory","Territory"),
                                         ("Commune","Commune"),
                                         ("Circumscription","Circumscription"),
                                         ("Cercle","Cercle"),
                                         ("Division","Division"),
                                         ("Fiefdom","Fiefdom"),
                                         ("Other...","Other...")
                                         ],
                                verbose_name=u"To province type",
                                max_length=40, blank=True)
