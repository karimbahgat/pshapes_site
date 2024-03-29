from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import Template,Context,RequestContext
from django.template.loader import get_template
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import admin

from django.utils.http import urlquote, urlencode

from django.core.paginator import Paginator

from rest_framework import response
from rest_framework.decorators import api_view

from formtools.wizard.views import SessionWizardView

from .models import ProvChange, Comment, Vouch, Issue, IssueComment, Source, Map, Milestone
from provshapes.models import ProvShape, CntrShape

from django.db.models import Count
from django.db import transaction

import datetime
import urllib2







####################################
# Country and region definitions

countries = [(u'Afghanistan', u'Afghanistan'), (u'\xc5land Islands', u'\xc5land Islands'), (u'Albania', u'Albania'), (u'Algeria', u'Algeria'), (u'American Samoa', u'American Samoa'), (u'Andorra', u'Andorra'), (u'Angola', u'Angola'), (u'Anguilla', u'Anguilla'), (u'Antigua and Barbuda', u'Antigua and Barbuda'), (u'Argentina', u'Argentina'), (u'Armenia', u'Armenia'), (u'Aruba', u'Aruba'), (u'Australia', u'Australia'), (u'Austria', u'Austria'), (u'Azerbaijan', u'Azerbaijan'), (u'The Bahamas', u'The Bahamas'), (u'Bahrain', u'Bahrain'), (u'Bangladesh', u'Bangladesh'), (u'Barbados', u'Barbados'), (u'Belarus', u'Belarus'), (u'Belgium', u'Belgium'), (u'Belize', u'Belize'), (u'Benin', u'Benin'), (u'Bermuda', u'Bermuda'), (u'Bhutan', u'Bhutan'), (u'Bolivia', u'Bolivia'), (u'Bonaire', u'Bonaire'), (u'Bosnia and Herzegovina', u'Bosnia and Herzegovina'), (u'Botswana', u'Botswana'), (u'Bouvet Island', u'Bouvet Island'), (u'Brazil', u'Brazil'), (u'British Indian Ocean Territory', u'British Indian Ocean Territory'), (u'United States Minor Outlying Islands', u'United States Minor Outlying Islands'), (u'British Virgin Islands', u'British Virgin Islands'), (u'Brunei', u'Brunei'), (u'Bulgaria', u'Bulgaria'), (u'Burkina Faso', u'Burkina Faso'), (u'Burundi', u'Burundi'), (u'Cambodia', u'Cambodia'), (u'Cameroon', u'Cameroon'), (u'Canada', u'Canada'), (u'Cape Verde', u'Cape Verde'), (u'Cayman Islands', u'Cayman Islands'), (u'Central African Republic', u'Central African Republic'), (u'Chad', u'Chad'), (u'Chile', u'Chile'), (u'China', u'China'), (u'Christmas Island', u'Christmas Island'), (u'Cocos (Keeling) Islands', u'Cocos (Keeling) Islands'), (u'Colombia', u'Colombia'), (u'Comoros', u'Comoros'), (u'Republic of the Congo', u'Republic of the Congo'), (u'Democratic Republic of the Congo', u'Democratic Republic of the Congo'), (u'Cook Islands', u'Cook Islands'), (u'Costa Rica', u'Costa Rica'), (u'Croatia', u'Croatia'), (u'Cuba', u'Cuba'), (u'Cura\xe7ao', u'Cura\xe7ao'), (u'Cyprus', u'Cyprus'), (u'Czech Republic', u'Czech Republic'), (u'Denmark', u'Denmark'), (u'Djibouti', u'Djibouti'), (u'Dominica', u'Dominica'), (u'Dominican Republic', u'Dominican Republic'), (u'Ecuador', u'Ecuador'), (u'Egypt', u'Egypt'), (u'El Salvador', u'El Salvador'), (u'Equatorial Guinea', u'Equatorial Guinea'), (u'Eritrea', u'Eritrea'), (u'Estonia', u'Estonia'), (u'Ethiopia', u'Ethiopia'), (u'Falkland Islands', u'Falkland Islands'), (u'Faroe Islands', u'Faroe Islands'), (u'Fiji', u'Fiji'), (u'Finland', u'Finland'), (u'France', u'France'), (u'French Guiana', u'French Guiana'), (u'French Polynesia', u'French Polynesia'), (u'French Southern and Antarctic Lands', u'French Southern and Antarctic Lands'), (u'Gabon', u'Gabon'), (u'The Gambia', u'The Gambia'), (u'Georgia', u'Georgia'), (u'Germany', u'Germany'), (u'Ghana', u'Ghana'), (u'Gibraltar', u'Gibraltar'), (u'Greece', u'Greece'), (u'Greenland', u'Greenland'), (u'Grenada', u'Grenada'), (u'Guadeloupe', u'Guadeloupe'), (u'Guam', u'Guam'), (u'Guatemala', u'Guatemala'), (u'Guernsey', u'Guernsey'), (u'Guinea', u'Guinea'), (u'Guinea-Bissau', u'Guinea-Bissau'), (u'Guyana', u'Guyana'), (u'Haiti', u'Haiti'), (u'Heard Island and McDonald Islands', u'Heard Island and McDonald Islands'), (u'Honduras', u'Honduras'), (u'Hong Kong', u'Hong Kong'), (u'Hungary', u'Hungary'), (u'Iceland', u'Iceland'), (u'India', u'India'), (u'Indonesia', u'Indonesia'), (u'Ivory Coast', u'Ivory Coast'), (u'Iran', u'Iran'), (u'Iraq', u'Iraq'), (u'Republic of Ireland', u'Republic of Ireland'), (u'Isle of Man', u'Isle of Man'), (u'Israel', u'Israel'), (u'Italy', u'Italy'), (u'Jamaica', u'Jamaica'), (u'Japan', u'Japan'), (u'Jersey', u'Jersey'), (u'Jordan', u'Jordan'), (u'Kazakhstan', u'Kazakhstan'), (u'Kenya', u'Kenya'), (u'Kiribati', u'Kiribati'), (u'Kuwait', u'Kuwait'), (u'Kyrgyzstan', u'Kyrgyzstan'), (u'Laos', u'Laos'), (u'Latvia', u'Latvia'), (u'Lebanon', u'Lebanon'), (u'Lesotho', u'Lesotho'), (u'Liberia', u'Liberia'), (u'Libya', u'Libya'), (u'Liechtenstein', u'Liechtenstein'), (u'Lithuania', u'Lithuania'), (u'Luxembourg', u'Luxembourg'), (u'Macau', u'Macau'), (u'Republic of Macedonia', u'Republic of Macedonia'), (u'Madagascar', u'Madagascar'), (u'Malawi', u'Malawi'), (u'Malaysia', u'Malaysia'), (u'Maldives', u'Maldives'), (u'Mali', u'Mali'), (u'Malta', u'Malta'), (u'Marshall Islands', u'Marshall Islands'), (u'Martinique', u'Martinique'), (u'Mauritania', u'Mauritania'), (u'Mauritius', u'Mauritius'), (u'Mayotte', u'Mayotte'), (u'Mexico', u'Mexico'), (u'Federated States of Micronesia', u'Federated States of Micronesia'), (u'Moldova', u'Moldova'), (u'Monaco', u'Monaco'), (u'Mongolia', u'Mongolia'), (u'Montenegro', u'Montenegro'), (u'Montserrat', u'Montserrat'), (u'Morocco', u'Morocco'), (u'Mozambique', u'Mozambique'), (u'Myanmar', u'Myanmar'), (u'Namibia', u'Namibia'), (u'Nauru', u'Nauru'), (u'Nepal', u'Nepal'), (u'Netherlands', u'Netherlands'), (u'New Caledonia', u'New Caledonia'), (u'New Zealand', u'New Zealand'), (u'Nicaragua', u'Nicaragua'), (u'Niger', u'Niger'), (u'Nigeria', u'Nigeria'), (u'Niue', u'Niue'), (u'Norfolk Island', u'Norfolk Island'), (u'North Korea', u'North Korea'), (u'Northern Mariana Islands', u'Northern Mariana Islands'), (u'Norway', u'Norway'), (u'Oman', u'Oman'), (u'Pakistan', u'Pakistan'), (u'Palau', u'Palau'), (u'Palestine', u'Palestine'), (u'Panama', u'Panama'), (u'Papua New Guinea', u'Papua New Guinea'), (u'Paraguay', u'Paraguay'), (u'Peru', u'Peru'), (u'Philippines', u'Philippines'), (u'Pitcairn Islands', u'Pitcairn Islands'), (u'Poland', u'Poland'), (u'Portugal', u'Portugal'), (u'Puerto Rico', u'Puerto Rico'), (u'Qatar', u'Qatar'), (u'Republic of Kosovo', u'Republic of Kosovo'), (u'R\xe9union', u'R\xe9union'), (u'Romania', u'Romania'), (u'Russia', u'Russia'), (u'Rwanda', u'Rwanda'), (u'Saint Barth\xe9lemy', u'Saint Barth\xe9lemy'), (u'Saint Helena', u'Saint Helena'), (u'Saint Kitts and Nevis', u'Saint Kitts and Nevis'), (u'Saint Lucia', u'Saint Lucia'), (u'Saint Martin', u'Saint Martin'), (u'Saint Pierre and Miquelon', u'Saint Pierre and Miquelon'), (u'Saint Vincent and the Grenadines', u'Saint Vincent and the Grenadines'), (u'Samoa', u'Samoa'), (u'San Marino', u'San Marino'), (u'S\xe3o Tom\xe9 and Pr\xedncipe', u'S\xe3o Tom\xe9 and Pr\xedncipe'), (u'Saudi Arabia', u'Saudi Arabia'), (u'Senegal', u'Senegal'), (u'Serbia', u'Serbia'), (u'Seychelles', u'Seychelles'), (u'Sierra Leone', u'Sierra Leone'), (u'Singapore', u'Singapore'), (u'Sint Maarten', u'Sint Maarten'), (u'Slovakia', u'Slovakia'), (u'Slovenia', u'Slovenia'), (u'Solomon Islands', u'Solomon Islands'), (u'Somalia', u'Somalia'), (u'South Africa', u'South Africa'), (u'South Georgia', u'South Georgia'), (u'South Korea', u'South Korea'), (u'South Sudan', u'South Sudan'), (u'Spain', u'Spain'), (u'Sri Lanka', u'Sri Lanka'), (u'Sudan', u'Sudan'), (u'Suriname', u'Suriname'), (u'Svalbard and Jan Mayen', u'Svalbard and Jan Mayen'), (u'Swaziland', u'Swaziland'), (u'Sweden', u'Sweden'), (u'Switzerland', u'Switzerland'), (u'Syria', u'Syria'), (u'Taiwan', u'Taiwan'), (u'Tajikistan', u'Tajikistan'), (u'Tanzania', u'Tanzania'), (u'Thailand', u'Thailand'), (u'East Timor', u'East Timor'), (u'Togo', u'Togo'), (u'Tokelau', u'Tokelau'), (u'Tonga', u'Tonga'), (u'Trinidad and Tobago', u'Trinidad and Tobago'), (u'Tunisia', u'Tunisia'), (u'Turkey', u'Turkey'), (u'Turkmenistan', u'Turkmenistan'), (u'Turks and Caicos Islands', u'Turks and Caicos Islands'), (u'Tuvalu', u'Tuvalu'), (u'Uganda', u'Uganda'), (u'Ukraine', u'Ukraine'), (u'United Arab Emirates', u'United Arab Emirates'), (u'United Kingdom', u'United Kingdom'), (u'United States', u'United States'), (u'Uruguay', u'Uruguay'), (u'Uzbekistan', u'Uzbekistan'), (u'Vanuatu', u'Vanuatu'), (u'Venezuela', u'Venezuela'), (u'Vietnam', u'Vietnam'), (u'Wallis and Futuna', u'Wallis and Futuna'), (u'Western Sahara', u'Western Sahara'), (u'Yemen', u'Yemen'), (u'Zambia', u'Zambia'), (u'Zimbabwe', u'Zimbabwe')]

regions = {"Europe": "\u00c5land Islands|Albania|Andorra|Austria|Belgium|Bulgaria|Bosnia and Herzegovina|Belarus|Switzerland|Cyprus|Czech Republic|Germany|Denmark|Spain|Estonia|Finland|France|Faroe Islands|United Kingdom|Guernsey|Gibraltar|Greece|Croatia|Hungary|Isle of Man|Republic of Ireland|Iceland|Italy|Jersey|Republic of Kosovo|Liechtenstein|Lithuania|Luxembourg|Latvia|Monaco|Moldova|Republic of Macedonia|Malta|Montenegro|Netherlands|Norway|Poland|Portugal|Romania|Svalbard and Jan Mayen|San Marino|Serbia|Slovakia|Slovenia|Sweden|Ukraine|Holy See", "Oceania": "American Samoa|Australia|Cocos (Keeling) Islands|Cook Islands|Christmas Island|Fiji|Federated States of Micronesia|Guam|Kiribati|Marshall Islands|Northern Mariana Islands|New Caledonia|Norfolk Island|Niue|Nauru|New Zealand|Pitcairn Islands|Palau|Papua New Guinea|French Polynesia|Solomon Islands|Tokelau|Tonga|Tuvalu|Vanuatu|Wallis and Futuna|Samoa", "Central America": "Aruba|Anguilla|Antigua and Barbuda|Bonaire|The Bahamas|Saint Barth\u00e9lemy|Belize|Barbados|Costa Rica|Cuba|Cura\u00e7ao|Cayman Islands|Dominica|Dominican Republic|Guadeloupe|Grenada|Guatemala|Honduras|Haiti|Jamaica|Saint Kitts and Nevis|Saint Lucia|Saint Martin|Mexico|Montserrat|Martinique|Nicaragua|Panama|Puerto Rico|El Salvador|Sint Maarten|Turks and Caicos Islands|Trinidad and Tobago|Saint Vincent and the Grenadines|Virgin Islands (British)|Virgin Islands (U.S.)", "Africa": "Angola|French Southern and Antarctic Lands|Burundi|Benin|Burkina Faso|Botswana|Central African Republic|Ivory Coast|Cameroon|Democratic Republic of the Congo|Republic of the Congo|Comoros|Cape Verde|Djibouti|Eritrea|Ethiopia|Gabon|Ghana|Guinea|The Gambia|Guinea-Bissau|Equatorial Guinea|British Indian Ocean Territory|Kenya|Liberia|Lesotho|Madagascar|Mali|Mozambique|Mauritania|Mauritius|Malawi|Mayotte|Namibia|Niger|Nigeria|R\u00e9union|Rwanda|Sudan|Senegal|Saint Helena|Sierra Leone|Somalia|South Sudan|S\u00e3o Tom\u00e9 and Pr\u00edncipe|Swaziland|Seychelles|Chad|Togo|Tanzania|Uganda|South Africa|Zambia|Zimbabwe", "Asia": "Afghanistan|Armenia|Azerbaijan|Bangladesh|Brunei|Bhutan|China|Georgia|Hong Kong|Indonesia|India|Japan|Kazakhstan|Kyrgyzstan|Cambodia|South Korea|Laos|Sri Lanka|Macau|Maldives|Myanmar|Mongolia|Malaysia|Nepal|Pakistan|Philippines|North Korea|Russia|Singapore|Thailand|Tajikistan|Turkmenistan|East Timor|Taiwan|Uzbekistan|Vietnam", "North America": "Bermuda|Canada|Greenland|Saint Pierre and Miquelon|United States", "South America": "Argentina|Bolivia|Brazil|Chile|Colombia|Ecuador|Falkland Islands|French Guiana|Guyana|Peru|Paraguay|South Georgia|Suriname|Uruguay|Venezuela", "Middle East": "United Arab Emirates|Bahrain|Algeria|Egypt|Western Sahara|Iran|Iraq|Israel|Jordan|Kuwait|Lebanon|Libya|Morocco|Oman|Palestine|Qatar|Saudi Arabia|Syria|Tunisia|Turkey|Yemen"}








###########################
# Info and text helpers

map_resources = """
                                    <li><a target="_blank" href="http://mapwarper.net/">MapWarper</a></li>
                                    <li><a target="_blank" href="http://www.oldmapsonline.org/">OldMapsOnline</a></li>
                                    <li><a target="_blank" href="http://www.vidiani.com/tag/administrative-maps/">Vidiani</a></li>
                                    <li><a target="_blank" href="http://www.mapsopensource.com">MapsOpenSource.com</a></li>
                                    <li><a target="_blank" href="http://www.ezilon.com">Ezilon.com</a></li>
                                    <li><a target="_blank" href="https://www.loc.gov/maps/?q=administrative%20divisions">The Library of Congress Map Collection</a></li>
                                    <li><a target="_blank" href="https://legacy.lib.utexas.edu/maps/map_sites/country_sites.html">The Perry-Castaneda Library Map Collection</a></li>
                                    <li><a target="_blank" href="http://alabamamaps.ua.edu/historicalmaps/">Alabama Maps Historical Maps</a></li>
                                    <li><a target="_blank" href="http://www.zum.de/whkmla/region/indexa.html">World History at KMLA</a></li>
                                    <li><a target="_blank" href="http://www.antiquemapsandprints.com/prints-and-maps-by-country-12-c.asp">Antique Maps and Prints</a></li>
                                    <li><a target="_blank" href="http://catalogue.defap-bibliotheque.fr/index.php?lvl=index">La bibliotheque du Defap</a></li>
                                    <li><a target="_blank" href="https://www.euratlas.net/history/hisatlas/index.html">EurAtlas Historical Maps</a></li>
                                    <li><a target="_blank" href="https://books.google.no/books?id=n-xZp-QMKCcC&amp;lpg=PA25&amp;ots=qM9PapNLCF&amp;dq=world%20mapping%20today%20parry&amp;hl=no&amp;pg=PA320#v=onepage&amp;q=world%20mapping%20today%20parry&amp;f=false">"World Mapping Today", by Bob Parry and Chris Perkins</a></li>
                """

geoinstruct = """
                <ol>
                    <li>
                    Guided by the map, draw a clipping polygon that <em>encircles</em> the province that gave away territory.
                    <br>
                    That is, do not follow the borders exactly, but rather draw with a significant error-margin around the province boundaries.
                    <br>
                    This makes it easier to draw and will avoid common topological and integration problems in border dataset,
                    since there are bound to be minor inaccuracies in the historical maps and their georeferencing. 
                    <br><br>
                    </li>
                    <li>
                    Only if the giving province shares a border with the
                    receiving province or any other giving provinces, should you follow those parts of the border exactly.
                    (To avoid gaps between the clipping polygon and any previously drawn giving provinces, shown in gray, 
                    just make sure they overlap.)
                    <br><br>
                    </li>
                    <li>
                    If the giving province only gave away parts of its territory
                    it's sufficient to just draw around the area that was transferred (e.g. a tiny corner of the province
                    or a series of islands).
                    <br><br>
                    </li>
                    <li>
                    Draw multiple polygons if necessary.
                    <br><br>
                    </li>
                </ol>
                
            </b>
            """

TYPEINFO = {"NewInfo": {"label": "NewInfo",
                         "short": "A change was made to a province's name, codes, or capital.",
                          "descr": """
                                    The province experienced a change in its basic information. In addition, provinces splitting up, 
                                    merging together, or experiencing other major territorial changes are sometimes accompanied by changes
                                    to their name and codes as well. 
                                    """,
                          "img": '<img style="width:100px" src="/static/webnewinfo.png"/>',
                          },
              "Breakaway": {"label": "Breakaway",
                            "short": "A new province was created by breaking away from an existing province.",
                              "descr": """
                                        This province is the result of breaking away or seceding from a province,
                                        one which continues to exist afterwards. 
                                        """,
                              "img": '<img style="width:100px" src="/static/webbreakaway.png"/>',
                              },
              "SplitPart": {"label": "SplitPart",
                            "short": "A new province was created as part of the splitting and dissolution of an existing province.",
                              "descr": """
                                        This is one of several parts created after the dissolution of a now defunct province.
                                        """,
                              "img": '<img style="width:100px" src="/static/websplit.png"/>',
                              },
              "TransferExisting": {"label": "TransferExisting",
                               "short": "Part of a province's territory was transferred to another province.",
                              "descr": """
                                        The transferred territory is sent to an existing province.
                                        (Requires a map showing the now defunct province) 
                                        """,
                              "img": '<img style="width:100px" src="/static/webtransferexisting.png"/>',
                              },
             "MergeExisting": {"label": "MergeExisting",
                              "short": "An entire province ceased to exist and became part of another province.",
                              "descr": """
                                        An entire province is merged into an existing province.
                                        (Requires a map showing the now defunct province) 
                                        """,
                              "img": '<img style="width:100px" src="/static/webmergeexisting.png"/>',
                              },
              "TransferNew": {"label": "TransferNew",
                               "short": "Part of a province's territory was transferred to form part of a new province.",
                              "descr": """
                                        The transferred territory is used to serve as part of the foundation for an entirely new province.
                                        (Requires a map showing the province outline prior to the transfer of territory)
                                        """,
                              "img": '<img style="width:100px" src="/static/webtransfernew.png"/>',
                              },
             "MergeNew": {"label": "MergeNew",
                              "short": "An entire province ceased to exist and merged to form part of a new province.",
                              "descr": """
                                        An entire province is merged to form part of the foundation for an entirely new province.
                                        (Requires a map showing the now defunct province) 
                                        """,
                              "img": '<img style="width:100px" src="/static/webmergenew.png"/>',
                              },
             "Begin": {"label": "Begin",
                              "short": "Marks the earliest known record for this province.",
                              "descr": """
                                        Typically used for entire country to say more information is needed
                                        beyond this point. 
                                        """,
                              "img": '<img style="width:100px" src="/static/webbegin.png"/>',
                              },
               }

EVENTTYPEINFO = {"NewInfo": {"label": "NewInfo",
                         "short": "A change was made to a province's name, codes, or capital.",
                          "descr": """
                                    
                                    """,
                          "img": '<img style="width:100px" src="/static/webnewinfo.png"/>',
                          },
              "Breakaway": {"label": "Breakaway",
                               "short": "A province lost territory to one or more breakaway regions.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/webbreakaway.png"/>',
                              },
              "Split": {"label": "Split",
                               "short": "A province split into multiple new ones.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/websplit.png"/>',
                              },
             "Form": {"label": "Form",
                              "short": "One or more provinces merged or transferred territory to a new province.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/webform.png"/>',
                              },
             "Expand": {"label": "Form",
                              "short": "One or more provinces merged or transferred territory to an existing province.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/webexpand.png"/>',
                              },
             "Begin": {"label": "Begin",
                              "short": "Marks the earliest known record for this province.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/webbegin.png"/>',
                              },
               }






####################################
# Helpers

def advancedchanges(request):
    bannertitle = "Advanced Change View"
    
    grids = []

    fields = [f.name for f in ProvChange._meta.get_fields()]
    changes = ProvChange.objects.filter(status__in="Pending Active".split())
    content = model2table(request, "Title", changes, fields)
    
    grids.append(dict(title="Change Table:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none; overflow:scroll",
                      width="99%",
                      ))
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           }
                  )

def slideshow():
    # from https://codepen.io/anon/pen/RGYPjP
    html = """
            //how many images we have
            $slides: 4;

            // how much we want each slide to show
            $time_per_slide: 4;

            // total time needed for full animation
            $total_animation_time: $time_per_slide * $slides;

            body{
              background:#000;
            }
            .container{
              margin:50px auto;
              width:500px;
              height:300px;
              overflow:hidden;
              border:10px solid;
              border-top-color:#856036;
              border-left-color:#5d4426;
              border-bottom-color:#856036;
              border-right-color:#5d4426;
              position:relative;

            }
            .photo{
              position:absolute;
              animation:round #{$total_animation_time}s infinite;
              opacity:0;
              
            }
            @keyframes round{   
              25%{
                opacity:1;
              }
              40%{
                opacity:0;
              }
            } 

            @for $index from 1 to $slides + 1{
              img:nth-child(#{$index}){
                animation-delay:#{$total_animation_time - $time_per_slide * $index}s
              }
            }
               
            <div class="container">
              <img class='photo'  src="http://farm9.staticflickr.com/8320/8035372009_7075c719d9.jpg" alt="" />
              <img class='photo'  src="http://farm9.staticflickr.com/8517/8562729616_35b1384aa1.jpg" alt="" />
              <img class='photo'  src="http://farm9.staticflickr.com/8465/8113424031_72048dd887.jpg" alt="" />
              <img class='photo'  src="http://farm9.staticflickr.com/8241/8562523343_9bb49b7b7b.jpg" alt="" />

            </div>
            """
    return html

class Grid:
    html = ""
    def add_cell(self, title, content, style="border-style:none", width="30%"):
        self.html += """
                    <div class="gridcell" style="float:left; width:{width}; padding-right:3%">
                            <h4>{title}</h4>
                            <div style="border-style:solid; border-color:black; border-radius:10px; padding:3% 5%; background-size:100% 100%; {style}">
                            {content}
                            </div>
                    </div>
                    """.format(title=title.encode("utf8"), content=content.encode("utf8"), style=style.encode("utf8"), width=width.encode("utf8"))

