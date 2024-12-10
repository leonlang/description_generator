import os
# from html_converter import get_html_links # type: ignore
from csv_converter import get_csv_files,read_csv,get_csv_path # type: ignore
from googledocs import return_links_and_titles # type: ignore

# use pathlib for later implementation
directory = os.path.dirname(os.path.abspath(__file__))

def create_de_description(read_csv,html_titles,html_links):
    description = "Finde das beste Angebot für "
    for csv_row in read_csv:
        csv_number_str = csv_row[0]
        if csv_number_str.isdigit():
            csv_number = int(csv_number_str) - 1
            if len(html_links[csv_number]) > 0:
                description += html_titles[csv_number] + '\n'
                first_amazon_link = False
                second_amazon_link = False
                for affiliate_link in html_links[csv_number]:
                    if affiliate_link.startswith("Amazon") and first_amazon_link == True:
                        second_amazon_link = True
                    if affiliate_link.startswith("Amazon"):
                        first_amazon_link = True
                    if first_amazon_link == True and second_amazon_link == True:
                        pass
                    else:
                        description += affiliate_link + '\n'
                description += '\n'
    return description

def create_en_description(read_csv,html_titles,html_links):
    description = "Find the best Deal for "

    for csv_row in read_csv:
        csv_number_str = csv_row[0]
        if csv_number_str.isdigit():
            csv_number = int(csv_number_str) - 1
            if len(html_links[csv_number]) > 0:
                description += html_titles[csv_number] + '\n'
                first_amazon_link = False
                second_amazon_link = False
                for affiliate_link in html_links[csv_number]:
                    if affiliate_link.startswith("Amazon") and first_amazon_link == True:
                        second_amazon_link = True
                    if affiliate_link.startswith("Amazon"):
                        first_amazon_link = True
                    if first_amazon_link == True and second_amazon_link == True:
                        description += affiliate_link + '\n'
                description += '\n'
    return description

def create_timestamp(read_csv,html_titles):
    timestamp = ""
    for csv_row in read_csv:
        timestamp += csv_row[1] + ' '
        if csv_row[0].isdigit():
            timestamp += html_titles[int(csv_row[0]) - 1]
        else:
            timestamp += csv_row[0]
        timestamp += '\n'
    timestamp += '\n'
    return timestamp

def description(read_csv,html_titles,html_links):
    description = ''
    description += create_de_description(read_csv,html_titles,html_links)
    description += create_timestamp(read_csv,html_titles)
    description += "Käufe durch Links können mir eine Provision bringen. \n"
    description += "Dieser Kanal benutzt Amazon Partnernet und weitere Affiliate Programme. \n\n\n\n"
    description += create_en_description(read_csv,html_titles,html_links)
    description += create_timestamp(read_csv,html_titles)
    description += "Purchases made through some store links may provide compensation to me."
    return description
def write_txt_file(read_csv,html_titles,html_links,csv_path):
    with open(csv_path[:-4] + '.txt', "w", encoding='utf-8') as file:
        file.write(description(read_csv,html_titles,html_links))
    os.remove(csv_path)

def fastprogram():
    for csv_file in get_csv_files(directory):
        csv_path = get_csv_path(csv_file,directory)
        docs_links_titles = return_links_and_titles(csv_file[0])
        docs_titles = docs_links_titles[0]
        docs_links = docs_links_titles[1]
        #create_en_description(read_csv(csv_path),html_titles,html_links)
        write_txt_file(read_csv(csv_path),docs_titles,docs_links,csv_path)
    #print(create_timestamp(read_csv(csv_path),html_titles))
    #print(html_links)
    #print(read_csv(csv_path))
    #for csv_line in read_csv(csv_path):
        #print(csv_line)
fastprogram()
