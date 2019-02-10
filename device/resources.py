import string, random
import syslog
import base64
import json
import urlparse
import datetime
from decimal import Decimal
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import Authentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.exceptions import NotFound
from tastypie.http import HttpCreated, HttpBadRequest, HttpForbidden, HttpNotFound, HttpApplicationError, HttpUnauthorized
from tastypie.serializers import Serializer
from tastypie.exceptions import ImmediateHttpResponse
from tastypie import fields
from user.models import User
from django.forms.models import model_to_dict

from  device.models import Extension

import logging
logging.basicConfig(filename='/var/log/api.log',level=logging.ERROR, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content):
        pass


class IPBasicAuthentication(BasicAuthentication):

    def is_authenticated(self, request, **kwargs):
        """
        Checks a user's basic auth credentials against the current
        Django auth backend.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """
        logging.debug(request.META)
        if not request.META.get('HTTP_AUTHORIZATION'):
            logging.error('HTTP_AUTHORIZATION not found')
            return self._unauthorized()

        try:
            logging.debug('start split')
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type.lower() != 'basic':
                logging.error('not basic')
                return self._unauthorized()
            user_pass = base64.b64decode(data).decode('utf-8')
        except:
            logging.error('plit issue')
            return self._unauthorized()

        bits = user_pass.split(':', 1)
        logging.debug(bits)
        if len(bits) != 2:
            logging.error('len bits issue')
            return self._unauthorized()

        if self.backend:
            user = self.backend.authenticate(username=bits[0], password=bits[1])
        else:
            user = authenticate(username=bits[0], password=bits[1])

        if user is None:
            logging.debug('username password is not correct.')
            return self._unauthorized()

        if not self.check_active(user):
            logging.debug('user is not active')
            return False
        request.user = user
        return True


class HttpOK(HttpResponse):
    status_code = 200

    def __init__(self, *args, **kwargs):
        location = ''

        if 'location' in kwargs:
            location = kwargs['location']
            del(kwargs['location'])

        super(HttpOK, self).__init__(*args, **kwargs)
        self['Location'] = location


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.exclude(role=1)
        allowed_methods = ['get']
        authentication = MultiAuthentication(IPBasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        serializer = urlencodeSerializer()
        fields = ['email', 'sure_name', 'ring_group_ext']
        filtering = {
            'sure_name': ALL,
            'email': ALL,
        }

    def get_list(self, request, **kwargs):
        if request.user.is_authenticated() and  request.user.role in [0,1]:
            return super(UserResource, self).get_list(request, **kwargs)
        else:
            if request.user.is_authenticated():
                kwargs["pk"] = request.user.pk
                return super(UserResource, self).get_detail(request, **kwargs)
            else:
                data_res = {'status': 'false', 'message': "obj not found"}
                response = self.error_response(request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)


class DeviceResource(ModelResource):
    is_bell = fields.CharField(blank=True, null=True)

    class Meta:
        queryset = Extension.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        authentication = MultiAuthentication(IPBasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        serializer = urlencodeSerializer()
        always_return_data = True
        fields = ['extension_uuid', 'extension', 'password', 'do_not_disturb', 'is_bell']
        filtering = {
            'uuid': ALL,
            'sip_username': ALL
        }
    def dehydrate_is_bell(self, bundle):
        obj = bundle.obj
        if obj.description == 'is_bell':
            return 'true'
        else:
            return 'false'

    def get_list(self, request, **kwargs):
        if 'uuid' in request.GET:
            if Device.objects.filter(uuid=request.GET['uuid']).count() == 1:
                kwargs["pk"] = Device.objects.filter(uuid=request.GET['uuid'])[0].id
                return super(DeviceResource, self).get_detail(request, **kwargs)
            else:
                kwargs["pk"] = 0
                return super(DeviceResource, self).get_detail(request, **kwargs)
        return super(DeviceResource, self).get_list(request, **kwargs)


    def obj_create(self, bundle, **kwargs):
        req = ['uuid']
        data = bundle.data
        for value in req:
            if value not in data or data[value] == '':
                data_res = {'error': "%s is not valid" % value}
                response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)
        if Extension.objects.filter(extension_uuid=data['uuid']).count() > 0:
            data_res = {'error': "uuid is exist, you cant create new one, please get sip account"}
            response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
            raise ImmediateHttpResponse(response=response)
        else:
            for value in data:
                if data[value] in ['true', 'True']:
                    data[value] = True
                elif data[value] in ['false', 'False']:
                    data[value] = False
            kwargs['extension'] = random.randint(100000,999999)
            kwargs['password'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
            ext = Extension()
            ext.extension = kwargs['extension']
            ext.password = kwargs['password']
            ext.extension_uuid = data['uuid']
            ext.accountcode = bundle.request.user.id
            if data.get('is_bell') == 'true':
                ext.description = 'is_bell'
            ext.save()
            data_res = {"extension": kwargs['extension'], "password": kwargs['password'], "resource_uri": "/api/v1/device/%s/" % data['uuid']}
            response = self.error_response(bundle.request, data_res, response_class=HttpOK)
            raise ImmediateHttpResponse(response=response)

    def obj_update(self, bundle, **kwargs):
        data = bundle.data
        unchange_list = ['uuid', 'username', 'password']
        for value in unchange_list:
            if value in data:
                del data[value]
        ret =  super(DeviceResource, self).obj_update(bundle, **kwargs)
        obj = bundle.obj
        if data.get('do_not_disturb'):
            if data['do_not_disturb'] == 'true':
                obj.dial_string = 'error/user_busy'
            else:
                obj.dial_string = ''
            obj.save()
        if data.get('is_bell'):
            if data.get('is_bell') == 'true':
                obj.description = 'is_bell'
            else:
                obj.description = ''
            obj.save()
        from device.models import sync_ring_group_user
        sync_ring_group_user(obj.accountcode)
        return ret