def markcountrychange(country, provtext, provcountries):
    if not isinstance(provcountries,list):
        provcountries = [provcountries]
    for provcountry in provcountries:
        if provcountry and provcountry != country:
            provtext += ' (<a id="blackbackground" style="color:gray" href="/contribute/view/{countryencode}">{countrytext}</a>)'.format(countryencode=urlquote(provcountry), countrytext=provcountry.encode('utf8'))
            break
    return provtext

def model2table(request, title, objects, fields):
    html = """
		<table class="modeltable"> 
		
			<style>
			table.modeltable {
				border-collapse: collapse;
				width: 100%;
			}

			th.modeltable, td.modeltable {
				text-align: left;
				padding: 8px;
			}

			tr.modeltable:nth-child(even){background-color: #f2f2f2}

			tr.modeltable:nth-child(odd){background-color: white}

			th.modeltable {
				background-color: orange;
				color: white;
			}
			</style>
		
			<tr class="modeltable">
				<th class="modeltable"> 
				</th>

				{% for field in fields %}
                                    <th class="modeltable">
                                        <b>{{ field }}</b>
                                    </th>
                                {% endfor %}
                                    
			</tr>
			</a>

                        {% if objects %}
			
                            {% for obj in objects %}
                                    <tr class="modeltable">
                                            <td class="modeltable">
                                                <a href="{% url 'viewchange' pk=obj.instance.pk %}">View</a>
                                            </td>
                                            
                                            {% for field in obj %}
                                                <td class="modeltable">{{ field.value }}</td>
                                            {% endfor %}
                                            
                                    </tr>
                            {% endfor %}

                        {% else %}

                            <tr class="modeltable">
                            <td class="modeltable"></td>
                            {% for _ in fields %}
                                <td class="modeltable"> - </td>
                            {% endfor %}
                            </tr>

                        {% endif %}
                            
		</table>
                """

    _fields = fields
    
    class ProvChangeForm(forms.ModelForm):

        class Meta:
            model = ProvChange
            fields = _fields
            
    objects = [ProvChangeForm(instance=obj) for obj in objects]
    rendered = Template(html).render(Context({"request":request, "fields":fields, "objects":objects, "title":title}))
    return rendered

def lists2table(request, lists, fields, classname="listtable", color='orange'):
    html = """
		<table class="{{ classname }}"> 
		
			<style>
			table.{{ classname }} {
				border-collapse: collapse;
				width: 100%;
			}

			th.{{ classname }}, td.{{ classname }} {
				text-align: left;
				padding: 8px;
			}

			tr.{{ classname }}:nth-child(even){background-color: #f2f2f2}

			tr.{{ classname }}:nth-child(odd){background-color: white}

			th.{{ classname }} {
				background-color: {{ color }};
				color: white;
			}
			</style>
		
			<tr class="{{ classname }}">
				<th class="{{ classname }}"> 
				</th>

				{% for field in fields %}
                                    <th class="{{ classname }}">
                                        <b>{{ field }}</b>
                                    </th>
                                {% endfor %}
                                    
			</tr>
			</a>
			
			{% for url,row in lists %}
				<tr class="{{ classname }}">
					<td style="vertical-align:top;" class="{{ classname }}">
					{% if url %}
                                            <a href="{{ url }}">View</a>
                                        {% endif %}
					</td>
					
                                        {% for value in row %}
                                            <td style="vertical-align:top" class="{{ classname }}">{{ value | safe}}</td>
                                        {% endfor %}
					
				</tr>
			{% endfor %}
		</table>
                """
    rendered = Template(html).render(Context({"request":request, "fields":fields, "lists":lists, "classname":classname, "color":color}))
    return rendered

def text_formatted(text):
    import re
    val = text
    
    def repl(matchobj):
        id = matchobj.group(2)
        return '<a target="_blank" href="/viewmap/{id}/"><img height="15px" src="/static/map.png">{id}</a>'.format(id=id)
    val,n = re.subn('#(map)([0-9]*)', repl, val)
    def repl(matchobj):
        id = matchobj.group(2)
        return '<a target="_blank" href="/viewsource/{id}/"><img height="15px" src="/static/source.png">{id}</a>'.format(id=id)
    val,n = re.subn('#(source)([0-9]*)', repl, val)
    return val.encode('utf8')
    










########################## BASIC OBJECT ACTIONS ###################












###########
# Users

def registration(request):
    
    if request.method == "POST":
        fieldnames = [f.name for f in User._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        if User.objects.filter(email=request.POST['email']).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        obj = User.objects.create_user(**formfieldvalues)
        print obj
        obj.save()

        html = redirect("/contribute/countries/")

    elif request.method == "GET":
        args = {'logininfo': LoginInfoForm(),
                'userinfo': UserInfoForm(),
                }
        html = render(request, 'provchanges/registration.html', args)

    return html

def login(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print username,password
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            auth_login(request, user)
            html = redirect("/contribute/countries/")
        else:
            args = {'login': LoginForm(),
                    'errormessage': "Could not find that username or password",
                    }
            html = render(request, 'provchanges/login.html', args)
            
    elif request.method == "GET":
        print request, request.user
        args = {'login': LoginForm(),
                }
        html = render(request, 'provchanges/login.html', args)

    return html

@login_required
def logout(request):
    print request, request.user
    auth_logout(request)
    html = render(request, 'provchanges/logout.html')
    return html


############
# Issues

class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = 'user country changeid added status title text'.split()
        widgets = {"text":forms.Textarea(attrs=dict(style="width:90%; font:inherit")),
                   "title":forms.TextInput(attrs=dict(style='width:80%; font:inherit')),
                   "country":forms.TextInput(attrs=dict(style='width:80%; font:inherit')),
                   }

class ReplyForm(forms.ModelForm):

    class Meta:
        model = IssueComment
        fields = 'user issue added status text'.split()
        widgets = {"text":forms.Textarea(attrs=dict(style="font-family:inherit; width:90%")),
                   'user':forms.HiddenInput(),
                   'added':forms.HiddenInput(),
                   'status':forms.HiddenInput(),
                   'issue':forms.HiddenInput(),
                   }

def issues2html(request, issues, commentheadercolor="orange"):
    fields = ["title","added"] #,"user"]
    
    lists = []
    for i in issues:
        title = i.title
        #print title
        rowdict = dict([(f,getattr(i, f, "")) for f in fields])
        rowdict['added'] = rowdict['added'].strftime('%b %#d, %Y')
        rowdict['title'] = '<div style="width:300px">%s</div>' % rowdict['title'].encode('utf8')
        link = "/viewissue/%s" % i.pk
        row = ['<a href="%s"><img src="/static/comment.png" style="opacity:0.2" height="45px"></a>' % link]
        row += [rowdict[f] for f in fields]
        #replies = IssueComment.objects.filter(issue=i, status='Active').count()
        #row += [replies]
        lists.append((None,row))  

    #print lists
    
    html = lists2table(request, lists, [''] + fields, classname="topicstable", color=commentheadercolor)
    
    return html

@login_required
def addissue(request):
    if request.method == 'POST':
        data = request.POST
        obj = Issue(user=request.user.username, country=data['country'],
                            added=datetime.datetime.now(),
                              title=data['title'], text=data['text'])
        if data.get('changeid'):
            obj.changeid = data['changeid']
        obj.save()
        print 'issue added'
        return redirect('/viewissue/%s' % obj.pk )
    
    elif request.method == 'GET':
        grids = []

        templ = '''
        	<h4 style="clear:both; margin-left:20px">New Topic:</h4>
		<div style="margin-left:60px">
                    <form action="/addissue/" method="post">
                    {% csrf_token %}

                    <p>
                    {{ issueform.title.label }}
                    {{ issueform.title }}
                    </p>
                    
                    <p>
                    {{ issueform.text.label }}
                    {{ issueform.text }}
                    </p>

                    {{ issueform.country.as_hidden }}
                    {{ issueform.changeid.as_hidden }}

                        <p>
                        Link to sources and maps by referencing their id number (e.g. #source12, #map9).
					<div style="width:45%; margin-left:20px; display:inline-block"><em>Suggested Sources:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in suggested_sources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/source.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
					<div style="width:45%; display:inline-block"><em>Suggested Maps:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in suggested_mapsources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/map.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewmap/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
			</p>
                    
                    <input type="submit" value="Submit" style="text-align:center; background-color:rgb(27,138,204); color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:3px;">
                    </form>

		</div>
		'''

        # new comm
        # SHOW EXTRA STUFF FOR COUNTRY AND CHANGE SPECIFIC
        # MAKE SURE IS SENT TO POST
        country = request.GET.get('country')
        changeid = request.GET.get('changeid')
        obj = Issue(user=request.user.username, country=country, changeid=changeid,
                    added=datetime.datetime.now())
        issueform = IssueForm(instance=obj)

        sources = get_country_sources(country)
        suggested_sources = sorted([(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources])
        maps = get_country_maps(country)
        suggested_mapsources = sorted([(m.pk, "{title} ({yr})".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps])
        
        content = Template(templ).render(RequestContext(request, {'issueform':issueform,
                                                                  'suggested_sources':suggested_sources,
                                                                  'suggested_mapsources':suggested_mapsources}))
		
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="99%",
                          ))

        return render(request, 'pshapes_site/base_grid.html', {"grids":grids,
                                                        "nomainbanner":True}
                          )

@login_required
def addissuecomment(request):
    if request.method == 'POST':
        data = request.POST
        print int(data['issue'])
        issue = get_object_or_404(Issue, pk=int(data['issue']))
        obj = IssueComment(user=request.user.username, issue=issue,
                            added=datetime.datetime.now(),
                              text=data['text'])
        obj.save()
        print 'issue comment added'
        return redirect('/viewissue/%s' % issue.pk )

@login_required
def editissue(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(Issue, pk=pk)
        
        fields = [f.name for f in Issue._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues['changeid'] = int(formfieldvalues['changeid']) if formfieldvalues['changeid'] else None
        print formfieldvalues
        for k,v in formfieldvalues.items():
            setattr(obj, k, v)
        obj.save()
        
        return redirect("/viewissue/%s" % pk )
        
    elif request.method == 'GET':
        grids = []

        templ = '''
        	<h4 style="clear:both; margin-left:20px">Edit Issue:</h4>
		<div style="margin-left:60px">
                    <form action="/editissue/{{ pk }}/" method="post">
                    {% csrf_token %}

                    <table style="border-spacing:0 10px; width:100%">

                        <tr>
                        <td style="width:5%; text-align:right; vertical-align:top">{{ issueform.country.label }}</td>
                        <td>{{ issueform.country }}</td>
                        </tr>
                        
                        <tr>
                        <td style="text-align:right; vertical-align:top">{{ issueform.changeid.label }}</td>
                        <td>{{ issueform.changeid }}</td>
                        </tr>

                        <tr>
                        <td style="text-align:right; vertical-align:top">{{ issueform.title.label }}</td>
                        <td>{{ issueform.title }}</td>
                        </tr>

                        <tr>
                        <td style="text-align:right; vertical-align:top">{{ issueform.text.label }}</td>
                        <td>{{ issueform.text }}</td>
                        </tr>
                    
                    </table>

                        <p>
                        Link to sources and maps by referencing their id number (e.g. #source12, #map9).
					<div style="width:45%; margin-left:20px; display:inline-block"><em>Suggested Sources:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in suggested_sources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/source.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
					<div style="width:45%; display:inline-block"><em>Suggested Maps:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in suggested_mapsources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/map.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewmap/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
			</p>
                    
                    <input type="submit" value="Submit" style="text-align:center; background-color:rgb(27,138,204); color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:3px;">
                    </form>
		</div>
		'''

        # new comm
        # SHOW EXTRA STUFF FOR COUNTRY AND CHANGE SPECIFIC
        # MAKE SURE IS SENT TO POST
        obj = get_object_or_404(Issue, pk=pk)
        issueform = IssueForm(instance=obj)
        
        sources = get_country_sources(obj.country)
        suggested_sources = sorted([(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources])
        maps = get_country_maps(obj.country)
        suggested_mapsources = sorted([(m.pk, "{title} ({yr})".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps])
        
        content = Template(templ).render(RequestContext(request, {'pk':pk,
                                                                  'issueform':issueform,
                                                                  'suggested_sources':suggested_sources,
                                                                  'suggested_mapsources':suggested_mapsources}))
	
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="99%",
                          ))

        return render(request, 'pshapes_site/base_grid.html', {"grids":grids,
                                                        "nomainbanner":True}
                          )

def viewissue(request, pk):
    commentheadercolor = 'rgb(27,138,204)'

    issue = get_object_or_404(Issue, pk=pk)
    comments = IssueComment.objects.filter(issue=issue, status="Active").order_by("added")
    fields = ["added","user","text","withdraw","status"]
    rows = []
    for c in [issue] + list(comments):
        rowdict = dict([(f,getattr(c, f, "")) for f in fields])
        rowdict['pk'] = c.pk
        rowdict['added'] = rowdict['added'].strftime('%Y-%m-%d %H:%M')
        rowdict['text'] = text_formatted(rowdict['text'])
        rows.append(rowdict)
    addreplyobj = IssueComment(user=request.user.username, issue=issue,
                            added=datetime.datetime.now())
    replyform = ReplyForm(instance=addreplyobj).as_p()
    rendered = render(request, 'provchanges/viewissue.html', {'issue':issue, 'comments':rows, 'replyform':replyform, 'commentheadercolor':commentheadercolor})
    return rendered


@login_required
def dropissue(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.user.username == issue.user:
        issue.status = 'Withdrawn'
        issue.save()
        print 'issue dropped'
    return redirect('/viewissue/%s' % pk)


@login_required
def dropissuecomment(request, pk):
    comment = get_object_or_404(IssueComment, pk=pk)
    if request.user.username == comment.user:
        comment.status = 'Withdrawn'
        comment.save()
        print 'issue comment dropped'
    return redirect('/viewissue/%s' % comment.issue.pk)


###########
# Vouches

@login_required
def addvouch(request, pk):
    # pk belongs to provchange
    change = get_object_or_404(ProvChange, pk=pk)
    if request.user.username != change.user:
        # can only vouch for others' provchange, not your own...
        vouch = next(iter(Vouch.objects.filter(user=request.user.username, changeid=change.changeid)), None)
        if vouch:
            # vouch already exists
            vouch.status = "Active"
            vouch.save()
        else:
            # create new vouch
            vouch = Vouch(user=request.user.username, changeid=change.changeid, added=datetime.datetime.now())
            vouch.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def withdrawvouch(request, pk):
    vouch = get_object_or_404(Vouch, user=request.user.username, changeid=pk)
    if request.user.username == vouch.user:
        vouch.status = "Withdraw"
        vouch.save()
    return redirect(request.META['HTTP_REFERER'])


###########
# Sources

def get_country_sources(country):
    sources = Source.objects.filter(status='Active').order_by('title')
    if not country:
        for s in sources:
            if not s.country:
                # only non-country-specific
                yield s
    else:
        countries = [cn.strip().lower() for cn in country.split('|') if cn.strip()]
        for s in sources:
            scountries = [cn.strip().lower() for cn in s.country.split('|') if cn.strip()]
            if any((cn in scountries for cn in countries)):
                # if in countrylist
                yield s

class SourceForm(forms.ModelForm):

    class Meta:
        model = Source
        fields = 'status title citation note url country'.split()
        widgets = {"country":forms.TextInput(attrs=dict(style="width:98%")),
                   "title":forms.TextInput(attrs=dict(style="width:98%")),
                   "citation":forms.Textarea(attrs=dict(style="font-family:inherit")),
                   "note":forms.Textarea(attrs=dict(style="font-family:inherit")),
                   #"country":forms.HiddenInput(),
                   }
    

##    def as_griditem(self):
##        source = self.instance
##        color = 'rgb(122,122,122)'
##        griditem = """
##                <a href="/viewsource/{pk}/" style="text-decoration:none; color:inherit;">
##                    <div class="griditem" style="float:left; width:200px; margin:10px">
##                        <div class="gridheader" style="background-color:{color}; padding-top:10px">
##                            <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
##                            <h4 style="display:inline-block">{title}</h4>
##                        </div>
##                        
##                        <div class="gridcontent">
##                            <p>{citation}</p>
##                        </div>
##                    </div>
##                </a>
##                    """.format(title=source.title, citation=source.citation, pk=source.pk, color=color)
##        return griditem

@login_required
def addsource(request):
    if request.method == "GET":
        # new empty form
        sourceform = SourceForm(initial=request.GET.dict())
        return render(request, "provchanges/addsource.html", {'sourceform':sourceform})
    
    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Source._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(added=datetime.datetime.now(),
                               modified=datetime.datetime.now())
        print formfieldvalues
        src = Source(**formfieldvalues)
        src.save()
        # TODO: find way to refer back to referrer, http_refererer doesnt work...
        return redirect("/viewsource/%s" % src.pk)

def viewsource(request, pk):
    obj = get_object_or_404(Source, pk=pk)
    sourceform = SourceForm(instance=obj)
    for field in sourceform.fields.values():
        field.disabled = True
        field.widget.disabled = True
        field.widget.attrs['readonly'] = 'readonly'
    countrylinks = ['<a id="blackbackground" href="/contribute/view/{countryencode}">{countrytext}</a>'.format(countryencode=urlquote(co.strip()), countrytext=co.strip().encode('utf8'))
                    for co in obj.country.split('|')]
    countrylinks = ', '.join(countrylinks)
    return render(request, "provchanges/viewsource.html", {'sourceform':sourceform, 'pk':obj.pk, 'countrylinks':countrylinks})

@login_required
def editsource(request, pk):
    obj = get_object_or_404(Source, pk=pk)
    if request.method == "GET":
        sourceform = SourceForm(instance=obj)
        return render(request, "provchanges/editsource.html", {'sourceform':sourceform, 'pk':obj.pk})

    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Source._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(modified=datetime.datetime.now())
        print formfieldvalues
        for k,v in formfieldvalues.items():
            setattr(obj, k, v)
        obj.save()
        return redirect("/viewsource/%s" % obj.pk)

@login_required
def dropsource(request, pk):
    obj = get_object_or_404(Source, pk=pk)
    obj.status = "Withdrawn"
    obj.modified = datetime.datetime.now()
    obj.save()
    return redirect("/viewsource/%s" % obj.pk)


########
# Maps

def get_country_maps(country):
    maps = Map.objects.filter(status='Active').order_by('year','title')
    if not country:
        for m in maps:
            if not m.country:
                # only non-country-specific
                yield m
    else:
        countries = [cn.strip().lower() for cn in country.split('|') if cn.strip()]
        for m in maps:
            mcountries = [cn.strip().lower() for cn in m.country.split('|') if cn.strip()]
            if any((cn in mcountries for cn in countries)):
                # if in countrylist
                yield m
    
class MapForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = 'status title year country note source url wms'.split()
        widgets = {"country":forms.TextInput(attrs=dict(style="width:98%")),
                   "note":forms.Textarea(attrs=dict(style="font-family:inherit")),
                   #"country":forms.HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super(MapForm, self).__init__(*args, **kwargs)

        # new
        if 'initial' in kwargs and kwargs["initial"].get('country'):
            # means country was set in GET param, so get only sources relevant for that country
            country = kwargs["initial"]["country"]
            sources = get_country_sources(country)
        elif 'instance' in kwargs and kwargs["instance"].country:
            # means country was set in existing instance (edit mode), so get only sources relevant for that country
            country = kwargs["instance"].country
            sources = get_country_sources(country)
        else:
            # NOTE: This prob should never be the case...
            # get only the global sources
            sources = get_country_sources("")
        #choices = [(s.pk, SourceForm(instance=s).as_griditem()) for s in sources]
        choices = [(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources]
        #self.fields["source"].widget = GridSelectOneWidget(choices=choices)
        self.fields["source"].widget = forms.Select(choices=[('','')]+choices, attrs=dict(style="width:99%")) 

        wms = self.instance.wms
        if wms:
            try:
                self.wms_helper = WMS_Helper(wms)
                self.extent = self.wms_helper.bbox
            except:
                self.wms_helper = None # something went wrong, skip gracefully

##    def as_custom(self):
##        wms = self.instance.wms
##        if wms and self.wms_helper:
##            extent = self.wms_helper.bbox
####            params = self.wms_helper.get_link_params(width=400)
####            wmslink = wms + "?" + params
####            wmsimage = '<img src="{wmslink}" width="40%">'.format(wmslink=wmslink)
##        else:
##            extent = None
####            wmslink = "http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png"
####            wmsimage = '<img src="{wmslink}" style="opacity:0.1; width:40%">'.format(wmslink=wmslink)
##        return get_template("provchanges/mapform.html").render({'mapform':self, 'extent':extent})

##    def as_griditem(self):
##        mapp = self.instance
##        wms = self.instance.wms
##        if wms and self.wms_helper:
##            params = self.wms_helper.get_link_params(height=40)
##            wmslink = wms + "?" + params
##            wmsimage = '<img src="{wmslink}" height="40px">'.format(wmslink=wmslink)
##        else:
##            wmslink = "http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png"
##            wmsimage = '<img src="{wmslink}" style="opacity:0.1; height:40px">'.format(wmslink=wmslink)
##        color = 'rgb(58,177,73)'
##        griditem = """
##                <a href="/viewmap/{pk}/" style="text-decoration:none; color:inherit;">
##                    <div class="griditem" style="float:left; width:200px; margin:10px">
##                        <div class="gridheader" style="background-color:{color}; padding:10px;">
##                            {wmsimage}
##                            <h4 style="display:inline-block">{year}</h4>
##                        </div>
##                        
##                        <div class="gridcontent">
##                            <p>{title}</p>
##                        </div>
##                    </div>
##                </a>
##                    """.format(year=mapp.year, title=mapp.title, note=mapp.note, wmsimage=wmsimage, pk=mapp.pk, color=color)
##        return griditem

class WMS_Helper:
    def __init__(self, url):
        self.url = url
        wmsmeta = urllib2.urlopen(url+"?service=wms&request=getcapabilities").read()
        bbox = wmsmeta.split('<BoundingBox SRS="EPSG:4326"')[-1].strip().split()[:4] # hacky, can be multiple, just choosing last
        self.bbox = [float(xory.split('=')[-1].strip('"')) for xory in bbox]

    def image_url(self, width=None, height=None):
        bbox = self.bbox
        if width and height:
            pass
        elif height:
            ratio = (bbox[2]-bbox[0]) / (bbox[3]-bbox[1])
            width = height * ratio
        elif width:
            ratio = (bbox[3]-bbox[1]) / (bbox[2]-bbox[0])
            height = width * ratio
        else:
            raise Exception('Either width or height must be set')
        # Note: better to get unrectified, via "&STATUS=unwarped", but in that case not sure how to find raw image bbox (ie width & height)
        params = "service=wms&version=1.1.1&request=getmap&format=image/png&srs=EPSG%3A4326&bbox={bbox}&width={width}&height={height}".format(bbox=",".join(map(str,self.bbox)), width=width, height=height)
        return self.url + "?" + params

@login_required
def addmap(request):
    if request.method == "GET":
        # new empty form
        mapform = MapForm(initial=request.GET.dict())
        return render(request, "provchanges/addmap.html", {'mapform':mapform, 'map_resources':map_resources})
    
    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Map._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(added=datetime.datetime.now(),
                               modified=datetime.datetime.now())

        sourceid = formfieldvalues['source']
        sourceobj = get_object_or_404(Source, pk=sourceid) if sourceid else None
        formfieldvalues['source'] = sourceobj
        
        print formfieldvalues
        obj = Map(**formfieldvalues)
        obj.save()
        # TODO: find way to refer back to referrer, http_refererer doesnt work...
        return redirect("/viewmap/%s" % obj.pk)

def viewmap(request, pk):
    obj = get_object_or_404(Map, pk=pk)
    mapform = MapForm(instance=obj)
    for field in mapform.fields.values():
        field.disabled = True
        field.widget.disabled = True
        field.widget.attrs['readonly'] = 'readonly'
    countrylinks = ['<a id="blackbackground" href="/contribute/view/{countryencode}">{countrytext}</a>'.format(countryencode=urlquote(co.strip()), countrytext=co.strip().encode('utf8'))
                    for co in obj.country.split('|')]
    countrylinks = ', '.join(countrylinks)
    return render(request, "provchanges/viewmap.html", {'mapform':mapform, 'pk':obj.pk, 'countrylinks':countrylinks})

@login_required
def editmap(request, pk):
    obj = get_object_or_404(Map, pk=pk)
    if request.method == "GET":
        mapform = MapForm(instance=obj, initial=request.GET.dict())
        return render(request, "provchanges/editmap.html", {'mapform':mapform, 'pk':obj.pk})

    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Map._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(modified=datetime.datetime.now())
        
        sourceid = formfieldvalues.pop('source')
        sourceobj = get_object_or_404(Source, pk=sourceid) if sourceid else None
        formfieldvalues['source'] = sourceobj
        print formfieldvalues
        for k,v in formfieldvalues.items():
            setattr(obj, k, v)
            
        obj.save()
        return redirect("/viewmap/%s" % obj.pk)

@login_required
def dropmap(request, pk):
    obj = get_object_or_404(Map, pk=pk)
    obj.status = "Withdrawn"
    obj.modified = datetime.datetime.now()
    obj.save()
    return redirect("/viewmap/%s" % obj.pk)


################
# Milestones

# TODO: Not sure, should it only evaluate existing cases,
# or should it also allow more flexible queries incl nonexisting cases,
# such as coding all modern countries from a fixed list of countrynames?

class MilestoneForm(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = 'status title description model subset condition'.split()
        widgets = {"title":forms.TextInput(attrs=dict(style="width:98%")),
                   "description":forms.Textarea(attrs=dict(style="width:98%; font-family:inherit")),
                   "subset":forms.Textarea(attrs=dict(style="width:98%; font-family:inherit")),
                   "condition":forms.Textarea(attrs=dict(style="width:98%; font-family:inherit")),
                   #"country":forms.HiddenInput(),
                   }

    def get_progress(self):
        obj = self.instance
        if obj.model == 'ProvChange':
            model = ProvChange
        elif obj.model == 'Map':
            model = Map
        elif obj.model == 'Source':
            model = Source
        elif obj.model == 'Issue':
            model = Issue

        if obj.subset:
            subsetquery = """SELECT 1 AS id, COUNT(id) AS idcount
                            FROM provchanges_{model}
                            WHERE {subset}""".format(model=obj.model.lower(),
                                                     subset=obj.subset)
            print subsetquery
            subsetcount = model.objects.raw(subsetquery)[0].idcount

            conditionquery = """
                            SELECT 1 AS id, COUNT(id) AS idcount
                            FROM provchanges_{model}
                            WHERE ({subset}) AND ({condition})
                            """.format(model=obj.model.lower(), subset=obj.subset, condition=obj.condition)
            print conditionquery
            conditioncount = model.objects.raw(conditionquery)[0].idcount
            
        else:
            subsetquery = """SELECT 1 AS id, COUNT(id) AS idcount
                            FROM provchanges_{model}""".format(model=obj.model.lower())
            print subsetquery
            subsetcount = model.objects.raw(subsetquery)[0].idcount

            conditionquery = """
                            SELECT 1 AS id, COUNT(id) AS idcount
                            FROM provchanges_{model}
                            WHERE {condition}
                            """.format(model=obj.model.lower(), subset=obj.subset, condition=obj.condition)
            print conditionquery
            conditioncount = model.objects.raw(conditionquery)[0].idcount

        if subsetcount:
            progress = conditioncount / float(subsetcount) * 100
        else:
            progress = 0

        return progress

    def get_unsolved(self, n=10):
        obj = self.instance
        if obj.model == 'ProvChange':
            model = ProvChange
        elif obj.model == 'Map':
            model = Map
        elif obj.model == 'Source':
            model = Source
        elif obj.model == 'Issue':
            model = Issue

        if obj.subset:
            conditionquery = """
                            SELECT id, *
                            FROM provchanges_{model}
                            WHERE ({subset}) AND ({condition})
                            """.format(model=obj.model.lower(), subset=obj.subset, condition=obj.condition)
            print conditionquery
            return model.objects.raw(conditionquery)[:n]

        else:
            conditionquery = """
                            SELECT id, *
                            FROM provchanges_{model}
                            WHERE {condition}
                            """.format(model=obj.model.lower(), subset=obj.subset, condition=obj.condition)
            print conditionquery
            return model.objects.raw(conditionquery)[:n]

@login_required
def addmilestone(request):
    if request.method == "GET":
        # new empty form
        milestoneform = MilestoneForm(initial=request.GET.dict())
        return render(request, "provchanges/addmilestone.html", {'milestoneform':milestoneform})
    
    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Milestone._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(added=datetime.datetime.now(),
                               modified=datetime.datetime.now())
        print formfieldvalues
        assert formfieldvalues['model']
        mls = Milestone(**formfieldvalues)
        mls.save()
        # TODO: find way to refer back to referrer, http_refererer doesnt work...
        return redirect("/viewmilestone/%s" % mls.pk)

def viewmilestone(request, pk):
    obj = get_object_or_404(Milestone, pk=pk)
    milestoneform = MilestoneForm(instance=obj)
    for field in milestoneform.fields.values():
        field.disabled = True
        field.widget.disabled = True
        field.widget.attrs['readonly'] = 'readonly'
    try:
        progress = milestoneform.get_progress()
        progresstext = '%.0f%%' % progress
    except Exception as err:
        print err
        progress = 0
        progresstext = "Error: Check that subset and condition are valid SQL expressions"

    # TODO: Maybe include list of cases that do not adhere to condition?
##    fields = [f.name for f in obj._meta.get_fields()]
##    lists = []
##    for m in milestones:
##        rowdict = dict([getattr(m)])
##        
##        # calculate progress here
##        milestoneform = MilestoneForm(instance=m)
##        try:
##            progress = milestoneform.get_progress()
##            progresstext = '%.0f%%' % progress
##        except:
##            progress = 0
##            progresstext = "NA"
##        progr = progresstext
##        
##        url = "/viewmilestone/%s" % m.pk
##        icon = '<img src="/static/milestone.png" style="height:50px; opacity:0.2">'
##        linkimg = '<a href="%s">%s</a>' % (url,icon)
##        row = [linkimg, title, descr, progr]
##        lists.append((None,row))
##        
##    fixtable = lists2table(request, lists=lists,
##                                  fields=[""] + fields,
##                                 classname='fixtable', color='rgb(255,108,72)')

        # OR: show one by one
##        randid = milestoneform.get_unresolved(1)[0].id
##        typeobj = obj.instance
##        if typeobj.model == 'ProvChange':
##            inst = ProvChange.get(pk=randid)
##        elif typeobj.model == 'Map':
##            model = Map
##        elif typeobj.model == 'Source':
##            model = Source
##        elif typeobj.model == 'Issue':
##            model = Issue
        
    return render(request, "provchanges/viewmilestone.html", {'milestoneform':milestoneform, 'progress':progress, 'progresstext':progresstext, 'pk':obj.pk})

@login_required
def editmilestone(request, pk):
    obj = get_object_or_404(Milestone, pk=pk)
    if request.method == "GET":
        milestoneform = MilestoneForm(instance=obj)
        return render(request, "provchanges/editmilestone.html", {'milestoneform':milestoneform, 'pk':obj.pk})

    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Milestone._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(modified=datetime.datetime.now())
        print formfieldvalues
        assert formfieldvalues['model']
        for k,v in formfieldvalues.items():
            setattr(obj, k, v)
        obj.save()
        return redirect("/viewmilestone/%s" % obj.pk)

@login_required
def dropmilestone(request, pk):
    obj = get_object_or_404(Milestone, pk=pk)
    obj.status = "Withdrawn"
    obj.modified = datetime.datetime.now()
    obj.save()
    return redirect("/viewmilestone/%s" % obj.pk)













###################### MAIN PAGES ###################













##########################
# User pages

from .models import User

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","password"]
        widgets = {"password":forms.PasswordInput()}

class LoginInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","password"]
        widgets = {"password":forms.PasswordInput()}

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name","last_name","email","affiliation"]

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['required'] = 'true'

    def clean(self):
        # NOTE: Doesnt get called yet, because form is not used when adding/editing
        data = self.cleaned_data
        print 'EMAIL',self.cleaned_data['email'],len(User.objects.filter(email=self.cleaned_data['email']))
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return data

@login_required
def account_edit(request):
    userobj = User.objects.get(username=request.user)
    form = UserInfoForm(instance=userobj)
    if request.POST:
        if User.objects.filter(email=request.POST['email']).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        userobj.first_name = request.POST["first_name"]
        userobj.last_name = request.POST["last_name"]
        userobj.email = request.POST["email"]
        userobj.affiliation = request.POST["affiliation"]
        print userobj.first_name
        userobj.save()
        return redirect("/account/")
    else:
        ##form.fields["email"].widget.attrs['readonly'] = "readonly"
        return render(request, 'provchanges/accountedit.html', {"user":request.user, "userinfoform":form}
                      )
class UploadFileForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UploadFileForm, self).__init__(*args, **kwargs)

    def as_p(self):
        templ = """
                    <form method="post" action="/update/" enctype="multipart/form-data">
                        {% csrf_token %}
                        <table>
                        {{ form }}
                        </table>
                        <br>
                        <input type="submit" value="Update Boundary Data" onClick="alert('The website boundary data will now be updated, this may take a while.');" style="font-weight:bold; background-color:rgb(7,118,183); color:white; border-radius:5px; padding:5px">
                        </input>
                    </form>
                """
        rendered = Template(templ).render(RequestContext(self.request, {'form':self}))
        return rendered

@login_required
def account(request):
    userobj = User.objects.get(username=request.user)
    userform = UserInfoForm(instance=userobj)

    changes = ProvChange.objects.filter(user=request.user.username).order_by("-added")   # the dash reverses the order
    pending = ProvChange.objects.filter(user=request.user.username, status="Pending")
    comments = Comment.objects.filter(user=request.user.username, status="Active").order_by("-added") # the dash reverses the order
    
    grids = []
    bannertitle = "User Settings for '%s'" % request.user
    
    for field in userform.fields.values():
        field.widget.attrs['readonly'] = "readonly"
        field.widget.attrs["style"] = 'background-color:black; color:white'
    bannerleft = """
                <table style="text-align:right; padding-left:20%; padding-bottom:3%;">
                    {userinfoform}
                </table>
                
                <div style="text-align:center">
                    <a href="/account/edit" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Edit
                    </a>                    
                </div>
                <br>
                """.format(userinfoform=userform.as_table(),
                           )

    if request.user.is_staff:
        uploadform = UploadFileForm(request=request).as_p()
        bannerright = """
                        {uploadform}
                        
                        <br><br>
                        <a href="/logout" style="background-color:orange; color:white; border-radius:5px; padding:5px">
                            <b>Logout</b>
                        </a>
                        """.format(uploadform=uploadform)
    else:
        bannerright = """
                        <br><br>
                        <a href="/logout" style="background-color:orange; color:white; border-radius:5px; padding:5px">
                            <b>Logout</b>
                        </a>
                        """

    custombanner = """
                    <div style="padding-top:20px">
                    <h2>{bannertitle}</h2>
                    
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>

                        <td style="width:20%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:middle">
                            <img width="80%" src="/static/user.png">
                        </td>
                        
                        <td style="width:60%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:middle">
                        {left}
                        </td>
                        
                        <td style="width:20%; padding:1%; padding:0px; margin:0px; vertical-align:top; text-align:center">
                        {right}
                        </td>

                        </tr>
                        </table>

                    <br><br>
                    </div>
                        """.format(left=bannerleft, right=bannerright, bannertitle=bannertitle)

    # stats
    fields = ['','user','added','fromcountry','fromname','type','status']
    lists = []
    for o in changes[:50]:
        link = "/provchange/%s/view" % o.pk
        linkimg = '<a href="%s"><img style="opacity:0.9" src="/static/typechange.png" height="25px"></a>' % link
        row = [linkimg, o.user, o.added.strftime('%b %#d, %Y, %H:%M'), o.fromcountry.encode('utf8'), o.fromname.encode('utf8'), o.type, o.status]
        lists.append((None,row))
        
    content = lists2table(request, lists=lists, fields=fields,
                          classname="recentadds", color='orange')


    grids.append(dict(title="Your Contributions (last 50 only):", #most recent, 1-%s of %s):" % (min(changes.count(),50), changes.count()),
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="100%",
                      ))

    # comments
    issues = Issue.objects.filter(status="Active").order_by("-added") # the dash reverses the order
    comments = IssueComment.objects.filter(status="Active").order_by("-added") # the dash reverses the order
    objects = sorted(list(issues[:10]) + list(comments[:10]),
                     key=lambda d: d.added, reverse=True)
    fields = ["added","country","title","user","text"]
    lists = []
    for o in objects[:10]:
        if isinstance(o, Issue):
            pk = o.pk
            rowdict = dict(added=o.added, user=o.user, text=o.text,
                           country=o.country, title=o.title)
        elif isinstance(o, IssueComment):
            pk = o.issue.pk
            rowdict = dict(added=o.added, user=o.user, text=o.text,
                           country=o.issue.country, title=o.issue.title)
        rowdict['added'] = rowdict['added'].strftime('%b %#d, %Y, %H:%M')
        rowdict['text'] = text_formatted(rowdict['text'][:300]+'...' if len(rowdict['text']) > 300 else rowdict['text'])
        rowdict['title'] = rowdict['title'].encode('utf8')
        rowdict['country'] = rowdict['country'].encode('utf8')
        link = "/viewissue/%s" % pk
        linkimg = '<a href="%s"><img style="opacity:0.9" src="/static/comment.png" height="25px"></a>' % link
        row = [linkimg] + [rowdict[f] for f in fields]
        lists.append((None,row))
        
    content = lists2table(request, lists=lists, fields=["","Added","Country","Title","User","Comment"],
                          classname='yourcomments', color='rgb(27,138,204)')

    grids.append(dict(title="Your Comments (last 10 only):", #most recent, 1-%s of %s):" % (min(comments.count(),10), comments.count()),
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="93%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "custombanner":custombanner}
                  )














####################
# Issues pages

class IssueSearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'size':60}))
    country = forms.CharField(widget=forms.TextInput(attrs={'size':30}))
    status = forms.CharField(widget=forms.Select(choices=[("Active","Active"),
                                                           ("Resolved","Resolved"),
                                                           ("Withdrawn","Withdrawn"),
                                                            ])
                             )

def contribute_discuss(request):
    bannertitle = "Issues and Comments"
    color = 'rgb(27,138,204)'

    custombanner = """
                    <style>
                        .blackbackground a { color:white }
                        .blackbackground a:visited { color:grey }
                    </style>
                    """

    grids = []

    # main banner
    if request.method == "GET":
        searchform = IssueSearchForm(request.GET)
 
    else:
        searchform = IssueSearchForm()

    templ = """
            <br>
            <div class="blackbackground" style="width:90%">
                <h2 style="text-align:center">{{ title }}</h2>
                <form action="/contribute/issues/" method="get">
                    {% csrf_token %}

                    <table>
                    <tr>

                    <td>
                    Text: <br> {{ searchform.text }}
                    </td>
                    
                    <td>
                    Country: <br> {{ searchform.country }}
                    </td>

                    <td>
                    Status: <br> {{ searchform.status }}
                    </td>

                    <td>
                    <h4>
                        <input type="submit" value="Search" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:3px;">
                    </h4>
                    </td>

                    </tr>
                    </table>
                    
                </form>
            </div>
                """

    custombanner += Template(templ).render( RequestContext(request, {'searchform':searchform, 'title':bannertitle}) )

    # issue list
    issues = Issue.objects.all()
    if request.GET.get('country'):
        issues = issues.filter(country__icontains=request.GET['country'])
    if request.GET.get('status'):
        issues = issues.filter(status=request.GET['status'])
    if request.GET.get('text'):
        issues = issues.filter(title__icontains=request.GET['text']) | issues.filter(text__icontains=request.GET['text'])
    issues = issues.order_by('-added')
    print issues
    
    table = issues2html(request, issues, color)

    content = '''
                 <h3 id="issues">
                     Results (first 50 only):
                </h3>
                <div style="margin-left:2%">
                    {table}
                    <br><div width="100%" style="text-align:center"><a href="/addmap/" style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                </div>
                '''.format(table=table.encode('utf8'), color=color)
        
    grids.append(dict(title="",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="95%",
                      ))

    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":'<h2 style="padding-top:10px">'+bannertitle+'</h2>',
                                                           'custombanner':custombanner,
                                                           #"bannerleft":bannerleft, "bannerright":bannerright,
                                                           }
                  )

##def contribute_discuss(request):
##    bannertitle = "Issues and Comments"
##
##    custombanner = ""
##
##    grids = []
##
##    # discussion list
##    issues = Issue.objects.filter(country='', changeid=None, status="Active").order_by('-added')
##    
##    issuetable = issues2html(request, issues, 'rgb(27,138,204)')
##
##    content = """
##                <div style="margin-left:22px">{issuetable}</div>
##                <br><div width="100%" style="text-align:center"><a href="/addissue" style="text-align:center; background-color:rgb(27,138,204); color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
##                """.format(issuetable=issuetable)
##
##    grids.append(dict(title='''<br><hr>
##                                <img src="/static/comment.png" height="37px" style="display:inline-block">
##                                Ask questions or suggest improvements to the website:''',
##                      content=content,
##                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="99%",
##                      ))
##
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":'<h2 style="padding-top:10px">'+bannertitle+'</h2>',
##                                                           'custombanner':custombanner,
##                                                           #"bannerleft":bannerleft, "bannerright":bannerright,
##                                                           }
##                  )












####################
# Map pages

class MapSearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'size':60}))
    country = forms.IntegerField(widget=forms.TextInput(attrs={'size':30}))
    fromyear = forms.CharField(widget=forms.TextInput(attrs={'size':6}))
    toyear = forms.CharField(widget=forms.TextInput(attrs={'size':6}))

