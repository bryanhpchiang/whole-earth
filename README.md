# whole-earth

Code to convert [Whole Earth](https://wholeearth.info/) archive into printable PDFs. 

Provide your data like so.

```py
data = [
    dict(name="we-summer1997", url="https://ia902504.us.archive.org/BookReader/BookReaderImages.php?id=wholeearthsummer00unse&itemPath=%2F34%2Fitems%2Fwholeearthsummer00unse&server=ia902504.us.archive.org&page=n{}_w1000.jpg"),
    # dict(name="we-winter1997", url="https://ia801405.us.archive.org/BookReader/BookReaderImages.php?id=wholeearthwinter00unse&itemPath=%2F25%2Fitems%2Fwholeearthwinter00unse&server=ia801405.us.archive.org&page=n{}_medium.jpg"),
    # dict(name="we-winter2000", url="https://ia601404.us.archive.org/BookReader/BookReaderImages.php?id=wholeearthwinter00unse_1&itemPath=%2F29%2Fitems%2Fwholeearthwinter00unse_1&server=ia601404.us.archive.org&page=n{}_medium.jpg")   
]
```
You can get the URL by clicking into any of the [publications](https://wholeearth.info/p/coevolution-quarterly-summer-1974) and then right click > Open Image in New Tab. Choose whatever name you want.

Run with:
```py
python scrape.py
```
