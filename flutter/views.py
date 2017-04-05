import json, os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse 
from .models import Info
from .forms import InfoForm
from .utils import ErrorLogHelper
from flutterwave import Flutterwave

FLUTTER_MERCHANT_KEY = os.environ['FLUTTER_MERCHANT_KEY']
FLUTTER_TEST_API_KEY = os.environ['FLUTTER_TEST_API_KEY']


def index(request):

    form = InfoForm()

    if request.method == 'POST':
        request.session['data'] = dict(request.POST)

        try:
            print 'Updating'                                        # Check if the inputted value already exists...
            to_save = Info.objects.get(name=request.POST['name'])   # ...If you get an error, it doesnt and you should create a new info
            to_save.bvn = request.POST['bvn'] 
            to_save.verifyUsing = request.POST['verifyUsing']
            to_save.country = request.POST['country']
            to_save.save()
            print 'True'

        except Exception, e:
            ErrorLogHelper.log_error(e, 'index_view')

            form = InfoForm(request.POST)

            if form.is_valid():

                obj = Info()
                obj.name = form.cleaned_data['name']
                obj.bvn = form.cleaned_data['bvn']
                obj.verifyUsing = form.cleaned_data['verifyUsing']
                obj.country = form.cleaned_data['country']

                obj.save()

                # save_it = form.save(commit=False)
                # save_it.save()
            else:
                print 'Invalid'
                print form.errors
                return render(request, 'flutter/index.html', {'form':form})

        return HttpResponseRedirect(reverse('flutter:results'))

    return render(request, 'flutter/index.html', {'form':form})


def results(request):

    flw = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn'][0]
    verify_using = data['verifyUsing'][0]
    country = data['country'][0]

    rar = flw.bvn.verify(bvn, verify_using, country)
    json_dict = json.loads(rar.text)

    # json_dict = {
    #     'data':{
    #         'transactionReference':"FLW00293154",
    #         'responseMessage':"Successful, pending OTP validation",
    #         'responseCode':"00"
    #     },

    #     'status':'success'
    # }

    if json_dict['data']['responseCode'] != 'B01':

        try:
            transaction_reference = json_dict['data']['transactionReference']
            to_save = Info.objects.get(name=name_string)
            to_save.transactionReference = transaction_reference
            to_save.save(update_fields=['transactionReference'])

        except Exception, e:
            ErrorLogHelper.log_error(e, 'results_view')
        
        return HttpResponseRedirect(reverse('flutter:enter_otp' ))
    else:
        response = HttpResponse(request)
        response.write('<h2>The BVN number you entered is invalid.</h2>')
        response.write('<h3>Please enter a correct number, or check your internet connection.</h3>')
        # response.write('<p>'+r['data']['firstName']+ ' ' + r['data']['lastName'] + '</p>')
        # response.write('<p>BVN:'+ str(bvn) + '</p>')
        return response


def enter_OTP(request):

    flw = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})
    data = request.session['data']
    name_string = data['name'][0]
    bvn = data['bvn'][0]
    country = data['country'][0]

    try:
        to_save = Info.objects.get(name=name_string)
        transaction_reference = to_save.transactionReference

        if request.method == 'POST':
            otp = request.POST['OTP']
            r = flw.bvn.validate(bvn, otp, transaction_reference, country)
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

            if json_dict['status'] == 'success':
                status = 'success'

                if json_dict['data']['firstName'] is not None and json_dict['data']['lastName'] is not None:

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

                context = {
                    'status': status,
                    'name': name,
                    'phone_number': phone_number,
                    'sortcode': sortcode,
                    'bvn_no': bvn_no,
                }

                return render(request, 'flutter/results.html', context)

            else:
                request.session.flush()
                status = 'failed'
                context = {
                    'status': status,
                }
                return render(request, 'flutter/results.html', context)

    except Exception, e:

        ErrorLogHelper.log_error(e, 'enter_otp')

        request.session.flush()
        status = 'failed'
        context = {
            'status': status,
        }
        return render(request, 'flutter/results.html', context)

    return render(request, 'flutter/enterOTP.html')


def resend_OTP(request):

    flw = Flutterwave(FLUTTER_TEST_API_KEY, FLUTTER_MERCHANT_KEY, {'debug': True})

    data = request.session['data']
    name_string = data['name'][0]
    verify_using = data['verifyUsing'][0]
    country = data['country'][0]

    try:
        to_save = Info.objects.get(name=name_string)
        transaction_reference = to_save.transactionReference

        resend = flw.bvn.resendOtp(verify_using, transaction_reference, country)
        json_dict = json.loads(resend.text)

        if json_dict['status'] == 'success':
            return HttpResponseRedirect(reverse('flutter:results'))

    except Exception, e:
        ErrorLogHelper.log_error(e, 'resend_OTP')

    # resend = {
    #         'data':{
    #         'responsemessage':"Successful, pending OTP validation",
    #         'responscode':"00"
    #     },

    #     'status':'failed'
    # }

    return render(request, 'flutter/resend_failed.html')