def contribute_maps(request):
    bannertitle = "Map Collection"
    color = 'rgb(58,177,73)'

    custombanner = """
                    <style>
                        .blackbackground a { color:white }
                        .blackbackground a:visited { color:grey }
                    </style>
                    """

    grids = []

    # main banner
    if request.method == "GET":
        searchform = MapSearchForm(request.GET)
 
    else:
        searchform = MapSearchForm()

    templ = """
            <br>
            <div class="blackbackground" style="width:90%">
                <h2 style="text-align:center">{{ title }}</h2>
                <form action="/maps/" method="get">
                    {% csrf_token %}

                    <table>
                    <tr>

                    <td>
                    Map text: <br> {{ searchform.text }}
                    </td>
                    
                    <td>
                    Country: <br> {{ searchform.country }}
                    </td>

                    <td>
                    Start: <br> {{ searchform.fromyear }}
                    </td>

                    <td>
                    End: <br> {{ searchform.toyear }}
                    </td>

                    <td>
                    <h4>
                        <input type="submit" value="Search" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:3px;">
                    </h4>
                    </td>

                    </tr>
                    </table>
                    
                </form>
            </div>
                """

    custombanner += Template(templ).render( RequestContext(request, {'searchform':searchform, 'title':bannertitle}) )

    # maps list
    maps = Map.objects.all()
    if request.GET.get('country'):
        maps = maps.filter(country__icontains=request.GET['country'])
    if request.GET.get('fromyear'):
        maps = maps.filter(year__gte=float(request.GET['fromyear']))
    if request.GET.get('toyear'):
        maps = maps.filter(year__lte=float(request.GET['toyear']))
    if request.GET.get('text'):
        maps = maps.filter(title__icontains=request.GET['text']) | maps.filter(note__icontains=request.GET['text'])
    maps = maps.filter(status='Active')
    maps = maps.order_by('-added')
    print maps
    
    fields = ['', 'year', 'title', 'note', 'external link']
    lists = []
    for mapp in maps[:10]: # only first 10
        wms = mapp.wms #"https://mapwarper.net/maps/wms/26754" #"https://mapwarper.net/maps/wms/19956"
        if wms:
            try:
                wmslink = WMS_Helper(wms).image_url(height=50)
                imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}"></a>'.format(pk=mapp.pk, wmslink=wmslink)
            except:
                wmslink = "/static/map.png"
                imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}" style="opacity:0.15"></a>'.format(pk=mapp.pk, wmslink=wmslink)
        else:
            wmslink = "/static/map.png"
            imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}" style="opacity:0.15"></a>'.format(pk=mapp.pk, wmslink=wmslink)
        urllink = '<a target="_blank" href="{url}">{urlshort}</a>'.format(url=mapp.url.encode('utf8'), urlshort=mapp.url.replace('http://','').replace('https://','').split('/')[0])
        row = [imglink, mapp.year, mapp.title, mapp.note, urllink]
        lists.append((None,row))

    table = lists2table(request, lists, fields, 'maptable', color)

    content = '''
                 <h3 id="maps">
                     Results (first 10 only):
                </h3>
                <div style="margin-left:2%">
                    {table}
                    <br><div width="100%" style="text-align:center"><a href="/addmap/" style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                </div>
                '''.format(table=table.encode('utf8'), color=color)
        
    grids.append(dict(title="",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="95%",
                      ))

    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":'<h2 style="padding-top:10px">'+bannertitle+'</h2>',
                                                           'custombanner':custombanner,
                                                           #"bannerleft":bannerleft, "bannerright":bannerright,
                                                           }
                  )















#########################
# Contribution pages

##def contribute_browse(request):
##    status = request.GET.get("status", "Accepted")
##    changes = ProvChange.objects.filter(status=status).order_by("-added") # the dash reverses the order
##    changestable = model2table(request, title="", objects=changes,
##                              fields=["date","type","fromname","toname","country","user","added","status"])
##    tabstyle = """
##            <style>
##            .curtab {
##                display:table-cell;
##                background-color:orange;
##                color:white;
##                border-radius:10px;
##                padding:10px; 
##                }
##            .tab {
##                display:table-cell;
##                background-color:null;
##                color:black;
##                border-radius:10px;
##                padding:10px;
##                }
##            </style>
##            """
##    
##    tabs = """
##            <div class="{Accepted}"><h4><a href="/contribute/browse?status=Accepted" style="color:inherit">Accepted</a></h4></div>
##            <div class="{Pending}"><h4><a href="/contribute/browse?status=Pending" style="color:inherit">Pending</a></h4></div>
##
##            <br>
##            <br>
##            
##            """.format(Accepted="curtab" if status=="Accepted" else "tab",
##                        Pending="curtab" if status=="Pending" else "tab")
##    content = tabstyle + tabs + changestable
##    
##    grids = []
##    grids.append(dict(title="Browse all province changes:",
##                      content=content,
##                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="99%",
##                      ))
##    
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"nomainbanner":True}
##                  )

def contribute_countries(request):
    bannertitle = "Contribute"

    bannerleft = """
                        <div style="width:100%; height:240px; overflow: hidden; text-align:left">
                            <img src="/static/webfrontimg.png" width="95%">
                        </div>
                        <br><br>
                """


    #QUOTE
    #Anyone who has an interest in coding some changes for one or more countries,
    #should have the ability to do so themselves, regardless of skills or background. 

    if request.user.is_authenticated():
        bannerright = """
                            <style>
                                .blackbackground a { color:white }
                                .blackbackground a:visited { color:grey }
                            </style>
                                    
                            <br><br>
                            <div class="blackbackground" style="text-align:left; width:70%%">
                                    <h3>Welcome, <a href="/account">%s</a>!</h2>
                                    <p>
                                    Contributing to Pshapes is both easy and fast: just register and
                                    contribute as little or as much as possible. You can add changes, quality check,
                                    vouch or edit the work of others, raise issues, or discuss difficult cases. 
                                    </p>

                                    <p>
                                    Read <a href="/about/tutorial">the tutorial</a> for a brief walkthrough of how it works,
                                    or get started right away by choosing a country from the map or list below.
                                    </p>

                            </div>
                            """ % request.user.username
    else:
        bannerright = """
                            <style>
                                .blackbackground a { color:white }
                                .blackbackground a:visited { color:grey }
                            </style>
                                    
                            <br><br>
                            <div class="blackbackground" style="text-align:left">
                                    <h3>Welcome!</h2>
                                    <p>
                                    If you're looking to get involved in the Pshapes project you've come to the right place!
                                    Contributing to Pshapes is both easy and fast: just register and
                                    contribute as little or as much as possible. You can add changes, quality check,
                                    vouch or edit the work of others, raise issues, or discuss difficult cases. 
                                    </p>

                                    <p>
                                    Read <a href="/about/tutorial">the tutorial</a> for a brief walkthrough of how it works,
                                    then sign up or login to get started.
                                    </p>

                                    <br>
                                            
                                    <div style="text-align:right">
                                    <a href="/registration" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                                    Sign Up
                                    </a>
                                    or
                                    <a href="/login" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                                    Login
                                    </a>
                                    </div>

                            </div>
                            """

