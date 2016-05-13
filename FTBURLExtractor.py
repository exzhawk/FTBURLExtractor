from flask import Flask, render_template
from xml.etree import ElementTree
import requests

FTB_URL_PREFIX = 'http://ftb.cursecdn.com/FTB2/'
STATIC_URL_PREFIX = FTB_URL_PREFIX + 'static/'
MODPACK_URL_PREFIX = FTB_URL_PREFIX + 'modpacks/'
MODPACKS_XML_URL = STATIC_URL_PREFIX + 'modpacks.xml'
THIRDPARTY_XML_URL = STATIC_URL_PREFIX + 'thirdparty.xml'

app = Flask(__name__)


def get_modpacks_from_url(xml_url):
    r = requests.get(xml_url)
    modpacks_xml = ElementTree.fromstring(r.text)
    modpacks_list = []
    for modpack in modpacks_xml:
        attrib = modpack.attrib
        if attrib.get('repoVersion'):
            modpacks_list.append(attrib)
    return render_template('modpacks.html', modpacks_list=modpacks_list, static_url_prefix=STATIC_URL_PREFIX,
                           modpack_url_prefix=MODPACK_URL_PREFIX)


@app.route('/')
def homepage():
    return 'Hello Minecraft Player!'


@app.route('/modpacks')
def modpacks():
    return get_modpacks_from_url(MODPACKS_XML_URL)


@app.route('/thirdparty')
def thirdparty():
    return get_modpacks_from_url(THIRDPARTY_XML_URL)


@app.route('/packcode/<code>')
def packcode(code):
    return get_modpacks_from_url(STATIC_URL_PREFIX + code + '.xml')


if __name__ == '__main__':
    app.run(debug=True,
            host=8090)
