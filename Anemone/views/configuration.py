""" view for configuration """

from flask import render_template, g, redirect, session
from Anemone import app

@app.route("/configuration")
@app.route("/configuration/")
def configuration_view():
    """ Displays the view for configuration """

    if session['logged_in'] is False:
        return redirect("/")

    g.selected_tab = "configuration"
    return render_template("configure.html")

def generate_rsa(bits=2048):
    """ Gatherd from: https://gist.github.com/lkdocs/6519378
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    """

    from Crypto.PublicKey import RSA

    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return private_key, public_key
