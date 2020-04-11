import streamlit as st 
import joblib,os
import spacy
nlp = spacy.load('en_core_web_sm')
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from summarizer import Summarizer
import folium
import numpy as np
#st.markdown(html,unsafe_allow_html=True,style = "background-color:Black")


st.markdown("""
<style>
body {

    color: #fff;
    background-color: #070757;
    
    etc. 
}
</style>

    
    """, unsafe_allow_html=True)

    
st.sidebar.markdown("""
<style>
body {

    color: #fff;
    background-color: #070757;
    
    etc. 
}
</style>

    
    """, unsafe_allow_html=True)
    

    #111 for black background and fff for white letters
from spacy import displacy
HTML_WRAPPER = """div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


#summary pkgs
from gensim.summarization import summarize

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def sumy_summarizer(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

#Bert
def bert_summary(docx):
    model = Summarizer()
    result = model(docx, min_length=60)
    full = ''.join(result)
    return full

# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime


#NLP
#@st.cache(allow_output_mutation=True)
def analyze_text(text):
    return nlp(text)

#webscrapping pkgs
from bs4 import BeautifulSoup
from urllib.request import urlopen

@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text




def main():
    
    
    st.title("Summary Generator and Entity checker")
    activities = ["Summarize","Summarize for URL","NER Checker","NER for URL"]
    choice = st.sidebar.selectbox("Select Activity",activities)

    
    if choice == 'Summarize':
        st.subheader("Summary with NLP")
        raw_text = st.text_area("Enter Text Here")
        #summary_choice = st.selectbox("Summary Choice",["Gensim","Sumy Lex Rank"])
        if st.button("Summarize"):
            summary_result = bert_summary(raw_text)
            st.write(summary_result)

            #if summary_choice == 'Gensim':
                #summary_result = summarize(raw_text)
            #elif summary_choice == 'Sumy Lex Rank':
        
        if st.button("WordCloud"):
            c_text = raw_text
            wordcloud = WordCloud().generate(c_text)
            plt.imshow(wordcloud,interpolation='bilinear')
            plt.axis("off")
            st.pyplot()
            #if raw_url != "Type here":
                #result = get_text(raw_text)
    #st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 10px 16px; background: #7f78d2; color: #f1f1f1; position:fixed;top:0;} .sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader">'+str('Summarator')+'</div>', unsafe_allow_html=True)            
            
    if choice == 'NER Checker':
        st.subheader("Entity Recognition with Spacy")
        raw_text = st.text_area("Enter Text Here","Type Here")
        if st.button("Analyze"):
            # NLP
            docx = analyze_text(raw_text)
            html = displacy.render(docx,style='ent')
            html = html.replace("\n\n","\n")
            st.write(html,unsafe_allow_html=True)
            #st.markdown(html,unsafe_allow_html=True)
        if st.button("WordCloud"):
            c_text = raw_text
            wordcloud = WordCloud().generate(c_text)
            plt.imshow(wordcloud,interpolation='bilinear')
            plt.axis("off")
            st.pyplot()
        
    if choice == 'NER for URL':
        st.subheader("Analyze text from URL")
        raw_url = st.text_input("Enter URL","Type here")
        text_length = st.slider("Length to Preview",50,100)
        if st.button("Extract"):
            if raw_url != "Type here":
                result = get_text(raw_url)
                estimatedTime_org = readingTime(result)
                
                st.info("Original Reading time::{}".format(estimatedTime_org))
                len_of_full_text = len(result)
                len_of_short_text = round(len(result)/text_length)
                #st.info("Length::Full Text::{}".format(len_of_full_text))
                #   st.info("Length::Short Text::{}".format(len_of_short_text))
                st.write(result[:len_of_short_text])
                summary_docx = sumy_summarizer(result)
                docx = analyze_text(summary_docx)
                html = displacy.render(docx,style='ent')
                html = html.replace("\n\n","\n")
                st.write(html,unsafe_allow_html=True)
                estimatedTime_sum = readingTime(summary_docx)
                st.info("Summary Reading time::{}".format(estimatedTime_sum))
                #st.markdown(html,unsafe_allow_html=True)
        if st.button("WordCloud"):
            if raw_url != "Type here":
                result = get_text(raw_url)
                c_text = result
                wordcloud = WordCloud().generate(c_text)
                plt.imshow(wordcloud,interpolation='bilinear')
                plt.axis("off")
                st.pyplot()
                
    if choice == 'Summarize for URL':
        st.subheader("Analyze text from URL")
        raw_url = st.text_input("Enter URL","Type here")
#        text_length = st.slider("Length to Preview",50,100)
        if st.button("Summarize"):
            if raw_url != "Type here":
                result = get_text(raw_url)
#                len_of_full_text = len(result)
 #               len_of_short_text = round(len(result)/text_length)
  #              st.info("Length::Full Text::{}".format(len_of_full_text))
   #             st.info("Length::Short Text::{}".format(len_of_short_text))
    #            st.write(result[:len_of_short_text])
                summary_result = sumy_summarizer(result)
                st.write(summary_result)
        if st.button("WordCloud"):
            if raw_url != "Type here":
                result = get_text(raw_url)
                cloud_mask = np.array(Image.open("cloud.png"))
                c_text = result
                wordcloud = WordCloud(max_font_size=50,background_color = 'white', max_words=600).generate(c_text)
                #, mask = cloud_mask
                plt.imshow(wordcloud,interpolation='bilinear')
                plt.axis("off")
                st.pyplot()
    


    

if __name__ == '__main__':
    main()
    
