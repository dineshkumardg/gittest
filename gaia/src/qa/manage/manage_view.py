from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context import RequestContext


@login_required
@permission_required('qa.can_manage')
def manage_home(request):
    return render_to_response('qa/manage/manage.html', {}, context_instance=RequestContext(request))
