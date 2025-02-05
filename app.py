from flask import Flask, render_template, request
import pickle
import numpy as np

#import data
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', #sending from pkl popular_df
                           book_name = list(popular_df['Book-Title'].values),
                           author =list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_of_user_rating'].values),
                           rating=list(popular_df['avg_rating'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

#asking data from form so method is POST
@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # we need to fetch index of the books
    index = np.where(pt.index == user_input)[0][0]
    # similar books
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        # print(i[0]) # this give index
        # print(pt.index[i[0]])# give name of book
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        # .extend  Adds each element of iterable individually to the list but, append Adds x as a single element to the list
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
