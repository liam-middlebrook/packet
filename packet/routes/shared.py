from flask import render_template

from packet import auth, app
from packet.models import Freshman, Packet
from packet.packet import get_signatures, get_number_required, get_number_signed
from packet.utils import before_request


@app.route("/packet/<uid>")
@auth.oidc_auth
@before_request
def freshman_packet(uid, info=None):
    freshman = Freshman.query.filter_by(rit_username=uid)[0]
    signatures = get_signatures(uid)
    required = sum(get_number_required(uid).values())
    signed = sum(get_number_signed(uid).values())
    return render_template("packet.html", info=info, signatures=signatures, uid=uid, required=required, signed=signed,
                           freshman=freshman)


@app.route("/packets")
@auth.oidc_auth
@before_request
def packets(info=None):
    packets = Packet.query.all()
    return render_template("active_packets.html", info=info, packets=packets)
