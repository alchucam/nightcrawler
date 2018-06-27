# nightcrawler
crawl, parse and analyze news articles

Frontend: HTML, Javascript, CSS
Backend: Python 
Database: MySQL
Libraries: BeautifulSoup, NLTK, HighCharts

In news tab: show titles, published dates and urls for articles from different publisher around the world, using BeautifulSoup
nytimes (USA), ecns (China), japantimes (Japan), yonhap (South Korea)
Furthermore, top 10 frequent words and sentiment scores are analyzed using NLTK.

In analysis tab: each publishers represent their own countries, and the articles that mentions other countries (by the name of country) are checked and analyzed in terms of sentiment scores and ratios.
The data are represented in the form of HighCharts along with Javascript/Jquery.
