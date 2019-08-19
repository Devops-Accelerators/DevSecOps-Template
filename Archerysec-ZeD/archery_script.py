
from pyArchery import api
from optparse import OptionParser, OptionGroup
import json
import time

parser = OptionParser()

group = OptionGroup(parser, "",
                   "")

parser.add_option_group(group)

group = OptionGroup(parser, "Archery Scan status",
                   "Upload multiple scanners reports"
                   )

group.add_option("--scanner",
                help="Input input scanner name i.e zap_scan, arachni_scan",
                action="store")

group.add_option("--scan_id",
                help="Input Scan Id",
                action="store")

group.add_option("--username",
                help="Input ArcherySec Username",
                action="store")

group.add_option("--password",
                help="Input ArcherySec Password",
                action="store")

group.add_option("--host",
                help="Input ArcherySec Host",
                action="store")

group.add_option("-r", "--high",
                help="Numbers of issue",
                action="store")

group.add_option("-m", "--medium",
                help="Numbers of issue",
                action="store")

(args, _) = parser.parse_args()

def archery_host():
   # Setup archery connection
   archery = api.ArcheryAPI(args.host)

   return archery

def archery_auth():
   # # Set Archery url
   # host = 'http://127.0.0.1:8000'
   archery = archery_host()

   # Provide Archery Credentials for authentication.
   authenticate = archery.archery_auth(args.username, args.password)

   # Collect Token after authentication
   token = authenticate.data
   for key, value in token.viewitems():
       token = value

   return token

# Get the scan result
if args.scanner == 'zap_scan':
   time.sleep(5)
   archery = archery_host()
   web_scan_result = archery.zap_scan_status(
       auth=archery_auth(),
       scan_id=args.scan_id,
   )
   results = web_scan_result.data_json()
   j_result = json.loads(results)
   for j in j_result:
       scan_status = j['vul_status']
       print scan_status
       while (int(scan_status) < 100):
           web_scan_result = archery.zap_scan_status(
               auth=archery_auth(),
               scan_id=args.scan_id,
           )
           results = web_scan_result.data_json()
           j_result = json.loads(results)
           try:
               for j in j_result:
                   scan_status = j['vul_status']
           except Exception as e:
               scan_status = 100
           time.sleep(10)
           print "Scan Status", scan_status
       time.sleep(60)
      
       web_scan_result = archery.zap_scan_status(
           auth=archery_auth(),
           scan_id=args.scan_id,
       )
       results = web_scan_result.data_json()
       j_result = json.loads(results)
       for j in j_result:
           total_vul = j['total_vul']
           high_vul = j['high_vul']
           medium_vul = j['medium_vul']
           low_vul = j['low_vul']

       print "Total Vul", total_vul
       print "Total High", high_vul
       print "Total Medium", medium_vul
       print "Total Low", low_vul

       if int(high_vul) >= int(args.high):
           fail = "FAILURE"
           print "Coz total high Vulnerability", high_vul
       elif int(medium_vul) >= int(args.medium):
           fail = "FAILURE"
           print "Coz total Medium Vulnerability", medium_vul
       else:
           fail = "SUCCESS"
           print "Test Passed"

       print fail