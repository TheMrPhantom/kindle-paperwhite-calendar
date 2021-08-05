from flask import Flask
from flask import jsonify
from flask_cors import CORS
import appointmentManager
import config

app = Flask(__name__)
CORS(app)
refreshs=60*5
refresh_remaining=refreshs
refresh_every_sec=60

@app.route('/nextAppointment')
def getNextAppointment():
   aps=appointmentManager.get_Appointments()
   name=aps[0].subject
   place=aps[0].location
   time=aps[0].fancyTime()
   date=aps[0].fancyDate()

   return jsonify({"name":name,"place":place,"time":time,"date":date})

@app.route('/nextAppointmentHTML')
def getNextAppointmentHTML():
   aps=appointmentManager.get_Appointments()
   name=aps[0].subject
   place=aps[0].location
   time=aps[0].fancyTime()
   date=aps[0].fancyDate()


   output=f'''
   <html>
   <center>
      <table style="background-color:darkblue;color:white;">
         <tr>
            <th>&ensp;{name}</th>
            <th>&emsp;&emsp;&emsp;&emsp;{time}&ensp;</th>
         </tr>
         <tr>
            <td>&ensp;{place}</td>
            <td>&emsp;&emsp;&emsp;&emsp;{date}&ensp;</td>
         </tr>
      </table>
   </center>
   </html>
   '''
   

   return output

@app.route('/nextAppointments')
def getNextAppointments():
   aps=appointmentManager.get_Appointments()
   output=[]
   for a in aps:
      name=a.subject
      place=a.location
      time=a.fancyTime()
      date=a.fancyDate()
      output.append({"name":name,"place":place,"time":time,"date":date})

   return jsonify(output)

@app.route('/html')
def html():
   global refresh_remaining
   aps=appointmentManager.get_Appointments()
   fancy_date=appointmentManager.cal.current_date()
   output="<html>"
   if refresh_remaining>0:
      refresh_remaining-=1
      output+=f'''
      <meta http-equiv="refresh" content="{refresh_every_sec}; URL=http://{config.ip}:9004/html">
      '''
   else:
      output+=f'''
      <meta http-equiv="refresh" content="{refresh_every_sec}; URL=http://{config.ip}:9004/black">
      '''
      refresh_remaining=refreshs
   
   output+=f"<h2>{fancy_date}</h2>"
   output+=format_appointment(aps[0],style="background-color:darkblue;color:white")

   last_day=""
   
   for idx,a in enumerate(aps[1:]):
      if last_day!=a.fancyDate():
         output+="<hr>"
         output+="<h4 style='margin-top:0px'>"+a.fancyShortDate()+"</h4>"
         last_day=a.fancyDate()
      output+=format_appointment(a,style="background-color: beige;" if idx %2 == 0 else "background-color: lightgrey;")
   output+="</html>"
   return output

def format_appointment(ap,style=""):
   name=ap.subject
   place=ap.location
   time=ap.fancyTime()
   date=ap.fancyDate()

   if place:
      output=f'''
      <center>
      <div style="margin-top:20px;{style};padding:10px">
         <div>
         <b>
         {name}
         </b>
         </div>
         <div>
         {time}
         </div>
         <div>
         {place}
         </div>
      </div>
      </center>
      '''
   else:
      output=f'''
      <center>
      <div style="margin-top:20px;{style};padding:10px">
         <div>
         <b>
         {name}
         </b>
         </div>
         <div>
         {time}
         </div>
      </div>
      </center>
      '''
   

   return output

@app.route('/black')
def black_screen():
   content=f'''
   <html style="background-color:black">
   <meta http-equiv="refresh" content="1; URL=http://{config.ip}:9004/white">

   </html>
   '''

   return content

@app.route('/white')
def white_screen():
   content=f'''
   <html style="background-color:white">
   <meta http-equiv="refresh" content="1; URL=http://{config.ip}:9004/html">

   </html>
   '''

   return content

app.run(host="0.0.0.0",port=9004)
