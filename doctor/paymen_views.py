from django.http import Http404
from django.views.generic import View
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from doctor.payments import Payment
from doctor.models import PaymentModel, PaymentWorkCountry, Doctor


class DoctorRegisterPayment(View):
    def get(self, request, *args, **kwargs):
        doctor_country_payment = request.GET.get('doctor_country_payment')
        paymentWorkCountry = get_object_or_404(PaymentWorkCountry,id=doctor_country_payment)
        pay = Payment(
            amount=int(paymentWorkCountry.quantity*100),
            description="Qeydiyyat"
        )
        doctor_o = get_object_or_404(Doctor,user=request.user)
        if paymentWorkCountry.work_country==doctor_o.work_country:
            pass
        else:
            raise Http404
        base_obj = PaymentModel(
            user=request.user,
            reference=pay.reference,
            prize=paymentWorkCountry.quantity,
            description=pay.description,
        )
        base_obj.save()
        return redirect(pay.run())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DoctorRegisterPayment, self).dispatch(*args, **kwargs)


import datetime
from dateutil.relativedelta import relativedelta
class BasePaymentCheckView(View):
    error_template = 'accounts/success/success_index.html'
    def get(self, request):
        if request.GET.get('reference'):
            base = PaymentModel.objects.get(user=request.user,reference=request.GET.get('reference'))
            base.done = True
            pay = Payment(amount=int(base.prize*100),description="Qeydiyyat")
            base_obj = pay.check_status(request.GET.get('reference'))
            base.data = base_obj['data']
            base.status = base_obj['status']
            base.save()
            today = datetime.date.today()
            user = request.user
            if base.status:
                doctor_o = Doctor.objects.get(user=user)
                doctor_o.payment_status = base_obj['status']
                paymentWorkCountry = PaymentWorkCountry.objects.get(work_country=doctor_o.work_country,quantity=base.prize)
                if doctor_o.payment_date:
                    if doctor_o.payment_date <= today:
                        doctor_o.payment_date = today + relativedelta(months=paymentWorkCountry.month_count)
                    else:
                        doctor_o.payment_date = doctor_o.payment_date + relativedelta(months=paymentWorkCountry.month_count)
                    doctor_o.save()
                else:
                    doctor_o.payment_date = today + relativedelta(months=paymentWorkCountry.month_count)
                    doctor_o.save()
                return redirect(reverse('base:dashboard-payment-success'))
            else:
                messages.success(
                    request, 'Hörmətli %s Ödənişiniz uğursuz alındı' % request.user.get_full_name()
                )
                return render(request, self.error_template)
        else:
            messages.success(
                request, 'Hörmətli %s Ödənişiniz uğursuz alındı' % request.user.get_full_name()
            )
            return render(request, self.error_template)


class SponsorPayment(View):
    def get(self, request):
        if request.GET.get('money'):
            pay = Payment(
                amount=int(request.GET.get('money')),
                description="Sponsored"
            )
            base_obj = PaymentModel(
                user=request.user,
                reference=pay.reference,
                prize=int(request.GET.get('money'))/100,
                description=pay.description,
            )
            base_obj.save()
            return redirect(pay.run())
        else:
            raise Http404


class UserMeetPayment(View):
    def get(self, request):
        if request.GET.get('money'):
            pay = Payment(
                amount=int(request.GET.get('money')),
                description="Gorush"
            )
            base_obj = PaymentModel(
                user=request.user,
                reference=pay.reference,
                prize=int(request.GET.get('money'))/100,
                description=pay.description,
            )
            base_obj.save()
            return redirect(pay.run())
        else:
            raise Http404