import envvars
import json
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
        bvn = request.POST['bvn'] 
        verifyUsing = request.POST['verifyUsing']
        country = request.POST['country']
        context_list = [bvn, verifyUsing, country]
        
        try:
            print 'Updating'                                        #Check if the inputted value already exists...
            to_save = Info.objects.get(name=request.POST['name'])   #...If you get an error, it doesnt and you should create a new info
            to_save.bvn = request.POST['bvn'] 
            to_save.verifyUsing = request.POST['verifyUsing']
            to_save.country = request.POST['country']
            to_save.save()
            print 'True'
        except Exception as e:
            print e
            form = InfoForm(request.POST)
            if form.is_valid():
                print 'valid'
                save_it = form.save(commit=False)
                save_it.save()
            else:
                print 'Invalid'
                print form.errors
        return HttpResponseRedirect(reverse('flutter:results'))




    return render(request, 'flutter/index.html', {'form':form})

def results(request):
    # user = get_object_or_404(Info, pk=user_id)
    flw  = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn'][0]
    verifyUsing = data['verifyUsing'][0]
    country = data['country'][0]
    # rar = flw.bvn.verify(bvn, verifyUsing, country)
    # json_dict = json.loads(rar.text)
    json_dict = {
        'data':{
            'transactionReference':"FLW00293154",
            'responseMessage':"Successful, pending OTP validation",
            'responseCode':"00"
        },

        'status':'success'
    }

    if json_dict['data']['responseCode'] != 'B01':
        transactionReference = json_dict['data']['transactionReference']
        to_save = Info.objects.get(name=name_string)
        to_save.transactionReference = transactionReference
        to_save.save(update_fields=['transactionReference'])
        
        return HttpResponseRedirect(reverse('flutter:enter_otp' ))
    else:
        response = HttpResponse(request)
        response.write('<h2>The BVN number you entered is invalid.</h2>')
        response.write('<h3>Please enter a correct number, or check your internet connection.</h3>')
        # response.write('<p>'+r['data']['firstName']+ ' ' + r['data']['lastName'] + '</p>')
        # response.write('<p>BVN:'+ str(bvn) + '</p>')
        return response

# the flow is enter BVN --> enter OTP (with resend OTP) --> Show final Details

def enter_OTP(request):
    flw  = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn'][0]
    verifyUsing = data['verifyUsing'][0]
    country = data['country'][0]
    
    to_save = Info.objects.get(name=name_string)
    transactionReference = to_save.transactionReference
    # print transactionReference
    
    if request.method == 'POST':
        otp = request.POST['OTP']
        r = flw.bvn.validate(bvn, otp, transactionReference, country)
        json_dict = json.loads(r.text)
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
        
        if json_dict['status']=='success':
            status = 'success'
            if json_dict['data']['firstName'] != None and json_dict['data']['lastName']!= None:
                status = 'Thankyou for using flutterbvn!'
                name = json_dict['data']['firstName'] + ' ' + json_dict['data']['lastName']
                phone_number = json_dict['data']['phoneNumber']
                sortcode = json_dict['data']['enrollmentBank']
                bvn_no = json_dict['data']['bvn']
            else:
                status = 'Something went wrong. Please try again.'
                name = 'Sample name'
                phone_number = '081XXXXXXXXX'
                sortcode = 'XXXX'
                bvn_no = 'XXXXXXXXXXX'
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
            request.session.flush()
            status = 'failed'
            context = {
            'status':status,
            }
            return render(request, 'flutter/results.html', context)




    return render(request, 'flutter/enterOTP.html')

def resend_OTP(request):
    flw  = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn'][0]
    verifyUsing = data['verifyUsing'][0]
    country = data['country'][0]
    to_save = Info.objects.get(name=name_string)
    transactionReference = to_save.transactionReference
    
    
    resend = flw.resendOtp(verifyUsing, transactionReference, country)
    json_dict = resend.loads(r.text)
    # resend = {
    #         'data':{
    #         'responsemessage':"Successful, pending OTP validation",
    #         'responscode':"00"
    #     },

    #     'status':'failed'
    # }

    if json_dict['status'] == 'success':
        return HttpResponseRedirect(reverse('flutter:results'))

    else:
        return render(request, 'flutter/resend_failed.html')


