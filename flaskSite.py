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

def call_proc(cmd):
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return output

def filter_output(output, host):
    o_filter = ""
    for line in output.stdout:
        o_filter = o_filter+line

    return_data = "%s" % host + " " +  o_filter
    return return_data

@app.route('/')
def index():
    return render_template('center.html', return_data='Home Page')

@app.route('/ping/')
@app.route('/ping/<host>')
@app.route('/pong/<host>', alias=True)
def ping(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "ping -c 4 %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/tracert/')
@app.route('/traceroute/')
@app.route('/traceroute/<host>')
@app.route('/tracert/<host>', alias=True)
def traceroute(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "traceroute -m 10 %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)


@app.route('/dns-lookup/')
@app.route('/lookup/')
@app.route('/dns-lookup/<host>')
@app.route('/lookup/<host>', alias=True)
def dns_lookup(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "nslookup %s 8.8.8.8" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/whois/')
@app.route('/whois/<host>')
def whois(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "whois %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/reverse/')
@app.route('/reverse-dns/')
@app.route('/reverse/<host>')
@app.route('/reverse-dns/<host>', alias=True)
def reverse(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "host %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/country/')
@app.route('/contry/<host>')
def contry_by_ip(host=None):
    if host is None:
        return render_template('center.html')
    else:
        ''' TODO: Use the IP to check with some geo-location service or even create a database w/ help of whois '''
        return 'Contry %s' % host

@app.route('/nmap/')
@app.route('/nmap/<host>')
def nmap(host=None):
    if host is None:
        return render_template('center.html')
    else:
        cmd = "nmap %s" % host
        output = call_proc(cmd)
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/url-status/')
@app.route('/site-status/')
@app.route('/url-status/<host>')
@app.route('/site-status/<host>', alias=True)
def site_status(host=None):
    if host is None:
        return render_template('center.html')
    else:
        ''' TODO: Use a fake browser to get the headers and have a 200 returned if OK, else, print the error too. '''
        output = urllib2.Request("%s" % host, headers = headers)
        o_response = urllib2.urlopen(output)
        o_filter = o_response.get_headers()
        return 'Url Status %s' % o_filter

@app.route('/encoding/')
@app.route('/encoding/<host>')
def encoding(host=None):
    if host is None:
        render_template('center.html')
    else:
        ''' TODO: Find a way to check encoding from a remote file '''
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/email-check/')
@app.route('/email-check/<host>/<user>')
def email_check(host=None,user=None):
    if host is None:
        render_template('center.html')
    else:
        ''' TODO: Use smtplib to send a test e-mail or even to check if it autenticates '''
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/proxy/')
@app.route('/proxy/<host>/<port>')
def proxy(host=None, port=None):
    if host is None:
        render_template('center.html')
    else:
        '''
        TODO: Check if a proxy is runnig and for what can be used ( tunnel, etc )
        http headers reveal the proxy user ('proxy via something')
        '''
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/telnet/')
@app.route('/telnet/<host>/<int:port>')
def telnet(host=None,port=None):
    if host is None:
        render_template('center.html')
    else:
        ''' TODO: Use telnetlib to test a port and maybe return the message received '''
        return_data = filter_output(output, host)
        return render_template('center.html', return_data=return_data)

@app.route('/port-check/')
@app.route('/port-check/<host>/<int:port>')
def port_check(host=None, port=None):
    if host is None:
        render_template('center.html')
    else:
        ''' TODO: Less precise telnet test, maybe a nmap like just to see if the port is opened or closed '''
        if port == "":
            port = 23

        tn = telnetlib.Telnet(host,port, 5)
        if tn.open(host,port, 5):
            return_data = filter_output(output, host)
            tn.close()
        else:
            return_data = filter_output(output, host)
        return return_data

''' TODO: Find a better way to handle errors, since web provides more errors and seems to much work to config all ( or almost all ) '''

@app.route('/about/')
@app.route('/about-me/', alias=True)
def about():
    return render_template('center.html', return_data='This site is build w/ Flask and Python 2.7, helped w/ some modules, the source can be found at my github. Any suggestions? Just do it and send a push.')

@app.errorhandler(403)
def forbidden():
    return render_template('center.html', return_data='Can\'t do that!' )

@app.errorhandler(404)
def page_not_found():
    return render_template('center.html', return_data='Nothing found here!')

@app.errorhandler(500)
def internal_server():
    return render_template('center.html', return_data='Something smells strange!')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8080)