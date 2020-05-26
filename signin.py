
# # A very simple Flask Hello World app for you to get started with...

# from flask import Flask,redirect,render_template,request,url_for
# import os
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return ' from Flask!'
from flask import Flask,render_template,request
import os
import datetime
import smtplib,ssl
# import email.mime as e#for sending hml content as additional feature
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app=Flask(__name__)
def logging_in(user,pa):
    os.chdir('/home/AngelFrancis/mysite')
    r=open('file.txt','r')
    Lines = r.readlines()
    uc=0
    pc=0
    for line in Lines:
      l = list(line.split())
      try:
          if user==l[1]:
              uc=1
              break
          if user==l[1] and l[2]!=pa:
              pc=1
              break
      except IndexError:
          continue
    if uc==0:
        return render_template("signin.html",e="alert('Error: NO SUCH USERNAME FOUND. Please Sign up ');go_to_signup();")
    if pc==1:
        return render_template("signin.html",e="alert('Error: Wrong password. Please Sign up ');go_to_signup();")

    else:
        check_remaind(user)
        # return 'l'
        return logged_in(user,"Logged in")
def signing_up(email, username, pa, rpa):
    os.chdir('/home/AngelFrancis/mysite')
    ecount=0
    ucount=0
    r = open('file.txt', 'r')
    f=open('file.txt','a')
    Lines = r.readlines()
    for line in Lines:
        l = list(line.split())
        try:
            if email==l[0]:
                ecount = 1
                break
            if username==l[1]:
                ucount = 1
                break
        except IndexError:
            continue

    if ecount == 1:
        return render_template("signin.html", e="alert('Error: EMAIL AlREADY REGISTERED ');login();")
    elif ucount == 1:
        return render_template("signin.html", e="alert('Error: USERNAME AlREADY REGISTERED .Use another name');go_to_signup();")
    else:
        if pa==rpa:
            f.write(email+" "+username+" "+rpa+"\n")
            return render_template("register.html",email=email,username=username, e="alert('Successfully Signed up!!!!!!!!!');")
        else:
            return render_template("signin.html", e="go_to_signup();password_mismatch();")
# signing_up('angel','a','a','a')
@app.route('/')
def s():
    return render_template('signin.html')

@app.errorhandler(500)
def fun500(error):
    return render_template(request.referrer,e="alert('Server error');")
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method =='POST':
        email=request.form['username']
        pa=request.form['password']
        return logging_in(email,pa)
    else:
        email = request.args.get('username')
        pa = request.args.get('pa')
        return logging_in(email, pa)
@app.route('/edit',methods=['POST','GET'])
def edit():
    if request.method =='POST':
        username = request.form['username']
        quoter = request.form['quoter']
        goalr = request.form['goalr']
        quote = request.form['quote']
        goal = request.form['goal']

        return edit_fun(username,quote,goal,quoter,goalr)
    else:
        username=request.args.get('username')
        quoter=request.args.get('quoter')
        goalr=request.args.get('goalr')
        quote = request.args.get('quote')
        goal = request.args.get('goal')
        return edit_fun(username,quote,goal,quoter,goalr)
def edit_fun(username,quote,goal,quoter,goalr):
    os.chdir("/home/AngelFrancis/mysite/_users/."+username)
    filer=open('info.txt','r')
    new_file=""
    Lines = filer.readlines()
    for line in Lines:
        try:
            l = line.strip()
            list_=list(line.split())
            if list_[0]=="quote":
                l=l.replace(quote," "+quoter)
            if list_[0]=="goal":
                l=l.replace(goal," "+goalr)
        except IndexError:
            continue
        new_file += l + "\n"
    filer.close()
    filew=open('info.txt','w')
    filew.write(new_file)
    filew.close()
    return logged_in(username,'alert("edited");')
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method =='POST':
        email=request.form['email']
        username=request.form['username']
        pa=request.form['password']
        rpa=request.form['rpassword']
        return signing_up(email,username,pa,rpa)
    else:
        email = request.args.get('email')
        username=request.args.get('username')
        pa = request.args.get('pa')
        rpa=request.args.get('rpassword')
        return signing_up(email,username,pa,rpa)
