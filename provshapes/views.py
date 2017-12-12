from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template,Context
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied

# Create your views here.

from django.contrib.gis import forms
from django.contrib.gis.geos import Polygon, MultiPolygon

from .models import ProvShape

from rest_framework import response
from rest_framework import decorators

import urllib2
import json
import datetime

def update_dataset(request):
    if 1: #'user.administrator' in request.user.get_all_permissions():
        print 'deleting existing...'
        ProvShape.objects.all().delete()
        print 'downloading...'
        raw = urllib2.urlopen('https://github.com/karimbahgat/pshapes/raw/master/processed.geojson').read()
        datadict = json.loads(raw)
        print 'adding', datadict.keys(), len(datadict['features'])
        for feat in datadict['features']:
            props = feat['properties']
            values = dict(name=props['Name'],
                          alterns='|'.join(props['Alterns']),
                          country=props['country'],
                          iso=props['ISO'],
                          fips=props['FIPS'],
                          hasc=props['HASC'],
                          start=props['start'],
                          end=props['end'],
                          )
            print values
##            values = dict()
##            for fl in ProvShape._meta.fields:
##                flname = fl.name
##                print flname
##                if flname == 'id':
##                    continue
##                values[flname] = feat[flname]
            if feat['geometry']['type'] == 'Polygon':
                polys = [Polygon(*feat['geometry']['coordinates'])]
            elif feat['geometry']['type'] == 'MultiPolygon':
                polys = [Polygon(*poly) for poly in feat['geometry']['coordinates']]
            else:
                raise Exception('Geometry must be polygon or multipolygon, not %s' % feat['geometry']['type'])
            #print str(polys)[:100]
            values['geom'] = MultiPolygon(*polys)
            provshape = ProvShape(**values)
            provshape.save()
        print 'provshapes updated!'
        return redirect(request.META['HTTP_REFERER'])
        
    else:
        print 'You do not have permission to update the provshapes dataset'
        raise PermissionDenied

@decorators.api_view(["GET"])
def apiview(request):
    print request.query_params
    print "------"
    queryset = ProvShape.objects.all()

    params = dict(((k,v) for k,v in request.query_params.items() if v))

    frmt = params.pop('format', None)
    
    yr = params.pop('year', None)
    mn = params.pop('month', None)
    dy = params.pop('day', None)
    
    if all((yr,mn,dy)):
        print 'filtering date'
        date = datetime.date(int(yr),int(mn),int(dy))
        queryset = queryset.filter(start__lte=date).filter(end__gte=date)

    bbox = params.pop('bbox', None)
    if bbox:
        bbox = map(float, bbox.split(','))
        print bbox
        box = Polygon.from_bbox(bbox)
        queryset = queryset.filter(geom__intersects=box)

    tolerance = params.pop('simplify', None)
    print 'simplify',tolerance

    # attribute filtering
    print 'apiparams',params
    if params:
        queryset = queryset.filter(**params)

    # convert to json
    jsondict = dict(type='FeatureCollection', features=[])
    for obj,props in zip(queryset, queryset.values('name','alterns','country','iso','fips','hasc','start','end')):
        geom = obj.geom
        if tolerance:
            geom = geom.simplify(float(tolerance))
        geoj = json.loads(geom.geojson)
        #print str(geoj)[:200]
        fdict = dict(type='Feature', properties=props, geometry=geoj)
        jsondict['features'].append(fdict)

##    from django.core.serializers import serialize
##    jsondict = serialize('geojson', queryset,
##                          geometry_field='geom',
##                          #fields=('name',))
##                         )
    
    return response.Response(jsondict)

class SearchForm(forms.ModelForm):

    class Meta:
        model = ProvShape
        fields = ["name","country"]

