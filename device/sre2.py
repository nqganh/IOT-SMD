import string, random
import syslog
import base64
import uuid
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
from user.models import User, RingGroup
from django.forms.models import model_to_dict

from  device.models import Extension, RingGroupDestination

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
#    ring_group_uuid = fields.ToManyField(RingGroupResource, 'ring_group_uuid', null = True)
    class Meta:
#        queryset = User.objects.exclude(role=1)
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get']
        authentication = MultiAuthentication(IPBasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        serializer = urlencodeSerializer()
        fields = ['email', 'sure_name', 'company']
        filtering = {
            'sure_name': ALL,
            'email': ALL,
        }

    def get_list(self, request, **kwargs):
        if request.user.is_authenticated() and request.user.role in [0,1]:
            return super(UserResource, self).get_list(request, **kwargs)
        else:
            if request.user.is_authenticated():
                kwargs["pk"] = request.user.pk
                return super(UserResource, self).get_detail(request, **kwargs)
            else:
                data_res = {'status': 'false', 'message': "obj not found"}
                response = self.error_response(request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)

class RingGroupResource(ModelResource):
    list_sip = fields.CharField(blank=True, null=True)
    department_uuid = fields.CharField(attribute='ring_group_uuid')
    department_name = fields.CharField(attribute='ring_group_name')
    department_extension = fields.CharField(attribute='ring_group_extension')
#    user = fields.ToManyField(UserResource, 'user')
    
    class Meta:
        queryset = RingGroup.objects.all()
        resource_name = 'department'
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        authentication = MultiAuthentication(IPBasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        serializer = urlencodeSerializer()
        always_return_data = True
        fields = []
       # fields = ['ring_group_name', 'ring_group_uuid', 'ring_group_extension']
        filtering = {
            'uuid': ALL,
        }
    def dehydrate_list_sip(self, bundle):
        obj = bundle.obj
        le = ""
        if RingGroupDestination.objects.filter(ring_group_uuid=obj.ring_group_uuid).count() == 0:
            return ''
        else:
            listext = RingGroupDestination.objects.filter(ring_group_uuid=obj.ring_group_uuid)
            for ext in listext:
                abc = Extension.objects.filter(extension=ext.destination_number)[0]
                le = str(abc.extension_uuid) + ', ' + le
            le = le.rstrip(', ')
            return le

    def get_object_list(self, request, **kwargs):
        ky = request.user.id
        kc = request.user.ring_group.all()
        if 'uuid' in request.GET:
            uuid = request.GET['uuid']
            if is_valid_uuid(uuid) == True:
                if RingGroup.objects.filter(ring_group_uuid=request.GET['uuid']).count() == 1:
                    return super(RingGroupResource, self).get_object_list(request, **kwargs).filter(ring_group_uuid=request.GET['uuid'])
                else:
                   # kwargs["pk"] = 0
                    uuid = request.GET['uuid']
                    data_res = {'error': "department's uuid doesn't exist"}
                    response = self.error_response(request, data_res, response_class=HttpBadRequest)
                    raise ImmediateHttpResponse(response=response)
            else:
                data_res = {'error': "department's uuid is not valid"}
                response = self.error_response(request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)
        else:
            if len(kc) == 0:
                data_res = {'error': "have no department's uuid. Let's create new once"}
                response = self.error_response(request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)
#                return super(RingGroupResource, self).get_object_list(request, **kwargs)
           #     kwargs[''] = request.user.ring_group.all()
            else:
                return super(RingGroupResource, self).get_object_list(request, **kwargs).filter(ring_group_uuid__in=kc)

    def obj_create(self, bundle, **kwargs):
        ky = bundle.request.user.id
        req = ['uuid']
        ren = ['name']
        data = bundle.data
        for value in req:
            if value not in data or data[value] == '' or is_valid_uuid(data[value]) == False:
                for vl2 in ren:
                    if vl2 not in data or data[vl2] == '':
                        data_res = {'error_uuid': "uuid is not valid", 'error_name': "name is not valid"}
                        response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                        raise ImmediateHttpResponse(response=response)
                    else:
                        data_res = {'error': "%s is not valid" % value}
                        response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                        raise ImmediateHttpResponse(response=response)
        for value1 in ren:
            if value1 not in data or data[value1] == '':
                for vl3 in req:
                    if vl3 not in data or data[vl3] == '' or is_valid_uuid(data[vl3]) == False:
                        data_res = {'error_uuid': "uuid is not valid", 'error_name': "name is not valid"}
                        response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                        raise ImmediateHttpResponse(response=response)
                    else:
                        data_res = {'error': "%s is not valid" % value1}
                        response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                        raise ImmediateHttpResponse(response=response)
        if RingGroup.objects.filter(ring_group_uuid=data['uuid']).count() > 0:
                data_res = {'error': "uuid exists, you cant create new one"}
                response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)
        else:
            for value in data:
                if data[value] in ['true', 'True']:
                    data[value] = True
                elif data[value] in ['false', 'False']:
                    data[value] = False
            kwargs['domain_uuid'] = '09f10c29-9f49-4209-9050-52bd09d1886a'
            kwargs['ring_group_extension'] = random.randint(100000,999999)            
            kwargs['dialplan_uuid'] = uuid.uuid4()
            kwargs['ring_group_name'] = data['name']
            rg = RingGroup()
            rg.ring_group_extension = kwargs['ring_group_extension']
            rg.ring_group_uuid = data['uuid']
            rg.ring_group_name = kwargs['ring_group_name']
            rg.dialplan_uuid = kwargs['dialplan_uuid']
            rg.save()
            User.objects.get(id=ky).ring_group.add(data['uuid'])            
           # rg.user.add(user)
#             ext.accountcode = bundle.request.user
            from device.models import sync_dialplan_rg
            sync_dialplan_rg(rg.ring_group_uuid)
            data_res = {"ring_group_name": kwargs['ring_group_name'], "ring_group_extension": kwargs['ring_group_extension'], "resource_uri": "/api/v1/department/%s/" % data['uuid']}
            response = self.error_response(bundle.request, data_res, response_class=HttpOK)
            raise ImmediateHttpResponse(response=response)
    def obj_update(self, bundle, **kwargs):
        ky = bundle.request.user.id
        data = bundle.data
        unchange_list = ['departmen_extension', 'department_uuid']
        for value in unchange_list:
            if value in data:
                del data[value]
        ret =  super(RingGroupResource, self).obj_update(bundle, **kwargs)
        obj = bundle.obj
        if data.get('department_name'):
            print data ['department_name']
            if data['department_name'] != '':
                obj.ring_group_name = data['department_name']
        obj.save()
        if data.get('list_sip'):
            data['list_sip'] = data['list_sip'].replace(' ','')
            data['list_sip'] = data['list_sip'].replace(';',',')
            if data['list_sip'] == '':
                if RingGroupDestination.objects.filter(ring_group_uuid=obj.ring_group_uuid).count() >0:
                    RingGroupDestination.objects.filter(ring_group_uuid=obj.ring_group_uuid).delete()
                  #  RingGroupDestination.save()
            else:
                data['list_sip'] = data['list_sip'].replace(' ','')
                data['list_sip'] = data['list_sip'].replace(';',',')
                data['list_sip'] = data['list_sip'].rstrip(',')
                listextadd = data['list_sip'].split(',')
                if Extension.objects.filter(accountcode=ky).count() == 0:
                    data_res = {'error': "have no sip account, let's create new one"}
                    response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                    raise ImmediateHttpResponse(response=response)
                else:
                    listextuser = Extension.objects.filter(accountcode=ky)
#                print data['list_sip'], listextadd, listextusero
                RingGroupDestination.objects.filter(ring_group_uuid=obj.ring_group_uuid).delete()
                for extel in listextadd:
                    if is_valid_uuid(extel) == False:
                        data_res = {'error_sip': "at least one invalid sip uuid exists. Please check sip uuid list"}
                        response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                        raise ImmediateHttpResponse(response=response)
                    if listextuser.filter(extension_uuid=extel).count() == 0:
                        data_res = {'error_sip': "at least one sip uuid doesn't exists in this user's sip list. Please check sip uuid list"}
                        response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                        raise ImmediateHttpResponse(response=response)
                    else:
                        ck_bell = listextuser.filter(extension_uuid=extel)[0]
                        if ck_bell.description == 'is_bell':
                            data_res = {'error_sip': "at least one sip uuid is bell. Please check sip uuid list"}
                            response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                            raise ImmediateHttpResponse(response=response)                        
                    rdg = RingGroupDestination()
                    rdg.ring_group_destination_uuid = uuid.uuid4()
                    rdg.ring_group_uuid = RingGroup.objects.get(ring_group_uuid=obj.ring_group_uuid)
                    rdg.destination_number = Extension.objects.get(extension_uuid=extel)
                    rdg.save()
        from device.models import sync_dialplan_rg
        sync_dialplan_rg(obj.ring_group_uuid)
        return ret

class DeviceResource(ModelResource):
    is_bell = fields.CharField(blank=True, null=True)
#    accountcode = fields.ForeignKey(UserResource, 'accountcode', full=True)
    class Meta:
        queryset = Extension.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'device'
        authentication = MultiAuthentication(IPBasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        serializer = urlencodeSerializer()
        always_return_data = True
        fields = ['accountcode', 'extension_uuid', 'extension', 'password', 'do_not_disturb', 'is_bell']
        filtering = {
            'uuid': ALL,
            'sip_username': ALL,
            'accountcode': ALL,
        }
    def dehydrate_is_bell(self, bundle):
        obj = bundle.obj
        if obj.description == 'is_bell':
            return 'true'
        else:
            return 'false'

    def get_object_list(self, request, **kwargs):
        ky = request.user.id
        if 'uuid' in request.GET:
            uuid = request.GET['uuid']
            if is_valid_uuid(uuid) == True:
                if Extension.objects.filter(extension_uuid=request.GET['uuid']).count() == 1:
#                 kwargs["pk"] = Extension.objects.filter(extension_uuid=request.GET['uuid'])
                    return super(DeviceResource, self).get_object_list(request, **kwargs).filter(extension_uuid=request.GET['uuid'])
                else:
                    data_res = {'error': "sip account's uuid doesn't exist"}
                    response = self.error_response(request, data_res, response_class=HttpBadRequest)
                    raise ImmediateHttpResponse(response=response)
            else:
                data_res = {'error': "sip account's uuid doesn't valid"}
                response = self.error_response(request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)
        else:
            if Extension.objects.filter(accountcode = ky).count() > 0:
#                ret = super(DeviceResource, self).get_object_list(request, **kwargs)
#                return ret.filter(accountcode=ky)
                return super(DeviceResource, self).get_object_list(request, **kwargs).filter(accountcode=ky)
            if Extension.objects.filter(accountcode=ky).count() == 0:
                data_res = {'error': "have no sip account, let's create new one"}
                response = self.error_response(request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)



    def obj_create(self, bundle, **kwargs):
        req = ['uuid']
        data = bundle.data
        for value in req:
            if value not in data or data[value] == '' or is_valid_uuid(data[value]) == False:
                data_res = {'error': "%s is not valid" % value}
                response = self.error_response(bundle.request, data_res, response_class=HttpBadRequest)
                raise ImmediateHttpResponse(response=response)
        if Extension.objects.filter(extension_uuid=data['uuid']).count() > 0:
            data_res = {'error': "uuid doesn't exist, you cant create new one, please get sip account"}
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
            ext.domain_uuid = '09f10c29-9f49-4209-9050-52bd09d1886a'
            ext.accountcode = bundle.request.user
            if data.get('is_bell') == 'true':
                ext.description = 'is_bell'
            ext.save()
            from device.models import sync_extension_user
            sync_extension_user(ext.extension)
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
        if data.get('is_bell'):
            if data.get('is_bell') == 'true':
                obj.description = 'is_bell'
            else:
                obj.description = ''
        obj.save()
        from device.models import sync_extension_user
        sync_extension_user(obj.extension)
        return ret


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
