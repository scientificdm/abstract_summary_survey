import numpy as np
import streamlit as st

st.set_page_config(layout="wide")

fileNames = ["Verifiable", "Soft", "Non-verifiable"]
#%%
# Load segments:
segments = []

for f_name in fileNames:
    # Parse txt files with summaries:
    f = open("segments/"+f_name+"_segments.txt", "r")
    
    segmenttext = ""
    for line in f:
        try:
            if '>>>' in line:
                # memorize previous segment:
                if segmenttext != "":
                    segments.append(segmenttext.strip())
                    segmenttext = ""
            else:
                segmenttext += line
                    
        except ValueError:
            print('Invalid input:',line)
    
    # Memorize the last segment:
    segments.append(segmenttext.strip())
    
    f.close()

# Load summaries:
summaries = []

for f_name in fileNames:
    # Parse txt files with summaries:
    f = open("summaries/"+f_name+"_summaries_0.txt", "r")
     
    for line in f:
        try:
            if ('> ' in line) and (not '>>' in line):
                summaries.append([line.split("> ")[1].strip()])
        except ValueError:
            print('Invalid input:',line)
    
    f.close()

for i in range(1,4):
    count = 0
    for f_name in fileNames:
        # Parse txt files with summaries:
        f = open("summaries/"+f_name+"_summaries_"+str(i)+".txt", "r")
         
        for line in f:
            try:
                if ('> ' in line) and (not '>>' in line):
                    summaries[count].append(line.split("> ")[1].strip())
                    count+=1
            except ValueError:
                print('Invalid input:',line)
        
        f.close()
#%%
user = 0

with st.sidebar:
    # Split data according to user id
    st.text_input("ID de l'utilisateur : ", key="name")
    #user = st.selectbox('User id: ',[1,2,3,4,5,6,7])

    indexes = []
    if st.session_state.name != "":
        user = int(st.session_state.name)
    # Two users get 33 segments (user 1 and 7), the others receive 30 each
    
    #user = 1
    
    if user in list(range(1,8)):
        if (user == 1) or (user == 7):
            indexes = list(range(0,18))+list(range(93,108))
        elif (user == 2) or (user == 3):
            indexes = list(range(18,48))
        elif user == 4:
            indexes = list(range(48,78))
        elif user == 5:
            indexes = list(range(63,93))
        if user == 6:
            indexes = list(range(48,63))+list(range(78,93))

#st.write('**Segments:**')

if (user==1) or (user==7):
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18, tab19, tab20, tab21, tab22, tab23, tab24, tab25, tab26, tab27, tab28, tab29, tab30, tab31, tab32, tab33, tab34 = st.tabs([str(i) for i in list(range(1,34))]+["Envoyer les résultats"])
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18, tab19, tab20, tab21, tab22, tab23, tab24, tab25, tab26, tab27, tab28, tab29, tab30, tab34 = st.tabs([str(i) for i in list(range(1,31))]+["Envoyer les résultats"])

scores = np.zeros((len(indexes),4), int)

