from django.shortcuts import render,redirect,HttpResponse
from auths.models import Authentications,States
from templates import *
from django.core import mail
import os
from datetime import datetime
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import prophet
from prophet.plot import plot_plotly
# Create your views here.

def index(request):
    if 'user_id' in request.session:
        return redirect('/admin/wall')
    else:
        return render(request, '/')

def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        stname="India"
        st=States.objects.get(state=stname)
        print(st.data)
        state_list = States.objects.values()
        if st.data:
            state_data = pd.read_csv(st.data)
            test=round(int(state_data["Tested"].sum())/1000000,2)
            conf=round(int(state_data["Confirmed"].sum())/1000000,2)
            rec=round(int(state_data["Recovered"].sum())/1000000,2)
            death=round(int(state_data["Death"].sum())/1000000,2)
            fig1 = px.line(state_data, x="Date", y="Confirmed", color="State", title="Confirmed Cases")
            fig2 = px.line(state_data, x="Date", y="Tested", color="State", title="Covid Tested")
            fig3 = px.line(state_data, x="Date", y="Recovered", color="State", title="Recovered Cases")
            fig4 = px.line(state_data, x="Date", y="Death", color="State", title="Deaths")
            fig5 = px.line(state_data, x="Date", y="Active", color="State", title="Active Cases")
            fig6 = px.line(state_data, x="Date", y="Total Vaccinated", color="State", title="Total Vaccinated")

            gplot1 = plot(fig1,output_type='div')
            gplot2 = plot(fig2,output_type='div')
            gplot3 = plot(fig3,output_type='div')
            gplot4 = plot(fig4,output_type='div')
            gplot5 = plot(fig5,output_type='div')
            gplot6 = plot(fig6,output_type='div')
            
            context = {
                'state_list':state_list,
                'Tested':test,
                'Confirmed':conf,
                'Recovered':rec,
                'Death':death,
                'st':st,
                "plot_div1":gplot1,
                "plot_div2":gplot2,
                "plot_div3":gplot3,
                "plot_div4":gplot4,
                "plot_div5":gplot5,
                "plot_div6":gplot6,
            }
            return render(request, 'admins/adminpage.html',context)
        else:
            data_error="India data hasnt been uploaded"
            context={
                'data_error':data_error,
                'state_list':state_list
            }
            return render(request, 'admins/adminpage.html',context)

