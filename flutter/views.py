import envvars
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse 
from .models import Info
from .forms import InfoForm
from flutterwave import Flutterwave

# = envvars.get('FLUTTER_MERCHANT_KEY') 
# = envvars.get('FLUTTER_TEST_API_KEY')

FLUTTER_MERCHANT_KEY = 'tk_UiszH5RVYr' 
FLUTTER_TEST_API_KEY  = 'tk_V0DiBQAymY5ZkWJOnxPM'
# Create your views here.


def index(request):
	# now = timezone.now()
    form = InfoForm()


    if request.method == 'POST':
    	print 'posting!'
    	request.session['data'] = request.POST
    	bvn = int(request.POST['bvn'])
    	verifyUsing = request.POST['verifyUsing']
    	country = request.POST['country']
    	context_list = [bvn, verifyUsing, country]
        
        form = InfoForm(request.POST)

        if form.is_valid():
            print 'valid'
            save_it = form.save(commit=False)
	    save_it.save()
	    return HttpResponseRedirect(reverse('flutter:results'))
	else:
	    print 'Invalid'
	    print form.errors




    return render(request, 'flutter/index.html', {'form':form})

def results(request):
	# user = get_object_or_404(Info, pk=user_id)
	# flw  = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
	# rar = flw.bvn.verify("1111111111", "SMS", "NG")
	data = request.session['data']
	bvn = int(data['bvn'])
	verifyUsing = data['verifyUsing']
	country = data['country']
    
        r = {
		'data': {'firstName': 'Ope',
		'lastName': 'Onikute',
		'phone number': '08155718567',
		}
	}
	response = HttpResponse(request)
	print response
	response.write('<h2>Your BVN number has been verfied!</h2>')
	response.write('<h3>Your Details:</h3>')
	response.write('<p>'+r['data']['firstName']+ ' ' + r['data']['lastName'] + '</p>')
	response.write('<p>BVN:'+ str(bvn) + '</p>')
	

	return response

# class IndexView(generic.DetailView):
# 	model = Info
# 	template_name = 'flutter/index.html'

# 	def query_set(self):
# 		"""
# 		Excludes any users that arent published yet.
# 		"""
# 		form = InfoForm()
# 		return Info.objects.filter(pub_date__lte=timezone.now())
