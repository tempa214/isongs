from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver_path = "C:\Automation and testing tools\chromedriver.exe"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0glhljsKR6b'
Bootstrap(app)


class AlbumForm(FlaskForm):
    album = StringField('Album Title', validators=[DataRequired(message='Please Enter The Album Name')])
    search = SubmitField(label='Search')


@app.route("/", methods=['GET', 'POST'])
def home():
    form = AlbumForm()
    if form.validate_on_submit():
        album_name = form.data.get('album')
        return redirect(url_for('results', album_name=album_name))
    return render_template("add.html", form=form)


@app.route('/results/<album_name>')
def results(album_name):
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.set_window_rect(1080, 1080, width=10, height=10)
    driver.get(f'https://www.isongs.info/?q={album_name}')
    album_link = driver.find_element(By.XPATH, '//*[@id="append-results"]/div[1]/div/div[1]/div/a').get_attribute(
        'href')
    driver.quit()
    response = requests.get(url=album_link)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')
    album_new = soup.find('h1', class_='p-name').text
    album_img = soup.find('img', class_='entry-thumbnail').get('src')
    songs_names = soup.find_all('td', class_='song-name')
    songs_text = [song.text.strip() for song in songs_names]
    song_links = soup.select('div.ui360 a')
    song_url = [song.get('href') for song in song_links]

    return render_template('index.html', album_name=album_new, image=album_img, songs_links = song_url, songs_names = songs_text)



if __name__ == '__main__':
    app.run(debug=True)
