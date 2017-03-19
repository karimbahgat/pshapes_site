"""pshapes_site

Static page views.

"""
from django.shortcuts import render
from django.template import Template,Context
from django.contrib.auth.decorators import login_required

from provchanges.models import ProvChange

shortdescr = """
Pshapes (pronounced p-shapes) is an open-source crowdsourcing project for creating and maintaining
data on historical provinces, created by and for data-enthusiasts, researchers,
and others. 
"""

def recentadds(request):
    html = """
		<table style="font-size:small"> 
		
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
				
				<th>
                <b>User</b>
				</th>

				<th>
                <b>Added</b>
				</th>
			
				<th>
                <b>Country</b>
				</th>

				<th>
                <b>Province</b>
				</th>
				
				<th>
                <b>Type</b>
				</th>
				
			</tr>
			</a>
			
			{% for change in changelist|slice:":3" %}
				<tr>
					<td>
					<a href="{% url 'viewchange' pk=change.pk %}">View</a>
					</td>
					
					<td>
					{{ change.user }}
					</td>

					<td>
					{{ change.added }}
					</td>

                            {% if "Transfer" in change.type %}

					<td>
					{{ change.tocountry }}
					</td>
					
					<td>
					{{ change.toname }}
					</td>

			    {% else %}

					<td>
					{{ change.fromcountry }}
					</td>
					
					<td>
					{{ change.fromname }}
					</td>

			    {% endif %}
					
					<td>
					{{ change.type }}
					</td>
					
				</tr>
			{% endfor %}
		</table>
	    """
    changelist = ProvChange.objects.all().order_by("-added") # the dash reverses the order
    rendered = Template(html).render(Context({"request":request, "shortdescr":shortdescr, "changelist":changelist}))
    return rendered



def home(request):
    changelist = ProvChange.objects.all().order_by("-added") # the dash reverses the order
    return render(request, 'pshapes_site/home.html', {"shortdescr":shortdescr, "changelist":changelist})

def home(request):
    bannertitle = ""
##    bannerleft = """
##			<style>
##			.shadow
##			{
##				display:block;
##				position:relative;
##				height:300px;
##				background-image:url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYci40tiT9XecIGMtu8pLPGd7XqYXwNT_CCZ5PtyDA9ubVl0-P7g);
##				background-size:100% 100%;
##			}
##			.shadow:before
##			{
##				display:block;
##				content:'';
##				position:absolute;
##				width:100%;
##				height:100%;
##				-moz-box-shadow:inset 0px 0px 3px 1px rgba(0,0,0,1);
##				-webkit-box-shadow:inset 0px 0px 3px 1px rgba(0,0,0,1);
##				box-shadow:inset 0px 0px 10px 10px rgba(0,0,0,1);
##			}
##			</style>
##			<div class="shadow"></div>
##    """
    if not request.user.is_authenticated():
        quickstartbut = """
			<a href="/registration" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Sign Up
			</a>
			or
			<a href="/login" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Login
			</a>
			"""
    else:
        quickstartbut = """
			<a href="/contribute" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Get Started
			</a>
			"""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">Crowdsourcing Historical Province Boundaries</h3>
                    <div style="text-align:left">
                        <p>%s</p>

                        <p style="font-size:smaller"><em>Note: This is an early Alpha trial version of the website to test
                        out the data collection effort. Suggestions
                        and feature requests are welcome.</em>
                        </p>

                        <p style="font-size:smaller"><em>Disclaimer: All website pictures and graphics are
                        currently just placeholders and will be replaced in the final version.</em>
                        </p>
                    </div>

                    <br>
                    <div style="text-align:right;">
                        <a href="/about" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        <b>Read More</b>
                        </a>
                    </div>
                    <br>
                    """ % shortdescr
    bannerleft = """
                    <br>
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYci40tiT9XecIGMtu8pLPGd7XqYXwNT_CCZ5PtyDA9ubVl0-P7g">
                    <p>
                    %s
                    </p>
                    """ % quickstartbut
##    if request.user.is_authenticated():
##        bannerright = """
##                        <br>
##                        <p>Not sure what to put here...</p>
##                        <p>Maybe slideshow of stepbystep instructions...</p>
##                        <p>Or latest site news or blog/progress notes...</p>
##                        """ 

    grids = []
    grids.append(dict(title="Project News:",
                      content="""
                            <p>October 2016: <br> Alpha Website Launched!</p>
                            """,
                      width="25%",
                      ))

