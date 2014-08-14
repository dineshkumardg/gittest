import sys
from django.conf import settings
from gaia.config.config import get_config


class GaiaAuthScheme:
    group_names = ['Administrators', 'QA', 'QAManagers', 'Browsers', 'Project Managers']
    permissions = [('can_manage', 'Can manage the QA process'),
                   ('can_qa',     'Can QA items'),
                   ('can_browse', 'Can browse the QA app')]

    def __init__(self):
        self.groups = {}
        self.perms = {}

    def create(self):
        self._create_perms()
        self._create_groups()

        self._add_perms_to_groups()
    
    def _create_perms(self):
        content_type, created = ContentType.objects.get_or_create(model = '', app_label = 'qa') # Do we want to tie these permissions to a specific model?!

        for codename, name in self.permissions:
            perm, created = Permission.objects.get_or_create(codename=codename, name=name, content_type=content_type)
            self.perms[codename] = perm

    def _create_groups(self):
        for group_name in self.group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            self.groups[group_name] = group
            
    def _add_perms_to_groups(self):
        # This makes QA people the same as QA Managers now.

        for group_name in 'QA', 'QAManagers':
            self.groups[group_name].permissions.add(self.perms['can_qa'])
            self.groups[group_name].permissions.add(self.perms['can_manage'])
        
        
class GaiaUsers:
    def add_admins(self, users):
        for username, first_name, last_name, email, password in users:
            user = self._create_user(username, first_name, last_name, email, password, is_admin=True)

            self._add_user_to_group(user, 'Administrators')

    def add_qa_users(self, users):
        for username, first_name, last_name, email, password in users:
            user = self._create_user(username, first_name, last_name, email, password)

            self._add_user_to_group(user, 'QA')

    def add_qa_managers(self, users):
        for username, first_name, last_name, email, password in users:
            user = self._create_user(username, first_name, last_name, email, password)

            self._add_user_to_group(user, 'QAManagers')

    def _create_user(self, username, first_name, last_name, email, password, is_admin=False):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist, e:
            user = User.objects.create_user(username=username, email=email, password=password)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)

        user.is_superuser = is_admin    # a Gaia Administrator gets both of these Django permissions.
        user.is_staff = is_admin

        user.save()
        return user

    def _add_user_to_group(self, user, group_name):
        group = Group.objects.get(name=group_name)   # Note: these must have already been created.

        user.groups.add(group)
        user.save()


    def dump(self, username):
        print '-' * 78
        print 'Details for', username
        print '-' * 78

        user = User.objects.get(username=username)
        print user.username, '(%s %s, %s)\n' % (user.first_name, user.last_name, user.email)

        if user.is_staff:
            print "is_staff"

        if user.is_superuser:
            print "is_superuser"

        print 'Groups:'
        for group in user.groups.all():
            print '\t', group.name

        print '\nPermissions:'
        for perm in user.get_all_permissions():
            print '\t', perm

        print


def setup_gaia_auth():
    admins = [('itadmin', 'IT', 'Admin', 'itadmin@cengage.com', '#55minor!'),
              ('jsears', 'James', 'Sears', 'james.sears@cengage.com', 'goodgod2'),
              ]

    qa =  [('chumphreys', 'Charlotte', 'Humphreys', 'charlotte.humphreys@cengage.com', 'ziggy12'),
            ('rturney', 'Rachel', 'Turney', 'rachel.turney@cengage.com', 'ziggy34'),
            ('lcarver', 'Lizzie', 'Carver', 'lizzie.carver@cengage.com', 'ziggy56'),
            ('vmccall', 'Victoria', 'McCall', 'victoria.mccall@cengage.com', 'ziggy78'),
            ('kmarcaccio', 'Kathy', 'Marcaccio', 'kathy.marcaccio@cengage.com', '1199'),
            ('kboyden', 'Karen', 'Boyden', 'karen.boyden@cengage.com', '3366'),
            ('sedgar', 'Susan', 'Edgar', 'susan.edgar@cengage.com', '7766'),
            ('csteinmetz', 'Carolyn', 'Steinmetz', 'carolyn.steinmetz@cengage.com', '9911'),
            ('lmaday', 'Lynne', 'Maday', 'lynne.maday@cengage.com', '2277'),
            ('jamiemendriss', 'Jamie', 'Endriss', 'jamiemendriss@aol.com', '5533'),
           ]

    qa_managers = [ ('roleary', 'Rose', "O'Leary", "rose.o'leary@cengage.com", 'ziggy123'),
                    ('sneate', 'Sarah', 'Neate', 'sarah.neate@cengage.com', 'ziggy345'), 
                    ('jdemowbray', 'Julia', 'Demowbray', 'julia.demowbray@cengage.com', 'cho1254'),
                    ('sbarker', 'Steve', 'Barker', 'steve.barker@cengage.com', 'sb432SB'),]

    testers = [('padavis', 'Paul', 'Davis', 'paul.davis@cengage.com', 'davedave'),
               ('kmarcaccio', 'Kathy', 'Marcaccio', 'kathy.marcaccio@cengage.com', 'km9872KM'),
               ]


    gaia_auth = GaiaAuthScheme()
    gaia_auth.create()

    users = GaiaUsers()
    users.add_admins(admins)

    # Note: We're keeping users separate, but they all get the same permissions for now.
    users.add_qa_users(qa)
    users.add_qa_managers(qa_managers)

    users.add_qa_users(testers)

    all_usernames = [x[0] for x in admins + qa + qa_managers + testers]
    for username in all_usernames:
        users.dump(username)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'USAGE:\n$ %s <config_name>' % __file__
        print 'e.g. $ %s TUSH_PC (or CHO_UAT, etc)' % __file__
        sys.exit()

    project_code = sys.argv[1]

    config = get_config(project_code)
    settings.configure(**config.get_django_settings())

    print 'USING config:\n%s\n' % str(config)


    from django.contrib.auth.models import Group, User, Permission, ContentType
    setup_gaia_auth()
