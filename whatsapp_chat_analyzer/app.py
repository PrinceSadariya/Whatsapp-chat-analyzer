import streamlit as st
import preprocessor,helper
import  matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.write(data)

    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Group')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to",user_list)

    if st.sidebar.button("Show Analysis"):

        total_messages,total_words,total_media_messages,num_links = helper.fetch_stats(selected_user,df)

        st.title("Top Stats")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(total_messages)

        with col2:
            st.header("Total Words")
            st.title(total_words)

        with col3:
            st.header("Media Shared")
            st.title(total_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #monthly timeline
        monthly_timeline = helper.monthly_timeline(selected_user,df)

        st.title("Monthly Timeline")

        fig,ax = plt.subplots()
        ax.plot(monthly_timeline['time'],monthly_timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        daily_timeline = helper.daily_timeline(selected_user, df)

        st.title("Daily Timeline")

        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # activity heat map

        user_heatmap = helper.activity_heatmap(selected_user,df)

        st.title("Weekly Activity Map")
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding busiest user
        if selected_user == 'Overall':

            st.title("Most Busy Users")

            busy_users,message_percent = helper.fetch_most_busy_users(df)

            fig,ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(busy_users.index,busy_users.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(message_percent)

        # wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)

        st.pyplot(fig)

        # most common words

        most_common_word_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_word_df[0],most_common_word_df[1])
        # plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        # st.dataframe(most_common_word_df)