##    custombanner = """
##                    <br>
##                    <div style="display:inline-block; width:60%%">
##                        <h2 style="text-align:center">%s</h2>
##                        %s</div>
##                    <div style="display:inline-block; width:35%%; vertical-align:top">%s</div>
##                    <br><br><br>
##                    """ % (bannertitle,bannerleft,bannerright)

    content = """
                    <h1>1</h1>
                    <div style="text-align:left">
                        Choose a country from the list below and begin registering historical changes.
                        After a vetting process the change will be included in the
                        next version of the data available from the website.

                        You can also browse,
                        quality check, suggest edits, and add comments to existing province changes
                        already submitted by other users.

                        <style>
                            #blackbackground a { color:white }
                            #blackbackground a:visited { color:grey }
                        </style>                        
                    </div>
            """

    
    grids = []



    # countries

    from django.db.models import Count,Max,Min

    # already coded
    fields = ["country","entries","issues","discussions","mindate","maxdate"]
    lists = []
    rowdicts = dict() #dict([(countryid,dict(country=countryid,entries=0,mindate="-",maxdate="-")) for countryid,countryname in countries])
    for rowdict in ProvChange.objects.values("fromcountry").exclude(status="NonActive").annotate(entries=Count('pk'),
                                                                                                 mindate=Min("date"),
                                                                                                 maxdate=Max("date")):
        rowdict["country"] = rowdict.pop("fromcountry")
        rowdicts[rowdict["country"]] = rowdict
    for rowdict in ProvChange.objects.values("tocountry").exclude(status="NonActive").annotate(entries=Count('pk'),
                                                                                                 mindate=Min("date"),
                                                                                                 maxdate=Max("date")):
        rowdict["country"] = rowdict.pop("tocountry")
        if rowdict["country"] in rowdicts:
            cur = rowdicts[rowdict["country"]]
            cur["entries"] = max(cur["entries"],rowdict["entries"]) # NOTE: by overwriting here, we are only keeping counts of tocountry (if we plus then we basically double the count)
            cur["mindate"] = min(cur["mindate"], rowdict["mindate"]) if cur["mindate"] != "-" else rowdict["mindate"]
            cur["maxdate"] = min(cur["maxdate"], rowdict["maxdate"]) if cur["maxdate"] != "-" else rowdict["maxdate"]
        else:
            rowdicts[rowdict["country"]] = rowdict

    for country in sorted(rowdicts.keys()):
        if not country: continue
        rowdict = rowdicts[country]
        rowdict['mindate'] = rowdict['mindate'].year
        rowdict['maxdate'] = rowdict['maxdate'].year
        rowdict['discussions'] = Issue.objects.filter(country=country, changeid=None, status="Active").count()
        rowdict['issues'] = Issue.objects.filter(country=country, changeid__isnull=False, status="Active").count()
        rowdict['url'] = "/contribute/view/%s" % urlquote(rowdict["country"])

        cntr = CntrShape.objects.raw('''SELECT 1 AS id, ST_AsSVG(geom) as svg, name, geom
                                        FROM provshapes_cntrshape
                                        WHERE simplify=0.2 AND name='%s'
                                        ''' % country)
        obj = next(iter(cntr), None)
        if obj:
            # TODO: not very effective since we parse and calculate bbox from the SVG string, because the coordinates in ST_AsSVG() are not the same as the real coords and bbox
            svg = obj.svg
            multis = svg.replace(' Z', '').split('M ')
            flat = [float(v) for mult in multis for v in mult.replace('L ','').strip().split()]
            xs,ys = flat[0::2],flat[1::2]
            bbox = min(xs),min(ys),max(xs),max(ys)
            xmin,ymin,xmax,ymax = bbox
            w,h = xmax-xmin,ymax-ymin
            viewbox = '%s %s %s %s' % (xmin,ymin,w,h)
            #print country,obj.name,bbox,viewbox
            icon = '<svg height="60px" width="80px" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet"><path d="{path}" /></svg>'.format(path=svg, viewbox=viewbox)
        else:
            icon = '<img src="/static/globe.png" style="height:60px; opacity:0.2">'
        url = "/contribute/view/%s" % urlquote(rowdict["country"])
        linkimg = '<a href="%s">%s</a>' % (url,icon)
        row = [linkimg, rowdict['country'], rowdict['entries'], rowdict['discussions'], rowdict['issues'], '%s &rarr; %s' % (rowdict['mindate'],rowdict['maxdate'])]
        lists.append((None,row))
        
    countriestable = lists2table(request, lists=lists,
                                  fields=["","Country","Changes","Discussions","Issues","Years"])
    content = """
                {countriestable}
                <br><div width="100%" style="text-align:center"><a href="/contribute/add/" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                """.format(countriestable=countriestable)
    grids.append(dict(title="Countries:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))

    # milestones
    milestones = Milestone.objects.filter(country='', status="Active")
    def iter_milestones():
        for m in milestones:
            # calculate progress here
            milestoneform = MilestoneForm(instance=m)
            try:
                progress = milestoneform.get_progress()
                progresstext = '%.0f%%' % progress
            except:
                progress = 0
                progresstext = "NA"
            yield m,milestoneform,progress,progresstext

    fields = ["","title","progress"]
    lists = []
    for m,milestoneform,progress,progresstext in sorted(iter_milestones(), key=lambda (m,milestoneform,progress,progresstext): -progress):
        title = m.title
        progbar = '''
                    <div style="display:relative; text-display:center; width:70%; padding:0px; margin-left:15%; margin-top:10px; height:13px; border-style:solid; border-color:black; border-width:1px">
                        <span style="display:block; padding:0; margin:0; height:100%; width:{progress}%; color:white; background-color:rgb(255,108,72)">
                        </span>
                    </div>
                    '''.format(progress=int(progress), progresstext=progresstext)
        url = "/viewmilestone/%s" % m.pk
        icon = '<img src="/static/milestone.png" style="height:50px; opacity:0.2">'
        linkimg = '<a href="%s">%s</a>' % (url,icon)
        row = [linkimg, title, progbar] #progresstext]
        lists.append((None,row))
        
    milestonetable = lists2table(request, lists=lists,
                                  fields=fields,
                                 classname='milestonetable', color='rgb(255,108,72)')
    content = """
                {milestonetable}
                <br><div width="100%" style="text-align:center"><a href="/addmilestone/" style="text-align:center; background-color:rgb(255,108,72); color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                """.format(milestonetable=milestonetable)
    grids.append(dict(title="<br><hr>Milestones:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))

    # comments
    issues = Issue.objects.filter(country='', changeid=None, status="Active").order_by('-added')
    
    issuetable = issues2html(request, issues, 'rgb(27,138,204)')

    content = """
                <div style="margin-left:20px">{issuetable}</div>
                <br><div width="100%" style="text-align:center"><a href="/addissue" style="text-align:center; background-color:rgb(27,138,204); color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                """.format(issuetable=issuetable)

    grids.append(dict(title="<br><hr>General Discussion:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":'<h2 style="padding-top:10px">'+bannertitle+'</h2>',
                                                           #'custombanner':custombanner,
                                                           "bannerleft":bannerleft, "bannerright":bannerright,
                                                           }
                  )

def contribute_regions(request):
    bannertitle = "Contribute"

    mapp = """
	<script src="http://openlayers.org/api/2.13/OpenLayers.js"></script>

            <div style="width:98%; height:400px; margins:auto; border-radius:10px; background-color:rgb(0,162,232);" id="map">
            </div>
	
	<script defer="defer">
	var map = new OpenLayers.Map('map', {allOverlays: true,
                                            fractionalZoom: true,
                                            //resolutions: [0.5,0.6,0.7,0.8,0.9,1],
                                            controls: [],
                                            });
	</script>

        <script>
	// empty country layer
	var style = new OpenLayers.Style({fillColor:"rgb(200,200,200)", strokeWidth:0.5, strokeColor:'black',
                                          label:""}, //${getLabel}", labelAlign:"cm"},
                                          {context: {getLabel: function(feature) {
                                                                                return feature.attributes.region.toUpperCase();
                                                                                }
                                                     }
                                            }
					);
	var countryLayer = new OpenLayers.Layer.Vector("Provinces", {styleMap:style});
	map.addLayers([countryLayer]);

	onlybigbbox = function(f) {
            var bbox = 0;
            for (g of f.geometry.components) {
                area = g.getArea();
                if (area > 30 | (f.attributes.region == 'Central America' & area > 2)) {
                    _box = g.getBounds();
                    if (bbox == 0) {
                        bbox = _box;
                    } else {
                        bbox.extend(_box);
                    }
                }
            }
            return bbox;
	};

        rendercountries = function(data) {
		var geojson_format = new OpenLayers.Format.GeoJSON();
		var geoj_str = JSON.stringify(data);
		countries = geojson_format.read(geoj_str, "FeatureCollection");
		
		feats = [];
		for (feat of countries) {
                        feats.push(feat);                        
		};
		map.zoomToExtent([-170,70,180,-40]);
		countryLayer.addFeatures(feats);

                // add progress popups
                for (feat of countryLayer.features) {
                        //var pos = feat.geometry.getBounds().getCenterLonLat();
                        //var pos = onlybigbbox(feat).getCenterLonLat();
                        //pos.lat = pos.lat + 20
                        //pos.lon = pos.lon - 30
                        
                        if (feat.attributes.region == 'Oceania') {
                            var pos = new OpenLayers.LonLat(104,-33);
                        } else if (feat.attributes.region == 'Asia') {
                            var pos = new OpenLayers.LonLat(69, 67);
                        } else if (feat.attributes.region == 'Middle East') { 
                            var pos = new OpenLayers.LonLat(42,40); // //48,38
                        } else if (feat.attributes.region == 'Africa') {
                            var pos = new OpenLayers.LonLat(10, 15);
                        } else if (feat.attributes.region == 'Europe') {
                            var pos = new OpenLayers.LonLat(-10, 85);
                        } else if (feat.attributes.region == 'South America') {
                            var pos = new OpenLayers.LonLat(-54, -30);
                        } else if (feat.attributes.region == 'Central America') {
                            var pos = new OpenLayers.LonLat(-152, 16);
                        } else if (feat.attributes.region == 'North America') {
                            var pos = new OpenLayers.LonLat(-130, 70);
                        };
                        var content = '<h3 style="padding:0; margin:0; color:black">'+feat.attributes.region+'</h3>'
                        content = content + '<div style="display:relative; text-display:center; width:100px; padding:0px; margin-left:5%; margin-top:10px; height:13px; border-style:solid; border-color:black; border-width:1px; background-color:rgb(145,145,145)">'
                        content = content + '<span id="map_progbar_'     +feat.attributes.region.replace(' ','_')+     '" style="display:block; padding:0; margin:0; height:100%; width:0%; color:white; background-color:orange">'
                        content = content + '</span></div>'
                        var popup = new OpenLayers.Popup(null,
                                           pos,
                                           new OpenLayers.Size(150,50),
                                           content,
                                           null);
                        popup.autoSize = true;
                        popup.backgroundColor = "none";

                        feat.popup = popup;
                        map.addPopup(popup);
                };

                updatemapbars();
	};

        // $.getJSON('https://gist.githubusercontent.com/hrbrmstr/91ea5cc9474286c72838/raw/59421ff9b268ff0929b051ddafafbeb94a4c1910/continents.json', {}, rendercountries);
        $.getJSON('/static/regions.geojson', {}, rendercountries);

        function selectfunc(feature) {
            var name = feature.attributes.region;
            window.location.href = "/contribute/regions/"+name;
        };
        function highlightfunc(feature) {
            //alert('hover');
            feature.style = {fillColor:"rgb(122,122,122)", strokeWidth:0.5, strokeColor:'black'}
            countryLayer.redraw();
        };
        function unhighlightfunc(feature) {
            //alert('unhover');
            feature.style = {fillColor:"rgb(200,200,200)", strokeWidth:0.5, strokeColor:'black'}
            countryLayer.redraw();
        };
        selectControl = new OpenLayers.Control.SelectFeature(countryLayer, {onSelect: selectfunc,
                                                                        callbacks: {over:highlightfunc,
                                                                                    out:unhighlightfunc}
                                                                        } );
        map.addControl(selectControl);
        selectControl.activate();       

        </script>
        """

    if request.user.is_authenticated():
        welcome = '<h3>Welcome, <a href="/account">{user}</a>!</h3>'.format(user=request.user.username)
        signuparea = ""

    else:
        welcome = '<h3>Welcome!</h3>'
        signuparea = """
                            <br>
                            <div style="text-align:center">
                            <a href="/registration" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Sign Up
                            </a>
                            or
                            <a href="/login" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Login
                            </a>
                            </div>
                            """

##                <p>
##                Contributing to Pshapes is both easy and fast: just register and
##                contribute as little or as much as possible. You can add changes, quality check,
##                vouch or edit the work of others, raise issues, or discuss difficult cases. 
##                </p>

    custombanner = """
                    <style>
                        .blackbackground a { color:white }
                        .blackbackground a:visited { color:grey }
                    </style>
                    """

    custombanner += """
                    <br>
                    <div class="blackbackground" style="width:95%">
                        <h2 style="display: none; text-align:center">Choose one of the regions to begin</h2>
                        <h2 style="text-align:center">Contributions</h2>
                        <div style="display:none; text-align:center">{welcome}</div>
                        <div style="text-align:center">
                            {mapp}
                        </div>
                    </div>
                    <div class="blackbackground" style="width:95%; vertical-align:top">

                            <br>
                            {signuparea}
                            <br>

                            <br>
                    
                            <div style="display:none; text-align:left; padding-left:8%">
                                    
                                    <div>
                                    <img src="/static/milestone.png" height="40px" style="display:inline-block; filter:invert(100%)">
                                    <h4 style="display:inline-block">
                                    Help reach a new milestone. Join existing efforts to improve the data. 
                                    </h4>
                                    </div>

                                    <div>
                                    <img src="/static/issue.png" height="40px" style="display:inline-block; filter:invert(100%)">
                                    <h4 style="display:inline-block">
                                    Quality check the work of others. You may raise issues, vouch, or edit the data.
                                    </h4>
                                    </div>

                                    <div>
                                    <img src="/static/comment.png" height="40px" style="display:inline-block; filter:invert(100%)">
                                    <h4 style="display:inline-block">
                                    Participate in discussions about the history and evolution of provinces. 
                                    </h4>
                                    </div>

                                    <div>
                                    <img src="/static/info.png" height="40px" style="display:inline-block; filter:invert(100%)">
                                    <h4 style="display:inline-block">
                                    Still new? Read <a href="/about/tutorial">the tutorial</a> for more on how it works.
                                    </h4>
                                    </div>

                            </div>

                    </div>
                    
                    """.format(bannertitle=bannertitle, welcome=welcome, signuparea=signuparea, mapp=mapp)
        

    
    grids = []


    # regions
    def iter_regions():
        countrypairs = ProvChange.objects.filter(status__in=['Active','Pending']).distinct('fromcountry','tocountry').values('fromcountry','tocountry')
        coded = set((c['fromcountry'] for c in countrypairs)) | set((c['tocountry'] for c in countrypairs))
        for reg,regcountries in regions.items():
            regcountries = regcountries.split('|')
            # calculate progress here
            regcoded = [c for c in coded if c in regcountries]
            progress = len(regcoded) / float(len(regcountries)) * 100
            yield reg, progress

    updatemapbars = ''
    color = 'orange' #'rgb(255,108,72)'
    fields = ["","region","progress"]
    lists = []
    #for m,milestoneform,progress,progresstext in sorted(iter_milestones(), key=lambda (m,milestoneform,progress,progresstext): -progress):
    for reg,progress in sorted(iter_regions(), key=lambda tup: tup[0]):
        # make table elements
        progbar = '''
                    <div style="display:relative; text-display:center; width:70%; padding:0px; margin-left:15%; margin-top:10px; height:13px; border-style:solid; border-color:black; border-width:1px">
                        <span style="display:block; padding:0; margin:0; height:100%; width:{progress}%; color:white; background-color:{color}">
                        </span>
                    </div>
                    '''.format(progress=int(progress), color=color)
        url = "/contribute/regions/%s" % reg
        icon = '<img src="/static/globe.png" style="height:50px; opacity:0.2">'
        linkimg = '<a href="%s">%s</a>' % (url,icon)
        row = [linkimg, reg, progbar] #progresstext]
        # also make js to update progbars on map
        updatemapbars += '''
                        //// {region}
                        mapbar = document.getElementById('map_progbar_{region}');
                        mapbar.style.width = '{progress}%';
                        '''.format(region=reg.replace(' ','_'), progress=progress)
        lists.append((None,row))

    updatemapbars = """<script>
                        updatemapbars = function() {
                            %s
                        };
                        </script>
                    """ % updatemapbars
        
##    regionstable = lists2table(request, lists=lists,
##                                  fields=fields,
##                                 )
##    content = """
##                <div style="margin-left:21px">{regionstable}</div>
##                """.format(regionstable=regionstable)
##    print updatemapbars
##    content += updatemapbars
##    grids.append(dict(title='''<img src="/static/globe.png" height="55px" style="display:inline-block; margin-left:0; padding-left:0">
##                                Choose one of the regions to begin:''',
##                      content=content,
##                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="99%",
##                      ))

    # map link
    content = """
                <div style="height:220px">
                <b>
                <a href="/contribute/maps/" style="color:black">
                    <img style="width:100%; max-height:80%" border="2" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfcsofKnVvMiG0mN7BKmmGlGfM_16ANpxoDMT4MjufR40Ya-ZdfQ">
                </a>
                
                <p>
                Add useful maps to the map collection. 
                </p>
                </b>
                
                </div>
              """

    grids.append(dict(title='''<img src="/static/map.png" height="40px" style="display:inline-block">
                                Maps:''',
                      content=content,
                      style="background-color:orange; border-radius:0",
                      width="47%",
                      ))

    # discussions link
    content = """
                <div style="height:220px">
                <b>
                <a href="/contribute/issues/" style="color:black">
                    <img width="100%" border="2" src="https://blog.tradeshift.com/wp-content/uploads/2015/10/collaboration-illustration.jpg">
                </a>
                    
                <p>
                Join the conversation to help clear up how exactly a province may have changed. 
                </p>
                </b>
                
                </div>
              """

    grids.append(dict(title='''<img src="/static/comment.png" height="40px" style="display:inline-block">
                                Discussions:''',
                      content=content,
                      style="background-color:orange; border-radius:0",
                      width="47%",
                      ))

    # milestones
    milestones = Milestone.objects.filter(country='', status="Active")
    def iter_milestones():
        for m in milestones:
            # calculate progress here
            milestoneform = MilestoneForm(instance=m)
            try:
                progress = milestoneform.get_progress()
                progresstext = '%.0f%%' % progress
            except:
                progress = 0
                progresstext = "NA"
            yield m,milestoneform,progress,progresstext

    color = 'orange' #'rgb(58,177,73)' #'rgb(255,108,72)'
    fields = ["","title","progress"]
    lists = []
    for m,milestoneform,progress,progresstext in sorted(iter_milestones(), key=lambda (m,milestoneform,progress,progresstext): -progress):
        title = m.title
        progbar = '''
                    <div style="display:relative; text-display:center; width:70%; padding:0px; margin-left:15%; margin-top:10px; height:13px; border-style:solid; border-color:black; border-width:1px">
                        <span style="display:block; padding:0; margin:0; height:100%; width:{progress}%; color:white; background-color:{color}">
                        </span>
                    </div>
                    '''.format(progress=int(progress), progresstext=progresstext, color=color)
        url = "/viewmilestone/%s" % m.pk
        icon = '<img src="/static/milestone.png" style="height:50px; opacity:0.2">'
        linkimg = '<a href="%s">%s</a>' % (url,icon)
        row = [linkimg, title, progbar] #progresstext]
        lists.append((None,row))
        
    milestonetable = lists2table(request, lists=lists,
                                  fields=fields,
                                 classname='milestonetable', color=color)
    content = """
                <div style="margin-left:20px">{milestonetable}</div>
                <br><div width="100%" style="text-align:center"><a href="/addmilestone/" style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                """.format(milestonetable=milestonetable, color=color)
    
    grids.append(dict(title='''<br>
                                <img src="/static/milestone.png" height="40px" style="display:inline-block">
                                Milestones:''',
                      content=content, #'Join existing efforts to improve the data:'
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":'<h2 style="padding-top:10px">'+bannertitle+'</h2>',
                                                           'custombanner':custombanner,
                                                           #"bannerleft":bannerleft, "bannerright":bannerright,
                                                           }
                  )


def contribute_region(request, region):
    bannertitle = region

    mapp = """
        <script>
        var region = '%s'
        </script>
        """ % region
    mapp += """
	<script src="http://openlayers.org/api/2.13/OpenLayers.js"></script>

            <div style="width:98%; height:400px; margins:auto; border-radius:10px; background-color:rgb(0,162,232);" id="map">
            </div>
	
	<script defer="defer">
	var map = new OpenLayers.Map('map', {allOverlays: true,
                                            fractionalZoom: true,
                                            //resolutions: [0.5,0.6,0.7,0.8,0.9,1],
                                            controls: [],
                                            });
	</script>

        <script>
	// empty country layer
	var style = new OpenLayers.Style({fillColor:"rgb(200,200,200)", strokeWidth:0.5, strokeColor:'black',
                                          label:""}, //${getLabel}", labelAlign:"cm"},
                                          {context: {getLabel: function(feature) {
                                                                                return feature.attributes.region.toUpperCase();
                                                                                }
                                                     }
                                            }
					);
	var countryLayer = new OpenLayers.Layer.Vector("Provinces", {styleMap:style});
	map.addLayers([countryLayer]);

        function getMaxPoly(polys) {
              // https://stackoverflow.com/questions/37306548/how-to-show-one-label-per-multi-polygon-in-open-layers-3
              var polyObj = [];
              //now need to find which one is the greater and so label only this
              for (var b = 0; b < polys.length; b++) {
                polyObj.push({ poly: polys[b], area: polys[b].getArea() });
              };
              polyObj.sort(function (a, b) { return a.area - b.area });

              return polyObj[polyObj.length - 1].poly;
        }

	onlymainbbox = function(lyr) {
            var bbox = 0;
            for (f of lyr.features) {
                mpol = getMaxPoly(f.geometry.components);
                _box = mpol.getBounds();
                if (bbox == 0) {
                    bbox = _box;
                } else {
                    bbox.extend(_box);
                }
            }
            return bbox;
	};

	onlybigbbox = function(lyr) {
            var bbox = 0;
            for (f of lyr.features) {
                for (g of f.geometry.components) {
                    area = g.getArea();
                    if (area > 30 | (f.attributes.region == 'Central America' & area > 2)) {
                        _box = g.getBounds();
                        if (bbox == 0) {
                            bbox = _box;
                        } else {
                            bbox.extend(_box);
                        }
                    }
                }
            }
            return bbox;
	}

        rendercountries = function(data) {
		var geojson_format = new OpenLayers.Format.GeoJSON();
		var geoj_str = JSON.stringify(data);
		countries = geojson_format.read(geoj_str, "FeatureCollection");
		
		feats = [];
		for (feat of countries) {
                        if (feat.attributes.region == region) {
                            feats.push(feat);
                        }
		};
		countryLayer.addFeatures(feats);
		bounds = onlybigbbox(countryLayer);
		map.zoomToExtent(bounds);
		
		markcodedcountries(countryLayer);
	};

        $.getJSON('/static/countries_simple.geojson', {}, rendercountries);

        function selectfunc(feature) {
            var name = feature.attributes.country;
            window.location.href = "/contribute/view/"+name;
        };
        function highlightfunc(feature) {
            //alert('hover');
            feature.normstyle = feature.style
            feature.style = {fillColor:"rgb(122,122,122)", strokeWidth:2.5, strokeColor:'black'}
            countryLayer.redraw();
        };
        function unhighlightfunc(feature) {
            //alert('unhover');
            feature.style = feature.normstyle //{fillColor:"rgb(200,200,200)", strokeWidth:0.5, strokeColor:'black'}
            countryLayer.redraw();
        };
        selectControl = new OpenLayers.Control.SelectFeature(countryLayer, {onSelect: selectfunc,
                                                                        callbacks: {over:highlightfunc,
                                                                                    out:unhighlightfunc}
                                                                        } );
        map.addControl(selectControl);
        selectControl.activate();

        </script>
        """

##                <p>
##                Contributing to Pshapes is both easy and fast: just register and
##                contribute as little or as much as possible. You can add changes, quality check,
##                vouch or edit the work of others, raise issues, or discuss difficult cases. 
##                </p>

    custombanner = """
                    <style>
                        .blackbackground a { color:white }
                        .blackbackground a:visited { color:grey }
                    </style>
                    """
    custombanner += """
                    <br>
                    
                    <div>
                    <a href="/contribute/regions/" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                    Back to World
                    </a>
                    </div>
                    
                    <div class="blackbackground" style="width:95%">
                        <h2 style="text-align:center">{bannertitle}</h2>
                        <div style="text-align:center">
                            {mapp}
                        </div>
                    </div>
                    
                    <div class="blackbackground" style="width:95%; vertical-align:top">
                    </div>

                    <br><br>
                    
                    """.format(bannertitle=bannertitle, mapp=mapp)
        

    
    grids = []

    # countries

    from django.db.models import Count,Max,Min

    regcountries = regions[region].split('|')

    # already coded
    fields = ["country","entries","issues","discussions","mindate","maxdate"]
    lists = []
    rowdicts = dict([(countryid,dict(country=countryid,entries=0,mindate="-",maxdate="-")) for countryid in regcountries])
    for rowdict in ProvChange.objects.filter(fromcountry__in=regcountries).values("fromcountry").exclude(status="NonActive").annotate(entries=Count('pk'),
                                                                                                 mindate=Min("date"),
                                                                                                 maxdate=Max("date")):
        rowdict["country"] = rowdict.pop("fromcountry")
        rowdicts[rowdict["country"]] = rowdict
    for rowdict in ProvChange.objects.filter(tocountry__in=regcountries).values("tocountry").exclude(status="NonActive").annotate(entries=Count('pk'),
                                                                                                 mindate=Min("date"),
                                                                                                 maxdate=Max("date")):
        rowdict["country"] = rowdict.pop("tocountry")
        if rowdict["country"] in rowdicts:
            cur = rowdicts[rowdict["country"]]
            cur["entries"] = max(cur["entries"],rowdict["entries"]) # NOTE: by overwriting here, we are only keeping counts of tocountry (if we plus then we basically double the count)
            cur["mindate"] = min(cur["mindate"], rowdict["mindate"]) if cur["mindate"] != "-" else rowdict["mindate"]
            cur["maxdate"] = min(cur["maxdate"], rowdict["maxdate"]) if cur["maxdate"] != "-" else rowdict["maxdate"]
        else:
            rowdicts[rowdict["country"]] = rowdict

    for country in sorted(rowdicts.keys()):
        if not country: continue
        rowdict = rowdicts[country]
        rowdict['mindate'] = rowdict['mindate'].year if rowdict["mindate"] != "-" else rowdict["mindate"]
        rowdict['maxdate'] = rowdict['maxdate'].year if rowdict["maxdate"] != "-" else rowdict["maxdate"]
        rowdict['discussions'] = Issue.objects.filter(country=country, changeid=None, status="Active").count()
        rowdict['issues'] = Issue.objects.filter(country=country, changeid__isnull=False, status="Active").count()
        rowdict['url'] = "/contribute/view/%s" % urlquote(rowdict["country"])

        cntr = CntrShape.objects.raw('''SELECT 1 AS id, ST_AsSVG(geom) as svg, name, geom
                                        FROM provshapes_cntrshape
                                        WHERE simplify=0.2 AND name='%s'
                                        ''' % country)
        obj = next(iter(cntr), None)
        if obj:
            # TODO: not very effective since we parse and calculate bbox from the SVG string, because the coordinates in ST_AsSVG() are not the same as the real coords and bbox
            svg = obj.svg
            multis = svg.replace(' Z', '').split('M ')
            flat = [float(v) for mult in multis for v in mult.replace('L ','').strip().split()]
            xs,ys = flat[0::2],flat[1::2]
            bbox = min(xs),min(ys),max(xs),max(ys)
            xmin,ymin,xmax,ymax = bbox
            w,h = xmax-xmin,ymax-ymin
            viewbox = '%s %s %s %s' % (xmin,ymin,w,h)
            #print country,obj.name,bbox,viewbox
            icon = '<svg height="60px" width="80px" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet"><path d="{path}" /></svg>'.format(path=svg, viewbox=viewbox)
        else:
            icon = '<img src="/static/globe.png" style="height:60px; opacity:0.2">'
        url = "/contribute/view/%s" % urlquote(rowdict["country"])
        linkimg = '<a href="%s">%s</a>' % (url,icon)
        row = [linkimg, rowdict['country'], rowdict['entries'], rowdict['discussions'], rowdict['issues'], '%s &rarr; %s' % (rowdict['mindate'],rowdict['maxdate'])]
        lists.append((None,row))
        
    countriestable = lists2table(request, lists=lists,
                                  fields=["","Country","Changes","Discussions","Issues","Years"])
    
    content = """
                {countriestable}
                <br><div width="100%" style="text-align:center"><a href="/contribute/add/" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                """.format(countriestable=countriestable)

    # also color in map
    coded = [k for k,d in rowdicts.items() if d['entries']]
    content += """
                <script>
                markcodedcountries = function(lyr) {
                    for (feat of lyr.features) {
                        if ( %s.indexOf(feat.attributes.country) >= 0 ) {
                            feat.style = {fillColor:"rgb(145,145,145)", strokeWidth:0.5, strokeColor:'black'};
                            lyr.drawFeature(feat);
                        }
                    }
                }
                </script>
                """ % coded
    
    grids.append(dict(title="Countries:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))

    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":'<h2 style="padding-top:10px">'+bannertitle+'</h2>',
                                                           'custombanner':custombanner,
                                                           #"bannerleft":bannerleft, "bannerright":bannerright,
                                                           }
                  )

def viewcountry(request, country):

    def getdateeventstable(date):
        changes = (ProvChange.objects.filter(fromcountry=country, date=date).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country, date=date).exclude(status="NonActive")).order_by("-added") # the dash reverses the order
        import itertools
        
        def typeprov(obj):
            typ = obj.type
            if typ in "MergeNew TransferNew":
                prov = obj.toname
                return prov,"Form",obj.fromcountry,obj.tocountry
            elif typ in "MergeExisting TransferExisting FullTransfer PartTransfer":
                prov = obj.toname
                return prov,"Expand",obj.fromcountry,obj.tocountry
            elif typ == "Breakaway":
                prov = obj.toname
                return prov,"Breakaway",obj.fromcountry,obj.tocountry
            elif typ == "SplitPart":
                prov = obj.fromname
                return prov,"Split",obj.fromcountry,obj.tocountry
            elif typ == "NewInfo":
                prov = obj.fromname
                return prov,typ,obj.fromcountry,obj.tocountry
            elif typ == "Begin":
                prov = obj.toname
                return prov,typ,obj.fromcountry,obj.tocountry
        def events():
            dategroup = list(changes)
            subkey = typeprov
            for typprov,subevents in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
                yield (date,typprov),subevents

        events = events()
        
        def getlinkrow(date,prov,typ,fromcountry,tocountry,items):
            items = list(items)
            firstitem = items[0]
            # link should point to country that was different, if any
            if fromcountry and fromcountry == country:
                linkcountry = fromcountry
            elif tocountry and tocountry == country:
                linkcountry = tocountry
            else:
                linkcountry = country
                
            if typ == "NewInfo":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type=NewInfo'
                img = 'webnewinfo.png'
                prov = markcountrychange(country, firstitem.fromname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Breakaway":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(firstitem.fromname)) + params + '&type=Breakaway'
                img = 'webbreakaway.png'
                prov = markcountrychange(country, firstitem.toname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Split":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type=Split'
                img = 'websplit.png'
                prov = markcountrychange(country, firstitem.fromname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Form":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","toname","toalterns","totype","tohasc","toiso","tofips","tocapital","tocapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type=Form'
                img = 'webform.png'
                prov = markcountrychange(country, firstitem.toname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Expand":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","toname","toalterns","totype","tohasc","toiso","tofips","tocapital","tocapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type=Expand'
                img = 'webexpand.png'
                prov = markcountrychange(country, firstitem.toname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Begin":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","toname","toalterns","totype","tohasc","toiso","tofips","tocapital","tocapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type=Begin'
                img = 'webbegin.png'
                prov = markcountrychange(country, firstitem.toname, [firstitem.fromcountry,firstitem.tocountry])

            changeids = [c.changeid for c in items]

            issues = Issue.objects.filter(changeid__in=changeids, status='Active').count()
            if issues:
                issueitem = '''
                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">{issues}</a>
                            <img src="/static/issue.png" height=25px/>
                            </div>
                            '''.format(issues=issues)
            else:
                issueitem = '<a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">0</a>'
            
            vouches=len(list(Vouch.objects.filter(changeid__in=changeids, status='Active')))
            if vouches:
                vouchitem = '''
                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                            <img src="/static/vouch.png" height=30px/>
                            </div>
                            '''.format(vouches=vouches)
            else:
                vouchitem = '<a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">0</a>'
            imglink = '<div style="width:50px; text-align:center"><a href="%s"><img height="30px" style="opacity:0.7" src="/static/%s"></a></div>' % (link,img)
            return None,(imglink,typ,prov,'<b>%s</b>'%len(items),vouchitem,issueitem)
        events = [getlinkrow(date,prov,typ,fromcountry,tocountry,items) for (date,(prov,typ,fromcountry,tocountry)),items in events]
        eventstable = lists2table(request, events, ["", "EventType", "Province", "Changes", "Vouches", "Issues"])

        content = eventstable
        
        return content

    if "date" in request.GET:
        raise Exception()

    else:
        bannertitle = "" #"Timeline for %s" % country.encode("utf8")
        top = """
                        <a href="/contribute/countries/" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Back to World
			</a>
			"""

        # GRIDS
        grids = []

        # dates            
        dates = [d["date"].isoformat() for d in (ProvChange.objects.filter(fromcountry=country).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country).exclude(status="NonActive")).order_by("date").values('date').distinct()]
        print dates

    ##    def getlinkrow(date):
    ##        link = "/contribute/view/{country}/?".format(country=urlquote(country)) + "date=" + date
    ##        return link, (date,)

    ##    daterows = [getlinkrow(date) for date in dates]
    ##    datestable = lists2table(request, daterows, ["Date"])

    ##    content = datestable

        content = '''<hr>
                    <h3 id="timeline">
                        <img src="/static/time.svg" height="40px">
                        Timeline:
                        <a style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:underline; margin:10px;" href="/contribute/add/{country}">New Date</a>
                    </h3>'''.format(country=urlquote(country))
        
        for date in dates:
            table = getdateeventstable(date)
            html = """
                    <div style="margin-left:2%">
                    <h4>
                        {date}
                    </h4>
                    {table}
                    <br><div width="100%" style="text-align:center"><a href="/contribute/add/{country}?date={date}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                    </div>
                    """.format(date=date, table=table.encode('utf8'), country=urlquote(country))
            content += html
            
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="95%",
                          ))

        # issues
        issues = Issue.objects.filter(country=country, changeid__isnull=False, status="Active")

        # discussions
        discussions = Issue.objects.filter(country=country, changeid=None, status="Active").order_by('-added')
        content = '<br><br><hr><h3 id="discussions"><img src="/static/comment.png" style="padding-right:5px" height="40px">Discussions:</h3>'
        content += '<div style="margin-left:2%%"> %s </div>' % issues2html(request, discussions, 'rgb(27,138,204)')
        content += '<br><div width="100%" style="text-align:center"><a href="/addissue?country={country}" style="text-align:center; background-color:rgb(27,138,204); color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>'.format(country=urlquote(country))
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="99%",
                          ))

        # maps
        color = 'rgb(58,177,73)'

        maps = list(get_country_maps(country))

        fields = ['', 'year', 'title', 'note', 'external link']
        lists = []
        for mapp in maps:
            wms = mapp.wms #"https://mapwarper.net/maps/wms/26754" #"https://mapwarper.net/maps/wms/19956"
            if wms:
                try:
                    wmslink = WMS_Helper(wms).image_url(height=50)
                    imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}"></a>'.format(pk=mapp.pk, wmslink=wmslink)
                except:
                    wmslink = "/static/map.png"
                    imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}" style="opacity:0.15"></a>'.format(pk=mapp.pk, wmslink=wmslink)
            else:
                wmslink = "/static/map.png"
                imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}" style="opacity:0.15"></a>'.format(pk=mapp.pk, wmslink=wmslink)
            urllink = '<a target="_blank" href="{url}">{urlshort}</a>'.format(url=mapp.url.encode('utf8'), urlshort=mapp.url.replace('http://','').replace('https://','').split('/')[0])
            row = [imglink, mapp.year, mapp.title, mapp.note, urllink]
            lists.append((None,row))

        table = lists2table(request, lists, fields, 'maptable', color)

        content = '''<br><br>
                    <hr>
                     <h3 id="maps">
                         <img src="/static/map.png" height="40px">
                         Maps:
                    </h3>
                    <div style="margin-left:2%">
                        {table}
                        <br><div width="100%" style="text-align:center"><a href="/addmap/?country={country}" style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                    </div>
                    '''.format(table=table.encode('utf8'), color=color, country=urlquote(country))
            
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="95%",
                          ))

        # sources
        color = "rgb(60,60,60)"

        sources = list(get_country_sources(country))

        fields = ['', 'title', 'note', 'external link']
        lists = []
        for source in sources:
            link = '/viewsource/{pk}/'.format(pk=source.pk)
            urllink = '<a target="_blank" href="{url}">{urlshort}</a>'.format(url=source.url.encode('utf8'), urlshort=source.url.replace('http://','').replace('https://','').split('/')[0])
            imglink = '<a href="{link}"><img height="45px" src="/static/source.png" style="opacity:0.25"></a>'.format(link=link)
            row = [imglink, source.title, source.note, urllink]
            lists.append((None,row))

        table = lists2table(request, lists, fields, 'sourcetable', color)

        content = '''<br><br>
                    <hr>
                     <h3 id="sources">
                         <img src="/static/source.png" height="40px">
                         Sources:
                    </h3>
                    <div style="margin-left:2%">
                        {table}
                        <br><div width="100%" style="text-align:center"><a href="/addsource/?country={country}" style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                    </div>
                    '''.format(table=table.encode('utf8'), color=color, country=urlquote(country))
            
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="95%",
                          ))

        # the country map

        mapdata = ProvShape.objects.filter(country=country)
        if mapdata:
            latest_date = mapdata.latest('end')
            countrymap = """
                <script src="http://openlayers.org/api/2.13/OpenLayers.js"></script>

                    <div style="width:90%%; height:40vh; margins:auto; border-radius:10px; background-color:rgb(0,162,232);" id="map">
                    </div>
                
                <script defer="defer">
                var map = new OpenLayers.Map('map', {allOverlays: true,
                                                    fractionalZoom: true,
                                                    //resolutions: [0.5,0.6,0.7,0.8,0.9,1],
                                                    controls: [],
                                                    });
                </script>

                <script>
                // empty country layer
                var style = new OpenLayers.Style({fillColor:"rgb(200,200,200)", strokeWidth:0.2, strokeColor:'white'},
                                                );
                var countryLayer = new OpenLayers.Layer.Vector("Provinces", {styleMap:style});
                map.addLayers([countryLayer]);
                
                // empty province layer
                var style = new OpenLayers.Style({fillColor:"rgb(122,122,122)", strokeWidth:0.1, strokeColor:'white'},
                                                );
                var provLayer = new OpenLayers.Layer.Vector("Provinces", {styleMap:style});
                map.addLayers([provLayer]);

                rendercountries = function(data) {
                        var geojson_format = new OpenLayers.Format.GeoJSON();
                        var geoj_str = JSON.stringify(data);
                        countries = geojson_format.read(geoj_str, "FeatureCollection");
                        
                        feats = [];
                        for (feat of countries) {
                                feats.push(feat);
                        };
                        countryLayer.addFeatures(feats);
                };

                $.getJSON('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json', {}, rendercountries);

                onlybigbbox = function(lyr) {
                    var bbox = 0;
                    totarea = 0
                    for (f of lyr.features) {
                        totarea += f.geometry.getArea();
                    };
                    for (f of lyr.features) {
                        for (g of f.geometry.components) {
                            area = g.getArea();
                            perc = area / totarea * 100
                            if (perc > 0.1) {
                                _box = g.getBounds();
                                if (bbox == 0) {
                                    bbox = _box;
                                } else {
                                    bbox.extend(_box);
                                }
                            }
                        }
                    }
                    return bbox;
                }

                renderprovs = function(data) {
                        var geojson_format = new OpenLayers.Format.GeoJSON();
                        var geoj_str = JSON.stringify(data);
                        allProvs = geojson_format.read(geoj_str, "FeatureCollection");
                        
                        dateFeats = [];
                        for (feat of allProvs) {
                                dateFeats.push(feat);
                        };
                        provLayer.addFeatures(dateFeats);
                        var bbox = onlybigbbox(provLayer);
                        map.zoomToExtent(bbox);
                        map.updateSize();
                };

                var latest = '%s'.split('-');
                $.getJSON('/api', {simplify:0.025, year:latest[0], month:latest[1], day:latest[2], country:'%s'}, renderprovs);
                
                </script>
                """ % (latest_date.end, country.encode("utf8"))
            
            left = """	
                            <h3 style="clear:both">{countrytext}</h3>
                            
                            <div style="text-align:center; margin-left:5%">

                            {countrymap}

                            </div>

                            <br>
                            <a href="/explore/?country={countrytext}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
                            Explore in Map View
                            </a>
                            
                            <br><br><br>
            """.format(countrytext=country.encode("utf8"), countrymap=countrymap)
            
        else:
            left = """	
                            <h3 style="clear:both">{countrytext}</h3>
                            
                            <div>

                            <p style="text-align:center; margin-left:10%; width:80%;">The historical boundaries for this country have not yet been reconstructed.
                            Just start adding events on the timeline below, and once they have been reviewed
                            and accepted by an administrator, you will see your changes visualized on a map here.</p>

                            </div>
            """.format(countrytext=country.encode("utf8"))


        right = """<br><br>
                        <div style="text-align:center; margin-left:5%">

                            <div style="width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#timeline" style="text-decoration:none; color:inherit">
                                <img style="filter:invert(100)" src="/static/time.svg" height="30px">
                                <h3 style="margin-left:20px; display:inline">{daterange}</h3>
                                </a>
                            </div>

                            <div style="width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#discussions" style="text-decoration:none; color:inherit">
                                <img style="filter:invert(100)" src="/static/comment.png" style="padding-right:5px" height="30px">
                                <h3 style="margin-left:20px; display:inline">{discussions} Discussions</h3>
                                </a>
                            </div>

                            <!-- COMMENTED OUT !!!!!!!!!!
                            <div style="width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#issues" style="text-decoration:none; color:inherit">
                                <img style="filter:invert(100)" src="/static/issue.png" style="padding-right:5px" height="30px">
                                <h3 style="margin-left:20px; display:inline">{issues} Issues</h3>
                                </a>
                            </div>
                            -->

                            <div style="width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#maps" style="text-decoration:none; color:inherit">
                                <img style="filter:invert(100)" src="/static/map.png" height="30px">
                                <h3 style="margin-left:20px; display:inline">{maps} Maps</h3>
                                </a>
                            </div>

                            <div style="width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#sources" style="text-decoration:none; color:inherit">
                                <img style="filter:invert(100)" src="/static/source.png" height="30px">
                                <h3 style="margin-left:20px; display:inline">{sources} Sources</h3>
                                </a>
                            </div>
                            
                        </div>

                <br><br>
                
                """.format(countrytext=country.encode("utf8"),
                           daterange='%s - %s' % (dates[0].split('-')[0],dates[-1].split('-')[0]) if dates else '-',
                           sources=len(sources),
                           maps=len(maps),
                           discussions=discussions.count(),
                           issues=issues.count(),
                           )

        custombanner = """

                        {top}
                        
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>
                        
                        <td style="width:48%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:top">
                        {left}
                        </td>
                        
                        <td style="width:48%; padding:1%; padding:0px; margin:0px; vertical-align:text-top;">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, right=right)
        
        return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"custombanner":custombanner}
                      )

def editcountry(request):
    pass

def addcountry(request):
    grids = []

    # new historical
    content = """
                <input id="customcountry" type="text" style="width:40%">
                <script>
                function getcountryval() {
                    return document.getElementById('customcountry').value;
                };
                </script>
                <a id="customcountrybutton" onclick="var countryval = getcountryval(); location.href='/contribute/view/' + countryval" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">
                Add
                </a>
                """
    grids.append(dict(title="Add a New Country",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    # remaining
    fromcountries = [vd['fromcountry'] for vd in ProvChange.objects.distinct('fromcountry').exclude(status="NonActive").values("fromcountry")]
    tocountries = [vd['tocountry'] for vd in ProvChange.objects.distinct('tocountry').exclude(status="NonActive").values("tocountry")]
    existing = set(fromcountries + tocountries)
    remaining = [cval for cval,clab in countries if cval not in existing]
    
    lists = []
    for country in sorted(remaining):
        url = '<a href="/contribute/view/%s">Add</a>' % urlquote(country)
        row = [url,country]
        lists.append((None,row))
    
    countriestable = lists2table(request, lists=lists,
                                  fields=["","Country"])
    content = countriestable
    grids.append(dict(title="",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))

    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,
                                                    "nomainbanner":True}
                      )















##################
# Event/date pages

# TODO: RENAME THESE TO 'event'

def viewprov(request, country, province):
    if all((k in request.GET for k in "date type".split())):
        # view event, ensure enough params
        return viewevent(request, country, province)

    else:
        raise Exception("You must set at least the date and type GET params to view an event")

def editprov(request, country, province):
    if all((k in request.GET for k in "date type".split())):
        # edit event, ensure enough params
        return editevent(request, country, province)

    else:
        raise Exception("You must set at least the date and type GET params to view an event")

def addprov(request, country, province=None):
    if len(request.GET) == 0:
        # add date
        return adddate(request, country)

    if len(request.GET) == 1 and "date" in request.GET:
        # add event, ensure enough params
        return addevent(request, country)

    else:
        # add individual change (preferably to existing event), ensure enough params are provided
        return addchange(request, country, province)

@login_required
def adddate(request, country):
    func = AddDateWizard.as_view(country=country)
    return func(request)

def viewevent(request, country, province, editmode=False):
    # TODO: add "edit-event" button in main banner
    # and "add-change" button down by the table
    assert all((param in request.GET for param in "date type".split()))
    #country = request.GET["country"].strip('"').strip("'").strip()
    y,m,d = map(int,request.GET["date"].strip('"').strip("'").strip().split("-"))
    date = datetime.date(year=y,month=m,day=d)
    prov = province #request.GET["prov"].strip('"').strip("'").strip()
    typ = request.GET["type"].strip('"').strip("'").strip()

##    if typ == "Split":
##        bannertitle = "{provtext} province split into new provinces on {date}".format(provtext=prov.encode("utf8"), date=date.strftime('%b %d, %Y'))
##    elif typ == "Expansion":
##        bannertitle = "{provtext} province received territory from existing provinces on {date}".format(provtext=prov.encode("utf8"), date=date.strftime('%b %d, %Y'))
##    elif typ == "NewInfo":
##        bannertitle = "{provtext} province changed some of its information on {date}".format(provtext=prov.encode("utf8"), date=date.strftime('%b %d, %Y'))
##    else:
##        raise Exception()
    
    #bannertitle = '<a href="/contribute/view/{country}" style="color:inherit">{countrytext}</a>, {provtext}:'.format(country=urlquote(country),countrytext=country.encode("utf8"),provtext=prov.encode("utf8"))
    bannertitle = ""
    grids = []

    if typ in 'Split Breakaway Form Expand':
        # edit buttons
        #editmode = False # testing only
        if not editmode:
            onbut = '<a href="/contribute/edit/{country}/{province}?{params}" style="text-align:center; background-color:gray; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">OFF</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode())

            grids.append(dict(title="Edit Multiple" + onbut,
                              content="",
                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                              width="99%",
                              ))
    
    print "TYPE",repr(typ)
    if typ == "NewInfo":
        fields = ["toname","type","status"]
        #changes = ProvChange.objects.filter(country=country,date=date,type="NewInfo",fromname=prov)
        if 'tocountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'], tocountry=request.GET['tocountry'], date=date, type="NewInfo", fromname=prov, bestversion=True).exclude(status="NonActive")
        else:
            # new event, so tocountry doesnt exist yet
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'], date=date, type="NewInfo", fromname=prov, bestversion=True).exclude(status="NonActive")
        change = next((c for c in changes.order_by("-added")), None)

        if change:
            oldinfo = '<li style="list-style:none">'+markcountrychange(country, change.fromname, change.fromcountry).encode("utf8")+"<br><br></li>"            
            if change.fromalterns != change.toalterns: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Altnerate names: '+change.fromalterns.encode("utf8")+"</li>"
            if change.fromiso != change.toiso: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.fromiso.encode("utf8")+"</li>"
            if change.fromfips != change.tofips: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.fromfips.encode("utf8")+"</li>"
            if change.fromhasc != change.tohasc: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.fromhasc.encode("utf8")+"</li>"
            if change.fromcapitalname != change.tocapitalname: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+change.fromcapitalname.encode("utf8")+"</li>"
            if change.fromcapital != change.tocapital: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+change.fromcapital.encode("utf8")+"</li>"
            if change.fromtype != change.totype: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+change.fromtype.encode("utf8")+"</li>"
            top = """<div style="position:relative">
                            <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to Country Overview
                            </a>

                            <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                    </div><br><br><br><br><br>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
            left = """
                            <div style="clear:both; text-align: left">
                            <h2 style="float:left">{oldinfo}</h2>
                            </div>
            """.format(oldinfo=oldinfo)

            mid = """
                    <h2><em>Changed info to:</em></h2>
                    """
        
            newinfo = '''<li style="font-size:smaller; list-style:none"> {provtext}<a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                        <div style="display:inline; border-radius:10px; ">
                        <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                        <img src="/static/vouch.png" height=30px style="filter:invert(100%)"/>
                        </div>

                        <div style="display:inline; border-radius:10px; ">
                        <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{issues}</a>
                        <img src="/static/issue.png" height=25px style="filter:invert(100%)"/>
                        </div>
				
                        <br><br></li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))), issues=len(list(Issue.objects.filter(changeid=change.changeid, status='Active'))))
            if change.fromalterns != change.toalterns: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+change.toalterns.encode("utf8")+"</li>"
            if change.fromiso != change.toiso: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.toiso.encode("utf8")+"</li>"
            if change.fromfips != change.tofips: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.tofips.encode("utf8")+"</li>"
            if change.fromhasc != change.tohasc: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.tohasc.encode("utf8")+"</li>"
            if change.fromcapitalname != change.tocapitalname: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+change.tocapitalname.encode("utf8")+"</li>"
            if change.fromcapital != change.tocapital: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+change.tocapital.encode("utf8")+"</li>"
            if change.fromtype != change.totype: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+change.totype.encode("utf8")+"</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{newinfo}</h2>
                            </div>  
            """.format(newinfo=newinfo)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:31%; padding:1%">
                            {left}
                            </td>

                            <td style="width:20%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:36%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)

##            pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            if pendingedits:
##                pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
##                                          fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##                grids.append(dict(title="Pending Edits",
##                                  content=pendingeditstable,
##                                  style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                                  width="99%",
##                                  ))
##
##            oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            if oldversions:
##                oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
##                                          fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##                grids.append(dict(title="Revision History",
##                                  content=oldversionstable,
##                                  style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                                  width="99%",
##                                  ))

        else:
            # newinfo event just added, so no change objects yet
            oldinfo = '<li style="list-style:none">'+markcountrychange(country, request.GET["fromname"], request.GET["fromcountry"]).encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+request.GET["fromalterns"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+request.GET["fromiso"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+request.GET["fromfips"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+request.GET["fromhasc"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+request.GET["fromcapitalname"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+request.GET["fromcapital"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+request.GET["fromtype"].encode("utf8")+"</li>"
            top = """<div style="position:relative">
                            <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to Country Overview
                            </a>

                            <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                    </div><br><br><br><br><br>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
            left = """
                            <div style="clear:both; text-align: left">
                            <h2 style="float:left">{oldinfo}</h2>
                            </div>
            """.format(oldinfo=oldinfo)
            mid = """
                    <h2><em>Changed info to:</em></h2>
                    """

            butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
            plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

            setinfobutton = '<li style="list-style:none">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + '<a style="{plusbutstyle}" href="/contribute/add/{country}/{province}?{params}">&nbsp;Set info&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{setinfobutton}</h2>
                            </div>  
            """.format(setinfobutton=setinfobutton)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:31%; padding:1%">
                            {left}
                            </td>

                            <td style="width:20%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:36%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)
        
    elif typ == "Split":
        fields = ["toname","type","status"]
        if 'tocountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'],tocountry=request.GET['tocountry'], date=date,type="SplitPart",fromname=prov).exclude(status="NonActive")
        else:
            # new event, so cant know the tocountry yet
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'],date=date,type="SplitPart",fromname=prov).exclude(status="NonActive")
        changes = changes.order_by("toname") 

        GET = request.GET.copy()
        GET["type"] = "NewInfo"
        newinfobut = '<a href="/contribute/view/{country}/{province}?{params}" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">Info</a>'.format(country=urlquote(country), province=urlquote(prov), params=GET.urlencode())

        top = """<div style="position:relative">
                        <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Back to Country Overview
                        </a>

                        <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                </div><br><br><br><br><br>
                        """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
        
        left = """
                        <div style="clear:both; text-align: left">
                        <h2 style="float:left">{provtext} {newinfobut}</h2>
                        </div>
        """.format(newinfobut=newinfobut, provtext=markcountrychange(country, changes[0].fromname, changes[0].fromcountry).encode("utf8") if changes else prov.encode("utf8"))

        mid = """
                <h2><em>Split into:</em></h2>
                """
        
        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'
        
        splitlist = "".join(('''<li style="padding:10px 0px; list-style:none">&rarr; {provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

				<div style="display:inline; border-radius:10px; ">
				<a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
				<img src="/static/vouch.png" height=30px style="filter:invert(100%)"/>
				</div>

                                <div style="display:inline; border-radius:10px; ">
                                <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{issues}</a>
                                <img src="/static/issue.png" height=25px style="filter:invert(100%)"/>
                                </div>
				
                                </li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))), issues=len(list(Issue.objects.filter(changeid=change.changeid, status='Active'))))
                                 for change in changes))
        splitlist += '<li style="padding:10px 0px; list-style:none">' + '&nbsp;&nbsp;&nbsp;<a style="{plusbutstyle}" href="/contribute/add/{country}/{province}?{params}">&nbsp;Add New&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
        right = """
                        <style>
                            #blackbackground a {{ color:white }}
                            #blackbackground a:visited {{ color:grey }}
                        </style>
                        
                        <div id="blackbackground">
                        <h2>{splitlist}</h2>
                        </div>  
        """.format(splitlist=splitlist)

        custombanner = """

                        {top}

                        <style>
                        td {{vertical-align:top}}
                        </style>
                        
                        <table width="99%" style="clear:both">
                        <tr>
                        
                        <td style="width:34%; padding:1%">
                        {left}
                        </td>

                        <td style="width:20%; padding:1%">
                        {mid}
                        </td>
                        
                        <td style="width:36%; padding:1%">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, mid=mid, right=right)

        # change forms
        if editmode:
            tables = []

            for obj in changes:

                viewbut = '<a href="/provchange/%s/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>' % obj.pk

                lists = [("",
                          [     SimpleTypeChangeForm(instance=obj).as_p(),
                               ToChangeNameForm(instance=obj).as_p(),
                               ToChangeCodesForm(instance=obj).as_p(),
                               ToChangeInfoForm(instance=obj).as_p(),
                                GeneralChangeForm(instance=obj).as_simple(),
                              ])
                          ]

                changestable = lists2table(request, lists,
                                          fields=["Type","Province","Codes","Info","General"])
                
                header = "<h3>{title}: {viewbut}</h3>".format(title=markcountrychange(country, obj.toname, obj.tocountry).encode("utf8"),
                                                                    viewbut=viewbut)
                tables.append((header,obj.pk,changestable))

    elif typ == "Breakaway":
        fields = ["toname","type","status"]
        if 'tocountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'],tocountry=request.GET['tocountry'], date=date,type="Breakaway",fromname=prov).exclude(status="NonActive")
        else:
            # new event, so cant know the tocountry yet
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'],date=date,type="Breakaway",fromname=prov).exclude(status="NonActive")
        changes = changes.order_by("toname") 

        GET = request.GET.copy()
        GET["type"] = "NewInfo"
        newinfobut = '<a href="/contribute/view/{country}/{province}?{params}" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">Info</a>'.format(country=urlquote(country), province=urlquote(prov), params=GET.urlencode())

        top = """<div style="position:relative">
                        <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Back to Country Overview
                        </a>

                        <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                </div><br><br><br><br><br>
                        """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
        
        left = """
                        <div style="clear:both; text-align: left">
                        <h2 style="float:left">{provtext} {newinfobut}</h2>
                        </div>
        """.format(newinfobut=newinfobut, provtext=markcountrychange(country, changes[0].fromname, changes[0].fromcountry).encode("utf8") if changes else prov.encode("utf8"))

        mid = """
                <h2><em>Broke off territory to:</em></h2>
                """
        
        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'
        
        splitlist = "".join(('''<li style="padding:10px 0px; list-style:none">&rarr; {provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

				<div style="display:inline; border-radius:10px; ">
				<a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
				<img src="/static/vouch.png" height=30px style="filter:invert(100%)"/>
				</div>

                                <div style="display:inline; border-radius:10px; ">
                                <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{issues}</a>
                                <img src="/static/issue.png" height=25px style="filter:invert(100%)"/>
                                </div>
				
                                </li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))), issues=len(list(Issue.objects.filter(changeid=change.changeid, status='Active'))))
                                 for change in changes))
        splitlist += '<li style="padding:10px 0px; list-style:none">' + '&nbsp;&nbsp;&nbsp;<a style="{plusbutstyle}" href="/contribute/add/{country}/{province}?{params}">&nbsp;Add New&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
        right = """
                        <style>
                            #blackbackground a {{ color:white }}
                            #blackbackground a:visited {{ color:grey }}
                        </style>
                        
                        <div id="blackbackground">
                        <h2>{splitlist}</h2>
                        </div>  
        """.format(splitlist=splitlist)

        custombanner = """

                        {top}

                        <style>
                        td {{vertical-align:top}}
                        </style>
                        
                        <table width="99%" style="clear:both">
                        <tr>
                        
                        <td style="width:34%; padding:1%">
                        {left}
                        </td>

                        <td style="width:20%; padding:1%">
                        {mid}
                        </td>
                        
                        <td style="width:36%; padding:1%">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, mid=mid, right=right)

        # change forms
        if editmode:
            tables = []

            for obj in changes:

                viewbut = '<a href="/provchange/%s/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>' % obj.pk

                lists = [("",
                          [     SimpleTypeChangeForm(instance=obj).as_p(),
                               ToChangeNameForm(instance=obj).as_p(),
                               ToChangeCodesForm(instance=obj).as_p(),
                               ToChangeInfoForm(instance=obj).as_p(),
                                GeneralChangeForm(instance=obj).as_simple(),
                              ])
                          ]

                changestable = lists2table(request, lists,
                                          fields=["Type","Province","Codes","Info","General"])
                
                header = "<h3>{title}: {viewbut}</h3>".format(title=markcountrychange(country, obj.toname, obj.tocountry).encode("utf8"),
                                                                    viewbut=viewbut)
                tables.append((header,obj.pk,changestable))

    elif typ == "Form":
        fields = ["fromname","type","status"]
        if 'fromcountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],fromcountry=request.GET['fromcountry'],date=date,type__in=["MergeNew","TransferNew"],toname=prov).exclude(status="NonActive")
        else:
            # new event, so fromcountry doesnt exist yet
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],date=date,type__in=["MergeNew","TransferNew"],toname=prov).exclude(status="NonActive")
        changes = changes.order_by("fromname") 

        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

        givelist = "".join(('''<li style="padding:10px 0px; list-style:none">{provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                            <img src="/static/vouch.png" height=30px style="filter:invert(100%)"/>
                            </div>

                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{issues}</a>
                            <img src="/static/issue.png" height=25px style="filter:invert(100%)"/>
                            </div>

                            &rarr;</li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.fromname, change.fromcountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))), issues=len(list(Issue.objects.filter(changeid=change.changeid, status='Active')))) for change in changes))
        givelist += '<li style="padding:10px 0px; list-style:none">' + '<a href="/contribute/add/{country}/{province}?{params}" style="{plusbutstyle}">&nbsp;Add New&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
        top = """<div style="position:relative">
                        <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Back to Country Overview
                        </a>

                        <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                </div><br><br><br><br><br>
                        """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
        
        left = """			
                        <style>
                            #blackbackground a {{ color:white }}
                            #blackbackground a:visited {{ color:grey }}
                        </style>
                        
                        <div style="clear:both; text-align:left">
                        <h2 id="blackbackground" style="float:left">{givelist}</h2>
                        </div>  
        """.format(givelist=givelist)
        mid = """
                <h2><em>Combined to form:</em></h2>
                """
        right = """
                        <div>
                        <h2>{provtext}</h2>
                        </div>
        """.format(provtext=markcountrychange(country, changes[0].toname, changes[0].tocountry).encode("utf8") if changes else prov.encode("utf8"))
        custombanner = """

                        {top}

                        <style>
                        td {{vertical-align:top}}
                        </style>
                        
                        <table width="99%" style="clear:both">
                        <tr>
                        
                        <td style="width:34%; padding:1%">
                        {left}
                        </td>

                        <td style="width:25%; padding:1%">
                        {mid}
                        </td>
                        
                        <td style="width:36%; padding:1%">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, mid=mid, right=right)

        # change forms
        if editmode:
            tables = []

            for obj in changes:

                viewbut = '<a href="/provchange/%s/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>' % obj.pk

                lists = [("",
                          [     SimpleTypeChangeForm(instance=obj).as_p(),
                               FromChangeForm(instance=obj).as_p(),
                               GeoChangeForm(instance=obj, country=obj.tocountry, province=obj.toname, date=obj.date).as_nogeo(),
                                GeneralChangeForm(instance=obj).as_simple(),
                              ])
                          ]

                changestable = lists2table(request, lists,
                                          fields=["Type","Province","Geo","General"])
                
                header = "<h3>{title}: {viewbut}</h3>".format(title=markcountrychange(country, obj.fromname, obj.fromcountry).encode("utf8"),
                                                                    viewbut=viewbut)
                tables.append((header,obj.pk,changestable))

    elif typ == "Expand":
        fields = ["fromname","type","status"]
        if 'fromcountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],fromcountry=request.GET['fromcountry'],date=date,type__in=["MergeExisting","TransferExisting","FullTransfer","PartTransfer"],toname=prov).exclude(status="NonActive")
        else:
            # new event, so fromcountry doesnt exist yet
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],date=date,type__in=["MergeExisting","TransferExisting","FullTransfer","PartTransfer"],toname=prov).exclude(status="NonActive")
        changes = changes.order_by("fromname") 

        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

        givelist = "".join(('''<li style="padding:10px 0px; list-style:none">{provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                            <img src="/static/vouch.png" height=30px style="filter:invert(100%)"/>
                            </div>

                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{issues}</a>
                            <img src="/static/issue.png" height=25px style="filter:invert(100%)"/>
                            </div>

                            &rarr;</li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.fromname, change.fromcountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))), issues=len(list(Issue.objects.filter(changeid=change.changeid, status='Active')))) for change in changes))
        givelist += '<li style="padding:10px 0px; list-style:none">' + '<a href="/contribute/add/{country}/{province}?{params}" style="{plusbutstyle}">&nbsp;Add New&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
        top = """<div style="position:relative">
                        <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Back to Country Overview
                        </a>

                        <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                </div><br><br><br><br><br>
                        """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
        
        left = """			
                        <style>
                            #blackbackground a {{ color:white }}
                            #blackbackground a:visited {{ color:grey }}
                        </style>
                        
                        <div style="clear:both; text-align:left">
                        <h2 id="blackbackground" style="float:left">{givelist}</h2>
                        </div>  
        """.format(givelist=givelist)
        mid = """
                <h2><em>Gave territory to:</em></h2>
                """
        right = """
                        <div>
                        <h2>{provtext}</h2>
                        </div>
        """.format(provtext=markcountrychange(country, changes[0].toname, changes[0].tocountry).encode("utf8") if changes else prov.encode("utf8"))
        custombanner = """

                        {top}

                        <style>
                        td {{vertical-align:top}}
                        </style>
                        
                        <table width="99%" style="clear:both">
                        <tr>
                        
                        <td style="width:34%; padding:1%">
                        {left}
                        </td>

                        <td style="width:25%; padding:1%">
                        {mid}
                        </td>
                        
                        <td style="width:36%; padding:1%">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, mid=mid, right=right)

        # change forms
        if editmode:
            tables = []

            for obj in changes:

                viewbut = '<a href="/provchange/%s/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>' % obj.pk

                lists = [("",
                          [     SimpleTypeChangeForm(instance=obj).as_p(),
                               FromChangeForm(instance=obj).as_p(),
                               GeoChangeForm(instance=obj, country=obj.tocountry, province=obj.toname, date=obj.date).as_nogeo(),
                                GeneralChangeForm(instance=obj).as_simple(),
                              ])
                          ]

                changestable = lists2table(request, lists,
                                          fields=["Type","Province","Geo","General"])
                
                header = "<h3>{title}: {viewbut}</h3>".format(title=markcountrychange(country, obj.fromname, obj.fromcountry).encode("utf8"),
                                                                    viewbut=viewbut)
                tables.append((header,obj.pk,changestable))

    elif typ == "Begin":
        fields = ["toname","type","status"]
        #changes = ProvChange.objects.filter(country=country,date=date,type="NewInfo",fromname=prov)
        if 'fromcountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'], fromcountry=request.GET['fromcountry'], date=date, type="Begin", toname=prov, bestversion=True).exclude(status="NonActive")
        else:
            # new event, so fromcountry doesnt exist yet
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'], date=date, type="Begin", toname=prov, bestversion=True).exclude(status="NonActive")
        change = next((c for c in changes.order_by("-added")), None)

        if change:
            top = """<div style="position:relative">
                            <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to Country Overview
                            </a>

                            <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                    </div><br><br><br><br><br>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
            
            left = """
                            <div style="clear:both; text-align: left">
                            
                            </div>
            """

            mid = """
                    <h2><em>Province was created:</em></h2>
                    """
        
            newinfo = '''<li style="font-size:smaller; list-style:none"> {provtext}<a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                        <div style="display:inline; border-radius:10px; ">
                        <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                        <img src="/static/vouch.png" height=30px style="filter:invert(100%)"/>
                        </div>

                        <div style="display:inline; border-radius:10px; ">
                        <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{issues}</a>
                        <img src="/static/issue.png" height=25px style="filter:invert(100%)"/>
                        </div>

                        <br><br></li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))), issues=len(list(Issue.objects.filter(changeid=change.changeid, status='Active'))))
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+change.toalterns.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.toiso.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.tofips.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.tohasc.encode("utf8")+"</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{newinfo}</h2>
                            </div>  
            """.format(newinfo=newinfo)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:33%; padding:1%">
                            {left}
                            </td>

                            <td style="width:20%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:36%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)


##            pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
##                                      fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##            grids.append(dict(title="Pending Edits",
##                              content=pendingeditstable,
##                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                              width="99%",
##                              ))
##
##            oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
##                                      fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##            grids.append(dict(title="Revision History",
##                              content=oldversionstable,
##                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                              width="99%",
##                              ))

        else:
            # begin event just added, so no change objects yet
            top = """<div style="position:relative">
                            <a href="/contribute/view/{country}" style="z-index:100; position:absolute; left:0px; top:15px; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to Country Overview
                            </a>

                            <h2 style="position:absolute; width:90%; text-align:center; padding-top:15px; margin:15px;"><span style="font-size:large">{countrytext}</span><br>{date}</h2>

                    </div><br><br><br><br><br>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"), date=date.isoformat())
            
            left = """
                            <div style="clear:both; text-align: left">
                            
                            </div>
            """

            mid = """
                    <h2><em>Province was created:</em></h2>
                    """

            toname = request.GET['toname']
            tocountry = request.GET['tocountry']
            toalterns = request.GET.get('toaltern', '')
            toiso = request.GET.get('toiso', '')
            tofips = request.GET.get('tofips', '')
            tohasc = request.GET.get('tohasc', '')
        
            newinfo = '''<li style="font-size:smaller; list-style:none"> {provtext}<a href="/contribute/add/{country}/{province}?{params}" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">Confirm</a>

                        <br><br></li>'''.format(provtext=markcountrychange(country, toname, tocountry).encode("utf8"),
                                                country=urlquote(country), province=urlquote(province), params=request.GET.urlencode())
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+toalterns.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+toiso.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+tofips.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+tohasc.encode("utf8")+"</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{newinfo}</h2>
                            </div>  
            """.format(newinfo=newinfo)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:33%; padding:1%">
                            {left}
                            </td>

                            <td style="width:20%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:36%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)









            
##            fieldnames = [f.name for f in ProvChange._meta.get_fields()]
##            formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
##            formfieldvalues["user"] = self.request.user.username
##            formfieldvalues["added"] = datetime.datetime.now()
##            formfieldvalues["bestversion"] = True
##            print formfieldvalues
##
##            eventvalues = dict(((k,v) for k,v in self.request.GET.items()))
##            print eventvalues
##
##            objvalues = dict(eventvalues)
##            objvalues.update(formfieldvalues)
##
##            # copy toinfo to frominfo
##            for fl in 'country name alterns iso fips hasc'.split():
##                objvalues['from'+fl] = objvalues.get('to'+fl)
##            
##            print 'final objvalues',objvalues
##            obj = ProvChange.objects.create(**objvalues)
##            obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions/edits
##            print obj
##            
##            obj.save()
##
##            prov = data["toname"]

    if editmode and typ in 'Split Breakaway Form Expand':
        templ = """
                    <form action="/contribute/edit/{{ country }}/{{ province }}/?{{ params }}" method="post">
                        {% csrf_token %}
                        <h4>
                            Edit Multiple
                            <a href="/contribute/view/{{ country }}/{{ province }}?{{ params }}" style="text-align:center; background-color:red; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">Cancel</a>
                            <input type="submit" value="Save" style="text-align:center; background-color:green; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">
                        </h4>
                        {% for h,pk,t in tables %}
                            <input type="hidden" name="pk" value={{ pk }}>
                            {{ h | safe }}
                            {{ t | safe }}
                        {% endfor %}
                    </form>
                    """

        changesform = Template(templ).render(RequestContext(request, {"tables":tables,
                                                             'country':urlquote(country), 'province':urlquote(prov), 'params':request.GET.urlencode(),
                                                             }))

        grids.append(dict(title="",
                          content=changesform,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="99%",
                          ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids, "custombanner":custombanner}
                  )


@login_required
def editevent(request, country, province):
    # batch editing multiple changes at once
    if request.method == "POST":
        # receive lists of values for each attribute incl pk, zip and loop over to change each
        modelfields = [f.name for f in ProvChange._meta.get_fields()]
        keys,vals = zip(*[(k,v) for k,v in request.POST.lists() if k in modelfields or k=='pk'])
        print keys
        print vals
        print '-----'
        rows = zip(*vals)
        
        with transaction.atomic():
            for row in zip(*vals):
                # QUITE MESSY, ADDS A NEW CHANGE SOMEHOW, LOOK AT EXISTING CODE...
                rowdict = dict(zip(keys,row))
                pk = rowdict.pop('pk')
                change = ProvChange.objects.get(pk=pk)

                formfieldvalues = dict(rowdict.items())
                print 'posted',formfieldvalues
                
                formfieldvalues["user"] = request.user.username
                formfieldvalues["added"] = datetime.datetime.now()
                formfieldvalues["status"] = "Pending"

                if request.user.username == change.user:
                    for c in ProvChange.objects.filter(changeid=change.changeid):
                        # all previous versions by same user become nonactive and nonbestversion
                        c.bestversion = False
                        c.status = "NonActive"
                        c.save()
                    formfieldvalues["bestversion"] = True

                formfieldvalues['transfer_map'] = get_object_or_404(Map, pk=int(formfieldvalues['transfer_map'])) if formfieldvalues.get('transfer_map') else None

                formfieldvalues.pop('sources',None) # deprecated
                formfieldvalues.pop('mapsources',None) # deprecated
                
                print formfieldvalues

                for k,v in formfieldvalues.items():
                    setattr(change, k, v)

                change.pk = None # nulling the pk will add a modified copy of the instance
                change.save()
                
                print change

        return viewevent(request, country, province)
        
    elif request.method == "GET":
        # make table into editable form
        return viewevent(request, country, province, editmode=True)

@login_required
def addevent(request, country):
    # wizard that lets you add the type of event
    # then from or to prov info, and maybe source (or maybe source should get listbox to choose from previous)
    # then requires inputting at least one breakaway for splitevents (self is added automatically), and at least one for expansion events, and only one for newinfo
    # after first change added, goto viewevent screen to potentially add more...
    func = AddEventWizard.as_view(country=country)
    return func(request)
    












#################
# Change pages

@login_required
def addchange(request, country, province):
    if request.GET["type"].lower().strip('"') == "split":
        func = AddSplitChangeWizard.as_view(country=country, province=province)
        print 888,func
    elif request.GET["type"].lower().strip('"') == "breakaway":
        func = AddBreakawayChangeWizard.as_view(country=country, province=province)
    elif request.GET["type"].lower().strip('"') == "form":
        func = AddFormChangeWizard.as_view(country=country, province=province)
    elif request.GET["type"].lower().strip('"') == "expand":
        func = AddExpandChangeWizard.as_view(country=country, province=province)
    elif request.GET["type"].lower().strip('"') == "newinfo":
        func = AddNewInfoChangeWizard.as_view(country=country, province=province)
    elif request.GET["type"].lower().strip('"') == "begin":
        # special handling, begin events dont require any further info
        # so just add immediately and redirect to same page
        objvalues = dict([(k,v) for k,v in request.GET.items()])
        objvalues["user"] = request.user.username
        objvalues["added"] = datetime.datetime.now()
        objvalues["bestversion"] = True
        print objvalues

        # copy toinfo to frominfo
        for fl in 'country name alterns iso fips hasc'.split():
            objvalues['from'+fl] = objvalues.get('to'+fl)

        sources = [get_object_or_404(Source, pk=int(pk)) for pk in objvalues.pop('sources').split(',') if pk]
        mapsources = [get_object_or_404(Map, pk=int(pk)) for pk in objvalues.pop('mapsources').split(',') if pk]
        print objvalues
        
        print 'final objvalues',objvalues
        obj = ProvChange.objects.create(**objvalues)
        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions/edits
        print obj
        
        obj.save()
        for s in sources:
            obj.sources.add(s)
        for m in mapsources:
            obj.mapsources.add(m)
        obj.save()

        fields = ["tocountry","date","source","sources","mapsources","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Begin&".format(country=urlquote(country), prov=urlquote(province)) + params

        return redirect(eventlink)
    
    return func(request)

def withdrawchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)
    if request.user.username == change.user or request.user.is_staff():
        change.status = "NonActive"
        change.save()

    return redirect("/provchange/{pk}/view/".format(pk=pk) )

def resubmitchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)
    if request.user.username == change.user or request.user.is_staff():
        change.status = "Pending"
        change.save()

    return redirect("/provchange/{pk}/view/".format(pk=pk) )

def viewchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if change.type in "NewInfo Breakaway SplitPart":
        conflicting = ProvChange.objects.filter(status__in="Active Pending".split(), fromcountry=change.fromcountry, tocountry=change.tocountry, date=change.date, type=change.type, fromname=change.fromname, toname=change.toname, bestversion=True).exclude(pk=change.pk)
        conflictingfields = ["date","type","fromname","fromcountry","toname","tocountry","user","added","status"]
    elif change.type in "MergeNew TransferNew MergeExisting TransferExisting Begin PartTransfer FullTransfer":
        # UNSURE: should we not match on same date here, bc begin should only happen once, so any duplicates on different dates are conflicting?
        # on other hand one should be able to say begin for specific provinces, so not necessarily true...
        conflicting = ProvChange.objects.filter(status__in="Active Pending".split(), fromcountry=change.fromcountry, tocountry=change.tocountry, date=change.date, type=change.type, fromname=change.fromname, toname=change.toname, bestversion=True).exclude(pk=change.pk)
        conflictingfields = ["date","type","fromname","fromcountry","toname","tocountry","user","added","status"]

    notes = []
    if not change.bestversion:
        note = """
                <div style="background-color:rgb(248,234,150); outline: black solid thick; padding:1%%; font-family: comic sans ms">
                <p style="font-size:large; font-weight:bold">Note:</p>
                <p style="font-size:medium; font-style:italic">
                There is a more recent version of this province change <a href="/provchange/%s/view/">here</a>.
                </p>
                </div>
                <br>
                """ % ProvChange.objects.get(changeid=change.changeid, bestversion=True).pk
        notes.append(note)
    if conflicting:
        # custom table
        html = """
                    <table class="conftable"> 
                    
                            <style>
                            table.conftable {
                                    border-collapse: collapse;
                                    width: 100%;
                            }

                            th.conftable, td.conftable {
                                    text-align: left;
                                    padding: 8px;
                            }

                            tr.conftable:nth-child(even){background-color: none}

                            tr.conftable:nth-child(odd){background-color: none}

                            th.conftable {
                                    background-color: black;
                                    color: white;
                            }
                            </style>
                    
                            <tr class="conftable">
                                    <th class="conftable"> 
                                    </th>

                                    {% for field in fields %}
                                        <th class="conftable">
                                            <b>{{ field }}</b>
                                        </th>
                                    {% endfor %}
                                        
                            </tr>
                            </a>

                            {% if changelist %}
                            
                                {% for pk,changerow in changelist %}
                                        <tr class="conftable">
                                                <td class="conftable">
                                                    <a href="{% url 'viewchange' pk=pk %}">View</a>
                                                </td>
                                                
                                                {% for value in changerow %}
                                                    <td class="conftable">{{ value }}</td>
                                                {% endfor %}
                                                
                                        </tr>
                                {% endfor %}

                            {% else %}

                                <tr class="conftable">
                                <td class="conftable"></td>
                                {% for _ in fields %}
                                    <td class="conftable"> - </td>
                                {% endfor %}
                                </tr>

                            {% endif %}
                                
                    </table>
                    """
        changelist = [(c.pk, [getattr(c,field) for field in conflictingfields]) for c in conflicting]
        conflictingtable = Template(html).render(Context({"request":request, "fields":conflictingfields, "changelist":changelist}))

        
        note = """
                <div style="background-color:rgb(248,234,150); outline: black solid thick; padding:1%%; font-family: comic sans ms">
                <p style="font-size:large; font-weight:bold">Note:</p>
                <p style="font-size:medium; font-style:italic">
                There seems to be conflicting versions of this change:
                </p>
                    %s
                </div>
                <br>
                """ % conflictingtable
        notes.append(note)

    if change.type == "Breakaway":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","tocountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Breakaway&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    elif change.type == "SplitPart":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","tocountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Split&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    elif change.type in "MergeExisting TransferExisting FullTransfer PartTransfer":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["tocountry","fromcountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Expand&".format(country=urlquote(change.tocountry), prov=urlquote(change.toname)) + params
    elif change.type in "MergeNew TransferNew":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["tocountry","fromcountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Form&".format(country=urlquote(change.tocountry), prov=urlquote(change.toname)) + params
    elif change.type == "NewInfo":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","tocountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=NewInfo&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    elif change.type == "Begin":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["tocountry","fromcountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Begin&".format(country=urlquote(change.tocountry), prov=urlquote(change.toname)) + params
    print 99999,change.type, change
    print 1111,eventlink

    pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
                              fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

    oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
                              fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

    vouches = list(Vouch.objects.filter(changeid=change.changeid, status='Active'))
    canvouch = request.user.username != change.user
    hasvouched = bool(vouches)




    obj = change
    country = obj.fromcountry
    if obj.fromcountry != obj.tocountry:
        tocountry = ' (%s)' % obj.tocountry
    else:
        tocountry = ''
    # override special for begin
    if obj.type == 'Begin':
        country = obj.tocountry
        tocountry = ''
    # texts
    if obj.type == 'NewInfo':
        changetext = "'%s' changed information to '%s'%s" % (obj.fromname,obj.toname,tocountry)
        #icon = 'webnewinfo.png'
    elif obj.type == 'Breakaway':
        changetext = "'%s'%s seceded from '%s'" % (obj.toname,tocountry,obj.fromname)
        #icon = 'webbreakaway.png'
    elif obj.type == 'SplitPart':
        changetext = "'%s'%s was created when '%s' split apart" % (obj.toname,tocountry,obj.fromname)
        #icon = 'websplitpart.png'
    elif obj.type == 'TransferNew':
        changetext = "'%s' transferred territory to form part of '%s'%s" % (obj.fromname,obj.toname,tocountry)
        #icon = 'webtransfernew.png'
    elif obj.type == 'MergeNew':
        changetext = "'%s' merged to form part of '%s'%s" % (obj.fromname,obj.toname,tocountry)
        #icon = 'webmergenew.png'
    elif obj.type == 'TransferExisting':
        changetext = "'%s' transferred territory to '%s'%s" % (obj.fromname,obj.toname,tocountry)
        #icon = 'webtransferexisting.png'
    elif obj.type == 'MergeExisting':
        changetext = "'%s' merged into '%s'%s" % (obj.fromname,obj.toname,tocountry)
        #icon = 'webmergeexisting.png'
    elif obj.type == 'Begin':
        changetext = "'%s' was created" % obj.toname
        #icon = 'webbegin.png'
    # OLD, to be deprecated
    elif obj.type == 'PartTransfer':
        changetext = "'%s' transferred territory to '%s'%s" % (obj.fromname,obj.toname,tocountry)
        #icon = 'webtransferexisting.png'
    elif obj.type == 'FullTransfer':
        changetext = "'%s' merged into '%s'%s" % (obj.fromname,obj.toname,tocountry)
        #icon = 'webmergeexisting.png'





    changetext = '%04d-%02d-%02d: ' % (change.date.year, change.date.month, change.date.day) + changetext
        




    

    args = {'pk': pk,
            'country':country.encode('utf8'),
            'summary':changetext.encode('utf8'),
            #'icon':icon,
            'notes': notes,
            'canvouch': canvouch,
            'hasvouched': hasvouched,
            'vouches': vouches,
            'eventlink': eventlink,
            'metachange': MetaChangeForm(instance=change),
            'typechange': TypeChangeForm(instance=change),
            'generalchange': GeneralChangeForm(instance=change),
##            'histomap': HistoMapForm(instance=change),
##            'georef': GeorefForm(instance=change),
            'fromchange': FromChangeForm(instance=change),
            'geochange': GeoChangeForm(instance=change, country=change.tocountry, province=change.toname, date=change.date),
            'tochange': ToChangeForm(instance=change),
            "pendingeditstable": pendingeditstable,
            "oldversionstable": oldversionstable,
            }
    
    for key,val in args.items():
        if hasattr(val,"fields"):
            for field in val.fields.values():
                field.widget.attrs['readonly'] = "readonly"

    # comments by topic
    issues = Issue.objects.filter(changeid=change.changeid, status="Active")
##    topics = []
##    for c in allcomments.distinct('title'):
##        title = c.title
##        print title
##        comments = allcomments.filter(title=title).order_by("added") # the dash reverses the order
##        fields = ["added","user","text","withdraw"]
##        rows = []
##        for c in comments:
##            rowdict = dict([(f,getattr(c, f, "")) for f in fields])
##            rowdict['added'] = rowdict['added'].strftime('%Y-%M-%d %H:%M')
##            if rowdict['user'] == request.user.username:
##                rowdict['withdraw'] = '''
##                                <div style="display:inline; border-radius:10px; ">
##                                <a href="/dropcomment/{pk}">
##                                <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/3058-200.png" height=30px/>
##                                </a>
##                                </div>
##                                    '''.format(pk=c.pk)
##            rows.append(rowdict)
##        addreplyobj = Comment(user=request.user.username, country=change.fromcountry, changeid=change.changeid,
##                                added=datetime.datetime.now(), title=title)
##        replyform = ReplyForm(instance=addreplyobj).as_p()
##        topics.append((title,rows,replyform))
##
##    print topics

    #topics = [(title,comm) for title,comm in sorted(topics.items(), key=lambda t,c: c[0]['added'])]
    args['topics'] = issues2html(request, issues, "rgb(27,138,204)")
    args['topics'] += '<br><div width="100%" style="text-align:center"><a href="/addissue?country={country}&changeid={changeid}" style="text-align:center; background-color:rgb(27,138,204); color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>'.format(country=urlquote(change.fromcountry), changeid=change.changeid)

    # try to emulate https://cloud.netlifyusercontent.com/assets/344dbf88-fdf9-42bb-adb4-46f01eedd629/b549e4a7-f9d9-4f64-b597-21c7d8f2a166/facebook-comments.png
    # user icon: "https://cdn4.iconfinder.com/data/icons/gray-user-management/512/rounded-512.png"


    

    

    # count of all comm
    args['issues'] = issues.count()
                
    html = render(request, 'provchanges/viewchange.html', args)
        
    return html

