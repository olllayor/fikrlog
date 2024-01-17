from slugify import slugify
import os
class Article:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        
    @property
    def slug(self):
        return slugify(self.title)
    
    def load_content(self):
        file_path = f"articles/{self.title}"
        with open(file_path, 'r', encoding='utf-8') as file:
            self.content = file.read()

    @classmethod
    def all(cls):
        titles = os.listdir('articles')
        slug_articles = {}                       
        for title in titles:
            slug = slugify(title)
            article = Article(title, "")
            article.load_content()
            slug_articles[slug] = article
        return slug_articles