def explore(request):

    ###
    
    #mapp = render_to_string("provshapes/mapview.html")

    initdict = dict(request.GET.items()) if request.GET else {}
    formfields = SearchForm(initial=initdict).as_p()
    bannerleft = """
    <form action="/explore/" method="get">

    %s
    
    <div style="padding:10px;">
    <input type="submit" value="Search" style="background-color:orange; color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:7px;">
    </div>

    </form>
    """ % formfields

    bannerright = """
    <h3 style="color:white; text-align:left;">
    Historical Provinces
    </h3>
    <div style="text-align:left">
        <p>
        Here you can search, browse, and view a map of all historical provinces that have been coded so far.
        </p>
    </div>
    """

    grids = []

    content = """
    <a class="toptabs" onClick="document.getElementById('maptab').style.display = 'none'; document.getElementById('listtab').style.display = '';">
    List
    </a>
    """
    
    grids.append(dict(title="",
                     content=content,
                      style="text-align:center; font-size:large; font-weight:bold",
                     width="10%",
                     ))


    content = """
    <a class="toptabs" onClick="document.getElementById('maptab').style.display = ''; document.getElementById('listtab').style.display = 'none';">
    Map
    </a>
    """
    
    grids.append(dict(title="",
                     content=content,
                      style="text-align:center; font-size:large; font-weight:bold",
                     width="10%",
                     ))
    

    # main area with table and map
    provs = ProvShape.objects.all().order_by("country", "name", "start")
    if request.GET:
        filterdict = dict(((k,v) for k,v in request.GET.items() if v))
        provs = provs.filter(**filterdict)
    else:
        filterdict = dict()

    fields = ["name","alterns","country","start","end"]
    lists = []
    for p in provs[:50]:
        rowdict = dict([(f,getattr(p, f, "")) for f in fields])
        row = [rowdict[f] for f in fields]
        lists.append(("[Link]",row))

    listtable = lists2table(request, lists, fields)
    
    content = render(request, 'provshapes/mapview.html',
                          dict(listtable=listtable, getparams=json.dumps(filterdict))
                          )
    grids.append(dict(title="",
                     content=content,
                     width="100%",
                     ))

##    content = """
##    <div id="provframe">
##    None selected
##    </div>
##    
##    <script>
##    function selectfunc(feature) {
##        alterns = feature.attributes.Alterns.join("; ");
##        if (alterns) {
##            alterns = " (" + alterns + ")";
##        };
##        table = "<table>"
##            table += "<tr>"
##            table += "<td>Country: </td>"
##            table += "<td>" + feature.attributes.country + "</td>"
##            table += "</tr>"
##            
##            table += "<tr>"
##            table += "<td>Name: </td>"
##            table += "<td>" + feature.attributes.Name + alterns + "</td>"
##            table += "</tr>"
##            
##            table += "<tr>"
##            table += "<td>Time period: </td>"
##            table += "<td>" + feature.attributes.start + " to " + feature.attributes.end + "</td>"
##            table += "</tr>"
##
##            table += "<tr>"
##            table += "<td>Codes: </td>"
##            table += "<td>ISO=" + feature.attributes.ISO + ", FIPS=" + feature.attributes.FIPS + ", HASC=" + feature.attributes.HASC + "</td>"
##            table += "</tr>"
##        table += "</table>"
##        document.getElementById("provframe").innerHTML = table;
##    };
##    function unselectfunc(feature) {
##        document.getElementById("provframe").innerHTML = "None selected";
##    };
##    selectControl = new OpenLayers.Control.SelectFeature(provLayer, {onSelect: selectfunc, onUnselect: unselectfunc, selectStyle: {fillColor: "turquoise", strokeWidth: 2}});
##    map.addControl(selectControl);
##    selectControl.activate();
##    </script>
##    """

    return render(request, 'pshapes_site/base_grid.html', dict(bannerleft=bannerleft,
                                                               bannerright=bannerright,
                                                               grids=grids)
                  )

def underconstruction(request):
    grids = []
    bannertitle = "Under construction..."
    bannerleft = "This page is currently under construction"
    bannerright = ""
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def lists2table(request, lists, fields):
    html = """
		<table> 
		
			<style>
			table {
				border-collapse: collapse;
				width: 100%;
			}

			th, td {
				text-align: left;
				padding: 8px;
			}

			tr:nth-child(even){background-color: #f2f2f2}

			th {
				background-color: orange;
				color: white;
			}
			</style>
		
			<tr>
				<th> 
				</th>

				{% for field in fields %}
                                    <th>
                                        <b>{{ field }}</b>
                                    </th>
                                {% endfor %}
                                    
			</tr>
			</a>
			
			{% for url,row in lists %}
				<tr>
					<td>
					{% if url %}
                                            <a href="{{ url }}">View</a>
                                        {% endif %}
					</td>
					
                                        {% for value in row %}
                                            <td>{{ value | safe}}</td>
                                        {% endfor %}
					
				</tr>
			{% endfor %}
		</table>
                """
    rendered = Template(html).render(Context({"request":request, "fields":fields, "lists":lists}))
    return rendered