@login_required
def editchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if request.method == "POST":
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))

        # post requests are different, so multivalue entries must be gotten as list
        formfieldvalues["sources"] = request.POST.getlist('sources')
        formfieldvalues["mapsources"] = request.POST.getlist('mapsources')
        
        formfieldvalues["user"] = request.user.username
        formfieldvalues["added"] = datetime.datetime.now()
        formfieldvalues["status"] = "Pending"

        with transaction.atomic():

            if request.user.username == change.user:
                for c in ProvChange.objects.filter(changeid=change.changeid):
                    # all previous versions by same user become nonactive and nonbestversion
                    c.bestversion = False
                    c.status = "NonActive"
                    c.save()
                formfieldvalues["bestversion"] = True

    ##        sources = [get_object_or_404(Source, pk=int(pk)) for pk in formfieldvalues.pop('sources') if pk]
    ##        mapsources = [get_object_or_404(Map, pk=int(pk)) for pk in formfieldvalues.pop('mapsources') if pk]

            formfieldvalues['transfer_map'] = get_object_or_404(Map, pk=int(formfieldvalues['transfer_map'])) if formfieldvalues.get('transfer_map') else None
            
            print formfieldvalues
            #print sources, mapsources

            for k,v in formfieldvalues.items():
                setattr(change, k, v)

            if formfieldvalues['type'] in 'MergeNew MergeExisting TransferNew TransferExisting PartTransfer FullTransfer':
                geoform = GeoChangeForm(instance=change, data=formfieldvalues, country=change.tocountry, province=change.toname, date=change.date)
                geoform.is_valid()
                change.transfer_geom = geoform.clean()["transfer_geom"]
            
            change.pk = None # nulling the pk will add a modified copy of the instance
            change.save()
            
    ##        for s in sources:
    ##            change.sources.add(s)
    ##        for m in mapsources:
    ##            change.mapsources.add(m)
    ##        change.save()

        html = redirect("/provchange/%s/view/" % change.pk)
        
    elif request.method == "GET":
        args = {'pk': pk,
                'typechange': SimpleTypeChangeForm(instance=change),
                'generalchange': GeneralChangeForm(instance=change),
                'fromchange': FromChangeForm(instance=change),
##                'histomap': HistoMapForm(instance=change),
##                'georef': GeorefForm(instance=change),
                'geochange': GeoChangeForm(instance=change, country=change.tocountry, province=change.toname, date=change.date),
                'tochange': ToChangeForm(instance=change),}
        html = render(request, 'provchanges/editchange.html', args)
        
    return html
















