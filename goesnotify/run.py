from pushbullet import Pushbullet
import requests
from bs4 import BeautifulSoup
import os


class GOES(object):
    def __init__(self, pushbullet_key, pushbullet_chan):
        pb = Pushbullet(pushbullet_key)
        self.pb_chan = filter(lambda x: x.channel_tag == pushbullet_chan, pb.channels)[0]
        pass

    def check_availability(self, username, password):
        '''Find new offers, and compare'''
        s = requests.Session()
        r = s.get('https://goes-app.cbp.dhs.gov/')
        r = s.post('https://goes-app.cbp.dhs.gov/goes/jsp/j_security_check', data={
            'j_username': username,
            'j_password': password,
            'login-form-type': 'pwd',
            'Sign In': 'Sign In'
        })
        r = s.get('https://goes-app.cbp.dhs.gov/main/goes/HomePagePreAction.do')
        print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find('input', {'name': 'org.apache.struts.taglib.html.TOKEN'})['value']
        r = s.post('https://goes-app.cbp.dhs.gov/main/goes/HomePagePostAction.do', data={
            'org.apache.struts.taglib.html.TOKEN': token,
            'forwardFlag': '',
            'actionFlag': 'scheduleInterview',
            'pageIndex': '',
            'homepageProgramIndex': 0
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find('input', {'name': 'org.apache.struts.taglib.html.TOKEN'})['value']
        r = s.post('https://goes-app.cbp.dhs.gov/main/goes/SelectEnrollmentCenterPostAction.do', data={
            'org.apache.struts.taglib.html.TOKEN': token,
            'forwardFlag': 'next',
            'page': 5,
            'selectedEnrollmentCenter': 7820
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        item = soup.find('div', {'class': 'maincontainer'})
        if item and ('' in item.text):
            return False
        if soup.find('form', {'id': 'scheduleForm'}):
            return True
        raise Exception('Not sure...')

    def send_notification(self, link):
        '''Sends a notification for the given item, and then marks it as sent in firebase'''
        self.pb_chan.push_link('GOES Availability Opened Up', 'https://goes-app.cbp.dhs.gov')
        print('Sent notification for {}'.format(link))


env = os.environ
goes = GOES(env['PB_KEY'], env['PB_CHAN'])
if goes.check_availability(env['USERNAME'], env['PASSWORD']):
    print("Available!")
    goes.send_notification('https://goes-app.cbp.dhs.gov/')
else:
    print("Not Available!")
