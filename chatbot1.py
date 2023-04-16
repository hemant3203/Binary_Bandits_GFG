from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog
import spacy



nlp = spacy.load('en_core_web_sm')


class Chatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")
        self.root.geometry("730x620+0+0")
        self.root.bind('<Return>',self.enter_fun)

        main_frame = Frame(self.root, bd=4, bg="powder blue", width=610)
        main_frame.pack()

        img_chat = Image.open("C:/Users/hp/Desktop/healthcare chatbot/th.jpeg")
        img_chat = img_chat.resize((200, 70), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img_chat)


        title_lbl = Label(main_frame, bd=3, relief=RAISED, anchor='center', width=730, compound=LEFT, 
                          image=self.photoimg, text="Dr.Sophia", font=("arial", 30, "bold"), bg="white", fg="green")

        title_lbl.pack(side=TOP)
        
        self.scroll_y=ttk.Scrollbar(main_frame,orient=VERTICAL)
        self.text=Text(main_frame,width=65,height=20,bd=3,relief=RAISED,font=('arial',14),yscrollcommand=self.scroll_y.set)
        self.scroll_y.pack(side=RIGHT,fill=Y)
        self.text.pack()

        btn_frame=Frame(self.root,bd=4,bg='white',width=730)
        btn_frame.pack()

        label_text = Label(btn_frame, text="Type Something", font=('arial','14','bold'), fg='green', bg='white')
        label_text.grid(row=0, column=0, padx=5, sticky=W)


        #self.entry=StringVar
        self.entry=ttk.Entry(btn_frame,width=40 ,font=('arial ','14','bold'))
        self.entry.grid(row=0,column=1,padx=5,sticky=W)

        self.send=Button(btn_frame,text="SEND>>",command=self.send, font=('arial','16','bold'),width=8,bg='green')
        self.send.grid(row=0, column=2, padx=5, sticky=W)
        

        self.clear=Button(btn_frame,text="Clear",font=('arial','16','bold'),width=8,bg='red',fg='white')
        self.clear.grid(row=1, column=0, padx=5, sticky=W)
        
        self.msg=''
        self.label_11 = Label(btn_frame, text=self.msg, font=('arial','14','bold'), fg='red', bg='white')
        self.label_11.grid(row=1, column=1, padx=5, sticky=W)


        #function


    def enter_fun(self,event):
        self.send.invoke()
        #self.entry1.set('')


    def send(self):
        send='\t\t\t'+'You: '+self.entry.get()
        self.text.insert(END,'\n'+send)

    #def clear_fun(self):
        
        #self.text.delete('1.0',END)
        #self.entry.set('')


    
    

    

        if self.entry.get()=='':
            self.msg='Please enter some input'
            self.label_11.config(text=self.msg,fg='red')
        else:
            self.msg=''
            #self.label_11.config(text=self.msg,fg='red')

        doc = nlp(self.entry.get().lower())
        for ent in doc.ents:
            if ent.label_ == 'CONDITION' or ent.label_ == 'SYMPTOM':
                self.text.insert(END, f"\n\nDr.Sophia: {ent.text} is a {ent.label_}. Would you like more information about it?")
        
        if 'medication' in [tok.text for tok in doc]:
            for ent in doc.ents:
                if ent.label_ == 'MEDICATION':
                    medication_name = ent.text
                    self.text.insert(END, f"\n\nDr.Sophia: What would you like to know about {medication_name}?")

        if 'appointment' in [tok.text for tok in doc]:
            self.text.insert(END, f"\n\nDr.Sophia: Sure, what type of appointment would you like to schedule?")

        if self.entry.get()=='':
            self.msg='Please enter some input'
            self.label_11.config(text=self.msg,fg='red')
        else:
            self.msg=''
            self.label_11.config(text=self.msg,fg='red')

        if self.entry.get().lower() == 'hello':
            self.text.insert(END, '\n\n' + 'Dr.Sophia: Hello! How can I assist you with your health today?')

        elif 'what are the side effects of' in self.entry.get().lower():
    # Extract the medication name from the input string
            medication_name = self.entry.get().lower().replace('what are the side effects of', '').strip('?')
            self.text.insert(END, f'\n\nDr.Sophia: The most common side effects of {medication_name} include [list of side effects]. However, it\'s important to speak with your doctor or pharmacist about any concerns you have regarding your medication.')
        elif 'corona' in self.entry.get().lower() or 'covid' in self.entry.get().lower():
    # List some common symptoms
            symptoms = ['1. fever\n' '2. cough\n' '3. shortness of breath\n' '4. fatigue\n' '5. body aches\n' '6. loss of taste or smell']
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of COVID-19 include:\n{", ".join(symptoms)}.')
    
    # List some possible causes
            causes = ['exposure to the SARS-CoV-2 virus', 'contact with infected individuals', 'travel to areas with high infection rates']
            causes_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: COVID-19 is caused by:\n{causes_list}.')

            
    
    # List some possible treatments and preventive measures
            cures = ['Getting vaccinated', 'Quarantining and isolating', 'Taking prescribed medication', 'Drinking plenty of fluids', 'Getting rest and sleep', 'Using a humidifier or taking hot showers to relieve symptoms', 'Seeking medical attention if symptoms worsen']
            cures_list = "\n".join([f"{i}. {cure}" for i, cure in enumerate(cures, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Some possible cures for COVID-19 include:\n{cures_list}.')

        elif 'what are some ways to manage' in self.entry.get().lower():
    # Extract the medical condition from the input string
            medical_condition = self.entry.get().lower().replace('what are some ways to manage', '').strip('?')
            self.text.insert(END, f'\n\nDr.Sophia: Some ways to manage {medical_condition} at home include [list of management strategies]. However, it\'s important to speak with your doctor to determine the best course of treatment for your specific condition.')
        

        elif 'tuberculosis' in self.entry.get().lower() or 'tb' in self.entry.get().lower():
    # Define tuberculosis
            definition = 'Tuberculosis (TB) is a bacterial infection that primarily affects the lungs, but can also affect other parts of the body.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Cough (that lasts for 3 or more weeks)\n' '2. Chest pain\n' '3. Fatigue\n' '4. Fever\n' '5. Night sweats\n' '6. Weight loss']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of TB include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Exposure to the bacteria that causes TB', 'Weak immune system', 'HIV/AIDS', 'Poor living conditions', 'Close contact with someone who has TB']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Causes of TB include:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Antibiotics', 'Vaccines (such as the BCG vaccine)', 'Isolation', 'Good nutrition', 'Rest and sleep']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for TB include:\n{treatment_list}. It is important to complete the full course of antibiotics as prescribed by your doctor in order to avoid developing drug-resistant TB.')
        

        elif 'anxiety' in self.entry.get().lower():
    # Define anxiety
            definition = 'Anxiety is a feeling of unease, such as worry or fear, that can be mild or severe. It is a natural response to stress or danger, but for some people it can become excessive or persistent, and can interfere with daily activities.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Nervousness, restlessness or tension\n' '2. A sense of impending danger, panic or doom\n' '3. Rapid heart rate, palpitations or sweating\n' '4. Trembling or shaking\n' '5. Shortness of breath or a feeling of choking\n' '6. Insomnia or sleep disturbances\n' '7. Gastrointestinal problems\n' '8. Fatigue or weakness']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of anxiety include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Genetics\n', 'Brain chemistry\n', 'Environmental stressors\n', 'Trauma\n', 'Substance abuse\n']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Causes of anxiety can include:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Therapy (such as cognitive-behavioral therapy or exposure therapy)\n', 'Medications (such as antidepressants or anti-anxiety drugs)\n', 'Relaxation techniques (such as deep breathing or yoga)\n', 'Regular exercise\n', 'Avoiding caffeine and alcohol\n', 'Getting enough sleep']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for anxiety include:\n{treatment_list}. It is important to speak with your healthcare provider to determine the best course of treatment for your specific needs.')
        


        elif 'hypertension' in self.entry.get().lower() or 'high blood pressure' in self.entry.get().lower():
    # Define hypertension
            definition = 'Hypertension, also known as high blood pressure, is a chronic medical condition in which the blood pressure in the arteries is elevated.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Headaches\n' '2. Shortness of breath\n' '3. Dizziness\n' '4. Chest pain\n' '5. Irregular heartbeat\n' '6. Vision problems']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of hypertension include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Unhealthy diet', 'Lack of physical activity', 'Obesity', 'Smoking', 'Stress', 'Genetics']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Causes of hypertension include:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Medications (such as diuretics, beta-blockers, or ACE inhibitors)', 'Lifestyle changes (such as exercise, weight loss, and a healthy diet)', 'Reducing stress', 'Limiting alcohol intake', 'Quitting smoking']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for hypertension include:\n{treatment_list}. It is important to manage hypertension to prevent serious health problems such as heart disease and stroke.')
        

        elif 'stroke' in self.entry.get().lower():
    # Define stroke
            definition = 'A stroke occurs when blood flow to the brain is disrupted, causing brain cells to die.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Sudden numbness or weakness in the face, arm, or leg (especially on one side of the body)\n',
                '2. Sudden confusion, trouble speaking or understanding speech\n',
                '3. Sudden trouble seeing in one or both eyes\n',
                '4. Sudden trouble walking, dizziness, loss of balance or coordination\n',
                '5. Sudden severe headache with no known cause']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of stroke include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Blood clot in a blood vessel in the brain', 'Ruptured blood vessel in the brain (hemorrhagic stroke)',
              'Narrowing or blockage of a blood vessel in the brain', 'Atrial fibrillation (a type of irregular heartbeat)',
              'High blood pressure, high cholesterol, smoking, diabetes, and other risk factors']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Causes of stroke include:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Clot-busting drugs (if the stroke is caused by a blood clot)',
                  'Surgery or medical procedures (if the stroke is caused by a ruptured blood vessel or blockage)',
                  'Rehabilitation therapy (to help regain lost skills or learn new ways to do things)',
                  'Lifestyle changes (such as quitting smoking, eating a healthy diet, and exercising regularly)',
                  'Medications to control high blood pressure, high cholesterol, and other risk factors']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for stroke include:\n{treatment_list}. It is important to seek immediate medical attention if you or someone you know is experiencing stroke symptoms, as early treatment can greatly improve outcomes.')
        

        # If asthma is mentioned in the user input
        elif 'asthma' in self.entry.get().lower():
    # Define asthma
            definition = 'Asthma is a chronic respiratory disease that affects the airways of the lungs. It causes inflammation and narrowing of the airways, making it difficult to breathe.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Wheezing\n', '2. Shortness of breath\n', '3. Chest tightness\n', '4. Coughing (especially at night or early in the morning)']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of asthma include:\n{symptom_list}.')

    # List some possible triggers
            triggers = ['Allergens (such as pollen, dust mites, or animal dander)', 'Irritants (such as smoke or pollution)', 'Physical activity', 'Respiratory infections', 'Stress', 'Weather changes']
            trigger_list = "\n".join([f"{i}. {trigger}" for i, trigger in enumerate(triggers, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Common triggers for asthma include:\n{trigger_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Inhaled bronchodilators (such as albuterol)', 'Inhaled corticosteroids (such as fluticasone)', 'Leukotriene modifiers (such as montelukast)', 'Immunomodulators (such as omalizumab)', 'Oral corticosteroids (for severe flare-ups)', 'Avoiding triggers', 'Keeping track of symptoms and using a peak flow meter']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for asthma include:\n{treatment_list}. It is important to work with your doctor to develop a personalized asthma action plan to manage your symptoms and prevent flare-ups.')
        

        elif 'heart disease' in self.entry.get().lower() or 'cardiovascular disease' in self.entry.get().lower():
    # Define heart disease
            definition = 'Heart disease, also known as cardiovascular disease, refers to a group of conditions that affect the heart or blood vessels.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Chest pain or discomfort\n' '2. Shortness of breath\n' '3. Heart palpitations\n' '4. Fatigue\n' '5. Swelling in the legs, ankles, or feet\n' '6. Dizziness or lightheadedness\n' '7. Nausea or vomiting']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of heart disease include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Smoking', 'High blood pressure', 'High cholesterol', 'Diabetes', 'Obesity', 'Family history of heart disease', 'Poor diet', 'Lack of physical activity']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Causes of heart disease include:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Medications (such as beta-blockers, ACE inhibitors, or statins)', 'Lifestyle changes (such as quitting smoking, improving diet, and increasing physical activity)', 'Medical procedures (such as angioplasty or bypass surgery)']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for heart disease include:\n{treatment_list}. Additionally, preventive measures such as regular exercise, a healthy diet, and avoiding smoking can help reduce the risk of developing heart disease.')
        

        elif 'copd' in self.entry.get().lower() or 'chronic obstructive pulmonary disease' in self.entry.get().lower():
    # Define COPD
            definition = 'Chronic Obstructive Pulmonary Disease (COPD) is a chronic inflammatory lung disease that obstructs airflow from the lungs and makes it difficult to breathe.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Shortness of breath\n', '2. Wheezing\n', '3. Chest tightness\n', '4. Chronic cough\n', '5. Sputum production\n']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of COPD include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Smoking', 'Long-term exposure to air pollutants', 'Genetic factors', 'Occupational exposure to dust and chemicals']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Causes of COPD include:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Smoking cessation', 'Bronchodilators and inhaled corticosteroids', 'Oxygen therapy', 'Pulmonary rehabilitation', 'Surgery (such as lung volume reduction surgery or lung transplant)']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for COPD include:\n{treatment_list}. It is important to avoid smoking and exposure to air pollutants to prevent COPD.')
        
        elif 'aids' in self.entry.get().lower() or 'hiv' in self.entry.get().lower() or 'human immunodeficiency virus' in self.entry.get().lower():
    # Define AIDS/HIV disease
            definition = 'Acquired immunodeficiency syndrome (AIDS) is a chronic, potentially life-threatening condition caused by the human immunodeficiency virus (HIV). HIV damages the immune system and interferes with the body\'s ability to fight off organisms that cause disease.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Rapid weight loss\n', '2. Recurring fever or profuse night sweats\n', '3. Extreme and unexplained tiredness\n', '4. Prolonged swelling of the lymph glands in the armpits, groin, or neck\n', '5. Diarrhea that lasts for more than a week\n', '6. Sores of the mouth, anus, or genitals\n', '7. Pneumonia\n', '8. Red, brown, pink, or purplish blotches on or under the skin or inside the mouth, nose, or eyelids\n', '9. Memory loss, depression, and other neurological disorders']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of AIDS/HIV disease include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Unprotected sex with an infected partner\n', 'Sharing needles or syringes contaminated with HIV-infected blood\n', 'From mother to child during pregnancy, childbirth or breastfeeding\n', 'Blood transfusion with HIV-contaminated blood']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: AIDS/HIV disease can be caused by:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Antiretroviral therapy (ART) to slow down the progression of the virus\n', 'Pre-exposure prophylaxis (PrEP) and post-exposure prophylaxis (PEP) to prevent the spread of HIV\n', 'Safe sex practices (using condoms)\n', 'Not sharing needles or other injection equipment\n', 'Testing for HIV and getting treatment if infected\n', 'Taking steps to prevent mother-to-child transmission during pregnancy and breastfeeding']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments and preventive measures for AIDS/HIV disease include:\n{treatment_list}.') 
        

        elif 'jaundice' in self.entry.get().lower():
    # Define jaundice
            definition = 'Jaundice is a medical condition that causes yellowing of the skin and whites of the eyes. It is often a sign of an underlying problem such as liver disease.'
            self.text.insert(END, f'\n\nDr.Sophia: {definition}')

    # List some common symptoms
            symptoms = ['1. Yellowing of the skin and whites of the eyes\n' '2. Dark urine\n' '3. Pale stools\n' '4. Fatigue\n' '5. Abdominal pain\n' '6. Itchy skin']
            symptom_list = "\n".join(symptoms)
            self.text.insert(END, f'\n\nDr.Sophia: Common symptoms of jaundice include:\n{symptom_list}.')

    # List some possible causes
            causes = ['Liver disease (such as hepatitis or cirrhosis)', 'Blockage of bile ducts', 'Inherited disorders of bilirubin metabolism', 'Certain medications or toxins', 'Infections such as malaria']
            cause_list = "\n".join([f"{i}. {cause}" for i, cause in enumerate(causes, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Causes of jaundice include:\n{cause_list}.')

    # List some possible treatments and preventive measures
            treatments = ['Treating the underlying cause of the jaundice', 'Light therapy (for newborns with jaundice)', 'Medications to increase bile flow', 'Liver transplant (in severe cases)', 'Avoiding alcohol and certain medications if you have liver disease']
            treatment_list = "\n".join([f"{i}. {treatment}" for i, treatment in enumerate(treatments, start=1)])
            self.text.insert(END, f'\n\nDr.Sophia: Possible treatments for jaundice include:\n{treatment_list}. It is important to talk to your doctor about any concerns you have about jaundice or any symptoms you may be experiencing.')

        else:
            self.text.insert(END, '\n\nDr.Sophia: I\'m sorry, I don\'t understand. Please try again or ask a different question.')

if __name__ == "__main__":
    root = Tk()
    obj = Chatbot(root)
    root.mainloop()