@app.route('/registered', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email=request.form['email']
        user=request.form['username']
        quote=request.form['quote']
        goal=request.form['goal']
        imagefile = request.files['imageh']
        return registered(email,user,quote,goal,imagefile.filename)
    else:
        email=request.args.get('email')
        user=request.args.get('username')
        quote=request.args.get('quote')
        goal=request.args.get('goal')
        image=request.args.get('imageh')
        return registered(email,user,quote,goal,image)
@app.route('/task',methods=['POST','GET'])
def new_task():
    if request.method =='POST':
        title=request.form['title']
        url=request.form['url']
        due=request.form['due']
        remainder=request.form['remainder']
        user=request.form['user']
        if url=="":
            url="default"
        return new_task_added(title,url,due,remainder,user)
    else:
        title = request.args.get('title')
        url=request.args.get('url')
        due = request.args.get('due')
        remainder=request.args.get('remainder')
        user=request.args.get('user')
        if url=="":
            url="default"
        return new_task_added(title,url,due,remainder,user)
@app.route('/remove/<user>/<title>')
def remove(title,user):
    os.chdir("/home/AngelFrancis/mysite/_users/." + user)
    filer = open('info.txt', 'r')
    new_file = ""
    Lines = filer.readlines()
    for line in Lines:
        l = line.strip()
        list_ = list(line.split())
        try:
            if list_[1] == title:
                continue
            new_file += l + "\n"
        except IndexError:
            continue
    filer.close()
    filew = open('info.txt', 'w')
    filew.write(new_file)
    filew.close()
    mailr = open('info.txt', 'r')
    os.chdir('/home/AngelFrancis/mysite/_users/.'+user)
    file=open('mail.txt','r')
    lines=file.readlines()
    n=''
    for li in lines:
        o=li.strip()
        l=li.split()
        if(l[0]==title):
            continue;
        n+=o+'\n'
    print(n)
    file.close()
    filew=open('mail.txt','w')
    filew.write(n)
    filew.close()
    return logged_in(user,'alert("Event deleted");')
@app.route('/delete_fill',methods=['POST','GET'])
def delete_fill():
    if request.method =='POST':
        user=request.form['username']
        pa=request.form['password']
        return delete_account(user,pa)
    else:
        user = request.args.get('username')
        pa = request.args.get('password')
        return delete_account(user,pa)
def delete_account(user,pa):
    n=''
    os.chdir("/home/AngelFrancis/mysite")
    file=open('file.txt','r')
    lines=file.readlines()
    found=0
    for line in lines:
        try:
            l=line.strip()
            lis=line.split()
            if(lis[1]==user and lis[2]==pa):
                found=1
                break
        except IndexError:
            continue
    if found==1:
        for line in lines:
            try:
                l=line.strip()
                lis=line.split()
                if(lis[1]==user):
                    continue
            except IndexError:
                continue
            n+=l+'\n'
        file.close()
        filew=open('file.txt','w')
        filew.write(n)
        filew.close()
        os.chdir("/home/AngelFrancis/mysite/_users/."+user)
        os.remove('info.txt')
        os.remove('mail.txt')
        os.chdir("/home/AngelFrancis/mysite/_users")
        os.rmdir('.'+user)
        return render_template("signin.html", e="alert('Account deleted');")
    else:
        return render_template("delete.html",user=user,e="alert('Wrong entry');")
@app.route('/delete_confirm/<user>')
def delete_confirm(user):
        return render_template("delete.html",user=user,e="")

@app.route('/maildelete/<user>')
def maildelete(user):
    os.chdir('/home/AngelFrancis/mysite')
    r = open('file.txt', 'r')
    Lines = r.readlines()
    for line in Lines:
        l = list(line.split())
        try:
            if l[1]==user:
                emailr=l[0]
                break
        except IndexError:
            continue
    port = 465  # for ssl only no=465
    password = "remainder111"
    rec = emailr
    sen = "remainderevent@gmail.com"
    message = MIMEMultipart("alternative")
    message['Subject']='Confirmation on deleting account'#defining subject ,from,to parts
    message['From']=sen
    message['To']=rec
    text="""
    Sorry for the inconvenience .You can write to this mail id about your problem with the product .Go to link  below and enter password to delete your account
    https://angelfrancis.pythonanywhere.com/delete_confirm/"""+user
    #three quotes for multilines without \n
    #html content
    html="""
    <html>
        <body>
    <p style="color:red"><b>    Sorry for the inconvenience .You can write to this mail id about your problem with the product .Click below and enter password to delete your account
</b></p>
<br><br><div align="center">
<a style=" background-color:#4285f4;color:white;width:190px;height:45px;border:1px solid gray;border-radius:5px;padding:10px 10px 10px 10px;" href='https://angelfrancis.pythonanywhere.com/delete_confirm/"""+user+"""'>Click here</a>
</div></body>
    </html>
    """
    part1=MIMEText(text,'plain')
    part2=MIMEText(html,'html')#html as part2 since MIME will first try to render last part
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()  # default content
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:  # using with as it closes server after with loop
        server.login('remainderevent@gmail.com', password)  # email from
        server.sendmail(sen, rec, message.as_string())#coverting to string and sending
        print("done")
    return logged_in(user,'alert("Delete link sent to your mail");')
#users.py
def registered(email,user,quote,goal,image):
    c=0
    os.chdir("/home/AngelFrancis/mysite")
    list_=open('file.txt','r')
    Lines = list_.readlines()
    user_files=os.listdir('/home/AngelFrancis/mysite/_users')
    for line in Lines:
        l = list(line.split())
        try:
            if user==l[1]:
                c=c+1
                u='.'+user
                if u in user_files:
                    return render_template('register.html', e="alert('Use the name with which you signed up');")
                else:
                    os.mkdir("_users/." + user)
                    path = "/home/AngelFrancis/mysite/_users/." + user
                    os.chdir(path)
                    file=open('/home/AngelFrancis/mysite/_users/.'+user+"/info.txt",'w')
                    mailr = open('/home/AngelFrancis/mysite/_users/.' + user + "/mail.txt", 'w')
                    file.write("email "+email+"\n"+"quote "+quote+"\n"+"goal "+goal+"\n"+"image "+'default')
                    return render_template("signin.html",e="alert('Error: Login to access your account ');go_to_signup();")
                    # return home(image, user, quote, goal)
        except IndexError:
            continue
    if c==0:
        return render_template('register.html',e="alert('Wrong username');")
def home(image,username,quote,goal):
    return render_template('home.html',img=image,user=username,quote=quote,goal=goal,len=0,title=[],url=[])
def logged_in(user,alert):
    check_remaind(user)
    os.chdir("/home/AngelFrancis/mysite")
    list_ = open('file.txt', 'r')
    Lines = list_.readlines()
    image,quote,goal,css1,css2,css3,inf="",[],[],[],[],[],[]
    g,q="",""
    for line in Lines:
        l = list(line.split())
        title=[]
        url=[]
        try:
            if user==l[1]:
                info = open('/home/AngelFrancis/mysite/_users/.' + user + "/info.txt", 'r')
                det=info.readlines()
                for i in det:
                    l=list(i.split())
                    try:
                        if l[0]=='image':
                            image=l[1:]
                        elif l[0]=='quote':
                            quote=l[1:]
                        elif l[0]=='goal':
                            goal=l[1:]
                        elif l[0]=='Title':
                            title.append(l[1])
                            url.append(l[3])
                            c=over(l[5],l[1],user)
                            if c=="over":
                                css1.append("#ff3700")
                                css2.append('#ffd900')
                                css3.append('#a4e2eb')
                                inf.append('is over')
                            else:
                                css1.append('#40ff46')
                                css2.append('#69abff')
                                css3.append("#d595fc")
                                inf.append('')
                    except IndexError:
                        continue
                for i in quote:
                    q=q+" "+i
                for i in goal:
                    g=g+" "+i
                return render_template('home.html',img=image,user=user,quote=q,goal=g,title=title,url=url,ln=len(title),css1=css1,css2=css2,css3=css3,inf=inf,e=alert)
        except IndexError:
            continue
#task.py
def new_task_added(title,url,due,remaind,user):
    os.chdir("/home/AngelFrancis/mysite/_users/."+user)
    file=open('info.txt','a')
    filer=open('info.txt','r')
    c=0
    lines=filer.readlines()
    for line in lines:
        l=line.split()
        try:
            if l[1]==title:
                c=1
        except IndexError:
            continue
    if c==0:
        file.write("\nTitle "+str(title)+" url "+str(url)+" due "+str(due)+" remaind "+str(remaind))
        check_remaind(user)
        return logged_in(user,"")
    else:
        check_remaind(user)
        return logged_in(user,"")

def check_remaind(user):
    os.chdir("/home/AngelFrancis/mysite/_users/."+user)
    file=open('info.txt','r')
    email=''
    Lines = file.readlines()
    for line in Lines:
        l=list(line.split())
        try:
            if l[0]=='email':
                email=l[1]
            if l[0]== 'Title':
                title=l[1]
                url=l[3]
                due=l[5]
                remaind=l[7]
                # over(due,title,user)
                remain(user,email,title,due,url,remaind)
        except IndexError:
            continue
def pydate(r):
    d = datetime.datetime.now()
    day = d.day
    month=d.month
    year=d.year
    min=d.minute
    hour=d.hour
    min=min+30
    hour=hour+5
    if r== '5':
        min=min+5
    elif r=='15':
        min=min+15
    elif r== '30':
        min=min+30
    elif r=='1h':
        hour=hour+1
    elif r=='2h':
        hour=hour+2
    elif r=='1d':
        day=day+1
    elif r=='2d':
        day=day+2
    elif r=='3d':
        day=day+3
    elif r=='7d':
        day=day+7
    min,hour,day,month,year=added(min,hour,day,month,year)
    if min < 10:
        min = '0' + str(min)
    if hour < 10:
        hour = '0' + str(hour)
    if day<10:
        day='0'+str(day)
    if month<10:
        month='0'+str(month)
    if year<10:
        year='0'+str(year)
    s=str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour)+':'+str(min)
    return (s)
