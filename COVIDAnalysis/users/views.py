from django.shortcuts import render,redirect
from auths.models import Authentications,States
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import prophet
from prophet.plot import plot_plotly
# Create your views here.

def index(request):
    if 'user_id' in request.session:
        return redirect('/user/wall')
    else:
        return render(request, '/')

def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['user_id']
        user = Authentications.objects.get(id=user_id)
        stob=user.state
        
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
            return render(request, 'users/userpage.html',context)
        else:
            data_error="State data hasnt been uploaded"
            context={
                'data_error':data_error,
                'st':st,
            }
            return render(request, 'users/userpage.html',context)

def reset(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session.clear()
        print("session has been cleared")
        return redirect("/")