########################### FORMS AND WIZARDS ##########################













#################################################
# Custom Widgets

from django.contrib.gis.forms.widgets import OpenLayersWidget

class ListTextWidget(forms.TextInput):
    # from http://stackoverflow.com/questions/24783275/django-form-with-choices-but-also-with-freetext-option
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class CustomDateWidget(forms.TextInput):

    ### WARNING: id_1-date is hacky for now, may not always work...
    
    def render(self, name, value, attrs = None):
        output = super(CustomDateWidget, self).render(name, value, attrs)
        output += """
<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>

<script>
$('#id_0-date').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: "yy-mm-dd",
    defaultDate: "2014-12-31",
    yearRange: '1946:2014',
    showOn: "both",
    buttonImage: 'http://jqueryui.com/resources/demos/datepicker/images/calendar.gif',
    buttonImageOnly: true,
});
$(".ui-datepicker-trigger").css("margin-bottom","-3px");
</script>
"""
        return output

class CustomOLWidget(OpenLayersWidget):
    default_zoom = 1

    #class Media:
        #extend = False
        #js = ("OpenLayers.js",)
    
    def render(self, name, value, attrs=None):
        #print self.Media.js, self.Media.
        output = super(CustomOLWidget, self).render(name, value, attrs=attrs)
        output += """
<script>
var jsmap = %s;
var selectedFeature;
var selectControl;

function syncwms() {
    var mapOverlayId = document.getElementById('id_transfer_map').value;
    var wmsurl = document.getElementById('id_transfer_map_wms_'+mapOverlayId).value;
    if (wmsurl.trim() != "") {
        var wmsurl = wmsurl.split("?")[0] + "?service=wms&format=image/png"; // trim away junk wms params and ensure uses transparency
        
        var layerlist = jsmap.map.getLayersByName('Historical Map');
        
        if (layerlist.length >= 1) 
            {
            // replace existing
            jsmap.map.removeLayer(layerlist[0]);
            };
            
        customwms = new OpenLayers.Layer.WMS("Historical Map", wmsurl, {layers: 'basic'} );
        customwms.isBaseLayer = false;
        jsmap.map.addLayer(customwms);
        jsmap.map.setLayerIndex(customwms, 1);

        // zoom to country bbox somehow
        //jsmap.map.zoomToExtent(customwms.getDataExtent());
    };
};

function setExistingClipFeatures(geoj) {
    var geojson_format = new OpenLayers.Format.GeoJSON();
    var features = geojson_format.read(geoj, "FeatureCollection");
    
    //vectors.addFeatures requires an array, thus
    if(features.constructor != Array) {
        features = [features];
    }
    existingClipLayer = jsmap.map.getLayersByName('Existing Clip Polygons')[0];
    existingClipLayer.addFeatures(features);
};

function onPopupClose(evt) {
    selectControl.unselect(selectedFeature);
};

function onFeatureSelect(feature) {
    selectedFeature = feature;
    popup = new OpenLayers.Popup.FramedCloud("featinfo", 
                             feature.geometry.getBounds().getCenterLonLat(),
                             null,
                             "<div style='font-size:.8em'>Feature: " + feature.id +"<br>Area: " + feature.geometry.getArea()+"</div>",
                             null, true, onPopupClose);
    feature.popup = popup;
    jsmap.map.addPopup(popup);
    return true;
};

function onFeatureUnselect(feature) {
    jsmap.map.removePopup(feature.popup);
    feature.popup.destroy();
    feature.popup = null;
};

function setupmap() {
    // layer switcher
    jsmap.map.addControl(new OpenLayers.Control.LayerSwitcher({'div':OpenLayers.Util.getElement('layerswitcher')}));
    jsmap.map.addControl(new OpenLayers.Control.MousePosition());

    // existing clips
    var existingClipLayer = new OpenLayers.Layer.Vector("Existing Clip Polygons", {style:{fillColor:"gray", fillOpacity:0.3}});
    jsmap.map.addLayers([existingClipLayer]);

    // enable popup for clips (currently only works if disabling the transfer_geom layer)
    //selectControl = new OpenLayers.Control.SelectFeature(existingClipLayer, {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
    //jsmap.map.addControl(selectControl);
    //selectControl.activate();

    // wms
    syncwms();
};

setupmap();

</script>
""" % self.attrs["jsmapname"]
        
        return output