def remain(user,email,title,due,url,r):
    # return render_template('signin.html')
    os.chdir("/home/AngelFrancis/mysite/_users/."+user)
    mailr=open("mail.txt",'r')
    mailw=open('mail.txt','a+')
    lines = mailr.readlines()
    c=0
    for line in lines:
        l = line.split()
        try:
            if l[0]==title:
                c=1
        except IndexError:
            continue
    da = datetime.datetime.now()
    hour = da.hour
    p=pydate(r)
    d=str(due)
    print(p,d)
    if(over(due,title,user)=='over' and c==0):
        print('1')
        title=title+" over"
        send_mail_html(email,title,url,due)
    elif r=='1d' or r=='2d' or r=='3d' or r=='7d':
        print("c")
        if p[:10] == d[:10] and hour > 2 and c==0:
            print('2')
            send_mail_html(email,title,url,due)
            mailw.write(title+" done\n")
    elif r=='0' or r=='5' or r=='15' or r=='30' or r=='1h' or r=='2h':
        print(p,d)
        if p == d and c==0:
            print('3')
            send_mail_html(email,title,url,due)
            mailw.write(title+" done\n")
    else:
        print('a')
        if p == d and c==0:
            print('4')
            send_mail_html(email,title,url,due)
            mailw.write(title+" done\n")
