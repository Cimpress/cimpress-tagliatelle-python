import json
import urllib
import urllib2

from tagliatelle import TAGLIATELLE_URL
from tagliatelle.data.TagBulkResponse import TagBulkResponse
from tagliatelle.data.TagResponse import TagResponse


class LowLevelClient:
    """This class wraps all the low level operations with Tagliatelle API"""

    def __init__(self, access_token, service_url):
        self.accessToken = access_token
        if service_url is None:
            self.serviceUrl = TAGLIATELLE_URL
        else:
            self.serviceUrl = service_url

    def get_tags(self, key="", resource_uri=""):
        try:
            query_params = {}

            if resource_uri is not None:
                query_params['resourceUri'] = resource_uri

            if key is not None:
                query_params['key'] = key

            req = urllib2.Request(self.serviceUrl + "/v0/tags?" + urllib.urlencode(query_params))
            req.add_header('Authorization', 'Bearer ' + self.accessToken)

            response = urllib2.urlopen(req)

            data = json.load(response)
            results = []
            if "results" in data:
                for tag in data["results"]:
                    results.append(TagResponse(tag.get("key"), tag.get("value"), tag.get("resourceUri"), tag.get("id"),
                                               tag.get("createdAt"), tag.get("createdBy"), tag.get("modifiedAt"),
                                               tag.get("modifiedBy"), tag.get("_links")))
                return TagBulkResponse(data.get('count'), data.get('total'), data.get('offset'), results)
            else:
                return TagBulkResponse(0, 0, 0, [])
        except urllib2.HTTPError as e:
            print e.read()

    def post_tag(self, request):
        try:
            req = urllib2.Request(self.serviceUrl + "/v0/tags")
            req.add_header("Authorization", "Bearer " + self.accessToken)
            req.add_header("Content-Type", "application/json")
            req.get_method = lambda: 'POST'
            req.add_data(json.dumps(request))
            urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            print e.read()

    def put_tag(self, id, request):
        try:
            req = urllib2.Request(self.serviceUrl + "/v0/tags/" + id)
            req.add_header("Authorization", "Bearer " + self.accessToken)
            req.add_header("Content-Type", "application/json")
            req.get_method = lambda: 'PUT'
            req.add_data(json.dumps(request))
            urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            print e.read()

    def delete_tag(self, id):
        try:
            req = urllib2.Request(self.serviceUrl + "/v0/tags/" + id)
            req.add_header("Authorization", "Bearer " + self.accessToken)
            req.get_method = lambda: 'DELETE'
            urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            print e.read()



