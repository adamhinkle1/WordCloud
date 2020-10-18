'''
Course: CECS 450 Assignment 1 - Tag Cloud
Group: Team 4
Creator: Orlando Elias, Adam Hinkle, Sonu Jacob
Date: 10/16/20
'''
import webbrowser, os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist

tagCloud = {}
maxUsed = 0
filter = 0

def main():
    global filter

    #filter lets user decide how focused to make the tag cloud. higher integer values will remove 'clutter' low frequency words
    filterInput = input("Enter minimum occurrences of a word to add to cloud? (default: 2):")
    try:
        filterInput = int(filterInput)
        if (filterInput >= 0):
            filter = filterInput
    except ValueError:
        filter = 2
        print("Input not recognized, default filter set to 2.")
    #test paragraph
    #word_string = 'oh oh oh oh oh oh verse wrote book stand title book would life superman thats make feel count privilege love ideal honored know feel see everyday things things say rock baby truth rock love rock rock everything need rock baby rock wanna kiss ya feel ya please ya right wanna touch ya love ya baby night reward ya things rock love rock love rock oh oh oh verse try count ways make smile id run fingers run timeless things talk sugar keeps going make wanna keep lovin strong make wanna try best give want need give whole heart little piece minimum talking everything single wish talking every dream rock baby truth rock love rock rock everything need rock baby rock wanna kiss ya feel ya please ya right wanna touch ya love ya baby night reward ya things rock love rock wanna rock bridge theres options dont want theyre worth time cause oh thank like us fine rock sand smile cry joy pain truth lies matter know count oh oh oh oh oh oh rock baby truth rock love rock rock everything need rock baby rock wanna kiss ya feel ya please ya right wanna touch ya love ya baby night reward ya things rock love rock love rock oh oh oh oh oh oh wanna kiss ya feel ya please ya right wanna touch ya love ya baby night reward ya things rock love rock wanna rock party people people party popping sitting around see looking looking see look started lets hook little one one come give stuff let freshin ruff lets go lets hook start wont stop baby baby dont stop come give stuff lets go black culture black culture black culture black culture party people people party popping sitting around see looking looking see look started lets hook come one give stuff let freshin little one one ruff lets go lets hook start wont stop baby baby dont stop come give stuff lets go black culture black culture black culture black culture lets hook come give stuff let freshin little one one ruff lets go lets hook start wont stop baby baby dont stop come give stuff lets go lets hook come give stuff let freshin little one one ruff lets go lets hook start wont stop baby baby dont stop come give stuff lets go black culture black culture black culture black culture black culture black culture black culture black culture'
    word_string = input("Input text to analyze here: \n")

    # Path to output html file
    htmlFile = 'index.html'

    # Read the file and get frequency of each word
    textSplitter(word_string)

    # Generate the HTML file
    createHTMLFile(tagCloud, htmlFile)

# Split text read from file by words and put into dictionary with frequency count
def textSplitter(word_string):
    global tagCloud
    global maxUsed
    global filter
    word_list = word_tokenize(word_string)
    # Filter out punctuation from text
    alphaWords = [word for word in word_list if word.isalpha()]

    # filter out stop words
    filtered_words = []
    stop_words = set(stopwords.words("english"))
    for w in alphaWords:
        if w not in stop_words:
            filtered_words.append(w)

    # filter lemmatizer -- condense list into a list of root words to make a better tag-cloud
    lem = WordNetLemmatizer()
    lem_words = []
    for w in filtered_words:
        lem_words.append(lem.lemmatize(w))

    # create dictionary of frequency distribution for key words in the form of {word:frequency}
    fdist = FreqDist(lem_words)
    maxUsed = fdist[fdist.max()]
    for word in fdist:
        f = fdist[word] / fdist[fdist.max()]
        if (fdist[word] >= int(filter)):  # word must be at least 1% frequency
            tagCloud[word] = f
    return tagCloud


# Set weight threshholds for font size based on tag frequency
def getFrequencyWeight(tag):
    if tag[1] > 0 and tag[1] <= 0.1:
        return 0
    elif tag[1] > 0.1 and tag[1] <= 0.2:
        return 1
    elif tag[1] > 0.2 and tag[1] <= 0.3:
        return 2
    elif tag[1] > 0.3 and tag[1] <= 0.4:
        return 3
    elif tag[1] > 0.4 and tag[1] <= 0.5:
        return 4
    elif tag[1] > 0.5 and tag[1] <= 0.6:
        return 5
    elif tag[1] > 0.6 and tag[1] <= 0.7:
        return 6
    elif tag[1] > 0.7 and tag[1] <= 0.8:
        return 7
    elif tag[1] > 0.8 and tag[1] <= 1.0:
        return 8


#generate the htmlfile which will produce wordcloud
def createHTMLFile(tags, outputFilePath):
    global maxUsed

    fontSize = ["xxs", "xs", "s", "m", "ml", "l", "xl", "xxl", "largest"] #references to css styles in styles.css

    sortedTags = sorted(tags.items())  #sort our words/values

    with open("styles.css") as f:  #open css styles
        with open("tooltip.html") as f1: #open tooltip information
            with open(outputFilePath, "w") as outputFile: #open output file
                #input html information
                outputFile.write("<html>")
                outputFile.write("<h2>TagCloud</h2>")
                #copy contents from styles onto our output
                for line in f:
                    outputFile.write(line)
                outputFile.write("\n")
                f.close()
                for line in f1:#copy contents from tooltip onto our output
                    outputFile.write(line)
                outputFile.write("\n")
                f1.close()

                for tag in sortedTags: #write our tag cloud out as elements with classes to html
                    fontSizeIndex = getFrequencyWeight(tag)
                    outputFile.write('<span class ="tooltip"><span class = "' + fontSize[fontSizeIndex] + '">' + tag[0]+"   "+ '</span><span class ="tooltiptext">' + str(int(tag[1]*maxUsed)) + '</span ></span>')
                outputFile.write("</html>")
                outputFile.close()
    webbrowser.open('file://' + os.path.realpath(outputFilePath)) #run html


if __name__ == "__main__":
    main()
    print("DONE")
