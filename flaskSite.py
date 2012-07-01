__author__ = 'filipecifalistangler'

from flask import Flask
from flask import render_template
import subprocess
import telnetlib
import urllib2

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

app = Flask(__name__)

def top_menu():
    pass

@app.route('/')
def index():
    return render_template('center.html', return_data='Home Page')

@app.route('/ping/<host>')
@app.route('/pong/<host>', alias=True)
def ping(host):
    cmd = "ping -c 4 %s" % host
    output = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    o_filter = ""
    for line in output.stdout.readlines():
        o_filter = o_filter+line

    return_data = "Ping(4 times) to %s" % host + " " +  o_filter
    return render_template('center.html', return_data=return_data)

@app.route('/traceroute/<host>')
@app.route('/tracert/<host>', alias=True)
def traceroute(host):
    cmd = "traceroute -m 10 %s" % host
    output = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    o_filter = ""
    for line in output.stdout.readlines():
        o_filter = o_filter + line + "<br>"

    return_data = "Traceroute(10 max hopes) to %s <br>" % host + "<br>" + o_filter
    return render_template('center.html', return_data=return_data)

@app.route('/dns-lookup/<host>')
@app.route('/lookup/<host>', alias=True)
def dns_lookup(host):
    cmd = "nslookup %s 8.8.8.8" % host
    output = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    o_filter = ""
    for line in output.stdout.readlines():
        o_filter = o_filter + line + "<br>"

    return_data = "Nslookup(server 8.8.8.8) to %s <br>" % host + "<br>" + o_filter
    return render_template('center.html', return_data=return_data)

@app.route('/whois/<host>')
def whois(host):
    cmd = "whois %s" % host
    output = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    o_filter = ""
    for line in output.stdout.readlines():
        o_filter = o_filter + line + "<br>"

    return_data = "Whois to %s <br>" % host + "<br>" + o_filter
    return render_template('center.html', return_data=return_data)

@app.route('/reverse/<host>')
def reverse(host):
    cmd = "host %s" % host
    output = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    o_filter = ""
    for line in output.stdout.readlines():
        o_filter = o_filter + line + "<br>"

    return_data = "Host to %s <br>" % host + "<br>" + o_filter
    return render_template('center.html', return_data=return_data)

@app.route('/contry/<host>')
def contry_by_ip(host):
    ''' TODO: Use the IP to check with some geo-location service or even create a database w/ help of whois '''
    return 'Contry %s' % host

@app.route('/nmap/<host>')
def nmap(host):
    cmd = "nmap %s" % host
    output = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    o_filter = ""
    for line in output.stdout.readlines():
        o_filter = o_filter + line + "<br>"

    return_data = "Nmap to %s <br>" % host + "<br>" + o_filter
    return render_template('center.html', return_data=return_data)

@app.route('/url-status/<host>')
@app.route('/site-status/<host>', alias=True)
def site_status(host):
    ''' TODO: Use a fake browser to get the headers and have a 200 returned if OK, else, print the error too. '''
    output = urllib2.Request("%s" % host, headers = headers)
    o_response = urllib2.urlopen(output)
    o_filter = o_response.get_headers()
    return 'Url Status %s' % o_filter

@app.route('/encoding/<host>')
def encoding(host):
    ''' TODO: Find a way to check encoding from a remote file '''
    return 'Encoding %s' % host

@app.route('/email-check/<host>/<user>')
def email_check(host,user):
    ''' TODO: Use smtplib to send a test e-mail or even to check if it autenticates '''
    return 'Email Check %s $s' % host % user

@app.route('/proxy/<host>/<port>')
def proxy(host, port):
    ''' TODO: Check if a proxy is runnig and for what can be used ( tunnel, etc ) '''
    return 'Proxy at %s %s' % host % port

@app.route('/telnet/<host>/<int:port>')
def telnet(host,port):
    ''' TODO: Use telnetlib to test a port and maybe return the message received '''
    return 'Telnet to %s %s returned: ' % host % port

@app.route('/port-check/<host>/<int:port>')
def port_check(host, port):
    ''' TODO: Less precise telnet test, maybe a nmap like just to see if the port is opened or closed '''
    if port == "":
        port = 23

    tn = telnetlib.Telnet(host,port, 10)
    if tn.open(host,port, 10):
        return_data = "Telnet(10 sec timeout) to %s <br>" % host + "<br> OK"
        tn.close()
    else:
        return_data = "Telnet(10 sec timeout) to %s <br>" % host + "<br> NOT OK"
    return return_data

''' TODO: Find a better way to handle errors, since web provides more errors and seems to much work to config all ( or almost all ) '''

@app.route('/about/')
@app.route('/about-me/', alias=True)
def about():
    return render_template('center.html', return_data='This site is build w/ Flask and Python 2.7, helped w/ some modules, the source can be found at my github. Any suggestions? Just for and send a push.')

@app.errorhandler(403)
def page_not_found(error):
    return render_template('center.html', return_data='Can\'t do that!' )

@app.errorhandler(404)
def page_not_found(error):
    return render_template('center.html', return_data='Nothing found here!')

@app.errorhandler(500)
def page_not_found(error):
    return render_template('center.html', return_data='Something smells strange!')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8080)