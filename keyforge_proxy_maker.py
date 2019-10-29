import json, requests, math, sys
from PIL import Image

def generate_proxy(argv):

    deck_id = input("\nPaste the deck id here (Example 1a550e50-e3e1-44ee-998b-d336099cd911) : \n")
    language = input("\nWhich language ? (Example fr en it es de...etc) : \n")

    print("\nOk, creating your file now.......\n")

    #get json data about the deck from the api
    response = requests.get('https://www.keyforgegame.com/api/decks/' + deck_id+ '/?links=cards')
    data = json.loads(response.content)

    #get the archon name
    archon = data['data']['name']
    #get a list of card ids from the json
    cardlist = data['data']['_links']['cards']
    #get the data for each card in the deck
    carddata = data['_linked']['cards']


    #
    cols = 3
    rows = 3
    #the offsets will be used to make sure each image is pasted in the correct
    #place in the blank image
    x_offset = 0
    y_offset = 0
    card_count = 0
    max_x_offset = 300*cols
    #create a blank image that matches the size of the rows and columns
    wallpaper = Image.new('RGB', (300*cols,420*rows))

    for card in cardlist:

        #using the link to the card image, download the image
        image_link_en = [x['front_image'] for x in carddata if x['id'] == card][0]
        image_link = image_link_en.replace("en",language)
        card_image = Image.open(requests.get(image_link, stream=True).raw)

        #paste the downloaded image into the blank image
        wallpaper.paste(card_image, (x_offset, y_offset))
        card_count += 1

        #update the offsets for the next card
        x_offset += 300
        if x_offset >= max_x_offset:
            x_offset = 0
            y_offset += 420
        if card_count%9 == 0:
            page_num = str(math.ceil(card_count/9))
            #save the file
            wallpaper.save(archon+'_p'+page_num+'.jpg')
            print(archon+'_p'+page_num+'.jpg')
            #new image
            wallpaper = Image.new('RGB', (300*cols,420*rows))
            x_offset = 0
            y_offset = 0

    print("\nProxy for "+archon+" was successfully created \n")

if __name__ == "__main__":
    #this is where the program starts
    #it passes the arguements you specified to the generate_wallpaper function
    generate_proxy(sys.argv[1:])

"""
Requisites : You need to install Python3 and Pillow
Once you have those installed you just need to copy that code into notepad and save it as "keyforge_proxy_maker.py" (or whatever you want to call it, as long as it ends in .py).

Then to run, open up your command prompt (or terminal if you're on a mac), navigate to the directory its saved, and type
python keyforge_proxy_maker.py

It will ask the deck_id and the desired language
where deck_id is the id used for your deck in the URL, such as https://www.keyforgegame.com/deck-details/4b676996-2ac2-4d47-ac3f-1d0682eede6d and language is the first 2 letters of the desired language (en,fr,it,es,de so far)


Then it should output 4 pages ready to print.
On my Brother laser printer scale 60% is the perfect size.

Enjoy !
ElSenorMaracas
"""
