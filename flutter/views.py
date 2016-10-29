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
        request.session['data'] = dict(request.POST)
        bvn = int(request.POST['bvn'])
        verifyUsing = request.POST['verifyUsing']
        country = request.POST['country']
        context_list = [bvn, verifyUsing, country]
        
        form = InfoForm(request.POST)
        print form.as_p()

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
    flw  = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn']
    verifyUsing = data['verifyUsing']
    country = str(data['country'])
    rar = flw.bvn.verify(bvn, verifyUsing, country)
    # rar = {
    #     'data':{
    #         'transactionReference':"FLW00293154",
    #         'responseMessage':"Successful, pending OTP validation",
    #         'responseCode':"00"
    #     },

    #     'status':'success'
    # }

    if rar['status'] == 'success':
        transactionReference = rar['data']['transactionReference']
        # resend the BVN OTP, retaining the previous variables, only new variable is transactionReference
        to_save = Info.objects.get(name=name_string)
        to_save.transactionReference = transactionReference
        to_save.save(update_fields=['transactionReference'])
        
        return HttpResponseRedirect(reverse('flutter:enter_otp' ))
    else:
        r = {
        'data': {'firstName': 'Ope',
        'lastName': 'Onikute',
        'phone number': '08155718567',
        }
        }
        response = HttpResponse(request)
        response.write('<h2>Your BVN verification failed.</h2>')
        response.write('<h3>Please enter a correct number, or check your internet connection.</h3>')
        # response.write('<p>'+r['data']['firstName']+ ' ' + r['data']['lastName'] + '</p>')
        # response.write('<p>BVN:'+ str(bvn) + '</p>')
    

    return response

# the flow is enter BVN --> enter OTP (with resend OTP) --> Show final Details

def enter_OTP(request):
    flw  = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn']
    verifyUsing = data['verifyUsing']
    country = data['country']
    
    to_save = Info.objects.get(name=name_string)
    transactionReference = to_save.transactionReference
    
    if request.method == 'POST':
        OTP = int(request.POST['OTP'])
        r = flw.bvn.validate(bvn, otp, transactionReference, country)
        # r = {
        # 'data': {
        #     'firstName':'Ope',
        #     'lastName':'Onikute',
        #     'phoneNumber':'08155718567',
        #     'enrollmentBank':'044',
        #     'bvn':'11111111111',
        #     'responseMessage':'Completed successfully',         
        # },
        # 'status':'success'
        # }
        
        if r['status']=='success':
            status = 'success'
            name = r['data']['firstName'] + ' ' + r['data']['lastName']
            phone_number = r['data']['phoneNumber']
            sortcode = r['data']['enrollmentBank']
            bvn_no = r['data']['bvn']
            # response = HttpResponse()
            # response.write('<h2>You have successfully validated your BVN!</h2><br>')
            # response.write('<h3>Your bank details are:</h3><br>')
            # response.write('<h4>Name</h4>')
            # response.write('<p>' + r['data']['firstName'] + ' ' + r['data']['lastName'] + '</p><br>')
            # response.write('<h4>Phone Number</h4>')
            # response.write('<p>' + r['data']['phoneNumber'] + '</p><br>')
            # response.write('<h4>Bank sort code</h4>')
            # response.write('<p>' + r['data']['enrollmentBank'] + '</p><br>')
            # response.write('<h4>BVN number</h4>')
            # response.write('<p>' + r['data']['bvn'] + '</p><br>')
            # return response

            context = {
            'status':status,
            'name':name, 
            'phone_number':phone_number,
            'sortcode':sortcode,
            'bvn_no':bvn_no, 
            }

            return render(request, 'flutter/results.html', context)


        else:
            status = 'failed'
            context = {
            'status':status,
            }
            response.write('<p>BVN validation failed, please try again.</p>')
            response.write('<a href ={% url "flutter:results" %}>Back</a>')
            return render(request, 'flutter/results.html', context)




    return render(request, 'flutter/enterOTP.html')

def resend_OTP(request):
    flw  = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn']
    verifyUsing = data['verifyUsing']
    country = data['country']
    to_save = Info.objects.get(name=name_string)
    transactionReference = to_save.transactionReference
    
    
    resend = flw.resendOtp(verifyUsing, transactionReference, country)
    # resend = {
    #         'data':{
    #         'responsemessage':"Successful, pending OTP validation",
    #         'responscode':"00"
    #     },

    #     'status':'failed'
    # }

    if resend['status'] == 'success':
        return HttpResponseRedirect(reverse('flutter:results'))

    else:
        return render(request, 'flutter/resend_failed.html')



