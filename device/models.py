import os
import syslog
import uuid, random, string
from django.utils.translation import get_language_from_request, ugettext_lazy as _
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models

# Create your models here.
from user.models import User, RingGroup

class Extension(models.Model):
    extension_uuid                 = models.CharField(max_length=256, primary_key=True)
    domain_uuid                    = models.CharField(max_length=256, blank=True, default=settings.DOMAIN_UUID)     
    extension                      = models.CharField(max_length=10, blank=True, unique=True)      
    number_alias                   = models.CharField(max_length=10, blank=True)      
    password                       = models.CharField(max_length=32, blank=True)      
    #accountcode                    = models.CharField(max_length=32, blank=True)      
    accountcode                    = models.ForeignKey(User, blank=True, null=True, db_constraint=False, db_column='accountcode')
    effective_caller_id_name       = models.CharField(max_length=128, blank=True)     
    effective_caller_id_number     = models.CharField(max_length=16, blank=True)      
    outbound_caller_id_name        = models.CharField(max_length=16, blank=True)      
    outbound_caller_id_number      = models.CharField(max_length=128, blank=True)     
    emergency_caller_id_name       = models.CharField(max_length=128, blank=True)     
    emergency_caller_id_number     = models.CharField(max_length=16, blank=True)      
    directory_first_name           = models.CharField(max_length=64, blank=True)      
    directory_last_name            = models.CharField(max_length=64, blank=True)      
    directory_visible              = models.CharField(max_length=8, blank=True, default='true')       
    directory_exten_visible        = models.CharField(max_length=8, blank=True, default='true')       
    limit_max                      = models.CharField(max_length=8, blank=True, default=5)       
    limit_destination              = models.CharField(max_length=64, blank=True, default='error/user_busy')       
    missed_call_app                = models.CharField(max_length=16, blank=True)      
    missed_call_data               = models.CharField(max_length=128, blank=True)     
    user_context                   = models.CharField(max_length=16, blank=True, default=settings.CONTEXT)      
    toll_allow                     = models.CharField(max_length=8, blank=True)       
    call_timeout                   = models.IntegerField(blank=True, default=30)
    call_group                     = models.CharField(max_length=32, blank=True)      
    call_screen_enabled            = models.CharField(max_length=8, blank=True, default='false')       
    user_record                    = models.CharField(max_length=8, blank=True)       
    hold_music                     = models.CharField(max_length=32, blank=True)      
    auth_acl                       = models.CharField(max_length=8, blank=True)       
    cidr                           = models.CharField(max_length=32, blank=True)      
    sip_force_contact              = models.CharField(max_length=32, blank=True)      
    nibble_account                 = models.IntegerField(blank=True)
    sip_force_expires              = models.IntegerField(blank=True)
    mwi_account                    = models.CharField(max_length=32, blank=True)   
    sip_bypass_media               = models.CharField(max_length=8, blank=True)    
    unique_id                      = models.IntegerField(blank=True)
    dial_string                    = models.CharField(max_length=128, blank=True)   
    dial_user                      = models.CharField(max_length=32, blank=True)   
    dial_domain                    = models.CharField(max_length=32, blank=True)   
    do_not_disturb                 = models.CharField(max_length=8, blank=True)    
    forward_all_destination        = models.CharField(max_length=8, blank=True)    
    forward_all_enabled            = models.CharField(max_length=8, blank=True)    
    forward_busy_destination       = models.CharField(max_length=8, blank=True)    
    forward_busy_enabled           = models.CharField(max_length=8, blank=True)    
    forward_no_answer_destination  = models.CharField(max_length=8, blank=True)    
    forward_no_answer_enabled      = models.CharField(max_length=8, blank=True)    
    forward_user_not_registered_destination = models.CharField(max_length=8, blank=True)
    forward_user_not_registered_enabled = models.CharField(max_length=8, blank=True)
    follow_me_uuid                 = models.UUIDField(blank=True)    
    enabled                        = models.CharField(max_length=8, blank=True, default='true')     
    description                    = models.CharField(max_length=128, blank=True)    
    forward_caller_id_uuid         = models.UUIDField(blank=True) 
    absolute_codec_string          = models.CharField(max_length=128, blank=True)    
    force_ping                     = models.CharField(max_length=8, blank=True)     

    def __unicode__(self):
        return "%s" % self.extension
    class Meta:
       managed = False
       db_table = 'v_extensions'


@receiver(models.signals.pre_save, sender=Extension)
def save_extension_fusionpbx_trigger(sender, instance, **kwargs):
    """
    delete temfile for app.lua recreate it again for login process.
    """
    tmp_dir = '/tmp/'
    file_name = tmp_dir + 'directory.%s@%s' % (instance.extension, settings.CONTEXT)
    try:
        os.remove(file_name)
    except:
        pass

    #sync_ring_group_user(instance.accountcode)
    return

DIALPLAN_XML = """<extension name="ring group" continue="" uuid="%s">           
        <condition field="destination_number" expression="^%s$">                                  
                <action application="ring_ready" data=""/>                                             
                <action application="set" data="ring_group_uuid=%s"/>
                <action application="lua" data="app.lua ring_groups"/>                                 
        </condition>                                                                                   
</extension>
"""
def sync_dialplan_rg(ri_gr_uuid):
    rg = RingGroup.objects.filter(ring_group_uuid=ri_gr_uuid)[0]
    if rg.ring_group_uuid:
        dialplan_uuid = rg.dialplan_uuid 
        syslog.syslog('process to create ring group in FusionPBX')
        if DialPlan.objects.filter(dialplan_uuid = dialplan_uuid).count() == 0:
            new_dialplan = DialPlan()
            new_dialplan.dialplan_uuid = dialplan_uuid
            new_dialplan.app_uuid = '1d61fb65-1eec-bc73-a6ee-a6203b4fe6f2'
            new_dialplan.dialplan_name = rg.ring_group_name
            new_dialplan.dialplan_number = rg.ring_group_extension
            new_dialplan.dialplan_xml = DIALPLAN_XML % (dialplan_uuid, rg.ring_group_extension, ri_gr_uuid)
            new_dialplan.save()
        tmp_dir = '/tmp/'
        file_name = tmp_dir + 'dialplan.%s' % (settings.CONTEXT)
        try:
            os.remove(file_name)
        except:
            pass
