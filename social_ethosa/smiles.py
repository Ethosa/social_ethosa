import requests

class Smile:

    """
    docstring for Smile

    usage:
    Smile('smile name'), example:
    Smile('Муравей')

    WARNING: there will be a slight delay on the first call

    Also you can see all smiles:
    Smile().smile # it return dictionary of all smiles.
    """

    def __init__(self):
        self.smiles = {}
        response = requests.get('https://kody-smajlov-vkontakte.ru').text.split('class="smile_table">')
        response.pop(0)
        for i in response:
            current_list = i.split('<tr')
            current_list.pop(0)
            for elem in current_list:
                if '"description">' in elem and '"smile_code">' in elem:
                    self.smiles[elem.split('"description">', 1)[1].split('</td', 1)[0].lower()] = elem.split('"smile_code">', 1)[1].split('</td', 1)[0].replace('&amp;', '&')
    def __new__(self, *args):
        string = args[0] if len(args) > 0 else ''
        if string:
            try:
                return self.smiles[string.lower()]
            except:
                self.__init__(self)
                return self.smiles[string.lower()]
        else:
            return self