class GeoChangeForm(forms.ModelForm):

    icon = "/static/globe.png"
    step_title = "Territory"
    step_descr = """
                    What did the giving province look like before giving away territory?
                   """

    class Meta:
        model = ProvChange
        fields = ["transfer_reference", "transfer_source", "transfer_map", "transfer_geom"]
        widgets = {"transfer_geom": CustomOLWidget(attrs={"id":"geodjango_transfer_geom"}),
                    "transfer_source": ListTextWidget([], name="sources", attrs={'style':'width:80%',"id":"id_transfer_source"}),
                    "transfer_reference": ListTextWidget([], name="references", attrs={'style':'width:80%',"id":"id_transfer_reference"}),
                   }
        
    def __init__(self, *args, **kwargs):
        self.inst = kwargs.get("instance")
        print "INST",self.inst
        self.country = kwargs.pop("country")
        self.province = kwargs.pop("province")
        self.date = kwargs.pop("date")
        print "kwargs",kwargs
        super(GeoChangeForm, self).__init__(*args, **kwargs)
        print 999, self.fields["transfer_geom"].widget

        # find other relates provs
        country = self.country
        province = self.province
        date = self.date
        otherfeats = ProvChange.objects.filter(fromcountry=country, toname=province, date=date).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country, toname=province, date=date).exclude(status="NonActive")
        if self.inst:
            otherfeats = otherfeats.exclude(pk=self.inst.pk)
        otherfeats = self.otherfeats = [f for f in otherfeats if f.transfer_geom] # only those with geoms

        print kwargs
        if "initial" in kwargs:
            country = kwargs["initial"]["country"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            sources = sorted((r.transfer_source for r in provs.distinct("transfer_source")))
            references = sorted((r.transfer_reference for r in provs.distinct("transfer_reference")))
            self.fields['transfer_source'].widget._list = sources
            self.fields['transfer_reference'].widget._list = references

        self.maps = maps = list(get_country_maps(country))
        choices = [(m.pk, "{yr} - {title}".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps]
        self.fields['transfer_map'].widget = forms.Select(choices=[('','')]+choices, attrs=dict(id="id_transfer_map", style='width:80%'))

        # make wms auto add/update on map change
        #self.fields['transfer_geom'].widget = EditableLayerField().widget
        print 888,kwargs
        jsmapname = "geodjango_transfer_geom" if kwargs.get("instance") else "geodjango_3_transfer_geom"
        self.fields['transfer_map'].widget.attrs.update({
##            "onload": "setupmap();",
##            'oninput': "".join(["alert(OpenLayers.objectName);","var wmsurl = document.getElementById('id_transfer_source').value;",
##                                "alert(wmsurl);",
##                                """var customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );""",
##                                #"""customwms.isBaseLayer = false;""",
##                                "alert(customwms.objectName);",
##                                """geodjango_transfer_geom.map.addLayer(customwms);""",
##                                ])
            "onchange": "syncwms();",
            })
        self.fields["transfer_geom"].widget.attrs["jsmapname"] = jsmapname
        
    def as_p(self):
        html = """
                        Before you begin:
                        <br><br>
                        To define the territory that changed you need a historical map that shows the giving province as it was prior to the change.
                        If you have not already done so, go ahead and <a href="/addmap/?country={{ country }}">register the map for this country now.</a> 

                        <div style="padding:20px">Map Overlay: {{ form.transfer_map }}</div>

                        <br>

                        <div>{{ form.transfer_geom }}</div>

                        <div style="clear:both">
                        <br>
                        Instructions:
                        <br>
                        {{ geoinstruct | safe }}

                        </div>
                        
                    """
        # add features
        import json
        geoj = {"type":"FeatureCollection",
                "features": [dict(type="Feature", properties=dict(fromname=f.fromname), geometry=json.loads(f.transfer_geom.json))
                             for f in self.otherfeats]}
        geoj_str = json.dumps(geoj).replace("'", "\\'") # if the any property names include a single apo, escape it so doesnt cancel the string quotes
        print geoj_str
        html += """<script>
                setExistingClipFeatures('{geoj}')
                </script>
                """.format(geoj=geoj_str)

        # add wms urls
        html += '<datalist id="id_datalist_map_wms">'
        for m in self.maps:
            html += '<option id="id_transfer_map_wms_{pk}" value="{wms}"></option>'.format(pk=m.pk, wms=m.wms)
        html += "</datalist>"

        html += "<script>syncwms();</script>"
        
        rendered = Template(html).render(Context({"form":self, 'geoinstruct':geoinstruct, 'country':urlquote(self.country)}))
        return rendered

    def as_simple(self):
        html = """
                        <div style="padding:20px">Map Overlay: {{ form.transfer_map }}</div>

                        <br>

                        <div>{{ form.transfer_geom }}</div>

                        <div style="clear:both">
                        <br>
                        Instructions:
                        <br>
                        {{ geoinstruct | safe }}
                        
                        </div>
                        
                    """
        # add features
        import json
        geoj = {"type":"FeatureCollection",
                "features": [dict(type="Feature", properties=dict(fromname=f.fromname), geometry=json.loads(f.transfer_geom.json))
                             for f in self.otherfeats]}
        geoj_str = json.dumps(geoj).replace("'", "\\'") # if the any property names include a single apo, escape it so doesnt cancel the string quotes
        print geoj_str
        html += """<script>
                setExistingClipFeatures('{geoj}')
                </script>
                """.format(geoj=geoj_str)

        # add wms urls
        html += '<datalist id="id_datalist_map_wms">'
        for m in self.maps:
            html += '<option id="id_transfer_map_wms_{pk}" value="{wms}"></option>'.format(pk=m.pk, wms=m.wms)
        html += "</datalist>"

        html += "<script>syncwms();</script>"
        
        rendered = Template(html).render(Context({"form":self, 'geoinstruct':geoinstruct}))
        return rendered

    def as_maponly(self):
        html = """
                        <div>{{ form.transfer_geom }}</div>

                        <div style="clear:both">                        
                    """
        # add features
        import json
        geoj = {"type":"FeatureCollection",
                "features": [dict(type="Feature", properties=dict(fromname=f.fromname), geometry=json.loads(f.transfer_geom.json))
                             for f in self.otherfeats]}
        geoj_str = json.dumps(geoj).replace("'", "\\'") # if the any property names include a single apo, escape it so doesnt cancel the string quotes
        print geoj_str
        html += """<script>
                setExistingClipFeatures('{geoj}')
                </script>
                """.format(geoj=geoj_str)

        # add wms urls
        html += '<datalist id="id_datalist_map_wms">'
        for m in self.maps:
            html += '<option id="id_transfer_map_wms_{pk}" value="{wms}"></option>'.format(pk=m.pk, wms=m.wms)
        html += "</datalist>"

        html += "<script>syncwms();</script>"
        
        rendered = Template(html).render(Context({"form":self, 'geoinstruct':geoinstruct}))
        return rendered

    def as_nogeo(self):
        html = """
                        <p>OLD (to be phased out)!</p>
                        <div style="padding:20px">WMS Map Link: {{ form.transfer_source }}</div>
                        <div style="padding:20px">Map Description: {{ form.transfer_reference }}</div>

                        <p>NEW!</p>
                        <div style="padding:20px">Map Overlay: {{ form.transfer_map }}</div>

                        <br>                        
                    """
        
        rendered = Template(html).render(Context({"form":self}))
        return rendered

    def as_nogeo_readonly(self):
        html = """
                        <p>OLD (to be phased out)!</p>
                        <div style="padding:20px">WMS Map Link: {{ form.transfer_source.value }}</div>
                        <div style="padding:20px">Map Description: {{ form.transfer_reference.value }}</div>

                        <p>NEW!</p>
                        <div style="padding:20px">Map Overlay: {{ form.transfer_map.value }}</div>

                        <br>                        
                    """
        
        rendered = Template(html).render(Context({"form":self}))
        return rendered

    def clean(self):
        cleaned_data = super(GeoChangeForm, self).clean()
        if cleaned_data and cleaned_data.get('transfer_map'):
            cleaned_data['transfer_map'] = get_object_or_404(Map, pk=int(cleaned_data['transfer_map'].pk))
        if cleaned_data and self.otherfeats:
            othergeoms = reduce(lambda res,val: res.union(val), (f.transfer_geom for f in self.otherfeats))
            diff = cleaned_data["transfer_geom"].difference(othergeoms)
            if diff.geom_type != "MultiPolygon":
                from django.contrib.gis.geos import MultiPolygon
                diff = MultiPolygon(diff)
            cleaned_data["transfer_geom"] = diff
        return cleaned_data












# Event forms

class SourceEventForm(forms.ModelForm):

    icon = "/static/info.png"
    step_title = "Source of Information"
    step_descr = """
                   Where are you getting the information from? 
                
                   """

    class Meta:
        model = ProvChange
        fields = ['source', 'sources', 'mapsources']
##        widgets = dict(sources=forms.CheckboxSelectMultiple(renderer=SelectMultipleOrCreate),
##                       mapsources=forms.CheckboxSelectMultiple(renderer=SelectMultipleOrCreate))

    def __init__(self, *args, **kwargs):
        super(SourceEventForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            country = kwargs["initial"]["fromcountry"]
        elif 'instance' in kwargs:
            country = kwargs["instance"].fromcountry
        else:
            raise Exception('Either initial or instance must be set')
        self.country = country

        # new
        sources = get_country_sources(country)
        self.suggested_sources = sorted([(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources])
        #self.fields["sources"].widget = GridSelectMultipleWidget(choices=[(s.pk, SourceForm(instance=s).as_griditem()) for s in sources])
        #self.fields["sources"].widget = forms.CheckboxSelectMultiple(choices=[(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources])
        
        maps = get_country_maps(country)
        self.suggested_mapsources = sorted([(m.pk, "{title} ({yr})".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps])
        #self.fields["mapsources"].widget = GridSelectMultipleWidget(choices=[(m.pk, MapForm(instance=m).as_griditem()) for m in maps])
        #self.fields["mapsources"].widget = forms.CheckboxSelectMultiple(choices=[(m.pk, "{yr} - {title}".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps])

        # old, to be phased out
        sources = [r.source for r in (ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)).annotate(count=Count('source')).order_by('-count')]
        if sources:
            mostcommon = sources[0]
            sources = sorted(set(sources))
            #self.fields["source"].widget = ListTextWidget(data_list=sources, name="sources", attrs=dict(type="text",size=120,autocomplete="on"))
            self.fields["source"].widget = forms.Textarea(attrs=dict(style='width:90%; font:inherit'))
            self.fields['source'].initial = mostcommon
        else:
            self.fields["source"].widget = forms.Textarea(attrs=dict(style='width:90%; font:inherit'))

    def clean(self):
        # store the sources and mapsources objects as pks
        cleaned_data = super(SourceEventForm, self).clean()
        cleaned_data['sources'] = ','.join([str(s.pk) for s in cleaned_data['sources']])
        cleaned_data['mapsources'] = ','.join([str(m.pk) for m in cleaned_data['mapsources']])
        return cleaned_data

    def as_p(self):
        html = """
                    <div style="margin-left:2%">

                        <p>Indicate the sources of information used to code this change (e.g. <em>'#source15'</em>).
                        <br>
                        This includes information that was inferred by visually comparing maps (e.g. <em>'deduced by comparing #map12 and #map9'</em>).
                        </p>
                        
                        <p>                        
                        If you have not already done so, go ahead and <a href="/addsource/?country={{ country }}">register the source(s) for this country now.</a> 
                        </p>

                        <div style="">
                        {{ form.source.label_tag }}
                        {{ form.source }}
                        </div>

                        <p>
					<div style="width:45%; margin-left:20px; display:inline-block"><em>Suggested Sources:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_sources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/source.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
					<div style="width:45%; display:inline-block"><em>Suggested Maps:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_mapsources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/map.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewmap/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
			</p>
                    </div>
                    """
        
        rendered = Template(html).render(Context({"form":self, 'country':urlquote(self.country)}))
        return rendered
        
from django.forms.widgets import RadioFieldRenderer

class TypeEventRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,EVENTTYPEINFO[w.choice_label]) for w in self]
        html = """
            <table class="myradio">
            {% for choice,extra in choices %}
            <tr>
                <td>{{ choice }}<td>
                <td>{{ extra.img|safe }}</td>
                <td>
                    <h4>{{ extra.short|safe }}</h4>
                    <p>{{ extra.descr|safe }}</p>
                </td>
            </tr>
            {% endfor %}
            </table>
            """
        rendered = Template(html).render(Context({"choices":choices }))
        return rendered

class TypeEventForm(forms.Form):

    icon = "/static/typechange.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of event was it? 
                   """
    type = forms.ChoiceField(choices=[("NewInfo","NewInfo"),("Breakaway","Breakaway"),("Split","Split"),("Expand","Expand"),("Form","Form"),("Begin","Begin")], widget=forms.RadioSelect(renderer=TypeEventRenderer))

##    class Meta:
##        widgets = {"type": forms.RadioSelect(renderer=TypeEventRenderer) }

class FromEventForm(forms.ModelForm):

    icon = "/static/fromicon.png"
    step_title = "From Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'fromcountry fromname fromalterns fromiso fromfips fromhasc fromcapitalname fromcapital fromtype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(FromEventForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["fromcountry"].widget = ListTextWidget(data_list=countrylist, name="fromcountrylist")
        
        country = kwargs["initial"]["fromcountry"]
        provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
        provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
        provlist = sorted(provlist)
        self.fields["fromname"].widget = ListTextWidget(data_list=provlist, name="fromprovlist")

class ToEventForm(forms.ModelForm):

    icon = "/static/toicon.png"
    step_title = "To Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'tocountry toname toalterns toiso tofips tohasc tocapitalname tocapital totype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(ToEventForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["tocountry"].widget = ListTextWidget(data_list=countrylist, name="tocountrylist")
        
        country = kwargs["initial"]["tocountry"]
        provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
        provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
        provlist = sorted(provlist)
        self.fields["toname"].widget = ListTextWidget(data_list=provlist, name="toprovlist")

class DateForm(forms.Form):

    step_title = "Date"
    step_descr = """
                    On what date did the changes occur? 
                   """
    year = forms.ChoiceField(choices=[(yr,yr) for yr in range(0, 2016+1)], initial=1950)
    month = forms.ChoiceField(choices=[(mn,mn) for mn in range(1, 12+1)])
    day = forms.ChoiceField(choices=[(dy,dy) for dy in range(1, 31+1)])

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'style' : 'font-size: x-large'})
        self.fields['month'].widget.attrs.update({'style' : 'font-size: x-large'})
        self.fields['day'].widget.attrs.update({'style' : 'font-size: x-large'})


class AddDateWizard(SessionWizardView):
    form_list = [   DateForm,
                      ]

    country = None

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)
 
    def get_context_data(self, form, **kwargs):
        context = super(AddDateWizard, self).get_context_data(form=form, **kwargs)
        context.update({'wizard_subclass': self})
        return context

    def get_template_names(self):
        return ["provchanges/adddate.html"]

    def done(self, form_list, form_dict, **kwargs):
        # NOT YET DONE...
        print "DONE!", form_list, form_dict, kwargs

        data = form_list[0].cleaned_data
        data = dict(((k,int(v)) for k,v in data.items()))
        date = datetime.date(**data)
        country = self.country

        url = "/contribute/add/{country}?date={date}".format(country=urlquote(country), date=urlquote(date))
        html = redirect(url)

        return html

class AddEventWizard(SessionWizardView):
    form_list = [   SourceEventForm,
                     TypeEventForm,
                      FromEventForm,
                      ToEventForm,
                      ]

    # NOTE: MUST BE EITHER EXPANSION OR SPLIT OR NEWINFO EVENT, WITH GET PARAMS FOR ALL CONSTANT EVENTINFO
    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: True,
                      "2": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] in ("Split","Breakaway","NewInfo") if wiz.get_cleaned_data_for_step("1") else False,
                      "3": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] in ("Form","Expand","Begin") if wiz.get_cleaned_data_for_step("1") else False,
                      }

    country = None

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step in "23": # from or to form
            typ = self.get_cleaned_data_for_step("1").get("type")
            if typ == "Split":
                kwargs["step_descr"] = "Please identify the province that split?"
            elif typ == "Breakaway":
                kwargs["step_descr"] = "Please identify the province that broke off territory?"
            elif typ == "NewInfo":
                kwargs["step_descr"] = "Please identify the province that changed information? Only the parts that have changed will be registered. "
            elif typ == "Expand":
                kwargs["step_descr"] = "Please identify the province that gained territory after all the mergers/transfers?"
            elif typ == "Form":
                kwargs["step_descr"] = "Please identify the province that was formed after all the mergers/transfers?"
            elif typ == "Begin":
                kwargs["step_descr"] = "Please identify the province for which this is the earliest known record?"

        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "0":
            data["fromcountry"] = self.country
        elif step == "2":
            data["fromcountry"] = self.country
        elif step == "3":
            data["tocountry"] = self.country
        return data

    def get_context_data(self, form, **kwargs):
        context = super(AddEventWizard, self).get_context_data(form=form, **kwargs)
        context.update({'wizard_subclass': self})
        return context

    def get_template_names(self):
        return ["provchanges/addevent.html"]

    def done(self, form_list, form_dict, **kwargs):
        # NOT YET DONE...
        print "DONE!", form_list, form_dict, kwargs
        
        data = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items()))
        data["date"] = self.request.GET["date"]
        print "DATA",data
        country = self.country
        
        if data["type"] in "Form Expand":
            prov = data["toname"]
        elif data["type"] in "Split Breakaway":
            prov = data["fromname"]
        elif data["type"] == "NewInfo":
            prov = data["fromname"]
        elif data["type"] == "Begin":
            prov = data["toname"]
        # if transfer, have to set the 3 geom vals and save to session
        # then, in addtransferchange, get the 3 geom vals from session, and set to the submit data
        # ...
            
        keys = data.keys() #["date","source","type"]
        params = urlencode( [(key,data[key]) for key in keys] ) #+ [("fromcountry",country),("tocountry",country)] )
        print params
        url = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params
        html = redirect(url)

        return html



















# Change forms

class MetaChangeForm(forms.ModelForm):

    icon = "/static/user.png"

    class Meta:
        model = ProvChange
        fields = ['user','added','status']

from django.forms.widgets import RadioFieldRenderer

class TypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if "-" not in w.choice_label]
        html = """
            <table class="myradio">
            {% for choice,extra in choices %}
            <tr>
                <td>{{ choice }}<td>
                <td>{{ extra.img|safe }}</td>
                <td>
                    <h4>{{ extra.short|safe }}</h4>
                    <p>{{ extra.descr|safe }}</p>
                </td>
            </tr>
            {% endfor %}
            </table>
            """
        rendered = Template(html).render(Context({"choices":choices }))
        return rendered

class FormTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label in "MergeNew TransferNew"]
        html = """
            <table class="myradio">
            {% for choice,extra in choices %}
            <tr>
                <td>{{ choice }}<td>
                <td>{{ extra.img|safe }}</td>
                <td>
                    <h4>{{ extra.short|safe }}</h4>
                    <p>{{ extra.descr|safe }}</p>
                </td>
            </tr>
            {% endfor %}
            </table>
            """
        rendered = Template(html).render(Context({"choices":choices }))
        return rendered

class ExpandTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label in "MergeExisting TransferExisting"]
        html = """
            <table class="myradio">
            {% for choice,extra in choices %}
            <tr>
                <td>{{ choice }}<td>
                <td>{{ extra.img|safe }}</td>
                <td>
                    <h4>{{ extra.short|safe }}</h4>
                    <p>{{ extra.descr|safe }}</p>
                </td>
            </tr>
            {% endfor %}
            </table>
            """
        rendered = Template(html).render(Context({"choices":choices }))
        return rendered

class BreakawayTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label in ["Breakaway"]]
        html = """
            <table class="myradio">
            {% for choice,extra in choices %}
            <tr>
                <td>{{ choice }}<td>
                <td>{{ extra.img|safe }}</td>
                <td>
                    <h4>{{ extra.short|safe }}</h4>
                    <p>{{ extra.descr|safe }}</p>
                </td>
            </tr>
            {% endfor %}
            </table>
            """
        rendered = Template(html).render(Context({"choices":choices }))
        return rendered

class SplitTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label in ["SplitPart"]]
        html = """
            <table class="myradio">
            {% for choice,extra in choices %}
            <tr>
                <td>{{ choice }}<td>
                <td>{{ extra.img|safe }}</td>
                <td>
                    <h4>{{ extra.short|safe }}</h4>
                    <p>{{ extra.descr|safe }}</p>
                </td>
            </tr>
            {% endfor %}
            </table>
            """
        rendered = Template(html).render(Context({"choices":choices }))
        return rendered

class TypeChangeForm(forms.ModelForm):

    icon = "/static/typechange.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=TypeChangeRenderer) }


class SimpleTypeChangeForm(forms.ModelForm):

    icon = "/static/typechange.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']

    def as_readonly(self):
        html = """
                    {{ form.type.label_tag }}
                    {{ form.type.value }}
                """
        rendered = Template(html).render(Context({"form":self}))
        return rendered

class FormTypeChangeForm(forms.ModelForm):
    icon = "/static/typechange.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=FormTypeChangeRenderer) }

class ExpandTypeChangeForm(forms.ModelForm):
    icon = "/static/typechange.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=ExpandTypeChangeRenderer) }

class BreakawayTypeChangeForm(forms.ModelForm):
    icon = "/static/typechange.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=BreakawayTypeChangeRenderer) }

class SplitTypeChangeForm(forms.ModelForm):
    icon = "/static/typechange.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=SplitTypeChangeRenderer) }

class GeneralChangeForm(SourceEventForm):

    # USED TO SHOW INDIVIDUAL CHANGES
    # THE DESCRIPTIONS DONT ACTUALLY SHOW, SO SHOULD BE REMOVED
    # ...

    icon = "/static/info.png"
    step_title = "Basic Information"
    step_descr = """
                    Welcome to the step-by-step wizard for submitting historical
                    changes to the "primary" or "level-1" sub-administrative units of countries.
                    For what country and at what date did the province change? 
                    <br><br>

                    <div style="background-color:rgb(248,234,150); outline: black solid thick; font-family: comic sans ms">
                    <p style="font-size:large; font-weight:bold">Note:</p>
                    <p style="font-size:medium; font-style:italic">
                    There are several types of sources you can use:
                    <ul>
                        <li>
                        <a target="_blank" href="http://www.statoids.com">The Statoids website</a> traces historical province changes
                        in great detail, and should be the first place to look.
                        </li>

                        <li>
                        The <a target="_blank" href="https://en.wikipedia.org/wiki/Table_of_administrative_divisions_by_country">Wikipedia entries for administrative units</a>
                        can sometimes also be a useful reference.
                        </li>

                        <li>
                        You can also use offline sources such as a book or an article.
                        </li>
                    </ul>
                    </p>
                    </div>

                    <div style="background-color:rgb(248,234,150); outline: black solid thick; font-family: comic sans ms">
                    <p style="font-size:large; font-weight:bold">Note:</p>
                    <p style="font-size:medium; font-style:italic">
                    It can be a good idea to start by looking at
                    <a target="_blank" href="/contribute">this list of countries and changes already submitted by other users</a>
                    to avoid double-registering. 
                    </p>
                    </div>
                   """

    class Meta:
        model = ProvChange
        fields = ['date', 'source', 'sources', 'mapsources']
        widgets = {"date": CustomDateWidget()}

    def as_p(self):
        html = """
                    <div style="margin-left:2%">

                        <p>
                        {{ form.date.label_tag }}
                        {{ form.date }}
                        </p>

                        <div style="">
                        {{ form.source.label_tag }}
                        {{ form.source }}
                        </div>

                        <p>
                        Link to sources and maps by referencing their id number (e.g. #source12, #map9).
					<div style="margin-left:20px; width:45%; display:inline-block"><em>Suggested Sources:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_sources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/source.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
					<div style="width:45%; display:inline-block"><em>Suggested Maps:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_mapsources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="/static/map.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewmap/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
			</p>
					
                    </div>
                    """
        
        rendered = Template(html).render(Context({"form":self, 'country':urlquote(self.country)}))
        return rendered

    def as_simple(self):
        html = """
                    <div style="margin-left:2%">

                        <p>
                        {{ form.date.label_tag }}
                        {{ form.date }}
                        </p>

                        <div style="">
                        {{ form.source.label_tag }}
                        {{ form.source }}
                        </div>

                        <p>
                        OLD:
                        Sources: {{ form.sources.value }}
                        Maps: {{ form.mapsources.value }}
                        </p>
					
                    </div>
                    """
        
        rendered = Template(html).render(Context({"form":self, 'country':urlquote(self.country)}))
        return rendered

    def as_simple_readonly(self):
        html = """
                    <div style="margin-left:2%">

                        <p>
                        {{ form.date.label_tag }}
                        {{ form.date.value }}
                        </p>

                        <div style="">
                        {{ form.source.label_tag }}
                        {{ form.get_source_formatted | safe }}
                        </div>
					
                    </div>
                    """
        rendered = Template(html).render(Context({"form":self}))
        return rendered

    def get_source_formatted(self):
        # should outsourcec the job to "text_formatted"
        import re
        val = self['source'].value()
        
        def repl(matchobj):
            id = matchobj.group(2)
            return '<a target="_blank" href="/viewmap/{id}/"><img height="15px" src="/static/map.png">{id}</a>'.format(id=id)
        val,n = re.subn('#(map)([0-9]*)', repl, val)
        def repl(matchobj):
            id = matchobj.group(2)
            return '<a target="_blank" href="/viewsource/{id}/"><img height="15px" src="/static/source.png">{id}</a>'.format(id=id)
        val,n = re.subn('#(source)([0-9]*)', repl, val)
        return val

class FromChangeForm(forms.ModelForm):

    icon = "/static/fromicon.png"
    step_title = "From Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'fromcountry fromname fromalterns fromiso fromfips fromhasc fromcapitalname fromcapital fromtype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(FromChangeForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["fromcountry"].widget = ListTextWidget(data_list=countrylist, name="fromcountrylist")

        if "initial" in kwargs:
            country = kwargs["initial"]["fromcountry"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
            provlist = sorted(provlist)
            self.fields["fromname"].widget = ListTextWidget(data_list=provlist, name="fromprovlist")

    def as_readonly(self):
        return as_readonly(self)

class FromChangeNameForm(forms.ModelForm):

    icon = "/static/fromicon.png"
    step_title = "From Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'fromcountry fromname fromalterns'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(FromChangeNameForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["fromcountry"].widget = ListTextWidget(data_list=countrylist, name="fromcountrylist")

        if "initial" in kwargs:
            country = kwargs["initial"]["fromcountry"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
            provlist = sorted(provlist)
            self.fields["fromname"].widget = ListTextWidget(data_list=provlist, name="fromprovlist")

    def as_readonly(self):
        return as_readonly(self)

class FromChangeCodesForm(forms.ModelForm):

    icon = "/static/fromicon.png"
    step_title = "From Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'fromiso fromfips fromhasc'.split()

    def as_readonly(self):
        return as_readonly(self)

class FromChangeInfoForm(forms.ModelForm):

    icon = "/static/fromicon.png"
    step_title = "From Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'fromcapitalname fromcapital fromtype'.split()

    def as_readonly(self):
        return as_readonly(self)

class ToChangeForm(forms.ModelForm):

    icon = "/static/toicon.png"
    step_title = "To Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'tocountry toname toalterns toiso tofips tohasc tocapitalname tocapital totype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(ToChangeForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["tocountry"].widget = ListTextWidget(data_list=countrylist, name="tocountrylist")

        if "initial" in kwargs:
            country = kwargs["initial"]["tocountry"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
            provlist = sorted(provlist)
            self.fields["toname"].widget = ListTextWidget(data_list=provlist, name="toprovlist")

    def as_readonly(self):
        return as_readonly(self)

class ToChangeNameForm(forms.ModelForm):

    icon = "/static/toicon.png"
    step_title = "To Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'tocountry toname toalterns'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(ToChangeNameForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["tocountry"].widget = ListTextWidget(data_list=countrylist, name="tocountrylist")

        if "initial" in kwargs:
            country = kwargs["initial"]["tocountry"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
            provlist = sorted(provlist)
            self.fields["toname"].widget = ListTextWidget(data_list=provlist, name="toprovlist")

    def as_readonly(self):
        return as_readonly(self)

class ToChangeCodesForm(forms.ModelForm):

    icon = "/static/toicon.png"
    step_title = "To Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'toiso tofips tohasc'.split()

    def as_readonly(self):
        return as_readonly(self)

class ToChangeInfoForm(forms.ModelForm):

    icon = "/static/toicon.png"
    step_title = "To Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'tocapitalname tocapital totype'.split()

    def as_readonly(self):
        return as_readonly(self)

def as_readonly(form):
    html = """
            {% for field in form %}
                    <p>
                    {{ field.label_tag }}
                    {{ field.value | safe }}
                    </p>
            {% endfor %}
                """
    rendered = Template(html).render(Context({"form":form}))
    return rendered


class AddChangeWizard(SessionWizardView):

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)
 
    def get_context_data(self, form, **kwargs):
        context = super(AddChangeWizard, self).get_context_data(form=form, **kwargs)
        context.update({'wizard_subclass': self})
        return context

    def get_template_names(self):
        return ["provchanges/addchange.html"]

    def done(self, form_list, form_dict, **kwargs):
        # NOT YET DONE...
        print "DONE!", form_list, form_dict, kwargs
        
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
        formfieldvalues["user"] = self.request.user.username
        formfieldvalues["added"] = datetime.datetime.now()
        formfieldvalues["bestversion"] = True
        print formfieldvalues

        eventvalues = dict(((k,v) for k,v in self.request.GET.items()))
        print eventvalues

        if eventvalues["type"].strip('"') in "Form Expand" and formfieldvalues["type"].strip('"') == "NewInfo":
            # all tos become froms when newinfo for merge event
            # ACTUALLY: shouldnt happen anymore
            raise Exception()
            #trans = dict([(k.replace("to","from"),v) for k,v in eventvalues.items() if k.startswith("to")])
            #eventvalues = dict([(k,v) for k,v in eventvalues.items() if not k.startswith("to")])
            #eventvalues.update(trans)

        objvalues = dict(eventvalues)
        objvalues.update(formfieldvalues)

        objvalues.pop('sources',None)
        objvalues.pop('mapsources',None)
        #sources = [get_object_or_404(Source, pk=int(pk)) for pk in objvalues.pop('sources').split(',') if pk]
        #mapsources = [get_object_or_404(Map, pk=int(pk)) for pk in objvalues.pop('mapsources').split(',') if pk]
        print objvalues
        
        obj = ProvChange.objects.create(**objvalues)
        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
        print obj
        
        obj.save()
##        for s in sources:
##            obj.sources.add(s)
##        for m in mapsources:
##            obj.mapsources.add(m)
##        obj.save()
        
        html = self.done_redirect(obj)

        return html

class AddNewInfoChangeWizard(AddChangeWizard):

    form_list = [   
                    ToChangeForm,
                      ]

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "0": # from or to form
            kwargs["step_descr"] = "Fill in the province information after the change. Only the parts that have changed will be registered." 
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "0":
            data["tocountry"] = self.request.GET["fromcountry"]
            data["toname"] = self.request.GET["fromname"]
            data["toalterns"] = self.request.GET["fromalterns"]
            data["toiso"] = self.request.GET["fromiso"]
            data["tofips"] = self.request.GET["fromfips"]
            data["tohasc"] = self.request.GET["fromhasc"]
            data["totype"] = self.request.GET["fromtype"]
            data["tocapital"] = self.request.GET["fromcapital"]
            data["tocapitalname"] = self.request.GET["fromcapitalname"]
        return data  

    def done_redirect(self, obj):
        fields = ["fromcountry","date","source","sources","mapsources","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=NewInfo&".format(country=urlquote(self.country), prov=urlquote(obj.fromname)) + params
        html = redirect(eventlink)
        return html

class AddBreakawayChangeWizard(AddChangeWizard):

    form_list = [   BreakawayTypeChangeForm,
                    ToChangeForm,
                      ]

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "1": # from or to form
            kwargs["step_descr"] = "Please identify the province that broke away?"
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "1":
            data["tocountry"] = self.country
        return data  

    def done_redirect(self, obj):
        fields = ["fromcountry","date","source","sources","mapsources","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Breakaway&".format(country=urlquote(self.country), prov=urlquote(obj.fromname)) + params
        html = redirect(eventlink)
        return html

class AddSplitChangeWizard(AddChangeWizard):

    form_list = [   SplitTypeChangeForm,
                    ToChangeForm,
                      ]

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "1": # from or to form
            kwargs["step_descr"] = "Please identify the province that broke away?"
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "1":
            data["tocountry"] = self.country
        return data  

    def done_redirect(self, obj):
        fields = ["fromcountry","date","source","sources","mapsources","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Split&".format(country=urlquote(self.country), prov=urlquote(obj.fromname)) + params
        html = redirect(eventlink)
        return html
    
class AddExpandChangeWizard(AddChangeWizard):

    form_list = [   ExpandTypeChangeForm,
                    FromChangeForm,
                    ToChangeForm,
##                     HistoMapForm,
##                     GeorefForm,
                      GeoChangeForm,
                      ]
    
    def _geomode(wiz):
        typeformdata = wiz.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
        print wiz.get_cleaned_data_for_step("0")
        return typeformdata["type"] in "TransferExisting MergeExisting FullTransfer PartTransfer"

    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: True,
                      "2": lambda wiz: False,
                      "3": _geomode,}

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "1": # from or to form
            kwargs["step_descr"] = "Please identify the province that merged or transferred territory?"
        elif step == "3":
            kwargs["country"] = self.country
            kwargs["province"] = self.province
            kwargs["date"] = self.request.GET["date"]
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "1":
            data["fromcountry"] = self.country
        elif step == "3":
            data["country"] = self.country
        return data
    
    def done_redirect(self, obj):
        fields = ["tocountry","date","source","sources","mapsources","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Expand&".format(country=urlquote(self.country), prov=urlquote(obj.toname)) + params
        html = redirect(eventlink)
        return html

class AddFormChangeWizard(AddChangeWizard):

    form_list = [   FormTypeChangeForm,
                    FromChangeForm,
                    ToChangeForm,
##                     HistoMapForm,
##                     GeorefForm,
                      GeoChangeForm,
                      ]
    
    def _geomode(wiz):
        typeformdata = wiz.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
        print wiz.get_cleaned_data_for_step("0")
        return typeformdata["type"] in "TransferNew MergeNew"

    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: True,
                      "2": lambda wiz: False,
                      "3": _geomode,}

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "1": # from or to form
            kwargs["step_descr"] = "Please identify the province that merged or transferred territory?"
        elif step == "3":
            kwargs["country"] = self.country
            kwargs["province"] = self.province
            kwargs["date"] = self.request.GET["date"]
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "1":
            data["fromcountry"] = self.country
        elif step == "3":
            data["country"] = self.country
        return data
    
    def done_redirect(self, obj):
        fields = ["tocountry","date","source","sources","mapsources","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Form&".format(country=urlquote(self.country), prov=urlquote(obj.toname)) + params
        html = redirect(eventlink)
        return html


