def sync_extension_user(exts):
    ext = Extension.objects.filter(extension=exts)[0]
    if ext.extension:
        tmp_dir = '/tmp/'
        file_name = tmp_dir + 'directory.%s@%s' % (ext.extension, settings.CONTEXT)
def sync_ring_group_user(user_id):
    if User.objects.filter(id=user_id).count() == 1:
        user = User.objects.filter(id=user_id)[0]
        if not user.ring_group_ext:
            rand_ring = random.randint(1000000,9999999)
            i = 0
            while i < 100000000:
                i += 1
                if User.objects.filter(ring_group_ext = rand_ring).count() == 0:
                    user.ring_group_ext = rand_ring
                    user.save()
                    break
        if user.ring_group_ext:
            syslog.syslog('process to create ring group in FusionPBX')
            # check or get ringgroup
            if RingGroup.objects.filter(ring_group_extension=user.ring_group_ext).count() == 0:
                dialplan_uuid = uuid.uuid4()
                ring_group_uuid = uuid.uuid4()
                n_rg = RingGroup()
                n_rg.ring_group_uuid = ring_group_uuid
                n_rg.ring_group_name = 'ringroup_%s' % user.id
                n_rg.ring_group_extension = user.ring_group_ext
                n_rg.dialplan_uuid =  dialplan_uuid
                n_rg.save()
            else:
                n_rg =  RingGroup.objects.filter(ring_group_extension=user.ring_group_ext)[0]
                dialplan_uuid = n_rg.dialplan_uuid
                ring_group_uuid = n_rg.ring_group_uuid
            if DialPlan.objects.filter(dialplan_uuid = dialplan_uuid).count() == 0:
                new_dialplan = DialPlan()
                new_dialplan.dialplan_uuid = dialplan_uuid
                new_dialplan.app_uuid = '1d61fb65-1eec-bc73-a6ee-a6203b4fe6f2'
                new_dialplan.dialplan_name = 'ringroup_%s' % user.id
                new_dialplan.dialplan_number = user.ring_group_ext
                new_dialplan.dialplan_xml = DIALPLAN_XML % (dialplan_uuid, user.ring_group_ext, ring_group_uuid)
                new_dialplan.save()
            # create destination for ringgroup
            for ext in Extension.objects.filter(accountcode__id=user.id):
                if ext.description == 'is_bell':
                    RingGroupDestination.objects.filter(destination_number=ext.extension, ring_group_uuid=ring_group_uuid).delete()
                elif RingGroupDestination.objects.filter(destination_number=ext.extension,ring_group_uuid=ring_group_uuid).count() == 0:
                    n_rg_dest = RingGroupDestination()
                    n_rg_dest.ring_group_uuid = ring_group_uuid
                    n_rg_dest.ring_group_destination_uuid = uuid.uuid4()
                    n_rg_dest.destination_number = ext.extension
                    n_rg_dest.save()
        # process to sync ringgroup 
        # remove dialplan xml
        tmp_dir = '/tmp/'
        file_name = tmp_dir + 'dialplan.%s' % (settings.CONTEXT)
        try:
            os.remove(file_name)
        except:
            pass


    else:
        syslog.syslog('user not found')


class RingGroupDestination(models.Model):
    ring_group_destination_uuid = models.UUIDField(blank=True,  primary_key=True)
    domain_uuid = models.UUIDField(blank=True, default=settings.DOMAIN_UUID)
   # ring_group_uuid = models.UUIDField(blank=True)
    ring_group_uuid = models.ForeignKey(RingGroup, blank=True, db_column='ring_group_uuid', to_field='ring_group_uuid')
   # destination_number = models.CharField(max_length=128, blank=True)
    destination_number = models.ForeignKey(Extension, blank=True, db_column='destination_number', to_field='extension')
    destination_delay = models.IntegerField(blank=True, default=0) 
    destination_timeout = models.IntegerField(blank=True, default=30) 
    destination_prompt = models.IntegerField(blank=True, default=None) 
   # def __str__(self):
   #     return str(self.destination_number)
    def __unicode__(self):
       return "%s" % self.destination_number

    class Meta:
       managed = False
       db_table = 'v_ring_group_destinations'

class DialPlan(models.Model):
    domain_uuid = models.UUIDField(blank=True, default=settings.DOMAIN_UUID)
    dialplan_uuid = models.UUIDField(blank=True,  primary_key=True)
    app_uuid = models.UUIDField(blank=True)
    hostname = models.CharField(max_length=128, blank=True, default=None)
    dialplan_context = models.CharField(max_length=128, blank=True, default=settings.CONTEXT)
    dialplan_name = models.CharField(max_length=128, blank=True)
    dialplan_number = models.CharField(max_length=128, blank=True)
    dialplan_continue = models.CharField(max_length=128, blank=True, default='false')
    dialplan_xml = models.TextField(blank=True)
    dialplan_order = models.IntegerField(blank=True, default=101)
    dialplan_enabled = models.CharField(max_length=128, blank=True, default='true')
    dialplan_description = models.CharField(max_length=128, blank=True)


    class Meta:
       managed = False
       db_table = 'v_dialplans'
