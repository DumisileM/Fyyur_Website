#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db,  Show, Venue, Artist
from flask_migrate import Migrate
import sys
import os
from sqlalchemy.exc import IntegrityError
import numpy as np
import re

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
        # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  venues = Venue.query.all()
  upcoming = Venue.query.join(Show).filter(Show.start_time > datetime.now()).count()
  
  data = []
  for venue in venues:
    data.append({"city": venue.city,
    "state": venue.state,
    "venues": [{
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": upcoming
      

    }]
    })
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    error = False
    try:
    
      search_term= request.form.get('search_term')
      res = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all() 
      count = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).count()
      response={
        "count": 0,
        "data": []
      }
      
      for item in range(count):
          upcoming=Venue.query.join(Show).filter(Show.start_time > datetime.now()).filter(Show.venue_id==res[item].id).count()
          response['data'].append(
            {'id': res[item].id,
            'name': res[item].name,
            'upcoming': upcoming})

      response['count'] = count
    
    except:
      error = True
      flash(f'An error occured. Unable to execute search.')
      # exc_type, exc_obj, exc_tb = sys.exc_info()
      # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(sys.exc_info())
    
    if error:
      return redirect(url_for('venues'))
  
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  error = False
  try:
    venue= Venue.query.get(venue_id)
    
    upcoming = Venue.query.join(Show).filter(Show.start_time > datetime.now()).filter(Show.venue_id==venue.id).count() 
    past= Venue.query.join(Show).filter(Show.start_time < datetime.now()).filter(Show.venue_id==venue.id).count()
    artist = Artist.query.join(Show).filter(Show.artist_id==Artist.id).filter(Show.venue_id==venue.id).first()
    start_time= Show.query.join(Artist).filter(Show.venue_id==venue_id).first()
    
    data = {}
    data['id'] = venue.id
    data['name'] = venue.name
    data['genres'] = re.sub(r"[^a-zA-Z0-9-&-,]"," ",''.join(venue.genres)).split(',')
    data['address'] = venue.address
    data['city'] = venue.city
    data['state'] = venue.state
    data['phone'] = venue.phone
    data['website'] = venue.website
    data['facebook_link'] = venue.facebook_link
    data['seeking_talent'] = venue.seeking_talent
    data['seeking_description'] = venue.seeking_description
    data['image_link'] = venue.image_link
    data['past_shows_count'] = past
    data['upcoming_shows_count'] =upcoming
    data['past_shows'] = []
    data['upcoming_shows'] = []
    
    for each in venue.shows:
      if each.start_time > datetime.now():
        data['upcoming_shows'].append({
        'artist_id': artist.id,
        'artist_name': artist.name,
        'artist_image_link': artist.image_link,
        'start_time': str(each.start_time)

      })
      elif each.start_time < datetime.now():
        data['past_shows'].append({
        'artist_id': artist.id,
        'artist_name': artist.name,
        'artist_image_link': artist.image_link,
        'start_time': str(each.start_time)

      })


   
    return render_template('pages/show_venue.html', venue=data)
  
  except:
    error = True
    flash(f'An error occured. Unable to show Venue information.')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
  if error:
    return redirect(url_for('index'))


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  # if form.validate():
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  if form.validate():
      try:
        venue= Venue (name = form.name.data,
                      address = form.address.data,
                      state= form.state.data,
                      phone= form.phone.data,
                      city= form.city.data,
                      genres = form.genres.data,
                      facebook_link = form.facebook_link.data,
                      image_link = form.image_link.data,
                      website = form.website_link.data,
                      seeking_talent = form.seeking_talent.data,
                      seeking_description = form.seeking_description.data

                    )
        
        db.session.add(venue)
        db.session.commit()
          # on successful db insert, flash success
        flash('Venue: ' + request.form['name'] + ' was successfully listed!')
     
      except PygtfsValidationError as e:
        db.session.rollback()
        flash(f'An error occured. Venue: ' + request.form['name'] + ' could not be created.')
        print(e)
        return redirect(url_for('venues'))
      except ValueError as e:
        db.session.rollback()
        flash(f'An error occured. Venue: ' + request.form['name'] + ' could not be created.')
        print(e)
        return redirect(url_for('venues'))
      except IntegrityError as e:
        db.session.rollback()
        flash(f'An error occured. Venue ' + request.form['name'] + ' could not be created.')
        print(e) 
        return redirect(url_for('venues'))
      
      except:
        #   TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
        flash(f'An error occured. Venue ' + request.form['name'] + ' could not be created.')
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return redirect(url_for('venues'))

          
      finally:
        db.session.close()

      return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete', methods=['GET', 'DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(venue_id)

    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully deleted')
  except:
    db.session.rollback()
    flash(f'Venue ' + venue.name + ' could not be deleted')
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data =[]

  for artist in artists:
    data.append(
      {
        "id":artist.id,
        "name":artist.name
      }
    )

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  error = False 
  try:
      search_term= request.form.get('search_term')
      res = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()  
      count = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).count()
      response = {
        "count": 0,
        "data": []
      }
      
      for item in range(count):
          upcoming = Artist.query.join(Show).filter(Show.start_time > datetime.now()).filter(Show.artist_id==res[item].id).count()
          response['data'].append(
            {'id': res[item].id,
            'name': res[item].name,
            'upcoming': upcoming})

      response['count'] = count
  
  except:
      error = True
      flash(f'An error occured. Unable to execute search.')
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
  
  if error:
    return redirect(url_for('venues'))
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  
    

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  error = False
  try:
    artist = Artist.query.get(artist_id)
    upcoming = Artist.query.join(Show).filter(Show.start_time > datetime.now()).filter(Show.artist_id == artist.id).count()
    past =Artist.query.join(Show).filter(Show.start_time < datetime.now()).filter(Show.artist_id == artist.id).count()
    venue = Venue.query.join(Show).filter(Show.venue_id==Venue.id).filter(Show.artist_id==artist.id).first()
    
    
    data = {}
    data['id'] = artist.id
    data['name'] = artist.name
    data['genres'] =  re.sub(r"[^a-zA-Z0-9-&-,]"," ",''.join(artist.genres)).split(',')
    data['city'] = artist.city
    data['state'] = artist.state
    data['phone'] = artist.phone
    data['website'] = artist.website_link
    data['facebook_link'] = artist.facebook_link
    data['seeking_venue'] = artist.seeking_venue
    data['seeking_description'] = artist.seeking_description
    data['image_link'] = artist.image_link
    data['past_shows_count'] = past
    data['upcoming_shows_count'] = upcoming
    data['upcoming_shows'] = []
    data['past_shows'] = []

    for each in artist.shows:
      if each.start_time > datetime.now():
        data['upcoming_shows'].append({
          'venue_id': venue.id,
          'venue_name': venue.name,
          'venue_image_link': venue.image_link,
          'start_time': str(each.start_time)
        })
      elif each.start_time < datetime.now():

        data['past_shows'].append({
                'venue_id': venue.id,
                'venue_name': venue.name,
                'venue_image_link': venue.image_link,
                'start_time': str(each.start_time)
              })

    
    # for each in artist.shows
    return render_template('pages/show_artist.html', artist=data)
  
  except:
    error = True
    flash(f'An error occured. Unable to show Artist information.')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
  
  if error:
    return redirect(url_for('index'))
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  form = ArtistForm(request.form)
  if form.validate_on_submit  :
      artist_obj = Artist.query.get(artist_id)
      artist={
        "id": artist_obj.id,
        "name": artist_obj.name,
        "genres": artist_obj.genres,
        "city": artist_obj.city,
        "state": artist_obj.state,
        "phone": artist_obj.phone,
        "website": artist_obj.website_link,
        "facebook_link": artist_obj.facebook_link,
        "seeking_venue": artist_obj.seeking_venue,
        "seeking_description": artist_obj.seeking_description,
        "image_link": artist_obj.image_link
      }

      form.name.data = artist_obj.name
      form.genres.data = artist_obj.genres
      form.city.data = artist_obj.city
      form.state.data = artist_obj.state
      form.phone.data = artist_obj.phone
      form.website_link.data = artist_obj.website_link
      form.facebook_link.data = artist_obj.facebook_link
      form.seeking_venue.data = artist_obj.seeking_venue
      form.seeking_description.data = artist_obj.seeking_description
      form.image_link.data = artist_obj.image_link
      
      return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  artist_obj = Artist.query.get(artist_id) 
  
  if form.validate_on_submit:
    try:

      artist_obj.name = form.name.data
      artist_obj.genres = form.genres.data
      artist_obj.city = form.city.data
      artist_obj.state = form.state.data
      artist_obj.phone = form.phone.data
      artist_obj.website_link = form.website_link.data
      artist_obj.facebook_link = form.facebook_link.data
      artist_obj.seeking_venue = form.seeking_venue.data
      artist_obj.seeking_description = form.seeking_description.data
      artist_obj.image_link = form.image_link.data
      
      db.session.add(artist_obj)
      db.session.commit()
      flash('Artist details have been successfully updated')

    except:
      db.session.rollback()
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
    finally:
      db.session.close

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  form= VenueForm(request.form)
  if form.validate_on_submit:
      venue_obj= Venue.query.get(venue_id)
      venue={
        "id": venue_obj.id,
        "name": venue_obj.name,
        "genres": venue_obj.genres,
        "address": venue_obj.address,
        "city": venue_obj.city,
        "state": venue_obj.state,
        "phone": venue_obj.phone,
        "website": venue_obj.website,
        "facebook_link": venue_obj.facebook_link,
        "seeking_talent": venue_obj.seeking_talent,
        "seeking_description": venue_obj.seeking_description,
        "image_link": venue_obj.image_link
      }
      form.name.data =venue_obj.name
      form.genres.data =venue_obj.genres
      form.address.data = venue_obj.address
      form.city.data = venue_obj.city
      form.state.data =venue_obj.state
      form.phone.data =venue_obj.phone
      form.website_link.data =venue_obj.website
      form.facebook_link.data=venue_obj.facebook_link
      form.seeking_talent.data=venue_obj.seeking_talent
      form.seeking_description.data=venue_obj.seeking_description
      form.image_link.data=venue_obj.image_link
          
      return render_template('forms/edit_venue.html', form=form, venue=venue)


 
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  venue_obj = Venue.query.get(venue_id)
  
  if form.validate_on_submit:
    
      try:
        venue_obj.name = form.name.data
        venue_obj.genres = form.genres.data
        venue_obj.address = form.address.data
        venue_obj.city = form.city.data
        venue_obj.state = form.state.data
        venue_obj.phone = form.phone.data
        venue_obj.website = form.website_link.data
        venue_obj.facebook_link = form.facebook_link.data
        venue_obj.seeking_talent = form.seeking_talent.data
        venue_obj.seeking_description = form.seeking_description.data
        venue_obj.image_link = form.image_link.data
        
  
        db.session.add(venue_obj)
        db.session.commit()
        flash('Venue details have been successfully updated')

      except:
        db.session.rollback()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
      
      finally:
        db.session.close
    
      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  if form.validate():
      try:
          artist= Artist(name = form.name.data,
                        state= form.state.data,
                        phone= form.phone.data,
                        city= form.city.data,
                        genres = form.genres.data,
                        facebook_link = form.facebook_link.data,
                        image_link = form.image_link.data,
                        website_link = form.website_link.data,
                        seeking_venue = form.seeking_venue.data,
                        seeking_description = form.seeking_description.data

                      )
          
          db.session.add(artist)
          db.session.commit()
          # on successful db insert, flash success
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
      except PygtfsValidationError as e:
        db.session.rollback()
        print(e)
        flash(f'An error occured. Artist' + {form.name.data} + 'could not be created.')
        return redirect(url_for('artists'))
      except ValueError as e:
        db.session.rollback() 
        flash(f'An error occured. Artist' + {form.name.data} + 'could not be created.')
        print(e)
        return redirect(url_for('artists'))
      except IntegrityError as e:
        db.session.rollback()
        flash(f'An error occured. Artist' + {form.name.data} + 'could not be created.')
        print(e)
        return redirect(url_for('artists'))
      except:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
          db.session.rollback()
          flash(f'An error occured. Artist' + {form.name.data} + 'could not be created.')
          exc_type, exc_obj, exc_tb = sys.exc_info()
          fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
          print(exc_type, fname, exc_tb.tb_lineno)
          return redirect(url_for('artists'))
      finally:
          db.session.close()
      
      return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  
  data =[]
  for show in shows:
    artist = Artist.query.join(Show).filter(show.artist_id==Artist.id).first()
    venue = Venue.query.join(Show).filter(show.venue_id==Venue.id).first()
    data.append(
      {
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.start_time)
      }
    )

 
  return render_template('pages/shows.html', shows=data)
  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form= ShowForm(request.form)
  if form.validate():
    try:
      show = Show(
        artist_id= form.artist_id.data,
        venue_id = form.venue_id.data,
        start_time = form.start_time.data
      )
      db.session.add(show)
      db.session.commit()

      # on successful db insert, flash success
      flash('Show was successfully listed!')
    except PygtfsValidationError as e:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
        print(e)
        return redirect(url_for('shows'))
    except IntegrityError as e:
        db.session.rollback()
        flash(f'An error occurred. Show could not be listed.')
        print(e) 
        return redirect(url_for('shows'))
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      db.session.rollback()
      flash('An error occurred. Show could not be listed.') 
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      
    finally:
      db.session.close()

    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