##    grids.append(dict(title="What is Pshapes?",
##                      content="""
##                        <p style="color:black;">
##                        <em><b><q>%s</q></b></em>
##                        </p>
##                        <div style="text-align:right;">
##                        <a href="/about" style="color:white;"><b>Read More</b></a>
##                        </div>
##                        """%shortdescr
##                      ))
##    grids.append(dict(title="The Timecapsule:",
##                  content="""
##		<a href="/interactive" style="text-decoration:none;">		
##		<table style="width:100%; border-radius:10px; padding:0% 0%; margins:0% 0%; background:linear-gradient(to left, rgba(255,165,0,0), rgba(255,165,0,1));">
##		<tr>
##		<td>
##		<h4 style="color:black;">
##		Go back in time to find out what the political landscape looked like at a particular date with our interactive time-enabled map.
##		</h4>
##		</td>
##		
##		<td>
##		<img style="height:100px" src="http://cdn.shopify.com/s/files/1/0297/6893/products/Rapport_Optima_Single_Time_Capsule_Watch_Winder_W193_profile_front.png?v=1445374446">
##		</td>
##		
##		</tr>
##		</table>
##		
##		</a>
##                """,
##                style="padding:0% 0%; background-size:100% 100%; background-image:url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxvPpRIf5PnwOmOqIz47XUiU99_7XhcfelMm5iiTrKbYiIoSXi)",
##                  ))
    
    grids.append(dict(title="Recent Additions:",
                      content=recentadds(request),
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="65%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def about(request):
    return render(request, 'pshapes_site/about.html')

def about(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">About the Pshapes Project</h3>
                    <div style="text-align:left">
                        <p>
                        The idea behind the Pshapes project is very simple. Most databases of administrative areas avilable today
                        are simply snapshots of their boundaries on a particular date. As long as we have this,
                        as well as a chronology of changes, that should be enough to reverse or forward engineer the situation to
                        any point in the past or future. Where Pshapes contributes is in the tracking of changes
                        as well as a method for reconstructing the world's boundaries based on these changes.
                        </p>
                    </div>
                    """
    bannerleft = """
                    <br>
                    <img width="50%" src="http://image.slidesharecdn.com/06-clipping-130211003001-phpapp01/95/06-clipping-25-638.jpg?cb=1360542662">
                    """

    grids.append(dict(title="Background and Motivation",
                      content="""
                        <p>
                        The Pshapes project was first inspired by <a href="http://nils.weidmann.ws/projects/cshapes.html">the Cshapes dataset</a>, which tracks historical
                        country borders and changes since 1946. Hence, the name Pshapes to parallel the Cshapes dataset. 
                        </p>

                        <p>
                        No such historical data exists yet for subnational administrative boundaries (see more below). 
                        Sub-national administrative area and boundary data 
                        have in recent years become essential for many analysts and policy makers.
                        The data that currently exist are great for representing
                        modern or the most-recent boundaries. But subnational borders and names
                        change quite frequently, and are very different today than
                        they were even just a few years ago.
                        </p>

                        <p>
                        This makes it quite challenging for data providers to get an overview of
                        past changes or regularly come out with new updates. For good reasons,
                        existing datasets on administrative boundaries simply 
                        do not capture these historical changes and are only updated every few years.
                        The only exception here is the UN's Global Administrative Units Layer (GAUL) data,
                        which provides yearly snapshots back to 1990. But these data are not publically
                        availabe to all, and its restrictive license prohibits certain uses.
                        </p>

                        <p>
                        Better data is needed for earlier historic periods.
                        In project afer project, geospatial data are frequently created based on information,
                        such as government statistics, that are originally reported at the administrative
                        level. These then have to be geocoded to their historical administrive areas, but using only data
                        for the modern period. This means a lot of names are no longer valid, or borders have changed
                        dramatically, requiring substantial followups to match historical units to modern boundaries.
                        </p>

                        <p>
                        The Pshapes project grew
                        out of this need for an open-source and easily maintainable dataset
                        for not only to uncover administrative units' changes for past historical periods,
                        but also to help keep track of future changes as they occur. 
                        </p>
                            """,
                      width="45%",
                      ))

    grids.append(dict(title="Why Crowdsourcing?",
                      content="""
                                <p>
                                The Pshapes project has a very different structure than other administrative area datasets.
                                Instead of being carefully collected and coded by a handful of experts, the project has focused
                                on the speed, efficiency, and quality control of a crowdsourcing approach. Such an approach is only
                                possible because it was realized that a lot of the work required to make spatially
                                integrated boundary data is wasted on duplicative and strenous work by GIS experts manually
                                repeating the same steps over and over. These repetative tasks can be automated,
                                while the information needed is actually fairly straightforward and do not require any
                                expert knowledge or skills.
                                </p>

                                <p>
                                This is why we broke these two processes apart: letting users and other contributors take care
                                of the data entry through the website's user-friendly interface. Then we leave the more difficult parts
                                of constructing the final dataset up to an automated algorithm with expert supervision.
                                </p>                                
                            """,
                      width="45%",
                      ))
    
    grids.append(dict(title="How the Algorithm Works",
                      content="""
                                <p>
                                To create a complete spatial dataset of the provinces themselves it is necessary
                                to start with a dataset of modern province boundaries and apply the changes in reverse
                                chronological order.
                                </p>

                                <p>
                                This maximizes the value of the user contributions, so that the information doesn't have to
                                be tied to a single province boundary dataset. 
                                This makes the data flexible and allows integration with any third-party province datasets.
                                </p>

                                <p>
                                All changes can be boiled down to three types.
                                
                                Splits happen when new provinces are entirely created from
                                part of an older province.
                                
                                Transfers include any changes where new provinces or created from
                                parts of multiple old provinces, <em>or</em> during partial transfers
                                of territory between provinces, <em>or</em> during complete mergers. 
                                
                                Finally, some changes may simply involve changes to a province name or code.
                                </p>

                                <p>
                                The algorithm to recreate a historical dataset starts at a recent date for
                                which we have a complete global overview of spatial extents. It then increments
                                through the dates of change-events backwards in time. For each date,
                                the goal is to determine the start-date for new provinces, and the end-date and
                                extent for older provinces. This can be done by identifying all the parts that were
                                transferred or split from one province to another, and then merging all those parts
                                to the provinces they previously belonged to, recreating the spatial extents as they
                                were before the changes. Through this process we can reverse geocode our
                                way back in time for as long as we have a continuous list of changes. 
                                </p>
                            """,
                      width="45%",
                      ))
    
    grids.append(dict(title="Contact",
                      content="""
                            For questions, issues, or feature requests, please contact
                            Karim Bahgat (karim.bahgat.norway@gmail.com). 
                            """,
                      width="45%",
                      ))
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannerleft":bannerleft,"bannerright":bannerright,"bannertitle":bannertitle}
                  )

def download(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">The Pshapes-Natural Earth Dataset</h3>
                    <div style="text-align:left">
                        <p>
                        The Pshapes dataset covers only the historical changes to provinces, so requires
                        another dataset to cover the modern boundaries.
                        For convenience to the average user, we here provide a complete dataset that has been reverse-engineered
                        using the <a target="_blank" style="color:white;" href="http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/">
                        <em>Natural Earth province boundaries</em></a>
                        as the starting-point. 
                        </p>
                        <p>Version: Alpha (2016-12-01)</p>
                        <p>Status: Only some test-countries so far.</p> 
                    </div>

                    <br>
                    <div style="text-align:right;">
                        <a href="/download/final/" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        <b>Download Boundary Data</b>
                        </a>
                    </div>
                    <br>
                    """
    bannerleft = """
                    <br>
                    <img width="50%" src="https://lh3.googleusercontent.com/4zN3BOlFGIynfAT1-10I0nhqi7w31aIoePUbvCVCmk83D5E89a59QjhgcLN-d59u1CU=w300">
                    """    
    
    grids.append(dict(title="Raw Data Dump",
                      content="""
                            <img width="100%" border="2" src="http://images.wisegeek.com/physical-data.jpg">

                            <p>
                                <b>
                                The latest data dump of the user
                                contributions data is always available on-demand. This is the data
                                used to replicate or rebuild the pshapes dataset. 

                                <div style="text-align:center">
                                <table>
                                    <tr>
                                        <td style="text-align:center"><a href="/download/raw/"><img width="50px" src="http://downloadicons.net/sites/default/files/csv-file-icon-32586.png"><p>CSV</p></a></td>
                                        <td style="text-align:center"><img width="50px" src="http://icons.iconarchive.com/icons/hopstarter/soft-scraps/256/Adobe-PDF-Document-icon.png"><p>Manual</p></td>
                                    </tr>
                                </table>
                                </div>
                            </p>
                            """,
                      width="46%",
                      ))


    grids.append(dict(title="Build Your Own",
                      content="""
                            <img width="100%" border="2" src="https://thumbs.dreamstime.com/z/coding-programming-source-code-screen-colorful-abstract-data-display-software-developer-web-program-script-computer-50188994.jpg">

                            <p>
                                The Pshapes framework is primilaly just a dataset of province changes, registering
                                only the information that changes for each time.
                                A reverse polygon geocoding tool was therefore developed to automatically build
                                a final dataset based on these changes, allowing integration with any third-party
                                province datasets. This open-source tool is freely available to programmers.
                            </p>

                            <p style="text-align:right">
                            <a href="/">
                            <b><a href="https://github.com/karimbahgat/pshapes">Go to GitHub</a></b>
                            </a>
                            </p>
                            """,
                      width="46%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannerleft":bannerleft,"bannerright":bannerright,"bannertitle":bannertitle}
                  )

def download_final(request):
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pshapes_natearth_final.json"'
    import csv, datetime, urllib
    raw = urllib.urlopen("http://raw.githubusercontent.com/karimbahgat/pshapes/master/processed.geojson").read()
    response.write(raw)
    return response

    #TODO: in future, create github releases of the data and maybe just redirect to there
    #return redirect("http://raw.githubusercontent.com/karimbahgat/pshapes/master/processed.geojson")

def download_raw(request):
    from django.http import HttpResponse
    import csv, datetime
    tday = datetime.date.today()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pshapes_raw_%s.csv"' % tday 
    fields = "source status date type fromcountry fromname fromalterns fromiso fromfips fromhasc fromtype fromcapitalname fromcapital tocountry toname toalterns toiso tofips tohasc totype tocapitalname tocapital transfer_source transfer_reference transfer_geom".split()
    writer = csv.writer(response)
    writer.writerow(fields)
    def encode(val):
        if isinstance(val, datetime.date):
            return val.isoformat()
        elif "Polygon" in str(type(val)):
            return val.json
        elif val is None:
            return None
        else:
            return val.encode("utf8")
    for obj in ProvChange.objects.all():
        row = [encode(getattr(obj, f)) for f in fields]
        writer.writerow(row)
        
    return response

def testgrid(request):
    grids = tuple([("title%s"%i, "content%s"%i) for i in range(5)])
    bannertitle = "Banner Title"
    bannerleft = "Banner left"
    bannerright = "Banner right"
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

