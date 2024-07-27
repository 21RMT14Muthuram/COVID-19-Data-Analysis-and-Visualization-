
import pandas as pd
import streamlit as st
import plotly_express as px
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='COVID-19 Viruas',page_icon=':bar_chart:',layout='wide')

st.title('COVID-19 Protection')
# st.markdown("<style>div.block-container{padding-top: 3rem;}</style>",unsafe_allow_html=True)

uploaded_file=st.file_uploader(':file_folder: Browse your file covid ',type=(['csv','xlsx','text','xls']))

# Check if a file has been uploaded
if uploaded_file is not None:
    try:
        #read csv file
        if uploaded_file.type=='text/csv':
            df=pd.read_csv(uploaded_file)
        #Excel file
        elif uploaded_file.type=='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df=pd.read_excel(uploaded_file)
        else:
            pass

    except Exception as e:
        st.error(f'Sorry file type error :{e}')
else:
    st.stop()

st.write(df)
col1,col2=st.columns(2)
df['Date']=pd.to_datetime(df['Date'])

start=pd.to_datetime(df['Date']).min()
end=pd.to_datetime(df['Date']).max()
with col1:
    date1=pd.to_datetime(st.date_input('Start Date',start))

with col2:
    date2=pd.to_datetime(st.date_input('End ',end))

#Filter Date
df=df[(df['Date']>=date1) & (df['Date']<=date2)]

st.sidebar.header('Select Filter')


# Filter Region
regions = df['region'].unique()
selected_regions = st.sidebar.multiselect('Pick the Region:', regions)
if selected_regions:
    filter_df = df[df['region'].isin(selected_regions)]
else:
    filter_df = df

# Filter Country based on the selected regions
countries = filter_df['country'].unique()
selected_countries = st.sidebar.multiselect('Pick the Country:', countries)
if selected_countries:
    filter_df = filter_df[filter_df['country'].isin(selected_countries)]
else:
    pass



date_df=filter_df.groupby(by=['Date'],as_index=False)['deaths'].sum()


#Bar chart for filter data
with col1:
    st.subheader('Date wise Death rate')
    fig=px.bar(date_df,x='Date',y='deaths',              
               text=[i for i in date_df['deaths']],template='gridon')
    st.plotly_chart(fig,use_container_width=True)


#pie chart for filter data
with col2:
    st.subheader('Region wise Death rate')
    fig=px.pie(filter_df,values='deaths',names='region')
    fig.update_traces(text=filter_df['region'])
    st.plotly_chart(fig,use_container_width=True)


with col1:
    with st.expander('Date wise Death rate'):
        st.write(date_df.style.background_gradient(cmap='Blues'))
        csv=date_df.to_csv(index=False)
        st.download_button('Get File',data=csv,file_name='Date_wise_DeadRate')

with col2:
    with st.expander('Region wise Death rate'):
        reg=filter_df.groupby(by='region',as_index=False)['deaths'].sum()
        st.write(reg.style.background_gradient(cmap='gray'))
        csv=reg.to_csv(index=False)
        st.download_button('Get data',data=csv,file_name='Region_wise_DeadRate')


chart1,chart2=st.columns(2)
#Pie chart
with chart1:
    st.subheader('Region wise recovered')
    fig=px.pie(filter_df,values='recovered',names='region')
    fig.update_traces(text=filter_df['region'])
    st.plotly_chart(fig,use_container_width=True)

with chart1:
    with st.expander('Region wise recovered'):
        recover=filter_df.groupby(by='region',as_index=False)['recovered'].sum()
        st.write(recover.style.background_gradient(cmap='Blues'))
        csv=recover.to_csv(index=False)
        st.download_button('get data',data=csv,file_name='Region_wise_recovered')

with chart1:
    st.subheader('Region wise active')
    fig=px.pie(filter_df,values='active',names='region')
    fig.update_traces(text=filter_df['region'])
    st.plotly_chart(fig,use_container_width=True)

with chart1:
    with st.expander('Region wise active'):
        recover=filter_df.groupby(by='region',as_index=False)['active'].sum()
        st.write(recover.style.background_gradient(cmap='Blues'))
        csv=recover.to_csv(index=False)
        st.download_button('get data',data=csv,file_name='Region_wise_active')


# Create line plot using Plotly Express
with chart2:
    st.subheader('COVID-19 Data Over Time')
    fig = px.line(filter_df, x='Date', y=['confirmed', 'deaths', 'recovered'],
                  labels={'value': 'Count', 'variable': 'Metric'})
    st.plotly_chart(fig)

with chart2:
    with st.expander('Date wise Confirmed, Deaths, Recovered'):
        data=filter_df.groupby(by='Date',as_index=False)[['confirmed','deaths','recovered']].sum()
        st.write(data)


with chart2:
    # Create scatter plot using Plotly Express
    st.subheader('Scatter Plot of Confirmed Cases vs Deaths')
    fig = px.scatter(df,x='confirmed', y='deaths', size='recovered', color='active', hover_name='country',
                     labels={
                         'confirmed': 'Confirmed Cases',
                         'deaths': 'Deaths',
                         'recovered': 'Recovered Cases',
                         'active': 'Active Cases'
                     }) 
                         # Display plot in Streamlit
    st.plotly_chart(fig)

with chart2:
    with st.expander('Confirmed and DeathRate'):
        data=filter_df.groupby(by='confirmed',as_index=False)[['deaths','recovered']].sum()
        st.write(data)


#scatter plot
st.subheader('Treemap of COVID-19 Data')
st.write("This treemap shows the distribution of confirmed cases by country and region.")

# Create treemap using Plotly Express
fig = px.treemap(df, path=['region', 'country'], values='confirmed', 
                 color='active', hover_data=['deaths', 'recovered'],
                 labels={'confirmed': 'Confirmed Cases',
                         'active': 'Active Cases',
                          'deaths': 'Deaths',
                          'recovered': 'Recovered Cases'},
                          title='Treemap of Confirmed Cases by Region and Country')

# Display plot in Streamlit
st.plotly_chart(fig)



