from flask import Flask
from flask import render_template, request
import requests
import ipaddress

# Initializing app
app = Flask(__name__)

"""
    Since it is a little web application the use
    of only having GET method it is enough..
"""
@app.route("/", methods=['GET'])
def index(response_data=None):

    """
        Fetching data from AWS 
    """
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    ip_ranges = response.json()['prefixes']

    """
         Let's create a list for each service
         we want to get the data
    """
    route53_healthchecks = [item for item in ip_ranges if item["service"] == "ROUTE53_HEALTHCHECKS"]
    s3 = [item for item in ip_ranges if item["service"] == "S3"]
    full_range_list = route53_healthchecks + s3

    """
        Since I do not know how to order in Javascript 
        I am parsing actions to the backend to order 
        by region, prefix, ip_prefix or none.
    """
    if request.args.get('order_by') == "region":

        order_by = request.args.get('order_by')
        newlist = sorted(full_range_list, key=lambda k: k[order_by].lower()) 

        return render_template('index.html', data=newlist)

    elif request.args.get('order_by') == "service":

        order_by = request.args.get('order_by')
        newlist = sorted(full_range_list, key=lambda k: k[order_by].lower()) 

        return render_template('index.html', data=newlist)

    elif request.args.get('order_by') == "ip_prefix":

        order_by = request.args.get('order_by')
        newlist = sorted(full_range_list, key=lambda item: ipaddress.ip_address(item[order_by].split('/')[0]))

        return render_template('index.html', data=newlist)
    else:
        return render_template('index.html', data=full_range_list)

@app.route("/route53_healthchecks", methods=['GET'])
def r_health(response_data=None):

    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    ip_ranges = response.json()['prefixes']
    range_list = [item for item in ip_ranges if item["service"] == "ROUTE53_HEALTHCHECKS"]

    if request.args.get('order_by') == "region":

        order_by = request.args.get('order_by')
        newlist = sorted(range_list, key=lambda k: k[order_by].lower()) 

        return render_template('r_health.html', data=newlist)

    elif request.args.get('order_by') == "ip_prefix":

        order_by = request.args.get('order_by')
        newlist = sorted(range_list, key=lambda item: ipaddress.ip_address(item[order_by].split('/')[0]))

        return render_template('r_health.html', data=newlist)
    else:
        return render_template('r_health.html', data=range_list)

@app.route("/s3", methods=['GET'])
def s3_ranges(response_data=None):

    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    ip_ranges = response.json()['prefixes']
    s3 = [item for item in ip_ranges if item["service"] == "S3"]

    if request.args.get('order_by') == "region":
        order_by = request.args.get('order_by')
        newlist = sorted(s3, key=lambda k: k[order_by].lower()) 
        return render_template('s3.html', data=newlist)

    elif request.args.get('order_by') == "ip_prefix":
        order_by = request.args.get('order_by')
        newlist = sorted(s3, key=lambda item: ipaddress.ip_address(item[order_by].split('/')[0]))
        return render_template('s3.html', data=newlist)

    else:
        return render_template('s3.html', data=s3)

if __name__ == "__main__":
    app.run(debug = True) 