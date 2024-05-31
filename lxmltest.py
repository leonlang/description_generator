from lxml import etree

html_data = '''
<div id="root">
  <div id="products">
    <div class="product">
      <p id="product_name">Dark Red Energy Potion</p>
      <a id="lol" href="google.de">DE</a>
      <div id="product_rate">4.7</div>
      <div id="product_description">Bring out the best in your gaming performance.</div>
    </div>
  </div>
</div>
'''

# Parse the HTML data using lxml
root = etree.fromstring(html_data)
if root[0][0][1].tag == 'a':
    print('Du bist a')

print(root[0][0][1].get('href'))
if root[0][0][1].text.lower() == 'de':
    print(root[0][0][1].get('href') + ' hi')
print(root[0][0][1].text)
'''
# Navigate through the document
for parent in root:
    print(f"Parent tag: {parent.tag}")
    for child in parent:
        print(f"Child tag: {child.tag}")
        for grandchild in child:
            print(f"Grandchild tag: {grandchild.tag}, Attribute: {grandchild.attrib}, Text: {grandchild.text}")

            '''