def approvalpage(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        accounts = Authentications.objects.filter(isAdmin=False).values()
        print(accounts)
        table_rows = []
        rows_dict = {}
        for x in range(len(accounts)):
            if accounts[x]['isApproved'] ==  False:
                id = accounts[x]['id']
                name = accounts[x]['name']
                email = accounts[x]['email']
                state = accounts[x]['state_id']
                rows_dict = {'id':id,'name':name,'email':email,'state':state}
                table_rows.append(rows_dict)
        
        return render(request, "admins/approvalpage.html", {'table_rows': table_rows})

def state(request,state):
        if 'user_id' not in request.session:
            return redirect('/')
        else:
            # user_id = request.session['user_id']
            # user = Authentications.objects.get(id=user_id)
            # stob=user.state

            stob=States.objects.get(state=state)
            print(stob)
            
            # print(stname)
            stname=stob.state
            st=States.objects.get(state=stname)
            print(st.data)

            #plotting covid data
            # covid_data= States.objects.all()
            if st.data:
                state_data = pd.read_csv(st.data)
                test=round(int(state_data["Tested"].sum())/1000000,2)
                conf=round(int(state_data["Confirmed"].sum())/1000000,2)
                rec=round(int(state_data["Recovered"].sum())/1000000,2)
                death=round(int(state_data["Death"].sum())/1000000,2)
                active=int(state_data.tail(1).Active)
                value=[test, conf, rec, death]
                name=['Tested', 'Confirmed', 'Recovered', 'Death']
                fig_pie = px.pie(names=name, values=value)
                fig=plot(fig_pie,output_type='div')
                # state_data = pd.read_csv('leave/DelhiCovidData.csv')
                date = list(state_data.Date)
                tested = list(state_data.Tested)
                confirmed = list(state_data.Confirmed)
                recovered = list(state_data.Recovered)
                fig1 = px.area(state_data, x="Date", y=["Confirmed", 'Tested'], title = 'Tested Vs Confirmed')
                fig2 = px.area(state_data, x = 'Date', y = ['Death', 'Recovered', 'Confirmed'], title = 'Confirmed, Recovered and Death')
                fig3 = px.area(state_data, x = 'Date', y = ['Active'], title = 'Active Cases')
                fig4 = px.area(state_data, x = 'Date', y = ['Total Vaccinated', 'Second Dose Vaccinated', 'First Dose Vaccinated'], title = 'Vaccination Details')
                fig5 = px.area(state_data, x = 'Date', y = ['Non-Vaccinated'], title = 'Not Vaccinated')
                fig6 = px.area(state_data, x = 'Date', y = ['Female Vaccinated', 'Male Vaccinated', 'Total Vaccinated'], title = 'Vaccination Details')
                fig7 = px.area(state_data, x = 'Date', y = ['Covaxin Doses', 'Covishield Doses'], title = 'No. of Covaxin and Covishield Doses')
                
                
                
                gplot1 = plot(fig1,output_type='div')
                gplot2 = plot(fig2,output_type='div')
                gplot3 = plot(fig3,output_type='div')
                gplot4 = plot(fig4,output_type='div')
                gplot5 = plot(fig5,output_type='div')
                gplot6 = plot(fig6,output_type='div')
                gplot7 = plot(fig7,output_type='div')
            

                dfn = state_data.iloc[: , [1,5]]
                dfn = dfn.rename(columns={'Date': 'ds', 'Death': 'y'})
                cd_prophet = prophet.Prophet(changepoint_prior_scale=0.15)
                cd_prophet.fit(dfn)
                cd_forecast = cd_prophet.make_future_dataframe(periods=61, freq='D')
                # Make predictions
                cd_forecast = cd_prophet.predict(cd_forecast)
                fig10 = plot_plotly(cd_prophet, cd_forecast).update_layout(xaxis_title="Date", yaxis_title="Death Count",title="Fatality Prediction")
                gplot10 = plot(fig10,output_type='div')

                dfa = state_data.iloc[: , [1,6]]
                dfa = dfa.rename(columns={'Date': 'ds', 'Active': 'y'})
                cda_prophet = prophet.Prophet(changepoint_prior_scale=0.15)
                cda_prophet.fit(dfa)
                cda_forecast = cda_prophet.make_future_dataframe(periods=15, freq='D')
                # Make predictions
                cda_forecast = cda_prophet.predict(cda_forecast)
                fig11 = plot_plotly(cda_prophet, cda_forecast).update_layout(xaxis_title="Date", yaxis_title="Active cases",title="Active Cases Prediction")
                gplot11 = plot(fig11,output_type='div')

                dfc = state_data.iloc[: , [1,3]]
                dfc = dfc.rename(columns={'Date': 'ds', 'Confirmed': 'y'})
                cdc_prophet = prophet.Prophet(changepoint_prior_scale=0.15)
                cdc_prophet.fit(dfc)
                cdc_forecast = cdc_prophet.make_future_dataframe(periods=61, freq='D')
                # Make predictions
                cdc_forecast = cdc_prophet.predict(cdc_forecast)
                fig12 = plot_plotly(cdc_prophet, cdc_forecast).update_layout(xaxis_title="Date", yaxis_title="Confirmed cases",title="Confirmed Cases Prediction")
                gplot12 = plot(fig12,output_type='div')
                context = {
                    'Tested':test,
                    'Confirmed':conf,
                    'Recovered':rec,
                    'Death':death,
                    'Active':active,
                    'st':st,
                    "plot_div1":gplot1,
                    "plot_div2":gplot2,
                    "plot_div3":gplot3,
                    "plot_div4":gplot4,
                    "plot_div5":gplot5,
                    "plot_div6":gplot6,
                    "plot_div7":gplot7,
                    "plot_div10":gplot10,
                    "plot_div11":gplot11,
                    "plot_div12":gplot12,
                    "plot_div":fig,
                }
                return render(request, 'admins/state.html',context)
            else:
                
                data_error="State data hasnt been uploaded"
                context={
                    'data_error':data_error,
                    'st':st,
                }
                return render(request, 'admins/state.html',context)

def accept_request(request):
    

    # Getting The PS No.
    # gen_id = Leave.objects.values_list('id', flat=True)
    # accepted_ps_no = int(request.GET['ps_no'])
    accepted_id = request.GET['id']
    details = Authentications.objects.filter(id=accepted_id).values()[0]
    acc_name = details["name"]
    acc_state = details["state_id"]
    acc_email = details["email"]
    Authentications.objects.filter(id = accepted_id).update(isApproved = True)
    try:
        print("mail sent")
    
        connection = mail.get_connection()
        connection.open()

        email1 = mail.EmailMessage(
        'Request Accepted',
        '''Dear {} 
            Your user creation request for state '{}' is accepted

            Thank you.'''.format(acc_name, acc_state),
        'proton01sam@proton.me',
        [acc_email],
        connection=connection,
        )
        email1.send() # Send the email
        print("hi leave request accepted")

        return redirect('/admin/approvalpage')
    except:
        print("connection error")
        return redirect('/admin/approvalpage')

def decline_request(request):
    

    # Getting The PS No.
    # gen_id = Leave.objects.values_list('id', flat=True)
    # accepted_ps_no = int(request.GET['ps_no'])
    accepted_id = request.GET['id']
    details = Authentications.objects.filter(id=accepted_id).values()[0]
    acc_name = details["name"]
    acc_state = details["state_id"]
    acc_email = details["email"]
    # Authentications.objects.filter(id = accepted_id).update(isApproved = True)
    
    #### Send Mail
    # try:
    #     print("mail sent")
    
    #     connection = mail.get_connection()
    #     connection.open()

    #     email1 = mail.EmailMessage(
    #     'Request Declined',
    #     '''Dear {} 
    #         Your user creation request for state '{}' is declined.

    #         Thank you.'''.format(acc_name, acc_state),
    #     'proton01sam@proton.me',
    #     [acc_email],
    #     connection=connection,
    #     )
    #     email1.send() # Send the email
    #     print("hi leave request accepted")

    #     return redirect('/admin/approvalpage')
    # except:
    #     print("connection error")
    #     return redirect('/admin/approvalpage')
    
def uploaddata(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        if request.method=='POST':
            
            state_name =request.POST.get('state')
            st = States.objects.get(state=state_name)
            print(st)
            if len(request.FILES) != 0:
                print(st.data)

                if st.data:
                    os.remove(st.data.path)
                    print(st.data)
                    print(request.FILES['data'])
                    print("_________yuioooooooooop______________________________________")
                st.data = request.FILES['data']
                print("__________________wertyu_____________________________")

                
            st.save()
            # messages.success(request, "Product Added Successfully")
        state_list = States.objects.values()
        context = {
            'state_list': state_list,
        }
        return render(request, 'admins/upload_data.html',context)

def reset(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session.clear()
        print("session has been cleared")
        return redirect("/")