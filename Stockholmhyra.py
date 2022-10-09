import PyPDF2
import re
import time
#import smtplib
#import ssl
#from email.message import EmailMessage
import imghdr


#öppna pdf
pdfFileObj = open('hyresvard.pdf', 'rb')
print(pdfFileObj)

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
numpage=pdfReader.numPages
numlist = [i for i in range(numpage)]


# creating a page object
maillist = []
for i in numlist:
    pageObj = pdfReader.getPage(i)
    pagetext=pageObj.extractText()
    match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', pagetext)
    maillist.append(match)

print(len(maillist))


results=[]
for i in numlist:
    page = str(maillist[i])
    substring = page.split(",")
    lengtsub = [i for i in range(len(substring))]
    time.sleep(0.1)
    print('Page: '+str(i)+', Email found: '+str(len(lengtsub))+'')
    for i in lengtsub:
        mail= str(substring[i])
        results.append(mail)


newresult =[]
for i in range(len(results)):
    s = results[i]
    sne = s.translate({ord(i): None for i in '[]'})
    snew= re.sub("'", '', sne)
    snew = snew.strip()
    newresult.append(snew)


mylist = sorted(set(newresult))

del mylist[1]
del mylist[47]
del mylist[57]
del mylist[36]
del mylist[69]

time.sleep(1)
print('Cleaning duplicates')
time.sleep(2)

print('printing list of privata hyresvärdar in Stockholm')
time.sleep(1)
for i in range(len(mylist)):
    print(''+str(i)+':  '+mylist[i]+'')
    time.sleep(0.5)


utskick=mylist

pdfFileObj.close()

#-----------------------------------
print('connecting to malte.meuller@gmail.com')

def sendit(i):
    # Define email sender and receiver


    email_sender = 'malte.meuller@gmail.com'
    email_password = 'xx'
    email_receiver = "" + str(i) + ""
    print('sending mail to:'+str(email_receiver)+'')

    # Set the subject and body of the email
    subject = 'Studerande par söker lägenhet!'
    body = """
Hej!

Vi heter Malte Meuller och Freja Orrbeck, är 23 samt 24 år gamla, och ska flytta till Stockholm för fortsatta studier. Malte ska påbörja sin master vid Handelshögskolan och Freja ska läsa statistik vid Stockholms Universitet. Därefter planerar vi att bosätta oss i Stockholm för att jobba. Därför söker vi nu en lägenhet till hösten, och fram, som vi önskar att kunna bo i långsiktigt, men även kortare perioder är av intresse. Vi tänker oss en maxhyra på 10 000 kr per månad. 

Vi är ursprungligen från Göteborg men har under de tre senaste åren bott i Lund där Malte har läst en kandidat i Nationalekonomi och Freja har pluggat en kandidat i Kriminologi. I Lund hyrde vi en lägenhet tillsammans i andrahand i två år men har under de senaste året bott varsin termin i Stockholm där vi inom våra program hade praktik. Freja gjorde praktik på Institutet för Framtidsstudier, och Malte praktiserade på Utrikesdepartementet. Under våra 5 år tillsammans har vi framförallt bott tillsammans men även på varsitt håll och goda referenser från tidigare boenden kan bifogas. 

Vi båda tar fullt CSN och har jobbat extra vid sidan av studierna samt på somrarna, och planerar att fortsätta så även i Stockholm. Vi är dessutom djur- och rökfria och tycker om att ha det rent och städat där vi bor. På fritiden tycker vi om att laga mat, träna och umgås med vänner. 

Om detta låter intressant får ni gärna höra av er till malte.meuller@gmail.com eller freja.orrbeck@hotmail.com så kan vi presentera oss ytterligare. Tack på förhand!

Mvh, Malte Meuller & Freja Orrbeck
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    with open('Malte&Freja.jpg', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    em.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    # Add SSL (layer of security)
    context = ssl.create_default_context()


    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    print('Email sent to: '+str(i)+'')

#------------------------------------------------------------------------

for i in utskick:
    sendit(i)
    time.sleep(4)