def displaySegment(i):
    if indexes != []:
        # Output segment:
        st.write('**Segment',i+1,' :**')
        #st.write(segments[indexes[i]])
        #st.markdown('<p style="color:Blue;">'+segments[indexes[i]]+'</p>', unsafe_allow_html=True)
        st.code(segments[indexes[i]])
        
        # 1st summary:
        st.write('**Portion de texte 1 :**')
        st.write(summaries[indexes[i]][0])
        option_1 = st.selectbox('Contient-elle suffisamment d’informations pour produire une règle (Y-Oui, N-No) ?',['N','Y'],key=i+100)
        if option_1=='Y':
            score_1 = st.selectbox('Classer cette portion de texte :',list(range(1,5)),key=str(i)+'a')
            #st.write('Vous avez sélectionné : ', score_1)
            scores[i][0] = score_1
        
        # 2nd summary:
        st.write('**Portion de texte 2 :**')
        st.write(summaries[indexes[i]][1])
        option_2 = st.selectbox('Contient-elle suffisamment d’informations pour produire une règle (Y-Oui, N-No) ?',['N','Y'],key=i+2000)
        if option_2=='Y':
            score_2 = st.selectbox('Classer cette portion de texte :',list(range(1,5)),key=str(i)+'b')
            #st.write('Vous avez sélectionné : ', score_2)
            scores[i][1] = score_2
        
        # 3rd summary:
        st.write('**Portion de texte 3 :**')
        st.write(summaries[indexes[i]][2])
        option_3 = st.selectbox('Contient-elle suffisamment d’informations pour produire une règle (Y-Oui, N-No) ?',['N','Y'],key=i+30000)
        if option_3=='Y':
            score_3 = st.selectbox('Classer cette portion de texte :',list(range(1,5)),key=str(i)+'c')
            #st.write('Vous avez sélectionné : ', score_3)
            scores[i][2] = score_3
        
        # 4th summary:
        st.write('**Portion de texte 4 :**')
        st.write(summaries[indexes[i]][3])
        option_4 = st.selectbox('Contient-elle suffisamment d’informations pour produire une règle (Y-Oui, N-No) ?',['N','Y'],key=i+400000)
        if option_4=='Y':
            score_4 = st.selectbox('Classer cette portion de texte :',list(range(1,5)),key=str(i)+'d')
            #st.write('Vous avez sélectionné : ', score_4)
            scores[i][3] = score_4
            
def outputResults():
    st.write('**Pour télécharger le fichier des résultats positionnez vous sur une colonne et choisissez la première icône comme dans l\'image ci-dessous :**')
    
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        st.write("")
    with col2:
        st.image('instruction.png')
    with col3:
        st.write("")
        
    st.write('**Ensuite, envoyez ce fichier à *maksim.koptelov (at) unicaen.fr*. Avant d\'envoyer le fichier n\'oubliez pas de vérifier les erreurs (en dessous du tableau)**')
    st.write(scores)
    
    option_err = st.selectbox('Vérifier les erreurs (Y-Oui, N-No) ?',['N','Y'],key='err')
    error = False
    if option_err == 'Y':
        count = 0
        while not error and count < len(indexes):
            tmp_list = sorted(scores[count])
            if (tmp_list != [0,0,0,0]) and (tmp_list != [0,0,0,1]) and (tmp_list != [0,0,1,2]) and (tmp_list != [0,1,2,3]) and (tmp_list != [1,2,3,4]):
                error = True
            count+=1
        if not error:
            st.write("Aucune erreur")
        else:
            st.write("Erreur dans le segment ",count)
    
with tab1:
    displaySegment(0)
    
with tab2:
    displaySegment(1)
    
with tab3:
    displaySegment(2)
    
with tab4:
    displaySegment(3)
    
with tab5:
    displaySegment(4)
    
with tab6:
    displaySegment(5)
    
with tab7:
    displaySegment(6)
    
with tab8:
    displaySegment(7)
    
with tab9:
    displaySegment(8)
    
with tab10:
    displaySegment(9)
    
with tab11:
    displaySegment(10)
    
with tab12:
    displaySegment(11)
    
with tab13:
    displaySegment(12)
    
with tab14:
    displaySegment(13)
    
with tab15:
    displaySegment(14)
    
with tab16:
    displaySegment(15)
    
with tab17:
    displaySegment(16)
    
with tab18:
    displaySegment(17)
    
with tab19:
    displaySegment(18)
    
with tab20:
    displaySegment(19)
    
with tab21:
    displaySegment(20)
    
with tab22:
    displaySegment(21)
    
with tab23:
    displaySegment(22)
    
with tab24:
    displaySegment(23)
    
with tab25:
    displaySegment(24)
    
with tab26:
    displaySegment(25)
    
with tab27:
    displaySegment(26)
    
with tab28:
    displaySegment(27)
    
with tab29:
    displaySegment(28)
    
with tab30:
    displaySegment(29)
    
if (user==1) or (user==7):
    with tab31:
        displaySegment(30)
    
    with tab32:
        displaySegment(31)
    
    with tab33:
        displaySegment(32)
        
    with tab34:
        outputResults()
        
elif user in [2,3,4,5,6]:
    with tab34:
        outputResults()
#%%
