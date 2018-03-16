from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pprint as pp
import pdb


app = Flask(__name__)
app.debug = True
import meetup.api
app.config['SECRET_KEY'] = 'foobar'

toolbar = DebugToolbarExtension(app)

def get_names():
    client = meetup.api.Client("55421977653b141662a185121411257")

    rsvps=client.GetRsvps(event_id='244121900', urlname='_ChiPy_')
    member_id = ','.join([str(i['member']['member_id']) for i in rsvps.results])
    members = client.GetMembers(member_id=member_id)

    foo={}
    for member in members.results:
        try:
            foo[member['name']] = member['photo']['thumb_link']
        except:
            pass # ignore those who do not have a complete profile
    return foo

member_rsvps=get_names()

# pp(member_rsvps)

# pdb.set_trace()


@app.route('/')
def home_page():
    return 'This is the home page!!'


@app.route('/rsvps')
def rsvps():
    return render_template('rsvps.html', rsvps=member_rsvps)


@app.route('/teams', methods=['GET', 'POST'])
def teams():
    results = request.form.to_dict()   
    #for key, group in itertools.groupby(results, lambda k: k//4):
        #print (key, list(group))
    return render_template('teams.html', teams=[results])


if __name__ == '__main__':
    app.run(debug=True)