def added(min,hour,day,month,year):
    if min>59:
        min=min-60
        hour=hour+1
    if hour>23:
        hour=hour-24
        day=day+1
    if day>29 and month==2 and year%4==0:
        day=day-29
        month=month+1
    elif day>28 and month==2 and year%4!=0:
        day=day-28
        month=month+1
    elif day>30 and (month==4 or month==6 or month==9 or month==11):
        day=day-30
        month=month+1
    elif day>31 and (month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
        day=day-31
        month=month+1
    if month>12:
        month=month-12
        year=year+1
    return min,hour,day,month,year
def over(due,title,user):
    d = datetime.datetime.now()
    day = d.day
    month = d.month
    year = d.year
    min = d.minute+30
    hour = d.hour+5
    min,hour,day,month,year=added(min,hour,day,month,year)
    due=str(due)
    if year>int(due[0:4]):
        return "over"
    elif month>int(due[5:7]) and year>=int(due[0:4]):
        return "over"
    elif month>=int(due[5:7]) and year>=int(due[0:4]) and day>int(due[8:10]):
        return "over"
    elif month>=int(due[5:7]) and year>=int(due[0:4]) and day>=int(due[8:10]) and hour>int(due[11:13]):
        return "over"
    elif month>=int(due[5:7]) and year>=int(due[0:4]) and day>=int(due[8:10]) and hour>=int(due[11:13]) and min>int(due[14:16]):
        return "over"
    else:
        return "not"
#gmail.py
def notify(title):
    return title
def send_mail_html(emailr,title,url,due):
    title=title.capitalize()
    port = 465  # for ssl only no=465
    password = "remainder111"
    rec = emailr
    sen = "remainderevent@gmail.com"
    message = MIMEMultipart("alternative")
    message['Subject']='Remainder:'+title#defining subject ,from,to parts
    message['From']=sen
    message['To']=rec
    #this is normal text as
#As not all email clients display HTML content by default, and some people choose only to receive plain-text emails for security reasons,
# it is important to include a plain-text alternative for HTML messages
    text="""
    Hi there.I am here to remaind you about   """+title+""" at """+due+"""

    """+url
    #three quotes for multilines without \n
    #html content
    html="""
    <html>
        <body>
    <p style="color:red"><b>Hi there.I am here to remaind you about """+title+""" at """+due+"""</b></p>
<br><br><div align="center">
<a style=" background-color:#4285f4;color:white;width:190px;height:45px;border:1px solid gray;border-radius:5px;padding:10px 10px 10px 10px;" href='"""+url+"""'>Click here</a>
</div></body>
    </html>
    """
    part1=MIMEText(text,'plain')
    part2=MIMEText(html,'html')#html as part2 since MIME will first try to render last part
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()  # default content
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:  # using with as it closes server after with loop
        server.login('remainderevent@gmail.com', password)  # email from
        server.sendmail(sen, rec, message.as_string())#coverting to string and sending
        print("done")
